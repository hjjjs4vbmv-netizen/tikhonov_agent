"""
run_pinn_full_training_pilot.py
================================
Full-training DeepXDE PINN pilot for two representative 2D inverse cases.

Training policy
---------------
  Stage 1 : Adam warm-up        — 10 000 iterations, lr = 1e-3
  Stage 2 : L-BFGS refinement   — 500 function evaluations, strong-Wolfe

Cases
-----
  A : gaussian_localized,      σ_noise = 0.1 K, medium (3×3 = 9 sensors), seed=0
  B : overlapping_multi_spot,  σ_noise = 0.1 K, medium (3×3 = 9 sensors), seed=0

Outputs
-------
  reports/pinn_full_training_pilot/raw_metrics.csv
  reports/pinn_full_training_pilot/config_used.json
  reports/pinn_full_training_pilot/training_log.txt
  reports/pinn_full_training_pilot/pilot_report.md
  figures/pinn_full_training_pilot/caseA_flux_comparison.png
  figures/pinn_full_training_pilot/caseA_T_snapshots.png
  figures/pinn_full_training_pilot/caseA_sensor_replay.png
  figures/pinn_full_training_pilot/caseA_loss_curve.png
  figures/pinn_full_training_pilot/caseB_flux_comparison.png
  figures/pinn_full_training_pilot/caseB_T_snapshots.png
  figures/pinn_full_training_pilot/caseB_sensor_replay.png
  figures/pinn_full_training_pilot/caseB_loss_curve.png
"""

from __future__ import annotations

import csv
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

REPORTS_DIR = _HERE / "reports" / "pinn_full_training_pilot"
FIGURES_DIR = _HERE / "figures" / "pinn_full_training_pilot"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

LOG_PATH = REPORTS_DIR / "training_log.txt"


# ---------------------------------------------------------------------------
# Training log helper
# ---------------------------------------------------------------------------
class TrainingLogger:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._f = path.open("w", buffering=1)
        self._t0 = time.perf_counter()

    def log(self, msg: str) -> None:
        elapsed = time.perf_counter() - self._t0
        line = f"[{elapsed:8.1f}s] {msg}"
        print(line)
        self._f.write(line + "\n")

    def close(self) -> None:
        self._f.close()


# ---------------------------------------------------------------------------
# Environment audit
# ---------------------------------------------------------------------------

def audit_environment(logger: TrainingLogger) -> dict[str, Any]:
    logger.log("=== Environment audit ===")
    info: dict[str, Any] = {}

    # Python
    info["python"] = sys.version.split()[0]
    logger.log(f"Python  : {info['python']}")

    # PyTorch
    try:
        import torch
        info["pytorch"] = torch.__version__
        info["cuda_available"] = torch.cuda.is_available()
        if torch.cuda.is_available():
            info["cuda_version"] = torch.version.cuda
            info["gpu_name"] = torch.cuda.get_device_name(0)
            info["gpu_memory_gb"] = round(
                torch.cuda.get_device_properties(0).total_memory / 1e9, 1
            )
            logger.log(f"PyTorch : {info['pytorch']}")
            logger.log(f"CUDA    : {info['cuda_version']}")
            logger.log(f"GPU     : {info['gpu_name']}  ({info['gpu_memory_gb']} GB)")
        else:
            info["gpu_name"] = "CPU"
            logger.log(f"PyTorch : {info['pytorch']}  (CUDA not available — CPU mode)")
    except ImportError:
        logger.log("ERROR: PyTorch not found")
        raise

    # DeepXDE
    os.environ.setdefault("DDE_BACKEND", "pytorch")
    try:
        import deepxde as dde
        from deepxde.backend import backend_name
        info["deepxde"] = dde.__version__
        info["dde_backend"] = backend_name
        logger.log(f"DeepXDE : {info['deepxde']}  backend={info['dde_backend']}")
        if backend_name != "pytorch":
            logger.log(
                f"WARNING: DDE_BACKEND={backend_name!r} — expected pytorch. "
                "Set DDE_BACKEND=pytorch before running."
            )
    except ImportError:
        logger.log("WARNING: deepxde not importable (will use raw PyTorch)")
        info["deepxde"] = "not_installed"
        info["dde_backend"] = "n/a"

    logger.log("=== Environment OK ===\n")
    return info


# ---------------------------------------------------------------------------
# PINN components (self-contained — no import from deepxde_pinn_solver_2d)
# ---------------------------------------------------------------------------

def _build_fnn(
    input_dim: int,
    hidden_layers: list[int],
    output_dim: int,
    device: Any,
    dtype: Any,
) -> Any:
    import torch.nn as nn
    layers: list[nn.Module] = []
    in_ch = input_dim
    for h in hidden_layers:
        layers.append(nn.Linear(in_ch, h))
        layers.append(nn.Tanh())
        in_ch = h
    layers.append(nn.Linear(in_ch, output_dim))
    net = nn.Sequential(*layers).to(device=device, dtype=dtype)
    for module in net.modules():
        if isinstance(module, nn.Linear):
            nn.init.xavier_normal_(module.weight)
            nn.init.zeros_(module.bias)
    return net


def _bilinear_interp_q(
    q_params: Any,   # (ny_q * nt_q,) flat Parameter
    y_pts: Any,      # (N,) normalised y ∈ [0,1]
    t_pts: Any,      # (N,) normalised t ∈ [0,1]
    ny_q: int,
    nt_q: int,
) -> Any:
    import torch
    q_grid = q_params.view(ny_q, nt_q)
    yf = y_pts * (ny_q - 1)
    tf = t_pts * (nt_q - 1)
    y0 = torch.clamp(yf.long(), 0, ny_q - 2)
    t0 = torch.clamp(tf.long(), 0, nt_q - 2)
    y1 = y0 + 1
    t1 = t0 + 1
    wy1 = yf - y0.float()
    wy0 = 1.0 - wy1
    wt1 = tf - t0.float()
    wt0 = 1.0 - wt1
    return (
        wy0 * wt0 * q_grid[y0, t0]
        + wy1 * wt0 * q_grid[y1, t0]
        + wy0 * wt1 * q_grid[y0, t1]
        + wy1 * wt1 * q_grid[y1, t1]
    )


def _compute_loss(
    net: Any,
    q_params: Any,
    *,
    # collocation arrays (normalised coords, pre-built tensors)
    pde_x: Any, pde_y: Any, pde_t: Any,
    ic_inp: Any,
    bc_lft_y: Any, bc_lft_t: Any,
    bc_rgt_y: Any, bc_rgt_t: Any,
    bc_top_x: Any, bc_top_t: Any,
    bc_bot_x: Any, bc_bot_t: Any,
    sd_x: Any, sd_y: Any, sd_t: Any, sd_T: Any,
    # domain params
    Lx: float, Ly: float, t_end: float, alpha: float, k: float,
    ny_q: int, nt_q: int,
    n_bc: int, n_ic: int,
    # weights
    w_pde: float, w_ic: float, w_bc_flux: float, w_bc_ins: float, w_data: float,
) -> tuple[Any, dict[str, float]]:
    import torch

    # --- PDE interior ---
    px = pde_x.requires_grad_(True)
    py = pde_y.requires_grad_(True)
    pt = pde_t.requires_grad_(True)
    T_pde = net(torch.stack([px.squeeze(), py.squeeze(), pt.squeeze()], dim=1))
    T_t  = torch.autograd.grad(T_pde.sum(), pt, create_graph=True)[0]
    T_x_ = torch.autograd.grad(T_pde.sum(), px, create_graph=True)[0]
    T_xx = torch.autograd.grad(T_x_.sum(), px, create_graph=True)[0]
    T_y_ = torch.autograd.grad(T_pde.sum(), py, create_graph=True)[0]
    T_yy = torch.autograd.grad(T_y_.sum(), py, create_graph=True)[0]
    pde_res = (T_t / t_end) - alpha * (T_xx / Lx**2 + T_yy / Ly**2)
    loss_pde = w_pde * torch.mean(pde_res ** 2)

    # --- IC: T(x,y,0) = 0 (T is shifted by T0) ---
    T_ic = net(ic_inp)
    loss_ic = w_ic * torch.mean(T_ic ** 2)

    # --- Left BC (flux): -k * dT/dx = q(y,t) ---
    bc_lft_x = torch.zeros(n_bc, dtype=pde_x.dtype, device=pde_x.device).requires_grad_(True)
    inp_lft = torch.stack([bc_lft_x, bc_lft_y, bc_lft_t], dim=1)
    T_lft = net(inp_lft)
    dT_dx_lft = torch.autograd.grad(T_lft.sum(), bc_lft_x, create_graph=True)[0]
    q_at_bc = _bilinear_interp_q(q_params, bc_lft_y.detach(), bc_lft_t.detach(), ny_q, nt_q)
    loss_bc_flux = w_bc_flux * torch.mean((-k * dT_dx_lft / Lx - q_at_bc) ** 2)

    # --- Right BC (insulated): dT/dx(1,y,t) = 0 ---
    bc_rgt_x = torch.ones(n_bc, dtype=pde_x.dtype, device=pde_x.device).requires_grad_(True)
    inp_rgt = torch.stack([bc_rgt_x, bc_rgt_y, bc_rgt_t], dim=1)
    T_rgt = net(inp_rgt)
    dT_dx_rgt = torch.autograd.grad(T_rgt.sum(), bc_rgt_x, create_graph=True)[0]
    loss_bc_rgt = w_bc_ins * torch.mean(dT_dx_rgt ** 2)

    # --- Top BC (insulated): dT/dy(x,1,t) = 0 ---
    bc_top_y = torch.ones(n_bc, dtype=pde_x.dtype, device=pde_x.device).requires_grad_(True)
    inp_top = torch.stack([bc_top_x, bc_top_y, bc_top_t], dim=1)
    T_top = net(inp_top)
    dT_dy_top = torch.autograd.grad(T_top.sum(), bc_top_y, create_graph=True)[0]
    loss_bc_top = w_bc_ins * torch.mean(dT_dy_top ** 2)

    # --- Bottom BC (insulated): dT/dy(x,0,t) = 0 ---
    bc_bot_y = torch.zeros(n_bc, dtype=pde_x.dtype, device=pde_x.device).requires_grad_(True)
    inp_bot = torch.stack([bc_bot_x, bc_bot_y, bc_bot_t], dim=1)
    T_bot = net(inp_bot)
    dT_dy_bot = torch.autograd.grad(T_bot.sum(), bc_bot_y, create_graph=True)[0]
    loss_bc_bot = w_bc_ins * torch.mean(dT_dy_bot ** 2)

    # --- Sensor data ---
    inp_data = torch.stack([sd_x, sd_y, sd_t], dim=1)
    T_pred_data = net(inp_data).squeeze(1)
    loss_data = w_data * torch.mean((T_pred_data - sd_T) ** 2)

    loss = loss_pde + loss_ic + loss_bc_flux + loss_bc_rgt + loss_bc_top + loss_bc_bot + loss_data

    components = {
        "pde": float(loss_pde.detach().cpu()),
        "ic": float(loss_ic.detach().cpu()),
        "bc_flux": float(loss_bc_flux.detach().cpu()),
        "bc_ins": float((loss_bc_rgt + loss_bc_top + loss_bc_bot).detach().cpu()),
        "data": float(loss_data.detach().cpu()),
        "total": float(loss.detach().cpu()),
    }
    return loss, components


# ---------------------------------------------------------------------------
# FD full-field extraction helper
# ---------------------------------------------------------------------------

def simulate_full_field(
    simulator: Any,
    q_flux_2d: np.ndarray,
    T0: float,
    snapshot_times: list[float],
    t_end: float,
) -> list[np.ndarray]:
    """Run FD and return T(x,y,t_k) snapshots at specified times.

    Returns list of (nx, ny) arrays, one per snapshot time.
    """
    dt = simulator.dt
    n_steps = int(np.ceil(t_end / dt))
    sim_times = np.arange(n_steps + 1, dtype=float) * dt

    nx, ny = simulator.nx, simulator.ny
    k = simulator.k

    nt_q = q_flux_2d.shape[1]
    t_q = np.linspace(0.0, t_end, nt_q)
    q_fine = np.zeros((ny, n_steps + 1), dtype=float)
    for j in range(ny):
        q_fine[j, :] = np.interp(sim_times, t_q, q_flux_2d[j, :])

    # Identify closest step indices for snapshot times
    snap_step_indices = [int(np.argmin(np.abs(sim_times - ts))) for ts in snapshot_times]
    snap_fields: list[np.ndarray | None] = [None] * len(snapshot_times)

    u = np.full((nx, ny), T0, dtype=float)

    # Record t=0 if requested
    for si_idx, step_idx in enumerate(snap_step_indices):
        if step_idx == 0:
            snap_fields[si_idx] = u.copy()

    for n in range(1, n_steps + 1):
        q_t = q_fine[:, n]
        u_left_ghost = u[0, :] + simulator.dx * q_t / k
        u_right_ghost = u[-1, :]
        u_ext_x = np.vstack([u_left_ghost[np.newaxis, :], u, u_right_ghost[np.newaxis, :]])
        laplx = (u_ext_x[:-2, :] - 2.0 * u_ext_x[1:-1, :] + u_ext_x[2:, :]) / simulator.dx**2

        u_bot_ghost = u[:, 0]
        u_top_ghost = u[:, -1]
        u_ext_y = np.hstack([u_bot_ghost[:, np.newaxis], u, u_top_ghost[:, np.newaxis]])
        laply = (u_ext_y[:, :-2] - 2.0 * u_ext_y[:, 1:-1] + u_ext_y[:, 2:]) / simulator.dy**2

        u = u + dt * simulator.alpha * (laplx + laply)

        for si_idx, step_idx in enumerate(snap_step_indices):
            if n == step_idx and snap_fields[si_idx] is None:
                snap_fields[si_idx] = u.copy()

    # Fill any remaining
    for si_idx, sf in enumerate(snap_fields):
        if sf is None:
            snap_fields[si_idx] = u.copy()

    return snap_fields  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Main PINN trainer for one case
# ---------------------------------------------------------------------------

def run_case(
    case_name: str,
    case_label: str,
    family_name: str,
    primary_axis_level: int,
    sigma_noise: float,
    sensor_config: str,
    seed: int,
    n_adam: int,
    lr_adam: float,
    n_lbfgs: int,
    hidden_layers: list[int],
    n_pde_pts: int,
    n_bc_pts: int,
    n_ic_pts: int,
    w_pde: float,
    w_ic: float,
    w_bc_flux: float,
    w_bc_ins: float,
    w_data: float,
    ny_q: int,
    nt_q: int,
    logger: TrainingLogger,
) -> dict[str, Any]:
    """Train PINN for one case and return metrics + artefacts."""
    import torch
    import torch.nn as nn

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dtype = torch.float64
    logger.log(f"\n{'='*60}")
    logger.log(f"CASE {case_label}: {case_name}  (family={family_name}, level={primary_axis_level})")
    logger.log(f"Device: {device}  |  dtype: {dtype}")
    logger.log(f"{'='*60}")

    t_case_start = time.perf_counter()

    # ------------------------------------------------------------------
    # Domain setup
    # ------------------------------------------------------------------
    from src.forward.heat2d_simulator import (
        HeatConduction2DFD,
        generate_sensor_grid,
        DEFAULT_LX, DEFAULT_LY, DEFAULT_ALPHA, DEFAULT_K,
        DEFAULT_T0, DEFAULT_T_TOTAL,
    )
    from src.heat_flux_families import generate_family_flux

    Lx = DEFAULT_LX
    Ly = DEFAULT_LY
    alpha_phys = DEFAULT_ALPHA
    k_phys = DEFAULT_K
    T0 = DEFAULT_T0
    t_end = DEFAULT_T_TOTAL
    obs_every = 8

    simulator = HeatConduction2DFD(Lx=Lx, Ly=Ly, nx=20, ny=20,
                                   alpha=alpha_phys, k=k_phys)

    sensor_positions = generate_sensor_grid(sensor_config, Lx, Ly)
    n_sensors = len(sensor_positions)

    # ------------------------------------------------------------------
    # Ground-truth flux (two resolutions)
    # ------------------------------------------------------------------
    y_q_grid = np.linspace(0.0, Ly, ny_q)           # coarse: (ny_q,) for PINN/metrics
    t_q_grid = np.linspace(0.0, t_end, nt_q)
    q_true = generate_family_flux(
        family_name, y_q_grid, t_q_grid,
        primary_axis_level=primary_axis_level, seed=seed,
    )   # (ny_q, nt_q)  — used for metrics and PINN target

    # Fine y-grid for FD forward model (must match simulator.ny = 20)
    y_fine = simulator.y_centers   # (ny,)
    q_fine_for_fd = generate_family_flux(
        family_name, y_fine, t_q_grid,
        primary_axis_level=primary_axis_level, seed=seed,
    )  # (ny, nt_q)

    logger.log(
        f"q_true (coarse): shape={q_true.shape}  "
        f"range=[{q_true.min():.1f}, {q_true.max():.1f}] W/m²"
    )

    # ------------------------------------------------------------------
    # Forward simulation → noisy sensor readings
    # ------------------------------------------------------------------
    rng_noise = np.random.default_rng(seed)
    T_sensors_clean, obs_times = simulator.simulate(
        q_fine_for_fd, T0, sensor_positions, t_end=t_end, obs_every=obs_every
    )
    T_obs_noisy = T_sensors_clean + rng_noise.normal(0.0, sigma_noise, T_sensors_clean.shape)

    logger.log(
        f"Sensors: {n_sensors}  |  obs steps: {T_obs_noisy.shape[1]}  "
        f"|  noise σ={sigma_noise} K"
    )

    # ------------------------------------------------------------------
    # Full-field FD snapshots for ground-truth T(x,y,t_k)
    # ------------------------------------------------------------------
    snapshot_times = [t_end * 0.25, t_end * 0.50, t_end * 0.75]
    T_fd_snapshots = simulate_full_field(
        simulator, q_fine_for_fd, T0, snapshot_times, t_end
    )   # list of (nx, ny) arrays

    logger.log(
        f"FD snapshots at t={[f'{s:.0f}s' for s in snapshot_times]}: "
        f"{[s.shape for s in T_fd_snapshots]}"
    )

    # ------------------------------------------------------------------
    # PINN training setup
    # ------------------------------------------------------------------
    rng = np.random.default_rng(seed + 100)

    def to_tensor(arr: np.ndarray) -> Any:
        return torch.as_tensor(arr, dtype=dtype, device=device)

    # Normalised sensor data (T shifted by T0)
    T_obs_shifted = T_obs_noisy - T0
    sensor_data_list = []
    for si, (xp, yp) in enumerate(sensor_positions):
        for ti, t_obs in enumerate(obs_times):
            sensor_data_list.append([xp / Lx, yp / Ly, t_obs / t_end,
                                      float(T_obs_shifted[si, ti])])
    sensor_data = np.array(sensor_data_list, dtype=float)

    sd_x = to_tensor(sensor_data[:, 0])
    sd_y = to_tensor(sensor_data[:, 1])
    sd_t = to_tensor(sensor_data[:, 2])
    sd_T = to_tensor(sensor_data[:, 3])

    # Collocation points (normalised)
    pde_x_np = rng.uniform(0, 1, n_pde_pts).astype(np.float64)
    pde_y_np = rng.uniform(0, 1, n_pde_pts).astype(np.float64)
    pde_t_np = rng.uniform(0, 1, n_pde_pts).astype(np.float64)

    pde_x_t = to_tensor(pde_x_np).unsqueeze(1)
    pde_y_t = to_tensor(pde_y_np).unsqueeze(1)
    pde_t_t = to_tensor(pde_t_np).unsqueeze(1)

    ic_inp = to_tensor(np.column_stack([
        rng.uniform(0, 1, n_ic_pts),
        rng.uniform(0, 1, n_ic_pts),
        np.zeros(n_ic_pts),
    ]))

    bc_lft_y = to_tensor(rng.uniform(0, 1, n_bc_pts))
    bc_lft_t = to_tensor(rng.uniform(0, 1, n_bc_pts))
    bc_rgt_y = to_tensor(rng.uniform(0, 1, n_bc_pts))
    bc_rgt_t = to_tensor(rng.uniform(0, 1, n_bc_pts))
    bc_top_x = to_tensor(rng.uniform(0, 1, n_bc_pts))
    bc_top_t = to_tensor(rng.uniform(0, 1, n_bc_pts))
    bc_bot_x = to_tensor(rng.uniform(0, 1, n_bc_pts))
    bc_bot_t = to_tensor(rng.uniform(0, 1, n_bc_pts))

    # Build network and flux parameters
    net = _build_fnn(3, hidden_layers, 1, device, dtype)
    q_params = nn.Parameter(torch.zeros(ny_q * nt_q, dtype=dtype, device=device))

    n_net = sum(p.numel() for p in net.parameters())
    logger.log(f"Net params: {n_net}  |  q_params: {ny_q * nt_q}  |  total: {n_net + ny_q * nt_q}")

    loss_kwargs = dict(
        pde_x=pde_x_t, pde_y=pde_y_t, pde_t=pde_t_t,
        ic_inp=ic_inp,
        bc_lft_y=bc_lft_y, bc_lft_t=bc_lft_t,
        bc_rgt_y=bc_rgt_y, bc_rgt_t=bc_rgt_t,
        bc_top_x=bc_top_x, bc_top_t=bc_top_t,
        bc_bot_x=bc_bot_x, bc_bot_t=bc_bot_t,
        sd_x=sd_x, sd_y=sd_y, sd_t=sd_t, sd_T=sd_T,
        Lx=Lx, Ly=Ly, t_end=t_end, alpha=alpha_phys, k=k_phys,
        ny_q=ny_q, nt_q=nt_q,
        n_bc=n_bc_pts, n_ic=n_ic_pts,
        w_pde=w_pde, w_ic=w_ic, w_bc_flux=w_bc_flux, w_bc_ins=w_bc_ins, w_data=w_data,
    )

    adam_loss_history: list[tuple[int, float, dict]] = []   # (iter, total, components)
    lbfgs_loss_history: list[tuple[int, float]] = []

    # ------------------------------------------------------------------
    # Stage 1: Adam
    # ------------------------------------------------------------------
    logger.log(f"\n--- Stage 1: Adam ({n_adam} iters, lr={lr_adam}) ---")
    optimizer_adam = torch.optim.Adam(list(net.parameters()) + [q_params], lr=lr_adam)

    log_every = max(1, n_adam // 50)
    for it in range(n_adam):
        optimizer_adam.zero_grad()
        loss, comps = _compute_loss(net, q_params, **loss_kwargs)
        loss.backward()
        # Gradient clipping for stability
        torch.nn.utils.clip_grad_norm_(list(net.parameters()) + [q_params], max_norm=1.0)
        optimizer_adam.step()

        if it % log_every == 0 or it == n_adam - 1:
            adam_loss_history.append((it, comps["total"], comps))
            logger.log(
                f"  Adam {it:6d}/{n_adam}  "
                f"total={comps['total']:.4e}  "
                f"pde={comps['pde']:.3e}  "
                f"data={comps['data']:.3e}  "
                f"bc_flux={comps['bc_flux']:.3e}"
            )

    adam_final = comps["total"]
    logger.log(f"Adam finished. Final loss: {adam_final:.4e}")

    # ------------------------------------------------------------------
    # Stage 2: L-BFGS with strong-Wolfe line search
    # ------------------------------------------------------------------
    logger.log(f"\n--- Stage 2: L-BFGS ({n_lbfgs} max_iter, strong-Wolfe) ---")
    optimizer_lbfgs = torch.optim.LBFGS(
        list(net.parameters()) + [q_params],
        lr=1.0,
        max_iter=20,
        max_eval=25,
        tolerance_grad=1e-7,
        tolerance_change=1e-9,
        history_size=50,
        line_search_fn="strong_wolfe",
    )

    lbfgs_iter = [0]
    lbfgs_final_loss = [adam_final]

    def lbfgs_closure():
        optimizer_lbfgs.zero_grad()
        loss_val, comps_val = _compute_loss(net, q_params, **loss_kwargs)
        loss_val.backward()
        torch.nn.utils.clip_grad_norm_(list(net.parameters()) + [q_params], max_norm=10.0)
        step_i = lbfgs_iter[0]
        lbfgs_loss_history.append((step_i, float(comps_val["total"])))
        lbfgs_final_loss[0] = float(comps_val["total"])
        if step_i % 50 == 0:
            logger.log(
                f"  L-BFGS closure #{step_i:4d}  "
                f"total={comps_val['total']:.4e}  "
                f"data={comps_val['data']:.3e}"
            )
        lbfgs_iter[0] += 1
        return loss_val

    # Run L-BFGS in batches of max_iter
    lbfgs_steps_done = 0
    while lbfgs_steps_done < n_lbfgs:
        optimizer_lbfgs.step(lbfgs_closure)
        lbfgs_steps_done = lbfgs_iter[0]
        if lbfgs_steps_done >= n_lbfgs:
            break

    lbfgs_final = lbfgs_final_loss[0]
    logger.log(f"L-BFGS finished after {lbfgs_iter[0]} closures. Final loss: {lbfgs_final:.4e}")

    t_training = time.perf_counter() - t_case_start
    logger.log(f"Total training time: {t_training:.1f} s")

    # ------------------------------------------------------------------
    # Extract predicted flux
    # ------------------------------------------------------------------
    with torch.no_grad():
        flux_pred = q_params.view(ny_q, nt_q).cpu().numpy().copy()

    logger.log(
        f"flux_pred: range=[{flux_pred.min():.1f}, {flux_pred.max():.1f}] W/m²"
    )

    # ------------------------------------------------------------------
    # Extract T_NN snapshots on fine spatial grid
    # ------------------------------------------------------------------
    nx_vis, ny_vis = simulator.nx, simulator.ny
    x_vis = np.linspace(0.0, 1.0, nx_vis)   # normalised
    y_vis = np.linspace(0.0, 1.0, ny_vis)
    XX, YY = np.meshgrid(x_vis, y_vis, indexing="ij")   # (nx, ny)

    T_nn_snapshots: list[np.ndarray] = []
    with torch.no_grad():
        for t_snap in snapshot_times:
            t_norm = t_snap / t_end
            TT_snap = np.full_like(XX, t_norm)
            pts = np.column_stack([XX.ravel(), YY.ravel(), TT_snap.ravel()])
            inp_snap = to_tensor(pts)
            T_pred_snap = net(inp_snap).cpu().numpy().reshape(nx_vis, ny_vis)
            T_nn_snapshots.append(T_pred_snap + T0)   # shift back to physical K

    # ------------------------------------------------------------------
    # Sensor replay (T_NN at sensor positions vs noisy observations)
    # ------------------------------------------------------------------
    replay_pred = np.zeros_like(T_obs_noisy)
    with torch.no_grad():
        for si, (xp, yp) in enumerate(sensor_positions):
            t_norms = (obs_times / t_end).astype(np.float64)
            x_norms = np.full_like(t_norms, xp / Lx)
            y_norms = np.full_like(t_norms, yp / Ly)
            pts = to_tensor(np.column_stack([x_norms, y_norms, t_norms]))
            replay_pred[si, :] = net(pts).cpu().numpy().squeeze() + T0

    replay_rmse = float(np.sqrt(np.mean((replay_pred - T_obs_noisy) ** 2)))
    logger.log(f"Sensor replay RMSE: {replay_rmse:.4f} K")

    # ------------------------------------------------------------------
    # Evaluation metrics
    # ------------------------------------------------------------------
    from src.metrics import compute_all_metrics
    metrics = compute_all_metrics(
        flux_pred, q_true,
        family_name=family_name,
        diag_dict={},
    )
    flux_rmse = metrics["rmse_flux"]
    ssim_val  = metrics["ssim_flux"]
    supp_ovl  = metrics["support_overlap"]
    logger.log(
        f"Metrics: flux_RMSE={flux_rmse:.2f} W/m²  "
        f"SSIM={ssim_val:.4f}  "
        f"support_overlap={supp_ovl:.4f}"
    )

    return {
        "case_name": case_name,
        "case_label": case_label,
        "family_name": family_name,
        "primary_axis_level": primary_axis_level,
        "sigma_noise": sigma_noise,
        "sensor_config": sensor_config,
        "seed": seed,
        # arrays
        "q_true": q_true,
        "flux_pred": flux_pred,
        "T_fd_snapshots": T_fd_snapshots,
        "T_nn_snapshots": T_nn_snapshots,
        "snapshot_times": snapshot_times,
        "T_obs_noisy": T_obs_noisy,
        "replay_pred": replay_pred,
        "obs_times": obs_times,
        "sensor_positions": sensor_positions,
        "adam_loss_history": adam_loss_history,
        "lbfgs_loss_history": lbfgs_loss_history,
        # scalars
        "flux_rmse": flux_rmse,
        "replay_rmse": replay_rmse,
        "ssim_flux": ssim_val,
        "support_overlap": supp_ovl,
        "runtime_seconds": t_training,
        "adam_final_loss": adam_final,
        "lbfgs_final_loss": lbfgs_final,
        "n_adam_iters": n_adam,
        "n_lbfgs_closures": lbfgs_iter[0],
    }


# ---------------------------------------------------------------------------
# Figure generation
# ---------------------------------------------------------------------------

def save_flux_comparison(result: dict, out_path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    q_true = result["q_true"]
    q_pred = result["flux_pred"]
    q_err  = q_pred - q_true
    vmax = max(abs(q_true.min()), abs(q_true.max())) or 1.0
    err_max = max(abs(q_err.max()), abs(q_err.min())) or 1.0

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    fig.suptitle(
        f"{result['case_label']}: {result['case_name']} — Flux Reconstruction\n"
        f"RMSE={result['flux_rmse']:.1f} W/m²  SSIM={result['ssim_flux']:.3f}  "
        f"Support={result['support_overlap']:.3f}",
        fontsize=10,
    )

    extent = [0, 100, 0, 0.1]
    kw = dict(origin="lower", aspect="auto", extent=extent)

    im0 = axes[0].imshow(q_true, cmap="RdBu_r", vmin=-vmax, vmax=vmax, **kw)
    axes[0].set_title("Ground truth q(y,t) [W/m²]")
    plt.colorbar(im0, ax=axes[0])

    im1 = axes[1].imshow(q_pred, cmap="RdBu_r", vmin=-vmax, vmax=vmax, **kw)
    axes[1].set_title("PINN prediction [W/m²]")
    plt.colorbar(im1, ax=axes[1])

    im2 = axes[2].imshow(q_err, cmap="RdBu_r", vmin=-err_max, vmax=err_max, **kw)
    axes[2].set_title("Error (pred − truth) [W/m²]")
    plt.colorbar(im2, ax=axes[2])

    for ax in axes:
        ax.set_xlabel("t [s]")
        ax.set_ylabel("y [m]")

    plt.tight_layout()
    plt.savefig(out_path, dpi=130, bbox_inches="tight")
    plt.close()
    print(f"  Saved {out_path.name}")


def save_T_snapshots(result: dict, out_path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    times = result["snapshot_times"]
    T_fd  = result["T_fd_snapshots"]
    T_nn  = result["T_nn_snapshots"]
    n = len(times)

    fig, axes = plt.subplots(3, n, figsize=(4 * n, 9))
    fig.suptitle(
        f"{result['case_label']}: {result['case_name']} — Temperature Field Snapshots",
        fontsize=11,
    )

    for col, (t_s, fd, nn) in enumerate(zip(times, T_fd, T_nn)):
        err = nn - fd
        T_all = np.concatenate([fd.ravel(), nn.ravel()])
        vmin_T, vmax_T = T_all.min(), T_all.max()
        err_abs = max(abs(err.min()), abs(err.max())) or 0.1

        kw = dict(origin="lower", aspect="auto")
        im0 = axes[0][col].imshow(fd.T, cmap="hot", vmin=vmin_T, vmax=vmax_T, **kw)
        axes[0][col].set_title(f"T_FD at t={t_s:.0f}s [K]")
        plt.colorbar(im0, ax=axes[0][col])

        im1 = axes[1][col].imshow(nn.T, cmap="hot", vmin=vmin_T, vmax=vmax_T, **kw)
        axes[1][col].set_title(f"T_NN at t={t_s:.0f}s [K]")
        plt.colorbar(im1, ax=axes[1][col])

        im2 = axes[2][col].imshow(err.T, cmap="RdBu_r",
                                  vmin=-err_abs, vmax=err_abs, **kw)
        axes[2][col].set_title(f"Error [K]  (max={err_abs:.2f})")
        plt.colorbar(im2, ax=axes[2][col])

    row_labels = ["T_FD (truth)", "T_NN (PINN)", "Error (NN−FD)"]
    for row_idx, label in enumerate(row_labels):
        axes[row_idx][0].set_ylabel(label, fontsize=9)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"  Saved {out_path.name}")


def save_sensor_replay(result: dict, out_path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    T_obs  = result["T_obs_noisy"]
    T_pred = result["replay_pred"]
    times  = result["obs_times"]
    n_s    = T_obs.shape[0]

    ncols = min(3, n_s)
    nrows = (n_s + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 3 * nrows), squeeze=False)
    fig.suptitle(
        f"{result['case_label']}: {result['case_name']} — Sensor Replay\n"
        f"Replay RMSE = {result['replay_rmse']:.4f} K",
        fontsize=10,
    )

    for si in range(n_s):
        row, col = divmod(si, ncols)
        ax = axes[row][col]
        ax.plot(times, T_obs[si, :], "k.", markersize=3, label="obs (noisy)")
        ax.plot(times, T_pred[si, :], "r-", linewidth=1.5, label="T_NN")
        ax.set_title(
            f"Sensor {si}  ({result['sensor_positions'][si][0]*100:.1f},{result['sensor_positions'][si][1]*100:.1f}) cm",
            fontsize=8,
        )
        ax.set_xlabel("t [s]", fontsize=7)
        ax.set_ylabel("T [K]", fontsize=7)
        ax.legend(fontsize=6)
        ax.grid(alpha=0.3)

    # Hide unused subplots
    for si in range(n_s, nrows * ncols):
        row, col = divmod(si, ncols)
        axes[row][col].set_visible(False)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"  Saved {out_path.name}")


def save_loss_curve(result: dict, out_path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    adam_hist  = result["adam_loss_history"]   # list of (iter, total, comps)
    lbfgs_hist = result["lbfgs_loss_history"]  # list of (step, total)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle(
        f"{result['case_label']}: {result['case_name']} — Training Loss",
        fontsize=11,
    )

    # Adam
    if adam_hist:
        iters  = [h[0] for h in adam_hist]
        totals = [h[1] for h in adam_hist]
        pdels  = [h[2].get("pde", float("nan")) for h in adam_hist]
        datas  = [h[2].get("data", float("nan")) for h in adam_hist]
        bc_fs  = [h[2].get("bc_flux", float("nan")) for h in adam_hist]

        ax1.semilogy(iters, totals, "k-", label="total", linewidth=1.5)
        ax1.semilogy(iters, pdels, "b--", label="PDE", linewidth=1.0)
        ax1.semilogy(iters, datas, "r-.", label="data", linewidth=1.0)
        ax1.semilogy(iters, bc_fs, "g:", label="flux BC", linewidth=1.0)
        ax1.set_xlabel("Adam iteration")
        ax1.set_ylabel("Loss")
        ax1.set_title(f"Stage 1: Adam ({result['n_adam_iters']} iters)")
        ax1.legend(fontsize=8)
        ax1.grid(alpha=0.3)

    # L-BFGS
    if lbfgs_hist:
        steps  = [h[0] for h in lbfgs_hist]
        losses = [h[1] for h in lbfgs_hist]
        ax2.semilogy(steps, losses, "m-", linewidth=1.5)
        ax2.set_xlabel("L-BFGS closure count")
        ax2.set_ylabel("Loss")
        ax2.set_title(
            f"Stage 2: L-BFGS ({result['n_lbfgs_closures']} closures)\n"
            f"Final: {result['lbfgs_final_loss']:.4e}"
        )
        ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"  Saved {out_path.name}")


# ---------------------------------------------------------------------------
# Report writing
# ---------------------------------------------------------------------------

def save_csv(results: list[dict], path: Path) -> None:
    fields = [
        "case_label", "case_name", "family_name", "primary_axis_level",
        "sigma_noise", "sensor_config", "seed",
        "flux_rmse", "replay_rmse", "ssim_flux", "support_overlap",
        "runtime_seconds", "adam_final_loss", "lbfgs_final_loss",
        "n_adam_iters", "n_lbfgs_closures",
    ]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(results)
    print(f"  Saved {path.name}")


def save_config(cfg: dict, path: Path) -> None:
    with path.open("w") as f:
        json.dump(cfg, f, indent=2, default=str)
    print(f"  Saved {path.name}")


def save_markdown_report(results: list[dict], env_info: dict, cfg: dict, path: Path) -> None:
    lines = [
        "# PINN Full-Training Pilot Report",
        "",
        "## Environment",
        "",
        f"- Python: {env_info.get('python', 'n/a')}",
        f"- PyTorch: {env_info.get('pytorch', 'n/a')}",
        f"- CUDA: {env_info.get('cuda_version', 'n/a')}",
        f"- GPU: {env_info.get('gpu_name', 'n/a')}",
        f"- DeepXDE: {env_info.get('deepxde', 'n/a')}  backend={env_info.get('dde_backend', 'n/a')}",
        "",
        "## Training Configuration",
        "",
        f"- Adam iterations: {cfg['n_adam']}",
        f"- Adam lr: {cfg['lr_adam']}",
        f"- L-BFGS max closures: {cfg['n_lbfgs']}",
        f"- Hidden layers: {cfg['hidden_layers']}",
        f"- PDE collocation points: {cfg['n_pde_pts']}",
        f"- BC collocation points: {cfg['n_bc_pts']}",
        f"- IC collocation points: {cfg['n_ic_pts']}",
        f"- Loss weights: pde={cfg['w_pde']}, ic={cfg['w_ic']}, bc_flux={cfg['w_bc_flux']}, bc_ins={cfg['w_bc_ins']}, data={cfg['w_data']}",
        "",
        "## Results Summary",
        "",
        "| Case | Family | Flux RMSE [W/m²] | Replay RMSE [K] | SSIM | Support Overlap | Runtime [s] |",
        "|------|--------|-----------------|-----------------|------|-----------------|-------------|",
    ]
    for r in results:
        lines.append(
            f"| {r['case_label']} | {r['family_name']} "
            f"| {r['flux_rmse']:.2f} "
            f"| {r['replay_rmse']:.4f} "
            f"| {r['ssim_flux']:.4f} "
            f"| {r['support_overlap']:.4f} "
            f"| {r['runtime_seconds']:.1f} |"
        )

    lines += [
        "",
        "## Per-Case Details",
        "",
    ]
    for r in results:
        lines += [
            f"### {r['case_label']}: {r['case_name']}",
            "",
            f"- **Family**: `{r['family_name']}` (primary_axis_level={r['primary_axis_level']})",
            f"- **Noise**: σ = {r['sigma_noise']} K",
            f"- **Sensors**: {r['sensor_config']} layout",
            f"- **Adam final loss**: {r['adam_final_loss']:.4e}",
            f"- **L-BFGS final loss**: {r['lbfgs_final_loss']:.4e}  "
            f"({r['n_lbfgs_closures']} closure evaluations)",
            f"- **Flux RMSE**: {r['flux_rmse']:.2f} W/m²",
            f"- **Sensor replay RMSE**: {r['replay_rmse']:.4f} K",
            f"- **SSIM**: {r['ssim_flux']:.4f}",
            f"- **Support overlap (Dice)**: {r['support_overlap']:.4f}",
            f"- **Runtime**: {r['runtime_seconds']:.1f} s",
            "",
            f"**Figures** (see `figures/pinn_full_training_pilot/`):",
            f"- `case{r['case_label']}_flux_comparison.png` — q(y,t) truth / pred / error",
            f"- `case{r['case_label']}_T_snapshots.png` — T field at t=25/50/75 s",
            f"- `case{r['case_label']}_sensor_replay.png` — sensor replay curves",
            f"- `case{r['case_label']}_loss_curve.png` — Adam + L-BFGS loss history",
            "",
        ]

    lines += [
        "## Notes",
        "",
        "- The PINN enforces the 2D heat equation PDE as a soft loss via automatic differentiation.",
        "- Boundary flux q(y,t) is parameterised on a coarse (ny_q × nt_q) grid and optimised jointly with network weights.",
        "- Stage 1 (Adam) provides a good initialisation; Stage 2 (L-BFGS strong-Wolfe) refines to lower loss.",
        "- `replay_rmse` measures how well T_NN reproduces the noisy sensor observations (data fit quality).",
        "- `flux_rmse` measures how well the recovered q(y,t) matches the ground truth (inversion quality).",
        "- SSIM and support_overlap measure structural fidelity of the flux reconstruction.",
        "",
        "---",
        "*Generated by `run_pinn_full_training_pilot.py`*",
    ]

    with path.open("w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  Saved {path.name}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    logger = TrainingLogger(LOG_PATH)
    t0 = time.perf_counter()

    # ------------------------------------------------------------------
    # Environment audit
    # ------------------------------------------------------------------
    env_info = audit_environment(logger)

    # ------------------------------------------------------------------
    # Training configuration
    # ------------------------------------------------------------------
    cfg: dict[str, Any] = {
        "n_adam":        10_000,
        "lr_adam":       1e-3,
        "n_lbfgs":       500,
        "hidden_layers": [64, 64, 64, 64],
        "n_pde_pts":     1200,
        "n_bc_pts":      150,
        "n_ic_pts":      300,
        "w_pde":         1.0,
        "w_ic":          20.0,
        "w_bc_flux":     10.0,
        "w_bc_ins":      2.0,
        "w_data":        100.0,
        "ny_q":          8,
        "nt_q":          10,
        "sigma_noise":   0.1,
        "sensor_config": "medium",
        "obs_every":     8,
    }

    logger.log(f"Config: {json.dumps(cfg, indent=2)}")

    # ------------------------------------------------------------------
    # Case definitions
    # ------------------------------------------------------------------
    cases = [
        {
            "case_name":          "gaussian_localized_medium",
            "case_label":         "A",
            "family_name":        "gaussian_localized",
            "primary_axis_level": 1,   # σ_y = 0.15
            "sigma_noise":        cfg["sigma_noise"],
            "sensor_config":      cfg["sensor_config"],
            "seed":               0,
        },
        {
            "case_name":          "overlapping_multi_spot_medium",
            "case_label":         "B",
            "family_name":        "overlapping_multi_spot",
            "primary_axis_level": 1,   # sep = 0.20
            "sigma_noise":        cfg["sigma_noise"],
            "sensor_config":      cfg["sensor_config"],
            "seed":               0,
        },
    ]

    # Persist full config
    full_cfg = {**cfg, "cases": cases, "env": env_info}
    save_config(full_cfg, REPORTS_DIR / "config_used.json")

    # ------------------------------------------------------------------
    # Run cases
    # ------------------------------------------------------------------
    all_results: list[dict] = []

    for case_def in cases:
        result = run_case(
            **case_def,
            n_adam=cfg["n_adam"],
            lr_adam=cfg["lr_adam"],
            n_lbfgs=cfg["n_lbfgs"],
            hidden_layers=cfg["hidden_layers"],
            n_pde_pts=cfg["n_pde_pts"],
            n_bc_pts=cfg["n_bc_pts"],
            n_ic_pts=cfg["n_ic_pts"],
            w_pde=cfg["w_pde"],
            w_ic=cfg["w_ic"],
            w_bc_flux=cfg["w_bc_flux"],
            w_bc_ins=cfg["w_bc_ins"],
            w_data=cfg["w_data"],
            ny_q=cfg["ny_q"],
            nt_q=cfg["nt_q"],
            logger=logger,
        )
        all_results.append(result)

        # Save figures
        lbl = result["case_label"].lower()
        logger.log(f"\nGenerating figures for Case {result['case_label']} ...")
        save_flux_comparison(result, FIGURES_DIR / f"case{lbl}_flux_comparison.png")
        save_T_snapshots(result,     FIGURES_DIR / f"case{lbl}_T_snapshots.png")
        save_sensor_replay(result,   FIGURES_DIR / f"case{lbl}_sensor_replay.png")
        save_loss_curve(result,      FIGURES_DIR / f"case{lbl}_loss_curve.png")

    # ------------------------------------------------------------------
    # Save summary outputs
    # ------------------------------------------------------------------
    logger.log("\n=== Saving outputs ===")
    save_csv(all_results, REPORTS_DIR / "raw_metrics.csv")
    save_markdown_report(all_results, env_info, cfg, REPORTS_DIR / "pilot_report.md")

    t_total = time.perf_counter() - t0
    logger.log(f"\nPilot complete. Wall time: {t_total:.1f} s")
    logger.log(f"Reports → {REPORTS_DIR}")
    logger.log(f"Figures → {FIGURES_DIR}")
    logger.close()

    # Print final summary to stdout
    print("\n" + "="*60)
    print("PINN PILOT RESULTS SUMMARY")
    print("="*60)
    print(f"{'Case':<8} {'Family':<28} {'FluxRMSE':>12} {'SSIM':>8} {'Support':>9} {'Time':>8}")
    print("-"*60)
    for r in all_results:
        print(
            f"  {r['case_label']:<6} {r['family_name']:<28} "
            f"{r['flux_rmse']:>10.2f}  "
            f"{r['ssim_flux']:>6.4f}  "
            f"{r['support_overlap']:>7.4f}  "
            f"{r['runtime_seconds']:>6.1f}s"
        )
    print("="*60)


if __name__ == "__main__":
    main()
