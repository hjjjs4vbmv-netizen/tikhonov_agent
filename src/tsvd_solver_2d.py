"""
tsvd_solver_2d.py
=================
2D IHCP Truncated SVD (TSVD) inverse solver.

Method
------
Decompose the sensitivity matrix  S = U Σ V^T  (thin SVD), keep only the
r largest singular values, and compute the regularised pseudoinverse:

    q_vec  =  V_r  Σ_r^{-1}  U_r^T  y_obs

where r is chosen by a relative-threshold rule:
    keep singular value σ_k  if  σ_k / σ_0 ≥ tol   (default tol = 0.01)

TSVD suppresses unstable small singular-value components that amplify noise,
while preserving the dominant (well-conditioned) signal modes.  The truncation
rank is a natural, interpretable hyperparameter.

Compared with Tikhonov, TSVD:
    + is parameter-free (tol has a clear geometric meaning)
    + produces sparser solutions in singular-vector space
    - may produce Gibbs-like ringing for highly localized targets

Public API
----------
    solve_2d_tsvd(problem_spec)  →  dict

problem_spec keys
-----------------
Required / optional:   identical to tikhonov_solver_2d (shared spec format).

Additional optional:
    tsvd_tol    : float  — relative truncation threshold  (default 0.01)
    tsvd_rank   : int    — explicit rank override (overrides tol if set)

Returns
-------
dict with keys:
    flux_pred        : ndarray (ny_q, nt_q) [W/m²]
    flux_rmse        : float   [W/m²] or None
    replay_rmse      : float   [K]
    loss             : float   — ½‖S q_vec − y_obs‖²
    convergence_flag : bool
    diagnostics      : dict    — includes kept_rank, singular_values, etc.
"""

from __future__ import annotations

import time
from typing import Any

import numpy as np

from src.tikhonov_solver_2d import build_diff_matrix   # reuse helper


# ---------------------------------------------------------------------------
# Main solver
# ---------------------------------------------------------------------------

def solve_2d_tsvd(problem_spec: dict[str, Any]) -> dict[str, Any]:
    """TSVD 2D IHCP solver — truncated SVD of the sensitivity matrix.

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
    tsvd_tol      = float(problem_spec.get("tsvd_tol", 0.01))
    tsvd_rank     = problem_spec.get("tsvd_rank", None)   # int or None
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
    # Observation vector
    # ------------------------------------------------------------------
    n_sensors   = len(sensor_pos)
    n_obs_rows  = S.shape[0]
    n_obs_times = n_obs_rows // n_sensors

    T_obs_use = T_obs_noisy[:, :n_obs_times]
    y_obs = T_obs_use.flatten() - T0

    # ------------------------------------------------------------------
    # Thin SVD of S
    # ------------------------------------------------------------------
    t_svd_start = time.perf_counter()

    # S shape: (M, N) where M = n_sensors * n_obs_times, N = ny_q * nt_q
    U, s, Vt = np.linalg.svd(S, full_matrices=False)   # U(M,K), s(K,), Vt(K,N)
    K = len(s)

    # ------------------------------------------------------------------
    # Rank selection
    # ------------------------------------------------------------------
    if tsvd_rank is not None:
        r = int(np.clip(tsvd_rank, 1, K))
    else:
        # Relative threshold: keep σ_k ≥ tol × σ_max
        r = int(np.sum(s >= tsvd_tol * s[0]))
        r = max(r, 1)   # always keep at least one mode

    # Truncated pseudoinverse
    U_r  = U[:, :r]         # (M, r)
    s_r  = s[:r]            # (r,)
    Vt_r = Vt[:r, :]        # (r, N)

    q_vec = Vt_r.T @ ((U_r.T @ y_obs) / s_r)   # (N,)

    t_svd = time.perf_counter() - t_svd_start
    t_total = time.perf_counter() - t0

    # ------------------------------------------------------------------
    # Metrics
    # ------------------------------------------------------------------
    flux_pred = q_vec.reshape(ny_q, nt_q)

    residual    = S @ q_vec - y_obs
    replay_rmse = float(np.sqrt(np.mean(residual ** 2)))
    loss        = float(0.5 * np.dot(residual, residual))

    flux_rmse: float | None = None
    if q_true is not None:
        q_true_arr = np.asarray(q_true, dtype=float)
        if q_true_arr.shape == flux_pred.shape:
            flux_rmse = float(np.sqrt(np.mean((flux_pred - q_true_arr) ** 2)))

    # Effective condition number using truncated spectrum
    cond_trunc = float(s[0] / s[r - 1]) if r > 0 else float("inf")

    diagnostics: dict[str, Any] = {
        "solver_name":       "tsvd_2d",
        "tsvd_tol":          tsvd_tol,
        "kept_rank":         r,
        "max_rank":          K,
        "sigma_max":         float(s[0]),
        "sigma_min_kept":    float(s[r - 1]),
        "cond_trunc":        cond_trunc,
        "frac_energy_kept":  float(np.sum(s_r ** 2) / np.sum(s ** 2)),
        "loss":              loss,
        "t_sensitivity_s":   t_sensitivity,
        "t_svd_s":           t_svd,
        "t_total_s":         t_total,
        "S_shape":           list(S.shape),
        "N_params":          ny_q * nt_q,
    }

    return {
        "flux_pred":        flux_pred,
        "flux_rmse":        flux_rmse,
        "replay_rmse":      replay_rmse,
        "loss":             loss,
        "convergence_flag": np.isfinite(flux_rmse if flux_rmse is not None else 0.0),
        "diagnostics":      diagnostics,
    }
