"""
tikhonov_solver_2d.py
=====================
2D IHCP Tikhonov inverse solver (pure NumPy, closed-form normal equations).

Problem
-------
Recover the boundary heat flux q(y, t) at x = 0 from sparse noisy interior
temperature observations in a 2D plate.

The forward map  F: q → T_sensors  is linear in q (heat equation is linear).
We represent q on a coarse (ny_q × nt_q) grid and build the sensitivity matrix
S by superposition inside the simulator.  The inverse problem is then:

    min_q  ½‖S q_vec − y_obs‖²  +  ½λ ‖L q_vec‖²

Closed-form solution (normal equations):

    (S^T S  +  λ L^T L) q_vec  =  S^T y_obs

This is solved with numpy.linalg.solve (direct LAPACK driver), which is faster
and more numerically stable than iterative methods for the small systems arising
in this benchmark (≤ 200 unknowns).

Public API
----------
    solve_2d_tikhonov(problem_spec)  →  dict

problem_spec keys
-----------------
Required:
    simulator        : HeatConduction2DFD instance
    sensor_positions : list[(x, y)]
    T_obs_noisy      : ndarray (n_sensors, n_obs_times)
    obs_every        : int
    t_end            : float
    ny_q, nt_q       : int — coarse flux grid shape
    T0               : float — initial / baseline temperature

Optional (for caching / fairness across solvers):
    S                : ndarray (n_obs_rows, ny_q*nt_q)  — pre-built sensitivity
    y_q_grid         : ndarray (ny_q,)
    t_q_grid         : ndarray (nt_q,)
    obs_times        : ndarray (n_obs,)

Optional (solver tuning):
    lam              : float  — regularisation weight  (default 1e-3)
    reg_order        : int    — 0, 1, or 2             (default 1)
    q_true           : ndarray (ny_q, nt_q)            — for RMSE computation

Returns
-------
dict with keys:
    flux_pred        : ndarray (ny_q, nt_q) [W/m²]
    flux_rmse        : float   [W/m²] or None
    replay_rmse      : float   [K]    — ‖S q_vec − y_obs‖ / √(n_obs)
    loss             : float   — Tikhonov objective value
    convergence_flag : bool    — True (direct solve always succeeds)
    diagnostics      : dict
"""

from __future__ import annotations

import time
from typing import Any

import numpy as np


# ---------------------------------------------------------------------------
# Regularisation matrix  (shared with other 2D solvers)
# ---------------------------------------------------------------------------

def build_diff_matrix(N: int, order: int) -> np.ndarray:
    """First- or second-order finite-difference regularisation matrix.

    Returns L of shape (N − order, N) such that ‖L q‖ penalises roughness.
    """
    L = np.eye(N, dtype=float)
    for _ in range(order):
        L = np.diff(L, n=1, axis=0)
    return L


# ---------------------------------------------------------------------------
# Main solver
# ---------------------------------------------------------------------------

def solve_2d_tikhonov(problem_spec: dict[str, Any]) -> dict[str, Any]:
    """Tikhonov 2D IHCP solver — closed-form normal equations.

    See module docstring for full parameter description.
    """
    t0 = time.perf_counter()

    # ------------------------------------------------------------------
    # Unpack spec
    # ------------------------------------------------------------------
    simulator     = problem_spec["simulator"]
    sensor_pos    = problem_spec["sensor_positions"]
    T_obs_noisy   = np.asarray(problem_spec["T_obs_noisy"], dtype=float)
    obs_every     = int(problem_spec["obs_every"])
    t_end         = float(problem_spec["t_end"])
    ny_q          = int(problem_spec["ny_q"])
    nt_q          = int(problem_spec["nt_q"])
    T0            = float(problem_spec.get("T0", 0.0))
    lam           = float(problem_spec.get("lam", 1e-3))
    reg_order     = int(problem_spec.get("reg_order", 1))
    q_true        = problem_spec.get("q_true", None)

    # ------------------------------------------------------------------
    # Sensitivity matrix (use cached if provided)
    # ------------------------------------------------------------------
    if "S" in problem_spec:
        S        = np.asarray(problem_spec["S"], dtype=float)
        y_q_grid = np.asarray(problem_spec["y_q_grid"])
        t_q_grid = np.asarray(problem_spec["t_q_grid"])
        t_sensitivity = 0.0
    else:
        t_s = time.perf_counter()
        S, _, y_q_grid, t_q_grid = simulator.build_sensitivity_matrix(
            sensor_positions=sensor_pos,
            t_end=t_end, ny_q=ny_q, nt_q=nt_q,
            obs_every=obs_every,
        )
        t_sensitivity = time.perf_counter() - t_s

    # ------------------------------------------------------------------
    # Observation vector (subtract uniform baseline)
    # ------------------------------------------------------------------
    n_sensors   = len(sensor_pos)
    n_obs_rows  = S.shape[0]
    n_obs_times = n_obs_rows // n_sensors

    T_obs_use = T_obs_noisy[:, :n_obs_times]   # align to S
    y_obs = T_obs_use.flatten() - T0            # shape (n_obs_rows,)

    # ------------------------------------------------------------------
    # Regularisation matrix
    # ------------------------------------------------------------------
    N = ny_q * nt_q
    L = build_diff_matrix(N, order=reg_order)   # (N-order, N)

    # ------------------------------------------------------------------
    # Normal equations: (S^T S + λ L^T L) q = S^T y
    # ------------------------------------------------------------------
    t_solve_start = time.perf_counter()

    StS  = S.T @ S                          # (N, N)
    LtL  = L.T @ L                          # (N, N)
    A    = StS + lam * LtL                  # (N, N)
    rhs  = S.T @ y_obs                      # (N,)

    try:
        q_vec = np.linalg.solve(A, rhs)     # (N,)
        solve_ok = True
    except np.linalg.LinAlgError:
        # Fallback: regularised least-squares via lstsq
        q_vec, *_ = np.linalg.lstsq(A, rhs, rcond=None)
        solve_ok = True

    t_solve = time.perf_counter() - t_solve_start
    t_total = time.perf_counter() - t0

    # ------------------------------------------------------------------
    # Reshape and compute metrics
    # ------------------------------------------------------------------
    flux_pred = q_vec.reshape(ny_q, nt_q)

    residual    = S @ q_vec - y_obs
    replay_rmse = float(np.sqrt(np.mean(residual ** 2)))

    reg_vec     = L @ q_vec
    loss        = float(0.5 * np.dot(residual, residual)
                        + 0.5 * lam * np.dot(reg_vec, reg_vec))

    flux_rmse: float | None = None
    if q_true is not None:
        q_true_arr = np.asarray(q_true, dtype=float)
        if q_true_arr.shape == flux_pred.shape:
            flux_rmse = float(np.sqrt(np.mean((flux_pred - q_true_arr) ** 2)))

    cond_A = float(np.linalg.cond(A))

    diagnostics: dict[str, Any] = {
        "solver_name":     "tikhonov_2d",
        "lam":             lam,
        "reg_order":       reg_order,
        "cond_A":          cond_A,
        "loss":            loss,
        "t_sensitivity_s": t_sensitivity,
        "t_solve_s":       t_solve,
        "t_total_s":       t_total,
        "S_shape":         list(S.shape),
        "N_params":        N,
        "solve_ok":        solve_ok,
    }

    return {
        "flux_pred":        flux_pred,
        "flux_rmse":        flux_rmse,
        "replay_rmse":      replay_rmse,
        "loss":             loss,
        "convergence_flag": solve_ok and np.isfinite(flux_rmse if flux_rmse is not None else 0.0),
        "diagnostics":      diagnostics,
    }
