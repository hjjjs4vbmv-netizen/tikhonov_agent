"""
deepxde_solver_2d.py
====================
2D IHCP inverse solver using the PyTorch backend (DeepXDE-style).

Problem
-------
Recover the spatially- and temporally-varying boundary heat flux

    q(y, t)   at x = 0

from sparse, noisy temperature observations inside a 2D plate.

Method
------
The 2D heat equation is *linear* in q, so the forward map

    q  →  T_sensors

is a linear operator.  We build this operator (the sensitivity matrix S) by
superposition (unit-impulse runs of the 2D FD simulator) and then solve the
resulting Tikhonov-regularised least-squares problem

    min_q  ||S q_vec − y_obs||²  +  λ ||L q_vec||²

using the PyTorch Adam (+ optional LBFGS) optimiser, exactly mirroring the
approach in `src/deepxde_solver.py` for the 1D case.

Public API
----------
    solve_2d(problem_spec)  →  dict

    problem_spec keys (all required):
        simulator        : HeatConduction2DFD instance (pre-configured)
        sensor_positions : list of (x, y) tuples
        T_obs_noisy      : (n_sensors, n_obs_steps) array  — sensor readings
        obs_every        : int — every obs_every-th internal step was recorded
        t_end            : float — simulation horizon [s]
        ny_q             : int — coarse flux grid size in y
        nt_q             : int — coarse flux grid size in t
        T0               : float — initial temperature (subtracted as baseline)

    Optional keys:
        lam              : float — regularisation weight (default 1e-4)
        n_iter           : int   — total optimisation iterations (default 2000)
        lr               : float — Adam learning rate (default 1e-2)
        reg_order        : int   — 0, 1, or 2 (default 1)
        use_lbfgs        : bool  — Adam warm-start + LBFGS refinement (default False)
        device           : str  — "cpu" or "cuda" (default "cpu")
"""

from __future__ import annotations

import os
from typing import Any

import numpy as np


# ---------------------------------------------------------------------------
# Regularisation matrix (1-D first/second-order difference operator)
# ---------------------------------------------------------------------------


def _build_reg_matrix(N: int, order: int) -> np.ndarray:
    """Build a difference regularisation matrix L of shape (N-order, N)."""
    L = np.eye(N)
    for _ in range(order):
        diff = np.diff(np.eye(L.shape[0]), n=1, axis=0)
        L = diff @ L
    return L


# ---------------------------------------------------------------------------
# Public solver entry point
# ---------------------------------------------------------------------------


def solve_2d(problem_spec: dict[str, Any]) -> dict[str, Any]:
    """Recover q(y, t) from 2D sensor observations using Tikhonov + PyTorch.

    Parameters
    ----------
    problem_spec : see module docstring

    Returns
    -------
    dict with keys:
        flux_pred    : (ny_q, nt_q) predicted flux on coarse grid [W/m^2]
        rmse         : float — RMSE of predicted vs true flux (if q_true provided)
        loss         : float — final optimisation loss
        diagnostics  : dict with timing, convergence, and iteration info
    """
    # -----------------------------------------------------------------------
    # Unpack spec
    # -----------------------------------------------------------------------
    simulator     = problem_spec["simulator"]
    sensor_pos    = problem_spec["sensor_positions"]
    T_obs_noisy   = np.asarray(problem_spec["T_obs_noisy"], dtype=float)
    obs_every     = int(problem_spec["obs_every"])
    t_end         = float(problem_spec["t_end"])
    ny_q          = int(problem_spec["ny_q"])
    nt_q          = int(problem_spec["nt_q"])
    T0            = float(problem_spec.get("T0", 0.0))

    lam           = float(problem_spec.get("lam", 1e-4))
    n_iter        = int(problem_spec.get("n_iter", 2000))
    lr            = float(problem_spec.get("lr", 1e-2))
    reg_order     = int(problem_spec.get("reg_order", 1))
    use_lbfgs     = bool(problem_spec.get("use_lbfgs", False))
    device_str    = str(problem_spec.get("device", "cpu"))
    q_true        = problem_spec.get("q_true", None)  # (ny_q, nt_q) or None

    import time
    t_start = time.perf_counter()

    # -----------------------------------------------------------------------
    # Build sensitivity matrix S (or reuse cached copy)
    # -----------------------------------------------------------------------
    if "S" in problem_spec:
        S        = np.asarray(problem_spec["S"],        dtype=float)
        y_q_grid = np.asarray(problem_spec["y_q_grid"])
        t_q_grid = np.asarray(problem_spec["t_q_grid"])
        t_sensitivity = 0.0
    else:
        S, obs_times_s, y_q_grid, t_q_grid = simulator.build_sensitivity_matrix(
            sensor_positions=sensor_pos,
            t_end=t_end,
            ny_q=ny_q,
            nt_q=nt_q,
            obs_every=obs_every,
        )
        t_sensitivity = time.perf_counter() - t_start

    # -----------------------------------------------------------------------
    # Prepare observation vector (subtract baseline T0)
    # -----------------------------------------------------------------------
    # T_obs_noisy has shape (n_sensors, n_obs).
    # The baseline (T0 with q=0) is simply T0 everywhere.
    n_obs = S.shape[0]  # n_sensors * n_obs_times
    y_obs_flat = T_obs_noisy.flatten() - T0   # shape (n_sensors * n_obs,)

    # Safety: clip to S row count if T_obs_noisy has more or fewer columns
    # (can happen if obs_every differs between generation and inversion)
    n_sensors = len(sensor_pos)
    n_obs_times = S.shape[0] // n_sensors
    if len(y_obs_flat) != n_obs:
        # Truncate or pad
        T_obs_trimmed = T_obs_noisy[:, :n_obs_times]
        y_obs_flat = T_obs_trimmed.flatten() - T0

    # -----------------------------------------------------------------------
    # Regularisation matrix L (on flattened q_vec of length ny_q * nt_q)
    # -----------------------------------------------------------------------
    N = ny_q * nt_q
    L = _build_reg_matrix(N, order=reg_order)

    # -----------------------------------------------------------------------
    # PyTorch optimisation
    # -----------------------------------------------------------------------
    os.environ.setdefault("DDE_BACKEND", "pytorch")
    try:
        import torch
    except ImportError as exc:
        raise ImportError(
            "deepxde_solver_2d requires PyTorch.  "
            "Install with:  pip install torch"
        ) from exc

    device = torch.device(device_str)
    dtype  = torch.float64

    S_t   = torch.as_tensor(S,          dtype=dtype, device=device)
    y_t   = torch.as_tensor(y_obs_flat, dtype=dtype, device=device)
    L_t   = torch.as_tensor(L,          dtype=dtype, device=device)

    q_vec = torch.nn.Parameter(torch.zeros(N, dtype=dtype, device=device))

    def loss_fn() -> "torch.Tensor":
        residual = S_t.matmul(q_vec) - y_t
        reg      = L_t.matmul(q_vec)
        return torch.sum(residual * residual) + lam * torch.sum(reg * reg)

    t_opt_start = time.perf_counter()
    final_loss  = float("nan")

    if use_lbfgs:
        # Adam warm-start
        warmup = min(n_iter // 2, 1000)
        adam = torch.optim.Adam([q_vec], lr=lr)
        for _ in range(warmup):
            adam.zero_grad()
            loss = loss_fn()
            loss.backward()
            adam.step()

        # LBFGS refinement
        lbfgs = torch.optim.LBFGS(
            [q_vec], lr=1.0, max_iter=n_iter - warmup,
            line_search_fn="strong_wolfe",
        )

        def closure() -> "torch.Tensor":
            lbfgs.zero_grad()
            loss = loss_fn()
            loss.backward()
            return loss

        loss_val = lbfgs.step(closure)
        final_loss = float(loss_val.detach().cpu())
        opt_used = "adam_lbfgs"
        n_iter_used = n_iter
    else:
        adam = torch.optim.Adam([q_vec], lr=lr)
        for _ in range(n_iter):
            adam.zero_grad()
            loss = loss_fn()
            loss.backward()
            adam.step()
        final_loss = float(loss_fn().detach().cpu())
        opt_used = "adam"
        n_iter_used = n_iter

    t_opt_elapsed = time.perf_counter() - t_opt_start
    t_total = time.perf_counter() - t_start

    # -----------------------------------------------------------------------
    # Extract result
    # -----------------------------------------------------------------------
    q_pred_vec  = q_vec.detach().cpu().numpy()  # (ny_q * nt_q,)
    flux_pred   = q_pred_vec.reshape(ny_q, nt_q)

    # -----------------------------------------------------------------------
    # RMSE against ground truth (if provided)
    # -----------------------------------------------------------------------
    rmse: float | None = None
    if q_true is not None:
        q_true_arr = np.asarray(q_true, dtype=float)
        if q_true_arr.shape == flux_pred.shape:
            rmse = float(np.sqrt(np.mean((flux_pred - q_true_arr) ** 2)))

    # -----------------------------------------------------------------------
    # Convergence flag: True when final loss is finite
    # -----------------------------------------------------------------------
    convergence_flag = bool(np.isfinite(final_loss))

    diagnostics: dict[str, Any] = {
        "solver_name":       "deepxde_pytorch_2d",
        "optimizer":         opt_used,
        "n_iter":            n_iter_used,
        "lam":               lam,
        "reg_order":         reg_order,
        "final_loss":        final_loss,
        "convergence_flag":  convergence_flag,
        "t_sensitivity_s":   t_sensitivity,
        "t_optim_s":         t_opt_elapsed,
        "t_total_s":         t_total,
        "S_shape":           list(S.shape),
        "n_params":          N,
        "y_q_grid":          y_q_grid.tolist(),
        "t_q_grid":          t_q_grid.tolist(),
    }

    return {
        "flux_pred":        flux_pred,        # (ny_q, nt_q)
        "rmse":             rmse,
        "loss":             final_loss,
        "convergence_flag": convergence_flag,
        "diagnostics":      diagnostics,
    }
