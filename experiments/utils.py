"""
utils.py
========
Shared utilities for the tikhonov_agent experiment pipeline.

Provides:
  - Synthetic heat-flux generators (step, ramp, single_pulse, multi_pulse,
    smooth_sinusoid).
  - Metric computation from ground-truth + RunSummary.
  - Variant override lookup table.
  - I/O helpers (load_case, save_result_row, load_manifest).
  - Logging setup.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging(level: str = "INFO") -> None:
    """Configure root logger with a timestamp-prefixed format."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout,
        force=True,
    )


# ---------------------------------------------------------------------------
# Flux generators
# ---------------------------------------------------------------------------

def make_step_flux(
    time_grid: np.ndarray,
    q_base: float = 0.0,
    q_step: float = 50_000.0,
    t_on_frac: float = 0.3,
) -> np.ndarray:
    """Step flux: q_base before t_on, q_step after t_on.

    Parameters
    ----------
    time_grid  : 1-D array of time points [s]
    q_base     : flux before the step [W/m^2]
    q_step     : flux after the step [W/m^2]
    t_on_frac  : fraction of total time horizon when the step occurs
    """
    t_on = time_grid[0] + t_on_frac * (time_grid[-1] - time_grid[0])
    q = np.where(time_grid >= t_on, q_step, q_base)
    return q.astype(float)


def make_ramp_flux(
    time_grid: np.ndarray,
    q_start: float = 0.0,
    q_end: float = 80_000.0,
) -> np.ndarray:
    """Linear ramp from q_start to q_end over the full time horizon."""
    t = time_grid
    q = q_start + (q_end - q_start) * (t - t[0]) / (t[-1] - t[0] + 1e-30)
    return q.astype(float)


def make_single_pulse_flux(
    time_grid: np.ndarray,
    q_base: float = 0.0,
    q_peak: float = 60_000.0,
    t_center_frac: float = 0.4,
    t_width_frac: float = 0.2,
) -> np.ndarray:
    """Gaussian-shaped single pulse.

    Parameters
    ----------
    t_center_frac : centre of the pulse as fraction of total time
    t_width_frac  : std-dev of Gaussian as fraction of total time
    """
    T = time_grid[-1] - time_grid[0]
    t_center = time_grid[0] + t_center_frac * T
    sigma = t_width_frac * T
    q = q_base + (q_peak - q_base) * np.exp(-0.5 * ((time_grid - t_center) / sigma) ** 2)
    return q.astype(float)


def make_multi_pulse_flux(
    time_grid: np.ndarray,
    q_base: float = 0.0,
    q_peak: float = 50_000.0,
    n_pulses: int = 3,
    t_width_frac: float = 0.08,
) -> np.ndarray:
    """Sum of evenly-spaced Gaussian pulses.

    Centres are at fractions 1/(n+1), 2/(n+1), …, n/(n+1) of the time horizon.
    """
    T = time_grid[-1] - time_grid[0]
    sigma = t_width_frac * T
    q = np.full_like(time_grid, q_base, dtype=float)
    for k in range(1, n_pulses + 1):
        t_c = time_grid[0] + k / (n_pulses + 1) * T
        q += (q_peak - q_base) * np.exp(-0.5 * ((time_grid - t_c) / sigma) ** 2)
    return q


def make_smooth_sinusoid_flux(
    time_grid: np.ndarray,
    q_mean: float = 40_000.0,
    q_amplitude: float = 20_000.0,
    n_cycles: float = 2.0,
) -> np.ndarray:
    """Smooth sinusoidal flux: q_mean + q_amplitude * sin(2π n_cycles t/T)."""
    T = time_grid[-1] - time_grid[0]
    phase = 2.0 * np.pi * n_cycles * (time_grid - time_grid[0]) / (T + 1e-30)
    q = q_mean + q_amplitude * np.sin(phase)
    return q.astype(float)


# Registry: name → generator function
_FLUX_GENERATORS: dict[str, Any] = {
    "step": make_step_flux,
    "ramp": make_ramp_flux,
    "single_pulse": make_single_pulse_flux,
    "multi_pulse": make_multi_pulse_flux,
    "smooth_sinusoid": make_smooth_sinusoid_flux,
}


def generate_flux(
    family: str,
    time_grid: np.ndarray,
    params: dict[str, Any],
) -> np.ndarray:
    """Generate a heat-flux profile for the given family and parameters.

    Parameters
    ----------
    family    : one of 'step', 'ramp', 'single_pulse', 'multi_pulse',
                'smooth_sinusoid'
    time_grid : 1-D time array [s]
    params    : dict of family-specific keyword arguments

    Returns
    -------
    q : shape (N_t,)  heat flux [W/m^2]

    Raises
    ------
    ValueError if family is not recognised.
    """
    if family not in _FLUX_GENERATORS:
        raise ValueError(
            f"Unknown flux family '{family}'. "
            f"Available: {sorted(_FLUX_GENERATORS)}"
        )
    return _FLUX_GENERATORS[family](time_grid, **params)


# ---------------------------------------------------------------------------
# Variant overrides
# ---------------------------------------------------------------------------

def get_variant_overrides(
    variant_name: str,
    variant_config: dict[str, Any],
) -> dict[str, Any]:
    """Return planner_overrides dict for a given variant.

    The variant_config comes from the experiment YAML's ``variants`` section.
    We pass it through almost verbatim as planner overrides; only the keys
    that ``make_initial_plan`` understands are used.
    """
    allowed_keys = {
        "reg_order", "lambda_strategy", "lambda_value", "lambda_grid",
        "physical_bounds", "max_retries", "iteration_budget", "stop_tolerance",
        "num_parameters", "skip_verifier",
    }
    overrides: dict[str, Any] = {}
    for k, v in variant_config.items():
        if k in allowed_keys:
            overrides[k] = v
    return overrides


# ---------------------------------------------------------------------------
# Metric computation
# ---------------------------------------------------------------------------

def compute_flux_metrics(
    q_true: np.ndarray,
    q_est: np.ndarray,
) -> dict[str, float]:
    """Reconstruction quality of the estimated flux vs ground truth.

    Both arrays must have the same shape (N_t,).

    Returns dict with keys:
      flux_l2_error, flux_relative_l2_error, flux_rmse, flux_peak_error,
      flux_correlation
    """
    if q_true.shape != q_est.shape:
        raise ValueError(
            f"Shape mismatch: q_true={q_true.shape}, q_est={q_est.shape}"
        )

    diff = q_true - q_est
    l2_err = float(np.linalg.norm(diff))
    denom = float(np.linalg.norm(q_true)) or 1.0
    rel_l2 = l2_err / denom
    rmse = float(np.sqrt(np.mean(diff**2)))
    peak_err = float(np.max(np.abs(diff)))

    # Pearson correlation (guard against flat signals)
    std_true = float(np.std(q_true))
    std_est = float(np.std(q_est))
    if std_true < 1e-10 or std_est < 1e-10:
        corr = 1.0 if std_true < 1e-10 and std_est < 1e-10 else 0.0
    else:
        corr = float(np.corrcoef(q_true, q_est)[0, 1])

    return {
        "flux_l2_error": l2_err,
        "flux_relative_l2_error": rel_l2,
        "flux_rmse": rmse,
        "flux_peak_error": peak_err,
        "flux_correlation": corr,
    }


def compute_forward_replay_metrics(
    y_obs: np.ndarray,
    y_fit: np.ndarray,
) -> dict[str, float]:
    """Forward-model replay quality: fitted temperatures vs observations.

    Both arrays are flattened (n_sensors × N_t,).
    """
    diff = y_obs - y_fit
    rmse = float(np.sqrt(np.mean(diff**2)))
    signal_range = float(np.ptp(y_obs)) or 1.0
    rel_err = rmse / signal_range
    max_abs = float(np.max(np.abs(diff)))
    return {
        "replay_rmse": rmse,
        "replay_relative_error": rel_err,
        "replay_max_abs_error": max_abs,
    }


def compute_regularity_metrics(
    q_est: np.ndarray,
    physical_bounds: tuple[float, float] | None = None,
    x_params: np.ndarray | None = None,
) -> dict[str, Any]:
    """Regularity and physical sanity metrics for an estimated flux.

    Parameters
    ----------
    q_est         : estimated flux expanded to full time series (N_t,)
    physical_bounds : optional (lo, hi) for violation counting
    x_params      : raw inversion parameter vector (N_p,).  When provided,
                    oscillation_score is computed on these N_p values instead
                    of the expanded q_est, which avoids a structural artifact
                    in piecewise-constant parameterization where every segment
                    boundary is counted as a direction change.

    Returns dict with keys:
      roughness_l1, roughness_l2, oscillation_score,
      sign_flip_count, physical_violation_count, within_bounds_flag

    oscillation_score definition
    ----------------------------
    Normalized second-difference energy of the parameter vector:
        osc = sum(diff(x, n=2)**2) / (sum(x**2) + 1e-30)
    This is zero for constant or linearly-varying solutions and large for
    rapidly oscillating ones.  It is dimensionless, scale-invariant, and
    computable from the N_p-element parameter vector alone.
    """
    metrics: dict[str, Any] = {}

    if len(q_est) < 2:
        return {
            "roughness_l1": 0.0, "roughness_l2": 0.0,
            "oscillation_score": 0.0, "sign_flip_count": 0,
            "physical_violation_count": 0, "within_bounds_flag": True,
        }

    dx = np.diff(q_est)
    metrics["roughness_l1"] = float(np.sum(np.abs(dx)))
    metrics["roughness_l2"] = float(np.linalg.norm(dx))

    # Oscillation score: computed on raw parameter vector when available.
    # Falls back to sign-change ratio on expanded signal otherwise.
    if x_params is not None and len(x_params) >= 3:
        x = np.asarray(x_params, dtype=float)
        d2x = np.diff(x, n=2)
        osc = float(np.sum(d2x**2) / (np.sum(x**2) + 1e-30))
    else:
        # Fallback: sign-change ratio on expanded signal (NOTE: will be
        # structurally constant for piecewise-constant parameterization)
        sign_changes_osc = int(np.sum(np.diff(np.sign(dx)) != 0))
        osc = sign_changes_osc / max(len(dx) - 1, 1)
    metrics["oscillation_score"] = osc

    # Sign flips in the flux itself
    sign_changes_flux = int(np.sum(np.diff(np.sign(q_est)) != 0))
    metrics["sign_flip_count"] = sign_changes_flux

    # Physical bounds
    if physical_bounds is not None:
        lo, hi = physical_bounds
        violations = int(np.sum((q_est < lo) | (q_est > hi)))
        metrics["physical_violation_count"] = violations
        metrics["within_bounds_flag"] = violations == 0
    else:
        metrics["physical_violation_count"] = 0
        metrics["within_bounds_flag"] = True

    return metrics


def compute_all_metrics(
    case_meta: dict[str, Any],
    q_true: np.ndarray,
    q_est_full: np.ndarray,
    y_obs: np.ndarray,
    y_fit: np.ndarray,
    summary: Any,            # RunSummary
    variant_name: str,
    runtime_sec: float,
    physical_bounds: tuple[float, float] | None = None,
    x_params: np.ndarray | None = None,
) -> dict[str, Any]:
    """Assemble the complete metrics row for the results CSV.

    Parameters
    ----------
    case_meta      : dict with keys: case_id, flux_family, noise_level,
                     sensor_count, sensor_layout, time_resolution, seed
    q_true         : ground-truth flux, shape (N_t,)
    q_est_full     : estimated flux expanded to (N_t,)
    y_obs          : observed temperatures, flattened (n_sensors * N_t,)
    y_fit          : fitted temperatures, flattened
    summary        : RunSummary from IHCPAgent.run()
    variant_name   : e.g. "fixed_solver"
    runtime_sec    : wall-clock seconds for the variant run
    physical_bounds: optional (lo, hi) used for violation count
    x_params       : raw parameter vector (N_p,) for oscillation_score
    """
    row: dict[str, Any] = {}

    # --- Metadata columns ---
    row.update(case_meta)
    row["variant_name"] = variant_name

    # --- Flux reconstruction metrics ---
    row.update(compute_flux_metrics(q_true, q_est_full))

    # --- Forward replay metrics ---
    row.update(compute_forward_replay_metrics(y_obs, y_fit))

    # --- Regularity / physical metrics ---
    row.update(compute_regularity_metrics(q_est_full, physical_bounds, x_params=x_params))

    # --- Agent / workflow metrics from RunSummary ---
    result = summary.final_result
    traces = summary.traces

    row["final_decision"] = summary.final_status
    row["success_flag"] = int(summary.final_status in ("pass", "weak_pass"))
    row["weak_pass_flag"] = int(summary.final_status == "weak_pass")
    row["manual_review_flag"] = int(summary.final_status == "manual_review")
    row["failure_flag"] = int(summary.final_status == "fail")
    row["iteration_count"] = len(traces)

    # Count distinct replanning actions (non-terminal)
    terminal_prefixes = ("stop_",)
    replan_actions = [
        t.replanning_action for t in traces
        if not any(t.replanning_action.startswith(p) for p in terminal_prefixes)
    ]
    row["replanning_count"] = len(replan_actions)

    row["runtime_sec"] = runtime_sec
    row["final_lambda"] = result.lambda_used
    row["final_reg_order"] = result.reg_order
    row["final_variant_name"] = variant_name

    # Improvement from first to last iteration
    if len(traces) >= 2:
        first_rmse = traces[0].verification.replay_rmse
        last_rmse = traces[-1].verification.replay_rmse
        denom = first_rmse or 1.0
        row["initial_to_final_improvement"] = (first_rmse - last_rmse) / denom
    else:
        row["initial_to_final_improvement"] = 0.0

    # Last verifier decision (may differ from final_status when budget exhausted)
    if traces:
        row["last_verifier_decision"] = traces[-1].verification.decision
    else:
        row["last_verifier_decision"] = "unknown"

    return row


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def load_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML config file and return as a dict.

    Raises ValueError on missing file or invalid YAML.
    """
    p = Path(path)
    if not p.exists():
        raise ValueError(f"Config file not found: {p}")
    with p.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"Config file does not contain a YAML mapping: {p}")
    return data


def load_manifest(cases_dir: str | Path) -> pd.DataFrame:
    """Load the case manifest CSV from a cases directory.

    Returns a DataFrame with at least columns: case_id, config_path, obs_path,
    truth_path, flux_family, noise_level, seed, sensor_count, sensor_layout,
    time_resolution.
    """
    manifest_path = Path(cases_dir) / "manifest.csv"
    if not manifest_path.exists():
        raise FileNotFoundError(
            f"Manifest not found at {manifest_path}. "
            "Run generate_cases.py first."
        )
    return pd.read_csv(manifest_path)


def load_truth(truth_path: str | Path) -> dict[str, np.ndarray]:
    """Load ground-truth arrays from a .npz file.

    Expected keys: q_true (N_t,), time_grid (N_t,).
    """
    data = np.load(truth_path)
    return {k: data[k] for k in data.files}


def save_result_row(row: dict[str, Any], output_csv: Path) -> None:
    """Upsert a single result row into the master results CSV.

    If the file exists and already contains a row with the same
    (case_id, variant_name), the old row is replaced.  Otherwise the new
    row is appended.  Creates the file with a header if it does not yet
    exist (thread-unsafe for parallel writes, use sequentially).
    """
    df_new = pd.DataFrame([row])
    if output_csv.exists():
        df_existing = pd.read_csv(output_csv)
        key_cols = ["case_id", "variant_name"]
        if all(c in df_existing.columns for c in key_cols) and all(c in df_new.columns for c in key_cols):
            mask = ~(
                (df_existing["case_id"] == row["case_id"]) &
                (df_existing["variant_name"] == row["variant_name"])
            )
            df_combined = pd.concat([df_existing[mask], df_new], ignore_index=True)
        else:
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(output_csv, index=False)
    else:
        output_csv.parent.mkdir(parents=True, exist_ok=True)
        df_new.to_csv(output_csv, index=False)


def build_time_grid(
    t_start: float,
    t_end: float,
    n_steps: int,
) -> np.ndarray:
    """Return a uniform time grid as a numpy array."""
    return np.linspace(t_start, t_end, n_steps)
