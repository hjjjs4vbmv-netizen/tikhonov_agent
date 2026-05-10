"""
run_pinn_recovery_pilot_v2.py
==============================
PINN Recovery Pilot v2 — Admission test for deepxde_pinn as a benchmark-equal solver.

Previous failure (pilot v1):
  - flux_rmse = 272/340 W/m²  |  SSIM ≈ 0.001  |  support_overlap = 0.0
  - q_params initialized to zeros, w_bc_flux = 10  → trivial q≈0 collapse
  - sensors in interior only (x ∈ [0.1,0.9]·Lx) → no spatial gradient signal

Recovery strategies implemented:
  A. Boundary-biased sensor layout  (x ≈ 0.01·Lx, vs 0.1–0.9·Lx in v1)
  B. Stronger flux-BC weighting     (w_bc_flux = 500, vs 10 in v1)
  C. Normalized loss balancing      (divide each component by its initial scale)
  D. Tikhonov warm start            (q_params ← Tikhonov flux estimate)
  E. Fourier-basis q parameterization (8×8 = 64 cosine modes, low-rank)
  F. Two-stage training             (Adam 20 000 + L-BFGS 400 closures)

Mandatory cases:
  1. gaussian_localized,      σ = 0.1 K, medium + boundary-biased, seed = 0
  2. overlapping_multi_spot,  σ = 0.1 K, medium + boundary-biased, seed = 0

Outputs:
  reports/pinn_recovery_pilot_v2/
  figures/pinn_recovery_pilot_v2/
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

REPORTS_DIR = _HERE / "reports" / "pinn_recovery_pilot_v2"
FIGURES_DIR = _HERE / "figures" / "pinn_recovery_pilot_v2"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

LOG1_PATH = REPORTS_DIR / "training_log_case1.txt"
LOG2_PATH = REPORTS_DIR / "training_log_case2.txt"


# ---------------------------------------------------------------------------
# Training logger
# ---------------------------------------------------------------------------
class TrainingLogger:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._f = path.open("w", buffering=1)
        self._t0 = time.perf_counter()

    def log(self, msg: str) -> None:
        elapsed = time.perf_counter() - self._t0
        line = f"[{elapsed:8.1f}s] {msg}"
        print(line, flush=True)
        self._f.write(line + "\n")

    def close(self) -> None:
        self._f.close()


# ---------------------------------------------------------------------------
# Environment audit
# ---------------------------------------------------------------------------
def audit_environment() -> dict[str, Any]:
    print("\n" + "="*60)
    print("ENVIRONMENT AUDIT")
    print("="*60)
    info: dict[str, Any] = {}

    info["python"] = sys.version.split()[0]
    print(f"Python  : {info['python']}")

    import torch
    info["pytorch"] = torch.__version__
    info["cuda_available"] = torch.cuda.is_available()
    if torch.cuda.is_available():
        info["cuda_version"] = torch.version.cuda
        info["gpu_name"] = torch.cuda.get_device_name(0)
        info["gpu_memory_gb"] = round(torch.cuda.get_device_properties(0).total_memory / 1e9, 1)
        print(f"PyTorch : {info['pytorch']}")
        print(f"CUDA    : {info['cuda_version']}")
        print(f"GPU     : {info['gpu_name']}  ({info['gpu_memory_gb']} GB)")
        info["gpu_actually_used"] = True
    else:
        info["gpu_name"] = "CPU"
        print(f"PyTorch : {info['pytorch']}  (CUDA not available — aborting per spec)")
        raise RuntimeError("GPU required for PINN recovery pilot. No CUDA device found.")

    os.environ.setdefault("DDE_BACKEND", "pytorch")
    import deepxde as dde
    from deepxde.backend import backend_name
    info["deepxde"] = dde.__version__
    info["dde_backend"] = backend_name
    print(f"DeepXDE : {info['deepxde']}  backend={info['dde_backend']}")
    if backend_name != "pytorch":
        raise RuntimeError(f"Need DDE_BACKEND=pytorch, got {backend_name!r}")

    print("="*60 + "\n")
    return info


# ---------------------------------------------------------------------------
# Sensor layout helpers
# ---------------------------------------------------------------------------
def make_boundary_biased_layout(ny_s: int = 3, Lx: float = 0.1, Ly: float = 0.1,
                                  x_frac: float = 0.01) -> list[tuple[float, float]]:
    """3×ny_s sensors placed at x ≈ x_frac·Lx (very close to flux boundary).

    y positions span [0.1·Ly, 0.9·Ly] in ny_s uniform steps.
    x positions: one column at x_frac*Lx, one at 5*x_frac*Lx, one at 10*x_frac*Lx.
    """
    xs = [x_frac * Lx, 5.0 * x_frac * Lx, 10.0 * x_frac * Lx]
    ys = np.linspace(0.1 * Ly, 0.9 * Ly, ny_s).tolist()
    positions: list[tuple[float, float]] = []
    for xi in xs:
        for yj in ys:
            positions.append((float(xi), float(yj)))
    return positions


# ---------------------------------------------------------------------------
# Fourier-basis q parameterization  (Strategy E)
# ---------------------------------------------------------------------------
class FourierBasisQ:
    """Low-rank q(y,t) via truncated cosine basis.

    q(y,t) = By @ coeffs @ Bt.T
    where  By[j,k] = cos(k*pi*y_j/Ly)  and  Bt[n,k] = cos(k*pi*t_n/T).
    """
    def __init__(
        self,
        n_modes_y: int,
        n_modes_t: int,
        ny_q: int,
        nt_q: int,
        Ly: float,
        t_end: float,
        device: Any,
        dtype: Any,
    ) -> None:
        import torch
        self.ny_q = ny_q
        self.nt_q = nt_q
        self.n_modes_y = n_modes_y
        self.n_modes_t = n_modes_t

        y_q = np.linspace(0.0, Ly, ny_q)
        t_q = np.linspace(0.0, t_end, nt_q)

        By_np = np.zeros((ny_q, n_modes_y), dtype=np.float64)
        for k in range(n_modes_y):
            By_np[:, k] = np.cos(k * np.pi * y_q / Ly) / (1.0 if k == 0 else np.sqrt(0.5))
        # Normalize columns so each mode has unit L2 norm on the grid
        col_norms = np.linalg.norm(By_np, axis=0, keepdims=True)
        col_norms = np.where(col_norms < 1e-12, 1.0, col_norms)
        By_np = By_np / col_norms

        Bt_np = np.zeros((nt_q, n_modes_t), dtype=np.float64)
        for k in range(n_modes_t):
            Bt_np[:, k] = np.cos(k * np.pi * t_q / t_end) / (1.0 if k == 0 else np.sqrt(0.5))
        col_norms_t = np.linalg.norm(Bt_np, axis=0, keepdims=True)
        col_norms_t = np.where(col_norms_t < 1e-12, 1.0, col_norms_t)
        Bt_np = Bt_np / col_norms_t

        self.By = torch.tensor(By_np, dtype=dtype, device=device)   # (ny_q, n_modes_y)
        self.Bt = torch.tensor(Bt_np, dtype=dtype, device=device)   # (nt_q, n_modes_t)
        import torch.nn as nn
        self.coeffs = nn.Parameter(
            torch.zeros(n_modes_y, n_modes_t, dtype=dtype, device=device)
        )

    def q_grid(self) -> Any:
        """Return q as (ny_q, nt_q) tensor via differentiable Fourier synthesis."""
        return self.By @ self.coeffs @ self.Bt.t()

    def warm_start_from_array(self, q_init: np.ndarray) -> None:
        """Fit Fourier coefficients to a (ny_q, nt_q) numpy array via least squares.

        coeffs = By^+ @ q_init @ (Bt^+)^T
        """
        import torch
        By_np = self.By.detach().cpu().numpy()   # (ny_q, n_modes_y)
        Bt_np = self.Bt.detach().cpu().numpy()   # (nt_q, n_modes_t)
        # Least squares: coeffs = By^+ @ q_init @ Bt^{+T}
        # By^+ = pinv(By)  (since By columns are nearly orthonormal, pinv ≈ By.T)
        By_pinv = np.linalg.pinv(By_np)          # (n_modes_y, ny_q)
        Bt_pinv = np.linalg.pinv(Bt_np)          # (n_modes_t, nt_q)
        coeffs_np = By_pinv @ q_init @ Bt_pinv.T  # (n_modes_y, n_modes_t)
        with torch.no_grad():
            self.coeffs.copy_(torch.tensor(coeffs_np, dtype=self.coeffs.dtype,
                                           device=self.coeffs.device))


# ---------------------------------------------------------------------------
# Bilinear interpolation of a q_grid tensor at normalised (y,t) points
# ---------------------------------------------------------------------------
def _bilinear_interp_from_grid(
    q_grid: Any,   # (ny_q, nt_q) tensor — differentiable
    y_pts: Any,    # (N,) normalised y ∈ [0,1]
    t_pts: Any,    # (N,) normalised t ∈ [0,1]
    ny_q: int,
    nt_q: int,
) -> Any:
    import torch
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


# ---------------------------------------------------------------------------
# FNN builder
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


# ---------------------------------------------------------------------------
# Loss computation  (supports FourierBasisQ or flat q_params)
# ---------------------------------------------------------------------------
def _compute_loss_v2(
    net: Any,
    q_source: Any,        # FourierBasisQ or flat nn.Parameter (ny_q*nt_q,)
    *,
    pde_x: Any, pde_y: Any, pde_t: Any,
    ic_inp: Any,
    bc_lft_y: Any, bc_lft_t: Any,
    bc_rgt_y: Any, bc_rgt_t: Any,
    bc_top_x: Any, bc_top_t: Any,
    bc_bot_x: Any, bc_bot_t: Any,
    sd_x: Any, sd_y: Any, sd_t: Any, sd_T: Any,
    Lx: float, Ly: float, t_end: float, alpha: float, k: float,
    ny_q: int, nt_q: int,
    n_bc: int, n_ic: int,
    w_pde: float, w_ic: float, w_bc_flux: float, w_bc_ins: float, w_data: float,
    # Optional: per-component scale normalization (Strategy C)
    loss_scales: dict[str, float] | None = None,
) -> tuple[Any, dict[str, float]]:
    import torch

    # Compute current q grid (differentiable)
    if isinstance(q_source, FourierBasisQ):
        q_grid = q_source.q_grid()          # (ny_q, nt_q)
        def interp_q(y_n, t_n):
            return _bilinear_interp_from_grid(q_grid, y_n, t_n, ny_q, nt_q)
    else:
        # flat parameter
        def interp_q(y_n, t_n):
            q_g = q_source.view(ny_q, nt_q)
            return _bilinear_interp_from_grid(q_g, y_n, t_n, ny_q, nt_q)

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
    raw_pde = torch.mean(pde_res ** 2)

    # --- IC ---
    T_ic = net(ic_inp)
    raw_ic = torch.mean(T_ic ** 2)

    # --- Left BC (flux): -k * dT/dx(0,y,t)/Lx = q(y,t) ---
    bc_lft_x = torch.zeros(n_bc, dtype=px.dtype, device=px.device).requires_grad_(True)
    inp_lft = torch.stack([bc_lft_x, bc_lft_y, bc_lft_t], dim=1)
    T_lft = net(inp_lft)
    dT_dx_lft = torch.autograd.grad(T_lft.sum(), bc_lft_x, create_graph=True)[0]
    q_at_bc = interp_q(bc_lft_y.detach(), bc_lft_t.detach())
    raw_bc_flux = torch.mean((-k * dT_dx_lft / Lx - q_at_bc) ** 2)

    # --- Right BC (insulated) ---
    bc_rgt_x = torch.ones(n_bc, dtype=px.dtype, device=px.device).requires_grad_(True)
    T_rgt = net(torch.stack([bc_rgt_x, bc_rgt_y, bc_rgt_t], dim=1))
    dT_dx_rgt = torch.autograd.grad(T_rgt.sum(), bc_rgt_x, create_graph=True)[0]
    raw_bc_rgt = torch.mean(dT_dx_rgt ** 2)

    # --- Top BC (insulated) ---
    bc_top_y = torch.ones(n_bc, dtype=px.dtype, device=px.device).requires_grad_(True)
    T_top = net(torch.stack([bc_top_x, bc_top_y, bc_top_t], dim=1))
    dT_dy_top = torch.autograd.grad(T_top.sum(), bc_top_y, create_graph=True)[0]
    raw_bc_top = torch.mean(dT_dy_top ** 2)

    # --- Bottom BC (insulated) ---
    bc_bot_y = torch.zeros(n_bc, dtype=px.dtype, device=px.device).requires_grad_(True)
    T_bot = net(torch.stack([bc_bot_x, bc_bot_y, bc_bot_t], dim=1))
    dT_dy_bot = torch.autograd.grad(T_bot.sum(), bc_bot_y, create_graph=True)[0]
    raw_bc_bot = torch.mean(dT_dy_bot ** 2)

    # --- Sensor data ---
    inp_data = torch.stack([sd_x, sd_y, sd_t], dim=1)
    T_pred_data = net(inp_data).squeeze(1)
    raw_data = torch.mean((T_pred_data - sd_T) ** 2)

    # Strategy C: normalized loss balancing
    eps = 1e-12
    if loss_scales is not None:
        s_pde  = loss_scales.get("pde",  1.0)
        s_ic   = loss_scales.get("ic",   1.0)
        s_bfl  = loss_scales.get("bc_flux", 1.0)
        s_bins = loss_scales.get("bc_ins",  1.0)
        s_data = loss_scales.get("data", 1.0)
        eff_w_pde     = w_pde     / (s_pde  + eps)
        eff_w_ic      = w_ic      / (s_ic   + eps)
        eff_w_bc_flux = w_bc_flux / (s_bfl  + eps)
        eff_w_bc_ins  = w_bc_ins  / (s_bins + eps)
        eff_w_data    = w_data    / (s_data + eps)
    else:
        eff_w_pde, eff_w_ic = w_pde, w_ic
        eff_w_bc_flux, eff_w_bc_ins, eff_w_data = w_bc_flux, w_bc_ins, w_data

    loss_pde     = eff_w_pde     * raw_pde
    loss_ic      = eff_w_ic      * raw_ic
    loss_bc_flux = eff_w_bc_flux * raw_bc_flux
    loss_bc_ins  = eff_w_bc_ins  * (raw_bc_rgt + raw_bc_top + raw_bc_bot)
    loss_data    = eff_w_data    * raw_data

    loss = loss_pde + loss_ic + loss_bc_flux + loss_bc_ins + loss_data

    components = {
        "pde":     float(loss_pde.detach().cpu()),
        "ic":      float(loss_ic.detach().cpu()),
        "bc_flux": float(loss_bc_flux.detach().cpu()),
        "bc_ins":  float(loss_bc_ins.detach().cpu()),
        "data":    float(loss_data.detach().cpu()),
        "total":   float(loss.detach().cpu()),
    }
    return loss, components


# ---------------------------------------------------------------------------
# Tikhonov warm start
# ---------------------------------------------------------------------------
def run_tikhonov_warmstart(
    simulator: Any,
    sensor_positions: list[tuple[float, float]],
    T_obs_noisy: np.ndarray,
    obs_every: int,
    t_end: float,
    ny_q: int,
    nt_q: int,
    T0: float,
    q_true: np.ndarray,
    lam: float = 1e-3,
    logger: TrainingLogger | None = None,
) -> np.ndarray:
    """Run Tikhonov solver and return flux_pred as (ny_q, nt_q) array."""
    from src.tikhonov_solver_2d import solve_2d_tikhonov
    spec = {
        "simulator": simulator,
        "sensor_positions": sensor_positions,
        "T_obs_noisy": T_obs_noisy,
        "obs_every": obs_every,
        "t_end": t_end,
        "ny_q": ny_q,
        "nt_q": nt_q,
        "T0": T0,
        "lam": lam,
        "q_true": q_true,
    }
    t0 = time.perf_counter()
    result = solve_2d_tikhonov(spec)
    dt = time.perf_counter() - t0
    flux_pred = result["flux_pred"]
    rmse = result.get("flux_rmse", float("nan"))
    msg = f"Tikhonov warm start: flux_rmse={rmse:.2f} W/m²  t={dt:.2f}s"
    if logger:
        logger.log(msg)
    else:
        print(msg)
    return flux_pred


# ---------------------------------------------------------------------------
# Full-field FD snapshots
# ---------------------------------------------------------------------------
def simulate_full_field(
    simulator: Any,
    q_flux_2d: np.ndarray,
    T0: float,
    snapshot_times: list[float],
    t_end: float,
) -> list[np.ndarray]:
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
    snap_step_indices = [int(np.argmin(np.abs(sim_times - ts))) for ts in snapshot_times]
    snap_fields: list[np.ndarray | None] = [None] * len(snapshot_times)
    u = np.full((nx, ny), T0, dtype=float)
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
    for si_idx, sf in enumerate(snap_fields):
        if sf is None:
            snap_fields[si_idx] = u.copy()
    return snap_fields  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Main case runner (v2 with all recovery strategies)
# ---------------------------------------------------------------------------
def run_case_v2(
    case_name: str,
    case_label: str,
    family_name: str,
    primary_axis_level: int,
    sigma_noise: float,
    sensor_layout: str,           # "medium" or "boundary_biased"
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
    n_modes_y: int,
    n_modes_t: int,
    use_fourier_basis: bool,
    use_warm_start: bool,
    use_normalized_loss: bool,
    logger: TrainingLogger,
) -> dict[str, Any]:
    """Train PINN v2 for one case with all recovery strategies."""
    import torch
    import torch.nn as nn

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dtype = torch.float64

    logger.log(f"\n{'='*70}")
    logger.log(f"CASE {case_label}: {case_name}")
    logger.log(f"  family={family_name}  level={primary_axis_level}  "
               f"sigma={sigma_noise}K  layout={sensor_layout}  seed={seed}")
    logger.log(f"  Recovery: fourier={use_fourier_basis}  warm_start={use_warm_start}  "
               f"normalized={use_normalized_loss}")
    logger.log(f"  Weights: w_pde={w_pde}  w_ic={w_ic}  w_bc_flux={w_bc_flux}  "
               f"w_data={w_data}")
    logger.log(f"  Training: Adam {n_adam}×  lr={lr_adam}  L-BFGS {n_lbfgs}×")
    logger.log(f"  Device: {device}  dtype: {dtype}")
    logger.log(f"{'='*70}")

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

    # Sensor layout
    if sensor_layout == "boundary_biased":
        sensor_positions = make_boundary_biased_layout(ny_s=3, Lx=Lx, Ly=Ly, x_frac=0.01)
        logger.log(f"Boundary-biased layout: {len(sensor_positions)} sensors, "
                   f"x in [{min(p[0] for p in sensor_positions)*100:.2f}, "
                   f"{max(p[0] for p in sensor_positions)*100:.2f}] cm")
    else:
        sensor_positions = generate_sensor_grid(sensor_layout, Lx, Ly)
        logger.log(f"Standard '{sensor_layout}' layout: {len(sensor_positions)} sensors")

    n_sensors = len(sensor_positions)

    # ------------------------------------------------------------------
    # Ground-truth flux
    # ------------------------------------------------------------------
    y_q_grid = np.linspace(0.0, Ly, ny_q)
    t_q_grid = np.linspace(0.0, t_end, nt_q)
    q_true = generate_family_flux(
        family_name, y_q_grid, t_q_grid,
        primary_axis_level=primary_axis_level, seed=seed,
    )
    y_fine = simulator.y_centers
    q_fine_for_fd = generate_family_flux(
        family_name, y_fine, t_q_grid,
        primary_axis_level=primary_axis_level, seed=seed,
    )
    logger.log(f"q_true: shape={q_true.shape}  "
               f"range=[{q_true.min():.1f}, {q_true.max():.1f}] W/m²")

    # ------------------------------------------------------------------
    # Forward simulation → noisy sensor readings
    # ------------------------------------------------------------------
    rng_noise = np.random.default_rng(seed)
    T_sensors_clean, obs_times = simulator.simulate(
        q_fine_for_fd, T0, sensor_positions, t_end=t_end, obs_every=obs_every
    )
    T_obs_noisy = T_sensors_clean + rng_noise.normal(0.0, sigma_noise, T_sensors_clean.shape)
    logger.log(f"Sensors: {n_sensors}  obs_steps: {T_obs_noisy.shape[1]}  "
               f"noise σ={sigma_noise} K")

    # ------------------------------------------------------------------
    # FD snapshots for ground truth
    # ------------------------------------------------------------------
    snapshot_times = [t_end * 0.25, t_end * 0.5, t_end * 0.75]
    T_fd_snapshots = simulate_full_field(simulator, q_fine_for_fd, T0, snapshot_times, t_end)

    # ------------------------------------------------------------------
    # Tikhonov warm start  (Strategy D)
    # ------------------------------------------------------------------
    q_warmstart: np.ndarray | None = None
    tikhonov_rmse: float = float("nan")
    if use_warm_start:
        logger.log("Running Tikhonov warm start...")
        try:
            # For warm start we use the medium layout sensor data always
            # (if boundary biased, use same data for warm start)
            q_warmstart_raw = run_tikhonov_warmstart(
                simulator=simulator,
                sensor_positions=sensor_positions,
                T_obs_noisy=T_obs_noisy,
                obs_every=obs_every,
                t_end=t_end,
                ny_q=ny_q,
                nt_q=nt_q,
                T0=T0,
                q_true=q_true,
                lam=1e-3,
                logger=logger,
            )
            q_warmstart = q_warmstart_raw
            tikhonov_rmse = float(np.sqrt(np.mean((q_warmstart - q_true)**2)))
            logger.log(f"Tikhonov warm start flux range: "
                       f"[{q_warmstart.min():.1f}, {q_warmstart.max():.1f}] W/m²  "
                       f"RMSE vs truth: {tikhonov_rmse:.2f}")
        except Exception as exc:
            logger.log(f"Tikhonov warm start FAILED: {exc} — proceeding without warm start")
            q_warmstart = None

    # ------------------------------------------------------------------
    # PINN setup
    # ------------------------------------------------------------------
    rng = np.random.default_rng(seed + 100)

    def to_tensor(arr: np.ndarray) -> Any:
        return torch.as_tensor(arr, dtype=dtype, device=device)

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

    # Collocation points
    pde_x_t = to_tensor(rng.uniform(0, 1, n_pde_pts)).unsqueeze(1)
    pde_y_t = to_tensor(rng.uniform(0, 1, n_pde_pts)).unsqueeze(1)
    pde_t_t = to_tensor(rng.uniform(0, 1, n_pde_pts)).unsqueeze(1)

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

    # ------------------------------------------------------------------
    # Build network and q representation
    # ------------------------------------------------------------------
    net = _build_fnn(3, hidden_layers, 1, device, dtype)
    n_net = sum(p.numel() for p in net.parameters())

    if use_fourier_basis:
        q_rep = FourierBasisQ(n_modes_y, n_modes_t, ny_q, nt_q,
                               Ly, t_end, device, dtype)
        q_trainable = [q_rep.coeffs]
        n_q_params = n_modes_y * n_modes_t
        q_param_type = f"Fourier {n_modes_y}×{n_modes_t}={n_q_params} modes"
    else:
        q_rep = nn.Parameter(torch.zeros(ny_q * nt_q, dtype=dtype, device=device))
        q_trainable = [q_rep]
        n_q_params = ny_q * nt_q
        q_param_type = f"dense grid {ny_q}×{nt_q}={n_q_params}"

    logger.log(f"Net: {hidden_layers} → {n_net} params  |  q: {q_param_type}")

    # Warm start initialization
    if use_warm_start and q_warmstart is not None:
        if use_fourier_basis:
            q_rep.warm_start_from_array(q_warmstart)
            # Verify fit quality
            with torch.no_grad():
                q_init_check = q_rep.q_grid().cpu().numpy()
            fit_rmse = float(np.sqrt(np.mean((q_init_check - q_warmstart)**2)))
            logger.log(f"Fourier warm start fit RMSE vs Tikhonov: {fit_rmse:.2f} W/m²")
        else:
            with torch.no_grad():
                q_rep.data[:] = torch.tensor(q_warmstart.flatten(),
                                              dtype=dtype, device=device)
        logger.log(f"Warm start applied from Tikhonov")
    else:
        logger.log("No warm start — q initialized to zero")

    # ------------------------------------------------------------------
    # Initial loss scales for normalization  (Strategy C)
    # ------------------------------------------------------------------
    loss_scales: dict[str, float] | None = None
    if use_normalized_loss:
        logger.log("Computing initial loss scales for normalization...")
        try:
            # Use w=1 so each component value = raw unweighted loss
            _, init_comps = _compute_loss_v2(
                net, q_rep,
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
                w_pde=1.0, w_ic=1.0, w_bc_flux=1.0, w_bc_ins=1.0, w_data=1.0,
                loss_scales=None,
            )
            # With w=1, each component value = raw unweighted MSE at init
            loss_scales = {
                "pde":     max(float(init_comps["pde"]),     1e-8),
                "ic":      max(float(init_comps["ic"]),      1e-8),
                "bc_flux": max(float(init_comps["bc_flux"]), 1e-8),
                "bc_ins":  max(float(init_comps["bc_ins"]),  1e-8),
                "data":    max(float(init_comps["data"]),    1e-8),
            }
            logger.log(f"Initial scales: pde={loss_scales['pde']:.3e}  "
                       f"bc_flux={loss_scales['bc_flux']:.3e}  "
                       f"data={loss_scales['data']:.3e}  "
                       f"ic={loss_scales['ic']:.3e}")
        except Exception as exc:
            logger.log(f"Warning: loss normalization failed ({exc}), using raw weights")
            loss_scales = None

    # ------------------------------------------------------------------
    # Optimizer setup
    # ------------------------------------------------------------------
    all_params = list(net.parameters()) + q_trainable
    optimizer_adam = torch.optim.Adam(all_params, lr=lr_adam)

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
        w_pde=w_pde, w_ic=w_ic, w_bc_flux=w_bc_flux,
        w_bc_ins=w_bc_ins, w_data=w_data,
        loss_scales=loss_scales,
    )

    adam_loss_history: list[tuple[int, float, dict]] = []
    lbfgs_loss_history: list[tuple[int, float]] = []

    # ------------------------------------------------------------------
    # Stage 1: Adam with cosine LR decay
    # ------------------------------------------------------------------
    logger.log(f"\n--- Stage 1: Adam ({n_adam} iters, lr={lr_adam}) ---")

    # Cosine LR schedule
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer_adam, T_max=n_adam, eta_min=lr_adam * 0.01
    )

    log_every = max(1, n_adam // 40)
    comps: dict[str, float] = {}
    for it in range(n_adam):
        optimizer_adam.zero_grad()
        loss, comps = _compute_loss_v2(net, q_rep, **loss_kwargs)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(all_params, max_norm=1.0)
        optimizer_adam.step()
        scheduler.step()

        if it % log_every == 0 or it == n_adam - 1:
            adam_loss_history.append((it, comps["total"], comps))
            # Check q evolution
            if use_fourier_basis:
                q_now = q_rep.q_grid().detach().cpu().numpy()
            else:
                q_now = q_rep.view(ny_q, nt_q).detach().cpu().numpy()
            q_range = f"[{q_now.min():.1f}, {q_now.max():.1f}]"
            logger.log(
                f"  Adam {it:6d}/{n_adam}  total={comps['total']:.4e}  "
                f"pde={comps['pde']:.3e}  data={comps['data']:.3e}  "
                f"bc_flux={comps['bc_flux']:.3e}  q_range={q_range} W/m²"
            )

    adam_final = comps["total"] if comps else float("nan")
    logger.log(f"Adam finished. Final loss: {adam_final:.4e}")

    # Extract q after Adam
    if use_fourier_basis:
        q_after_adam = q_rep.q_grid().detach().cpu().numpy().copy()
    else:
        q_after_adam = q_rep.view(ny_q, nt_q).detach().cpu().numpy().copy()
    logger.log(f"q after Adam: range=[{q_after_adam.min():.1f}, {q_after_adam.max():.1f}] W/m²")

    # ------------------------------------------------------------------
    # Stage 2: L-BFGS
    # ------------------------------------------------------------------
    logger.log(f"\n--- Stage 2: L-BFGS ({n_lbfgs} max closures, strong-Wolfe) ---")
    optimizer_lbfgs = torch.optim.LBFGS(
        all_params,
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
        loss_val, comps_val = _compute_loss_v2(net, q_rep, **loss_kwargs)
        loss_val.backward()
        torch.nn.utils.clip_grad_norm_(all_params, max_norm=10.0)
        step_i = lbfgs_iter[0]
        lbfgs_loss_history.append((step_i, float(comps_val["total"])))
        lbfgs_final_loss[0] = float(comps_val["total"])
        if step_i % 50 == 0:
            logger.log(f"  L-BFGS #{step_i:4d}  total={comps_val['total']:.4e}  "
                       f"bc_flux={comps_val['bc_flux']:.3e}  data={comps_val['data']:.3e}")
        lbfgs_iter[0] += 1
        return loss_val

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
        if use_fourier_basis:
            flux_pred = q_rep.q_grid().cpu().numpy().copy()
        else:
            flux_pred = q_rep.view(ny_q, nt_q).cpu().numpy().copy()

    logger.log(f"flux_pred: range=[{flux_pred.min():.1f}, {flux_pred.max():.1f}] W/m²")

    # Check for collapse
    q_collapsed = bool(np.abs(flux_pred).max() < 10.0)  # <10 W/m² max → collapsed
    logger.log(f"q collapsed to ~0? {q_collapsed}  (|q|_max = {np.abs(flux_pred).max():.2f})")

    # ------------------------------------------------------------------
    # T_NN snapshots
    # ------------------------------------------------------------------
    nx_vis, ny_vis = simulator.nx, simulator.ny
    x_vis = np.linspace(0.0, 1.0, nx_vis)
    y_vis = np.linspace(0.0, 1.0, ny_vis)
    XX, YY = np.meshgrid(x_vis, y_vis, indexing="ij")

    T_nn_snapshots: list[np.ndarray] = []
    with torch.no_grad():
        for t_snap in snapshot_times:
            t_norm = t_snap / t_end
            TT_snap = np.full_like(XX, t_norm)
            pts = to_tensor(np.column_stack([XX.ravel(), YY.ravel(), TT_snap.ravel()]))
            T_pred_snap = net(pts).cpu().numpy().reshape(nx_vis, ny_vis)
            T_nn_snapshots.append(T_pred_snap + T0)

    # ------------------------------------------------------------------
    # Sensor replay
    # ------------------------------------------------------------------
    replay_pred = np.zeros_like(T_obs_noisy)
    with torch.no_grad():
        for si, (xp, yp) in enumerate(sensor_positions):
            t_norms = (obs_times / t_end).astype(np.float64)
            x_norms = np.full_like(t_norms, xp / Lx)
            y_norms = np.full_like(t_norms, yp / Ly)
            pts = to_tensor(np.column_stack([x_norms, y_norms, t_norms]))
            replay_pred[si, :] = net(pts).cpu().numpy().squeeze() + T0

    replay_rmse = float(np.sqrt(np.mean((replay_pred - T_obs_noisy)**2)))
    logger.log(f"Sensor replay RMSE: {replay_rmse:.4f} K")

    # ------------------------------------------------------------------
    # Metrics
    # ------------------------------------------------------------------
    from src.metrics import compute_all_metrics
    metrics = compute_all_metrics(
        flux_pred, q_true,
        family_name=family_name,
        diag_dict={},
    )
    flux_rmse = float(np.sqrt(np.mean((flux_pred - q_true)**2)))
    ssim_flux = metrics.get("ssim_flux", float("nan"))
    support_overlap = metrics.get("support_overlap", float("nan"))
    peak_err = metrics.get("peak_localization_error", float("nan"))

    logger.log(f"\n=== METRICS ===")
    logger.log(f"  flux_rmse       : {flux_rmse:.4f} W/m²")
    logger.log(f"  replay_rmse     : {replay_rmse:.4f} K")
    logger.log(f"  ssim_flux       : {ssim_flux:.6f}")
    logger.log(f"  support_overlap : {support_overlap:.6f}")
    logger.log(f"  peak_loc_err    : {peak_err}")
    logger.log(f"  q_max_pred      : {np.abs(flux_pred).max():.2f} W/m²")
    logger.log(f"  q_max_true      : {np.abs(q_true).max():.2f} W/m²")
    logger.log(f"  q_collapsed     : {q_collapsed}")
    logger.log(f"  runtime         : {t_training:.1f} s")

    return {
        "case_label":         case_label,
        "case_name":          case_name,
        "family_name":        family_name,
        "primary_axis_level": primary_axis_level,
        "sigma_noise":        sigma_noise,
        "sensor_layout":      sensor_layout,
        "seed":               seed,
        "use_fourier":        use_fourier_basis,
        "use_warm_start":     use_warm_start,
        "use_normalized":     use_normalized_loss,
        "w_bc_flux":          w_bc_flux,
        "flux_pred":          flux_pred,
        "q_true":             q_true,
        "flux_rmse":          flux_rmse,
        "replay_rmse":        replay_rmse,
        "ssim_flux":          ssim_flux,
        "support_overlap":    support_overlap,
        "peak_loc_err":       peak_err,
        "q_max_pred":         float(np.abs(flux_pred).max()),
        "q_max_true":         float(np.abs(q_true).max()),
        "q_collapsed":        q_collapsed,
        "adam_final_loss":    adam_final,
        "lbfgs_final_loss":   lbfgs_final,
        "runtime_seconds":    t_training,
        "n_adam_iters":       n_adam,
        "n_lbfgs_closures":   lbfgs_iter[0],
        "adam_loss_history":  adam_loss_history,
        "lbfgs_loss_history": lbfgs_loss_history,
        "T_fd_snapshots":     T_fd_snapshots,
        "T_nn_snapshots":     T_nn_snapshots,
        "T_obs_noisy":        T_obs_noisy,
        "replay_pred":        replay_pred,
        "obs_times":          obs_times,
        "sensor_positions":   sensor_positions,
        "snapshot_times":     snapshot_times,
        "tikhonov_rmse":      tikhonov_rmse,
        "q_after_adam":       q_after_adam,
        "hidden_layers":      hidden_layers,
        "n_q_params":         n_modes_y * n_modes_t if use_fourier_basis else ny_q * nt_q,
    }


# ---------------------------------------------------------------------------
# Figure generators
# ---------------------------------------------------------------------------
def save_flux_comparison(result: dict, out_path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors

    q_true = result["q_true"]
    q_pred = result["flux_pred"]
    q_err  = q_pred - q_true

    v_max = float(np.abs(q_true).max()) * 1.1
    v_min = -v_max * 0.1

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    titles = ["q_true(y,t)  [W/m²]", "q_pred(y,t)  [W/m²]", "q_error(y,t)  [W/m²]"]
    data   = [q_true, q_pred, q_err]
    cmaps  = ["hot", "hot", "RdBu_r"]
    vlims  = [(v_min, v_max), (v_min, v_max),
              (-max(0.1, float(np.abs(q_err).max())), max(0.1, float(np.abs(q_err).max())))]

    for ax, title, arr, cmap, (vlo, vhi) in zip(axes, titles, data, cmaps, vlims):
        im = ax.imshow(arr, aspect="auto", origin="lower",
                       vmin=vlo, vmax=vhi, cmap=cmap)
        ax.set_title(f"{title}\n{result['case_name']}  {result['sensor_layout']}")
        ax.set_xlabel("time index")
        ax.set_ylabel("y index")
        plt.colorbar(im, ax=ax, shrink=0.85)

    rmse_str = f"flux_rmse={result['flux_rmse']:.1f}  SSIM={result['ssim_flux']:.4f}  " \
               f"support_overlap={result['support_overlap']:.4f}"
    fig.suptitle(rmse_str, fontsize=10, y=1.01)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {out_path.name}")


def save_temperature_snapshots(result: dict, out_path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    T_fd_snaps  = result["T_fd_snapshots"]
    T_nn_snaps  = result["T_nn_snapshots"]
    snap_times  = result["snapshot_times"]
    n_snaps = len(snap_times)

    T_all = np.concatenate([np.concatenate(T_fd_snaps), np.concatenate(T_nn_snaps)])
    T_vmin, T_vmax = float(T_all.min()), float(T_all.max())

    fig, axes = plt.subplots(3, n_snaps, figsize=(5 * n_snaps, 12))

    for col, (t_s, T_fd, T_nn) in enumerate(zip(snap_times, T_fd_snaps, T_nn_snaps)):
        T_err = T_nn - T_fd
        err_lim = float(max(0.5, np.abs(T_err).max()))

        ax_fd  = axes[0, col]
        ax_nn  = axes[1, col]
        ax_err = axes[2, col]

        im0 = ax_fd.imshow(T_fd.T, origin="lower", aspect="auto",
                           vmin=T_vmin, vmax=T_vmax, cmap="plasma")
        im1 = ax_nn.imshow(T_nn.T, origin="lower", aspect="auto",
                           vmin=T_vmin, vmax=T_vmax, cmap="plasma")
        im2 = ax_err.imshow(T_err.T, origin="lower", aspect="auto",
                            vmin=-err_lim, vmax=err_lim, cmap="RdBu_r")

        ax_fd.set_title(f"T_FD  t={t_s:.0f}s")
        ax_nn.set_title(f"T_NN  t={t_s:.0f}s")
        ax_err.set_title(f"T_error  t={t_s:.0f}s")
        for ax in [ax_fd, ax_nn, ax_err]:
            ax.set_xlabel("x index")
            ax.set_ylabel("y index")
        plt.colorbar(im0, ax=ax_fd, shrink=0.8)
        plt.colorbar(im1, ax=ax_nn, shrink=0.8)
        plt.colorbar(im2, ax=ax_err, shrink=0.8)

    fig.suptitle(f"{result['case_name']}  {result['sensor_layout']}  "
                 f"replay_rmse={result['replay_rmse']:.4f} K", fontsize=11)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {out_path.name}")


def save_sensor_replay(result: dict, out_path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    obs   = result["T_obs_noisy"]
    pred  = result["replay_pred"]
    times = result["obs_times"]
    positions = result["sensor_positions"]
    n_s = obs.shape[0]

    ncols = min(3, n_s)
    nrows = int(np.ceil(n_s / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 3 * nrows), squeeze=False)

    for si in range(n_s):
        row, col = divmod(si, ncols)
        ax = axes[row][col]
        ax.plot(times, obs[si, :], "k.", ms=2, alpha=0.6, label="obs (noisy)")
        ax.plot(times, pred[si, :], "r-", lw=1.5, label="T_NN")
        ax.set_title(f"S{si}  ({positions[si][0]*100:.1f},{positions[si][1]*100:.1f}) cm")
        ax.set_xlabel("t [s]")
        ax.set_ylabel("T [K]")
        if si == 0:
            ax.legend(fontsize=8)

    for idx in range(n_s, nrows * ncols):
        r, c = divmod(idx, ncols)
        axes[r][c].set_visible(False)

    fig.suptitle(f"{result['case_name']}  {result['sensor_layout']}  "
                 f"replay_rmse={result['replay_rmse']:.4f} K", fontsize=10)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {out_path.name}")


def save_loss_curve(result: dict, out_path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    adam_hist  = result["adam_loss_history"]   # (iter, total, comps)
    lbfgs_hist = result["lbfgs_loss_history"]  # (step, total)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Adam — component breakdown
    ax = axes[0]
    iters = [h[0] for h in adam_hist]
    for key, color in [("pde","blue"), ("data","green"), ("bc_flux","red"),
                        ("ic","purple"), ("total","black")]:
        vals = [h[2].get(key, float("nan")) for h in adam_hist]
        ax.semilogy(iters, vals, label=key, color=color,
                    lw=2 if key == "total" else 1)
    ax.set_xlabel("Adam iteration")
    ax.set_ylabel("loss (log scale)")
    ax.set_title("Stage 1: Adam loss components")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # L-BFGS — total loss
    ax2 = axes[1]
    if lbfgs_hist:
        steps = [h[0] for h in lbfgs_hist]
        totals = [h[1] for h in lbfgs_hist]
        ax2.semilogy(steps, totals, "b-", lw=1.5)
        ax2.set_xlabel("L-BFGS closure #")
        ax2.set_ylabel("total loss (log scale)")
        ax2.set_title(f"Stage 2: L-BFGS  (final={result['lbfgs_final_loss']:.4e})")
        ax2.grid(True, alpha=0.3)
    else:
        ax2.text(0.5, 0.5, "L-BFGS not run", ha="center", va="center",
                 transform=ax2.transAxes)

    fig.suptitle(f"{result['case_name']}  {result['sensor_layout']}  "
                 f"w_bc_flux={result['w_bc_flux']}", fontsize=10)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {out_path.name}")


def save_admission_summary(all_results: list[dict], out_path: Path) -> None:
    """Compact admission summary: v1 vs v2 flux comparison per case."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Previous pilot metrics (hard-coded from run_pinn_full_training_pilot)
    prev = {
        "gaussian_localized": {
            "flux_rmse": 272.39, "ssim_flux": 0.000658, "support_overlap": 0.0,
            "replay_rmse": 0.0822, "label": "v1 (failed)",
        },
        "overlapping_multi_spot": {
            "flux_rmse": 339.83, "ssim_flux": 0.001097, "support_overlap": 0.0,
            "replay_rmse": 0.0813, "label": "v1 (failed)",
        },
    }

    n_cases = len(all_results)
    fig, axes = plt.subplots(n_cases, 4, figsize=(20, 4 * n_cases))
    if n_cases == 1:
        axes = axes[np.newaxis, :]

    metrics_labels = ["flux_rmse (W/m²)", "ssim_flux", "support_overlap", "replay_rmse (K)"]
    metrics_keys   = ["flux_rmse", "ssim_flux", "support_overlap", "replay_rmse"]

    for row_i, r in enumerate(all_results):
        fam = r["family_name"]
        pv = prev.get(fam, {})

        for col_i, (mlbl, mkey) in enumerate(zip(metrics_labels, metrics_keys)):
            ax = axes[row_i, col_i]
            v2_val = r.get(mkey, float("nan"))
            v1_val = pv.get(mkey, float("nan"))
            bars  = [v1_val, v2_val]
            color = ["#d62728", "#2ca02c"]
            labels = ["v1 (failed)", f"v2 {r['sensor_layout']}"]
            x = np.arange(len(bars))
            ax.bar(x, bars, color=color, alpha=0.8)
            ax.set_xticks(x)
            ax.set_xticklabels(labels, fontsize=8)
            ax.set_ylabel(mlbl, fontsize=8)
            ax.set_title(f"{r['case_name'][:30]}\n{mlbl}", fontsize=8)
            ax.grid(axis="y", alpha=0.3)
            if mkey in ("ssim_flux", "support_overlap"):
                ax.set_ylim(0, max(0.1, max(bars) * 1.3))

    fig.suptitle("PINN Admission Test: v1 (failed) vs v2 (recovery pilot)", fontsize=12)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {out_path.name}")


# ---------------------------------------------------------------------------
# CSV + YAML config
# ---------------------------------------------------------------------------
def save_csv(results: list[dict], path: Path) -> None:
    fieldnames = [
        "case_label", "case_name", "family_name", "primary_axis_level",
        "sigma_noise", "sensor_layout", "seed",
        "use_fourier", "use_warm_start", "use_normalized",
        "w_bc_flux", "flux_rmse", "replay_rmse",
        "ssim_flux", "support_overlap", "peak_loc_err",
        "q_max_pred", "q_max_true", "q_collapsed",
        "runtime_seconds", "adam_final_loss", "lbfgs_final_loss",
        "n_adam_iters", "n_lbfgs_closures", "tikhonov_rmse", "n_q_params",
    ]
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in results:
            writer.writerow({k: r.get(k, "") for k in fieldnames})
    print(f"  Saved {path.name}")


def save_config_yaml(cfg: dict, path: Path) -> None:
    import yaml
    with path.open("w") as f:
        yaml.dump(cfg, f, default_flow_style=False)
    print(f"  Saved {path.name}")


# ---------------------------------------------------------------------------
# Admission decision
# ---------------------------------------------------------------------------
def compute_admission_decision(results: list[dict]) -> str:
    """Determine PINN admission status from v2 results."""
    # Admission thresholds (must satisfy on ≥1 case to reach CONDITIONAL)
    SSIM_THRESHOLD     = 0.05    # SSIM > 0.05 = structurally non-trivial
    SUPPORT_THRESHOLD  = 0.10    # Dice > 0.10 = some support recovered
    FLUX_RMSE_IMPROVE  = 0.80    # flux_rmse < 0.80 × previous (272/340) = improvement

    # Previous baselines
    prev_rmse = {"gaussian_localized": 272.39, "overlapping_multi_spot": 339.83}

    admitted_cases    = 0
    conditional_cases = 0
    failed_cases      = 0

    decision_lines: list[str] = []
    for r in results:
        fam  = r["family_name"]
        rmse = r["flux_rmse"]
        ssim = r["ssim_flux"]
        supp = r["support_overlap"]
        coll = r["q_collapsed"]
        prev = prev_rmse.get(fam, float("nan"))
        improved = (rmse < FLUX_RMSE_IMPROVE * prev) if np.isfinite(prev) else False
        nontrivial_q = not coll and (r["q_max_pred"] > 20.0)

        decision_lines.append(
            f"  {r['case_name']} ({r['sensor_layout']}): "
            f"flux_rmse={rmse:.1f} (prev {prev:.1f})  "
            f"SSIM={ssim:.4f}  supp={supp:.4f}  "
            f"q_max={r['q_max_pred']:.1f}  collapsed={coll}"
        )

        if ssim > SSIM_THRESHOLD and supp > SUPPORT_THRESHOLD and not coll and improved:
            admitted_cases += 1
            decision_lines[-1] += " → FULL"
        elif (nontrivial_q and (ssim > 0.01 or supp > 0.05)) and improved:
            conditional_cases += 1
            decision_lines[-1] += " → CONDITIONAL"
        else:
            failed_cases += 1
            decision_lines[-1] += " → NOT ADMITTED"

    total = len(results)
    lines = "\n".join(decision_lines)

    if admitted_cases >= total // 2 + 1 or (total == 1 and admitted_cases >= 1):
        verdict = "ADMITTED"
        reasoning = ("PINN recovers nontrivial q(y,t) with material structure. "
                     "Flux metrics are in a credible range and performance exceeds "
                     "temperature-replay-only trivial solution.")
    elif conditional_cases + admitted_cases >= 1:
        verdict = "CONDITIONALLY ADMITTED"
        reasoning = ("PINN shows real flux recovery on at least one case. "
                     "Still fragile or expensive. Can be included in benchmark tables "
                     "with honest caveats about recovery prerequisites (warm start, "
                     "high w_bc_flux, boundary sensors).")
    else:
        verdict = "NOT ADMITTED YET"
        reasoning = ("PINN still collapses to q≈0 or near-trivial pattern. "
                     "Structural metrics fail minimum thresholds. "
                     "Should remain exploratory branch, not benchmark-equal solver.")

    report = (
        f"\n{'='*70}\n"
        f"PINN ADMISSION DECISION\n"
        f"{'='*70}\n"
        f"Case results:\n{lines}\n\n"
        f"Admitted cases:     {admitted_cases}/{total}\n"
        f"Conditional cases:  {conditional_cases}/{total}\n"
        f"Failed cases:       {failed_cases}/{total}\n\n"
        f"VERDICT: {verdict}\n\n"
        f"Reasoning: {reasoning}\n"
        f"{'='*70}\n"
    )
    print(report)
    return verdict, report


# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------
def write_report(
    results: list[dict],
    verdict: str,
    admission_report: str,
    cfg: dict,
    env_info: dict,
    out_path: Path,
) -> None:
    lines: list[str] = []
    lines.append("# PINN Recovery Pilot v2 — Admission Test Report\n")
    lines.append(f"*Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}*\n")

    lines.append("## 1. Environment\n")
    lines.append(f"- Python: {env_info['python']}")
    lines.append(f"- PyTorch: {env_info['pytorch']}")
    lines.append(f"- CUDA: {env_info.get('cuda_version', 'N/A')}")
    lines.append(f"- GPU: {env_info.get('gpu_name', 'CPU')}")
    lines.append(f"- DeepXDE: {env_info['deepxde']}  backend={env_info['dde_backend']}")
    lines.append(f"- GPU actually used: {env_info.get('gpu_actually_used', False)}")
    lines.append("")

    lines.append("## 2. Training Schedule\n")
    lines.append(f"- Stage 1: Adam {cfg['n_adam']} iters, lr={cfg['lr_adam']} (cosine decay)")
    lines.append(f"- Stage 2: L-BFGS ≤{cfg['n_lbfgs']} closures, strong-Wolfe")
    lines.append(f"- Network: {cfg['hidden_layers']}  (tanh activations, Xavier init)")
    lines.append(f"- Collocation: {cfg['n_pde_pts']} PDE, {cfg['n_bc_pts']} BC, "
                 f"{cfg['n_ic_pts']} IC")
    lines.append("")

    lines.append("## 3. Recovery Strategies\n")
    lines.append("| Strategy | Status | Details |")
    lines.append("|----------|--------|---------|")
    lines.append("| A: Boundary-biased sensors | **Enabled** | "
                 "x ∈ {0.01, 0.05, 0.10}·Lx, 9 sensors |")
    lines.append(f"| B: Stronger flux BC weight | **Enabled** | w_bc_flux = {cfg['w_bc_flux']} |")
    lines.append("| C: Normalized loss balancing | **Enabled** | "
                 "divide each component by initial scale |")
    lines.append("| D: Tikhonov warm start | **Enabled** | λ=1e-3, fit via normal equations |")
    lines.append("| E: Fourier basis q | **Enabled** | "
                 f"{cfg['n_modes_y']}×{cfg['n_modes_t']} cosine modes = "
                 f"{cfg['n_modes_y']*cfg['n_modes_t']} coefficients |")
    lines.append("| F: Two-stage training | **Enabled** | "
                 f"Adam {cfg['n_adam']}k + L-BFGS |")
    lines.append("")

    lines.append("## 4. Sensor Layouts Used\n")
    lines.append("- `medium`: standard 3×3 grid, x ∈ [0.1·Lx, 0.9·Lx]")
    lines.append("- `boundary_biased`: 3×3 grid, x ∈ {0.01, 0.05, 0.10}·Lx")
    lines.append("")

    lines.append("## 5. Case-by-Case Metrics\n")
    lines.append("### Previous pilot (v1 — failed)")
    lines.append("| Case | flux_rmse | replay_rmse | ssim_flux | support_overlap |")
    lines.append("|------|-----------|-------------|-----------|-----------------|")
    lines.append("| gaussian_localized   | 272.39 | 0.0822 | 0.000658 | 0.0000 |")
    lines.append("| overlapping_multi_spot | 339.83 | 0.0813 | 0.001097 | 0.0000 |")
    lines.append("")
    lines.append("### Recovery pilot v2")
    lines.append("| Case | Layout | flux_rmse | replay_rmse | ssim_flux | "
                 "support_overlap | q_max | collapsed | runtime |")
    lines.append("|------|--------|-----------|-------------|-----------|"
                 "-----------------|-------|-----------|---------|")
    for r in results:
        lines.append(
            f"| {r['case_name'][:30]} | {r['sensor_layout']} | "
            f"{r['flux_rmse']:.2f} | {r['replay_rmse']:.4f} | "
            f"{r['ssim_flux']:.6f} | {r['support_overlap']:.6f} | "
            f"{r['q_max_pred']:.1f} | {r['q_collapsed']} | "
            f"{r['runtime_seconds']:.0f}s |"
        )
    lines.append("")

    lines.append("## 6. Comparison vs Benchmark-Ready Solvers\n")
    lines.append("*(On gaussian_localized medium, σ=0.1 K — from benchmark_2d_v2_results.csv)*")
    lines.append("| Solver | flux_rmse | notes |")
    lines.append("|--------|-----------|-------|")
    lines.append("| tikhonov_2d | ~224 | benchmark-ready |")
    lines.append("| tsvd_2d | ~134 | benchmark-ready |")
    lines.append("| deepxde_2d (sensitivity) | ~164 | benchmark-ready |")
    lines.append("| **deepxde_pinn (v1)** | **272** | **failed — q≈0** |")
    best_v2 = min(results, key=lambda r: r["flux_rmse"])
    lines.append(f"| **deepxde_pinn (v2)** | **{best_v2['flux_rmse']:.1f}** | "
                 f"**recovery pilot** |")
    lines.append("")

    lines.append("## 7. Admission Decision\n")
    lines.append(f"**Verdict: {verdict}**\n")
    lines.append("```")
    lines.append(admission_report.strip())
    lines.append("```")
    lines.append("")

    lines.append("## 8. Next Recommended Actions\n")
    if verdict == "ADMITTED":
        lines.append("- Include deepxde_pinn in full benchmark suite with recovery config")
        lines.append("- Run stress-track cases (noise=0.5K, harder families)")
        lines.append("- Document required hyperparameters in solver registry")
    elif "CONDITIONAL" in verdict:
        lines.append("- Run additional tuning: try w_bc_flux ∈ {300, 1000}")
        lines.append("- Test on harder families (moving_hotspot, discontinuous_piecewise)")
        lines.append("- Report PINN in benchmark with caveats about recovery prerequisites")
        lines.append("- Consider physics-constrained initialization for all cases")
    else:
        lines.append("- Investigate whether deeper network helps spatial gradient learning")
        lines.append("- Try explicit q-regularization term in loss")
        lines.append("- Try physics-based pretraining (fit T to FD solution first)")
        lines.append("- Do not include in benchmark yet — exploratory only")
    lines.append("")

    lines.append("## 9. Output Files\n")
    lines.append(f"- `reports/pinn_recovery_pilot_v2/raw_results.csv`")
    lines.append(f"- `reports/pinn_recovery_pilot_v2/config_used.yaml`")
    lines.append(f"- `reports/pinn_recovery_pilot_v2/training_log_case1.txt`")
    lines.append(f"- `reports/pinn_recovery_pilot_v2/training_log_case2.txt`")
    lines.append(f"- `figures/pinn_recovery_pilot_v2/` (all figures)")

    out_path.write_text("\n".join(lines))
    print(f"  Saved {out_path.name}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    t0 = time.perf_counter()

    # ------------------------------------------------------------------
    # Environment audit
    # ------------------------------------------------------------------
    env_info = audit_environment()

    # ------------------------------------------------------------------
    # Master configuration
    # ------------------------------------------------------------------
    CFG = {
        "n_adam":          20_000,
        "lr_adam":         1e-3,
        "n_lbfgs":         400,
        "hidden_layers":   [64, 64, 64, 64],
        "n_pde_pts":       900,
        "n_bc_pts":        120,
        "n_ic_pts":        200,
        "w_pde":           1.0,
        "w_ic":            20.0,
        "w_bc_flux":       500.0,
        "w_bc_ins":        2.0,
        "w_data":          100.0,
        "ny_q":            8,
        "nt_q":            10,
        "n_modes_y":       8,
        "n_modes_t":       8,
        "use_fourier_basis":    True,
        "use_warm_start":       True,
        "use_normalized_loss":  True,
        "sigma_noise":     0.1,
        "seed":            0,
        "env":             env_info,
    }

    print("\nRecovery Configuration:")
    for k, v in CFG.items():
        if k != "env":
            print(f"  {k}: {v}")
    print()

    # ------------------------------------------------------------------
    # Case definitions: each family with boundary_biased layout
    # ------------------------------------------------------------------
    CASE_DEFS = [
        {
            "case_name":          "case1_gaussian_boundary_biased",
            "case_label":         "1",
            "family_name":        "gaussian_localized",
            "primary_axis_level": 1,
            "sensor_layout":      "boundary_biased",
            "log_path":           LOG1_PATH,
        },
        {
            "case_name":          "case2_multi_spot_boundary_biased",
            "case_label":         "2",
            "family_name":        "overlapping_multi_spot",
            "primary_axis_level": 1,
            "sensor_layout":      "boundary_biased",
            "log_path":           LOG2_PATH,
        },
    ]

    all_results: list[dict] = []

    for case_def in CASE_DEFS:
        logger = TrainingLogger(case_def["log_path"])
        try:
            result = run_case_v2(
                case_name          = case_def["case_name"],
                case_label         = case_def["case_label"],
                family_name        = case_def["family_name"],
                primary_axis_level = case_def["primary_axis_level"],
                sigma_noise        = CFG["sigma_noise"],
                sensor_layout      = case_def["sensor_layout"],
                seed               = CFG["seed"],
                n_adam             = CFG["n_adam"],
                lr_adam            = CFG["lr_adam"],
                n_lbfgs            = CFG["n_lbfgs"],
                hidden_layers      = CFG["hidden_layers"],
                n_pde_pts          = CFG["n_pde_pts"],
                n_bc_pts           = CFG["n_bc_pts"],
                n_ic_pts           = CFG["n_ic_pts"],
                w_pde              = CFG["w_pde"],
                w_ic               = CFG["w_ic"],
                w_bc_flux          = CFG["w_bc_flux"],
                w_bc_ins           = CFG["w_bc_ins"],
                w_data             = CFG["w_data"],
                ny_q               = CFG["ny_q"],
                nt_q               = CFG["nt_q"],
                n_modes_y          = CFG["n_modes_y"],
                n_modes_t          = CFG["n_modes_t"],
                use_fourier_basis  = CFG["use_fourier_basis"],
                use_warm_start     = CFG["use_warm_start"],
                use_normalized_loss = CFG["use_normalized_loss"],
                logger             = logger,
            )
            all_results.append(result)
        except Exception as exc:
            logger.log(f"CASE FAILED: {exc}")
            import traceback
            logger.log(traceback.format_exc())
        finally:
            logger.close()

    if not all_results:
        print("ERROR: All cases failed. No results to report.")
        sys.exit(1)

    # ------------------------------------------------------------------
    # Figures
    # ------------------------------------------------------------------
    print(f"\n{'='*60}")
    print("GENERATING FIGURES")
    print(f"{'='*60}")

    for r in all_results:
        lbl = r["case_label"]
        layout = r["sensor_layout"]
        tag = f"case{lbl}_{layout}"
        save_flux_comparison(r, FIGURES_DIR / f"{tag}_flux_comparison.png")
        save_temperature_snapshots(r, FIGURES_DIR / f"{tag}_temperature_snapshots.png")
        save_sensor_replay(r, FIGURES_DIR / f"{tag}_sensor_replay.png")
        save_loss_curve(r, FIGURES_DIR / f"{tag}_loss_curve.png")

    # Best result per family for admission summary
    save_admission_summary(all_results, FIGURES_DIR / "pinn_admission_summary.png")

    # ------------------------------------------------------------------
    # CSV + config
    # ------------------------------------------------------------------
    print(f"\n{'='*60}")
    print("SAVING RESULTS")
    print(f"{'='*60}")
    save_csv(all_results, REPORTS_DIR / "raw_results.csv")

    try:
        save_config_yaml(
            {k: v for k, v in CFG.items() if k != "env"},
            REPORTS_DIR / "config_used.yaml"
        )
    except ImportError:
        # yaml not available, save as json
        with (REPORTS_DIR / "config_used.json").open("w") as f:
            json.dump({k: v for k, v in CFG.items() if k != "env"}, f, indent=2)
        print("  Saved config_used.json (yaml not available)")

    # ------------------------------------------------------------------
    # Admission decision
    # ------------------------------------------------------------------
    verdict, admission_report = compute_admission_decision(all_results)

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------
    write_report(
        all_results, verdict, admission_report, CFG, env_info,
        REPORTS_DIR / "pinn_recovery_pilot_v2_report.md"
    )

    total_time = time.perf_counter() - t0

    # ------------------------------------------------------------------
    # Final summary
    # ------------------------------------------------------------------
    print(f"\n{'='*70}")
    print("PINN RECOVERY PILOT v2 — FINAL SUMMARY")
    print(f"{'='*70}")
    print(f"1. Environment audit:")
    print(f"   Python={env_info['python']}  PyTorch={env_info['pytorch']}  "
          f"DeepXDE={env_info['deepxde']}")
    print(f"   GPU={env_info.get('gpu_name','CPU')}  CUDA={env_info.get('cuda_version','N/A')}")
    print(f"\n2. Recovery strategies enabled:")
    print(f"   A. Boundary-biased sensor layout (x ∈ {{0.01,0.05,0.10}}·Lx)")
    print(f"   B. Stronger flux-BC weighting: w_bc_flux = {CFG['w_bc_flux']}")
    print(f"   C. Normalized loss balancing (initial-scale normalization)")
    print(f"   D. Tikhonov warm start (λ=1e-3 normal equations)")
    print(f"   E. Fourier basis q ({CFG['n_modes_y']}×{CFG['n_modes_t']} cosine modes)")
    print(f"   F. Two-stage: Adam {CFG['n_adam']} + L-BFGS ≤{CFG['n_lbfgs']}")
    print(f"\n3. Cases run:")
    for r in all_results:
        print(f"   {r['case_label']}: {r['case_name']} ({r['sensor_layout']})")
    print(f"\n4. GPU actually used: {env_info.get('gpu_actually_used', False)}")
    print(f"\n5. Metrics before vs after recovery pilot:")
    print(f"   {'Case':<40} {'v1 RMSE':>10} {'v2 RMSE':>10} {'v1 SSIM':>10} {'v2 SSIM':>10}")
    prev_rmse = {"gaussian_localized": 272.39, "overlapping_multi_spot": 339.83}
    prev_ssim = {"gaussian_localized": 0.000658, "overlapping_multi_spot": 0.001097}
    for r in all_results:
        fam = r["family_name"]
        print(f"   {r['case_name'][:40]:<40} "
              f"{prev_rmse.get(fam, float('nan')):>10.2f} "
              f"{r['flux_rmse']:>10.2f} "
              f"{prev_ssim.get(fam, float('nan')):>10.6f} "
              f"{r['ssim_flux']:>10.6f}")
    print(f"\n6. PINN recovered nontrivial q(y,t)?")
    for r in all_results:
        nontrivial = not r["q_collapsed"] and r["q_max_pred"] > 20.0
        print(f"   {r['case_name']}: nontrivial={nontrivial}  "
              f"q_max={r['q_max_pred']:.1f} W/m²  collapsed={r['q_collapsed']}")
    print(f"\n7. Admission decision: {verdict}")
    print(f"\n8. Output locations:")
    print(f"   Reports: {REPORTS_DIR}")
    print(f"   Figures: {FIGURES_DIR}")
    print(f"\n9. Remaining blockers:")
    if verdict == "ADMITTED":
        print(f"   None — proceed to full benchmark inclusion")
    elif "CONDITIONAL" in verdict:
        print(f"   - PINN recovery requires specific prerequisites (boundary sensors,")
        print(f"     warm start, high w_bc_flux) — must be documented as solver conditions")
        print(f"   - Not yet tested on stress-track families or higher noise")
    else:
        print(f"   - q still collapses or shows insufficient structure")
        print(f"   - Need architectural changes beyond hyperparameter tuning")
    print(f"\n10. Next commands for follow-up:")
    print(f"    # Stress-track case (harder, higher noise):")
    print(f"    python tikhonov_agent/run_pinn_recovery_pilot_v2.py  # after adding case 3")
    print(f"    # Full benchmark with PINN:")
    print(f"    python tikhonov_agent/scripts/run_benchmark_2d_v2.py --solvers pinn_recovery")
    print(f"\nTotal wall time: {total_time:.1f} s")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
