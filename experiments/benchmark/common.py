"""
common.py
=========
Shared utilities for the three-track benchmark experiment infrastructure.

Provides:
  - Solver dispatcher (runs any of the 4 registered 2D solvers)
  - S-matrix cache (avoid redundant sensitivity matrix builds)
  - Uniform result schema (raw CSV row structure)
  - Auto-parameter selection helpers
  - Logging setup
"""

from __future__ import annotations

import logging
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

# ------------------------------------------------------------------
# Path setup
# ------------------------------------------------------------------
_HERE         = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parent.parent   # tikhonov_agent/
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.forward.heat2d_simulator import (  # noqa: E402
    HeatConduction2DFD,
    DEFAULT_LX, DEFAULT_LY, DEFAULT_ALPHA, DEFAULT_K,
    DEFAULT_T0, DEFAULT_T_TOTAL, DEFAULT_Q_MAX,
    DEFAULT_NX, DEFAULT_NY,
)
from src.tikhonov_solver_2d    import solve_2d_tikhonov   # noqa: E402
from src.tsvd_solver_2d        import solve_2d_tsvd        # noqa: E402
from src.fast_bayesian_solver_2d import solve_2d_bayesian  # noqa: E402
from src.heat_flux_families    import (                     # noqa: E402
    generate_family_flux, get_family, n_peaks_for_family,
)
from src.metrics import compute_all_metrics                 # noqa: E402


# ------------------------------------------------------------------
# Constants for the benchmark (small grid for speed)
# ------------------------------------------------------------------
NY_Q      = 8     # coarse flux grid rows (y dimension)
NT_Q      = 10    # coarse flux grid cols (t dimension)
OBS_EVERY = 8     # record every 8th FD step (≈ 14 obs per sensor for dt~0.5s)

# Tikhonov auto-lambda: L-curve candidate range
LAM_CANDIDATES = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1]

# TSVD auto-rank: energy fraction candidates
ENERGY_THRESHOLDS = [0.70, 0.85, 0.95]

# Bayesian default n_modes: auto (energy threshold 0.90)
BAYESIAN_ENERGY_THRESH = 0.90

# DeepXDE PINN budget
PINN_N_ITER    = 200
PINN_LR        = 5e-3
PINN_HIDDEN    = [32, 32, 32]
PINN_N_PDE     = 400
PINN_N_BC      = 60
PINN_N_IC      = 100

# ------------------------------------------------------------------
# Raw CSV column schema
# ------------------------------------------------------------------
RAW_COLUMNS = [
    # Experiment metadata
    "track_name",
    "family_name",
    "primary_axis_name",
    "primary_axis_level",
    "primary_axis_value",
    "secondary_axis_name",
    "secondary_axis_level",
    "secondary_axis_value",
    "solver_name",
    "sensor_config",
    "sensor_count",
    "noise_sigma",
    "seed",
    # Metrics
    "rmse_flux",
    "ssim_flux",
    "peak_localization_error",
    "band_error_scalar",
    "band_low_rel_error",
    "band_mid_rel_error",
    "band_high_rel_error",
    "support_overlap",
    # Diagnostics
    "runtime_seconds",
    "success",
    "failure_reason",
    "selected_reg_param",
    "selected_rank",
    "selected_n_modes",
    "posterior_uncertainty_mean",
    "solver_notes",
    # Reproducibility
    "ny_q",
    "nt_q",
]


# ------------------------------------------------------------------
# S-matrix cache
# ------------------------------------------------------------------

class SMatrixCache:
    """Cache sensitivity matrices keyed by sensor configuration."""

    def __init__(self, simulator: HeatConduction2DFD):
        self._sim = simulator
        self._cache: dict[str, tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]] = {}
        self._build_times: dict[str, float] = {}

    def get(
        self,
        cache_key: str,
        sensor_positions: list[tuple[float, float]],
        t_end: float = DEFAULT_T_TOTAL,
        ny_q: int = NY_Q,
        nt_q: int = NT_Q,
        obs_every: int = OBS_EVERY,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Return cached (S, obs_times, y_q_grid, t_q_grid) or build fresh."""
        if cache_key not in self._cache:
            log = logging.getLogger("benchmark.common")
            log.info("Building S for key=%s …", cache_key)
            t0 = time.perf_counter()
            S, obs_times, y_q_grid, t_q_grid = self._sim.build_sensitivity_matrix(
                sensor_positions=sensor_positions,
                t_end=t_end, ny_q=ny_q, nt_q=nt_q,
                obs_every=obs_every,
            )
            elapsed = time.perf_counter() - t0
            self._cache[cache_key] = (S, obs_times, y_q_grid, t_q_grid)
            self._build_times[cache_key] = elapsed
            log.info("  S built in %.1fs  shape=%s", elapsed, S.shape)
        return self._cache[cache_key]


# ------------------------------------------------------------------
# Sensor layout generators (extended from run_benchmark_2d_v2)
# ------------------------------------------------------------------

def make_sensor_positions(
    layout: str,
    Lx: float = DEFAULT_LX,
    Ly: float = DEFAULT_LY,
) -> list[tuple[float, float]]:
    """Return sensor positions for a named layout.

    Layouts
    -------
    sparse           : 2×2 = 4 sensors  (uniform)
    medium           : 3×3 = 9 sensors  (uniform)
    dense            : 4×4 = 16 sensors (uniform)
    uniform          : alias for medium
    boundary_biased  : 9 sensors, x biased toward x=0
    clustered        : 9 sensors bunched in centre
    sparse_boundary  : 4 sensors close to x=0 boundary
    """
    if layout in ("medium", "uniform"):
        xs = np.linspace(0.10 * Lx, 0.90 * Lx, 3)
        ys = np.linspace(0.10 * Ly, 0.90 * Ly, 3)
    elif layout == "sparse":
        xs = np.linspace(0.20 * Lx, 0.80 * Lx, 2)
        ys = np.linspace(0.20 * Ly, 0.80 * Ly, 2)
    elif layout == "dense":
        xs = np.linspace(0.10 * Lx, 0.90 * Lx, 4)
        ys = np.linspace(0.10 * Ly, 0.90 * Ly, 4)
    elif layout == "boundary_biased":
        xs = np.array([0.10, 0.20, 0.35]) * Lx
        ys = np.linspace(0.10 * Ly, 0.90 * Ly, 3)
    elif layout == "clustered":
        xs = np.linspace(0.35 * Lx, 0.65 * Lx, 3)
        ys = np.linspace(0.35 * Ly, 0.65 * Ly, 3)
    elif layout == "sparse_boundary":
        xs = np.array([0.10, 0.25]) * Lx
        ys = np.linspace(0.20 * Ly, 0.80 * Ly, 2)
    else:
        raise ValueError(f"Unknown sensor layout {layout!r}")

    return [(float(xi), float(yj)) for xi in xs for yj in ys]


def n_sensors_for_layout(layout: str) -> int:
    positions = make_sensor_positions(layout)
    return len(positions)


# ------------------------------------------------------------------
# Observation generator
# ------------------------------------------------------------------

def make_observation(
    simulator: HeatConduction2DFD,
    family_name: str,
    primary_level: int,
    secondary_values: dict[str, Any] | None,
    noise_sigma: float,
    sensor_positions: list[tuple[float, float]],
    seed: int,
    ny_q: int = NY_Q,
    nt_q: int = NT_Q,
) -> dict[str, Any]:
    """Generate one complete observation package.

    Returns
    -------
    dict with:
        q_true_coarse : (ny_q, nt_q)
        T_obs_noisy   : (n_sensors, n_obs)
        T_obs_clean   : (n_sensors, n_obs)
        family_info   : dict with axis metadata
    """
    rng = np.random.default_rng(seed)

    # Ground-truth flux on coarse evaluation grid
    y_q = np.linspace(0.0, simulator.Ly, ny_q)
    t_q = np.linspace(0.0, DEFAULT_T_TOTAL, nt_q)

    q_true = generate_family_flux(
        family_name, y_q, t_q,
        primary_axis_level=primary_level,
        secondary_axis_values=secondary_values,
        Ly=simulator.Ly, T_total=DEFAULT_T_TOTAL,
        q_max=DEFAULT_Q_MAX, seed=seed,
    )

    # True flux on fine y-grid for forward simulation
    y_fine = simulator.y_centers  # (ny,)
    q_fine = generate_family_flux(
        family_name, y_fine, t_q,
        primary_axis_level=primary_level,
        secondary_axis_values=secondary_values,
        Ly=simulator.Ly, T_total=DEFAULT_T_TOTAL,
        q_max=DEFAULT_Q_MAX, seed=seed,
    )

    T_clean, obs_times = simulator.simulate(
        q_flux_2d=q_fine,
        T0=DEFAULT_T0,
        sensor_positions=sensor_positions,
        t_end=DEFAULT_T_TOTAL,
        obs_every=OBS_EVERY,
    )

    noise = rng.normal(0.0, noise_sigma, size=T_clean.shape)
    T_noisy = T_clean + noise

    # Retrieve axis metadata
    fam = get_family(family_name)
    primary_val = fam.primary_axis_levels[max(0, min(primary_level, len(fam.primary_axis_levels)-1))]

    return {
        "q_true_coarse": q_true,
        "T_obs_noisy":   T_noisy,
        "T_obs_clean":   T_clean,
        "obs_times":     obs_times,
        "primary_axis_name":  fam.primary_axis_name,
        "primary_axis_value": primary_val,
    }


# ------------------------------------------------------------------
# Auto-lambda selection (L-curve heuristic for Tikhonov 2D)
# ------------------------------------------------------------------

def auto_select_lambda_tikhonov(
    S: np.ndarray,
    y_obs: np.ndarray,
    ny_q: int,
    nt_q: int,
    reg_order: int = 1,
    candidates: list[float] | None = None,
) -> float:
    """Select Tikhonov regularisation parameter via L-curve heuristic.

    Evaluates each candidate lambda, computes the residual norm and
    regularisation norm, then picks the corner of the L-curve using
    the maximum curvature criterion.
    """
    from src.tikhonov_solver_2d import build_diff_matrix

    if candidates is None:
        candidates = LAM_CANDIDATES

    N = ny_q * nt_q
    L = build_diff_matrix(N, order=reg_order)
    StS = S.T @ S
    LtL = L.T @ L
    Sty = S.T @ y_obs

    res_norms: list[float] = []
    reg_norms: list[float] = []

    for lam in candidates:
        A = StS + lam * LtL
        try:
            q_vec = np.linalg.solve(A, Sty)
        except np.linalg.LinAlgError:
            q_vec, *_ = np.linalg.lstsq(A, Sty, rcond=None)
        res_norms.append(float(np.linalg.norm(S @ q_vec - y_obs)))
        reg_norms.append(float(np.linalg.norm(L @ q_vec)))

    log_res = np.log(np.array(res_norms) + 1e-300)
    log_reg = np.log(np.array(reg_norms) + 1e-300)

    # L-curve corner: maximum curvature approximated by maximum product criterion
    # (maximise ||res||_log * ||reg||_log product change)
    if len(candidates) < 3:
        return candidates[len(candidates) // 2]

    # Simple heuristic: pick the lambda where the curve transitions from
    # residual-dominated to regularisation-dominated
    # Use the maximum of d(log_res)/d(log_lam) × d(log_reg)/d(log_lam)
    log_lam = np.log(np.array(candidates))
    dres = np.gradient(log_res, log_lam)
    dreg = np.gradient(log_reg, log_lam)
    # Corner: where the product of slopes changes sign or is most balanced
    corner_score = -dres + dreg   # large when res drops and reg rises
    best_idx = int(np.argmax(corner_score))
    best_idx = max(0, min(best_idx, len(candidates) - 1))
    return float(candidates[best_idx])


# ------------------------------------------------------------------
# Auto-rank selection for TSVD
# ------------------------------------------------------------------

def auto_select_rank_tsvd(
    S: np.ndarray,
    energy_threshold: float = 0.85,
) -> float:
    """Select TSVD truncation threshold from singular value energy."""
    sing_vals = np.linalg.svd(S, compute_uv=False)   # 1D array only
    energy = np.cumsum(sing_vals ** 2) / (np.sum(sing_vals ** 2) + 1e-300)
    n_keep = int(np.searchsorted(energy, energy_threshold) + 1)
    n_keep = max(1, min(n_keep, len(sing_vals)))
    # Convert to relative tolerance
    tol = float(sing_vals[n_keep - 1] / (sing_vals[0] + 1e-300))
    return tol


# ------------------------------------------------------------------
# Solver dispatcher
# ------------------------------------------------------------------

def run_solver(
    solver_name: str,
    S: np.ndarray,
    y_q_grid: np.ndarray,
    t_q_grid: np.ndarray,
    obs_data: dict[str, Any],
    simulator: HeatConduction2DFD,
    sensor_positions: list[tuple[float, float]],
    noise_sigma: float,
    seed: int,
) -> dict[str, Any]:
    """Run one solver on one case and return a uniform result dict.

    The sensitivity matrix S is shared across all solvers (fair comparison).
    Auto-parameter selection is applied where appropriate.
    """
    t0 = time.perf_counter()

    T_obs_noisy = obs_data["T_obs_noisy"]
    q_true      = obs_data["q_true_coarse"]
    n_sensors   = len(sensor_positions)
    n_obs_rows  = S.shape[0]
    n_obs_times = n_obs_rows // n_sensors
    T_obs_use   = T_obs_noisy[:, :n_obs_times]
    y_obs       = T_obs_use.flatten() - DEFAULT_T0

    base_spec = {
        "simulator":        simulator,
        "sensor_positions": sensor_positions,
        "T_obs_noisy":      T_obs_noisy,
        "obs_every":        OBS_EVERY,
        "t_end":            DEFAULT_T_TOTAL,
        "ny_q":             NY_Q,
        "nt_q":             NT_Q,
        "T0":               DEFAULT_T0,
        "q_true":           q_true,
        "S":                S,
        "y_q_grid":         y_q_grid,
        "t_q_grid":         t_q_grid,
    }

    raw: dict[str, Any] = {}
    failure_reason = ""
    success = True

    try:
        if solver_name == "tikhonov_2d":
            # Auto lambda selection
            lam = auto_select_lambda_tikhonov(S, y_obs, NY_Q, NT_Q)
            spec = dict(base_spec)
            spec["lam"]       = lam
            spec["reg_order"] = 1
            raw = solve_2d_tikhonov(spec)
            raw.setdefault("diagnostics", {})
            raw["diagnostics"]["lam"] = lam

        elif solver_name == "tsvd_2d":
            # Auto rank via energy threshold
            tsvd_tol = auto_select_rank_tsvd(S, energy_threshold=0.85)
            spec = dict(base_spec)
            spec["tsvd_tol"] = tsvd_tol
            raw = solve_2d_tsvd(spec)
            raw.setdefault("diagnostics", {})
            raw["diagnostics"]["tsvd_tol_selected"] = tsvd_tol

        elif solver_name == "fast_bayesian":
            spec = dict(base_spec)
            spec["n_modes"]         = "auto"
            spec["energy_threshold"]= BAYESIAN_ENERGY_THRESH
            spec["noise_sigma"]     = noise_sigma
            spec["prior_std"]       = 2e3
            raw = solve_2d_bayesian(spec)
            raw.setdefault("diagnostics", {})

        elif solver_name == "deepxde_pinn":
            spec = dict(base_spec)
            # PINN does NOT use the sensitivity matrix
            spec["n_iter"]      = PINN_N_ITER
            spec["lr"]          = PINN_LR
            spec["hidden_layers"] = PINN_HIDDEN
            spec["n_pde_pts"]   = PINN_N_PDE
            spec["n_bc_pts"]    = PINN_N_BC
            spec["n_ic_pts"]    = PINN_N_IC
            spec["seed"]        = seed
            try:
                from src.deepxde_pinn_solver_2d import solve_2d_pinn
                raw = solve_2d_pinn(spec)
            except ImportError as e:
                raise RuntimeError(f"deepxde_pinn unavailable: {e}") from e
            raw.setdefault("diagnostics", {})

        else:
            raise ValueError(f"Unknown solver {solver_name!r}")

    except Exception as exc:  # noqa: BLE001
        logging.getLogger("benchmark.common").error(
            "Solver %s FAILED: %s", solver_name, exc
        )
        raw = {
            "flux_pred": np.zeros((NY_Q, NT_Q)),
            "flux_rmse": float("nan"),
            "convergence_flag": False,
            "diagnostics": {"solver_name": solver_name},
        }
        failure_reason = str(exc)
        success = False

    runtime = time.perf_counter() - t0

    flux_pred = np.asarray(raw.get("flux_pred", np.zeros((NY_Q, NT_Q))))
    diag      = raw.get("diagnostics", {})

    # Compute full metrics
    metrics = compute_all_metrics(
        flux_pred, q_true,
        family_name=None,   # caller fills this
        diag_dict=diag,
    )

    if not success:
        metrics["success"] = False
        metrics["failure_reason"] = failure_reason

    # Override runtime with wall-clock timing
    metrics["runtime_seconds"] = runtime

    return {
        "flux_pred":  flux_pred,
        "raw_result": raw,
        "metrics":    metrics,
        "success":    success,
        "failure_reason": failure_reason,
    }


# ------------------------------------------------------------------
# CSV row builder
# ------------------------------------------------------------------

def build_raw_row(
    track_name: str,
    family_name: str,
    primary_axis_level: int,
    primary_axis_value: Any,
    secondary_axis_name: str,
    secondary_axis_level: str,
    secondary_axis_value: Any,
    solver_name: str,
    sensor_config: str,
    noise_sigma: float,
    seed: int,
    result: dict[str, Any],
) -> dict[str, Any]:
    """Build a flat raw-CSV row from a solver result dict."""
    m = result.get("metrics", {})
    fam = get_family(family_name) if family_name in [
        "fourier_kl_smooth", "gaussian_localized", "overlapping_multi_spot",
        "moving_hotspot", "matern_grf", "discontinuous_piecewise"
    ] else None

    return {
        "track_name":             track_name,
        "family_name":            family_name,
        "primary_axis_name":      fam.primary_axis_name if fam else "",
        "primary_axis_level":     primary_axis_level,
        "primary_axis_value":     str(primary_axis_value),
        "secondary_axis_name":    secondary_axis_name,
        "secondary_axis_level":   secondary_axis_level,
        "secondary_axis_value":   str(secondary_axis_value),
        "solver_name":            solver_name,
        "sensor_config":          sensor_config,
        "sensor_count":           n_sensors_for_layout(sensor_config),
        "noise_sigma":            noise_sigma,
        "seed":                   seed,
        "rmse_flux":              m.get("rmse_flux", float("nan")),
        "ssim_flux":              m.get("ssim_flux", float("nan")),
        "peak_localization_error": m.get("peak_localization_error", float("nan")),
        "band_error_scalar":      m.get("band_error_scalar", float("nan")),
        "band_low_rel_error":     m.get("band_low_rel_error", float("nan")),
        "band_mid_rel_error":     m.get("band_mid_rel_error", float("nan")),
        "band_high_rel_error":    m.get("band_high_rel_error", float("nan")),
        "support_overlap":        m.get("support_overlap", float("nan")),
        "runtime_seconds":        m.get("runtime_seconds", float("nan")),
        "success":                int(m.get("success", False)),
        "failure_reason":         m.get("failure_reason", ""),
        "selected_reg_param":     m.get("selected_reg_param", float("nan")),
        "selected_rank":          m.get("selected_rank", float("nan")),
        "selected_n_modes":       m.get("selected_n_modes", float("nan")),
        "posterior_uncertainty_mean": m.get("posterior_uncertainty_mean", float("nan")),
        "solver_notes":           m.get("solver_notes", solver_name),
        "ny_q":                   NY_Q,
        "nt_q":                   NT_Q,
    }


# ------------------------------------------------------------------
# Logging setup
# ------------------------------------------------------------------

def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s  %(levelname)-8s  %(name)-20s  %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout,
        force=True,
    )
