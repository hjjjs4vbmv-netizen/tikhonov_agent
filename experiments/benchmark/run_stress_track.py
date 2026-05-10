"""
run_stress_track.py
===================
Track 3: stress_track — failure regimes and hard cases,
WITH primary-axis sweeps inside the hard-case families.

Design
------
Stress cases are NOT one-off examples.  Each family is swept along its
primary axis from "difficult" to "very difficult" (using harder portions
of the primary axis).

Families  : discontinuous_piecewise (hardest 3 levels)
            moving_hotspot (hard speed regime)
            overlapping_multi_spot (near-unresolvable overlap)
            matern_grf (short correlation / rough regime)
Primary axis: 3 levels, all in the "hard" regime
Solvers   : tikhonov_2d, tsvd_2d, fast_bayesian, deepxde_pinn
Layout    : sparse (4 sensors — constrained setting)
Noise     : 0.5, 1.0 K
Seeds     : 0, 1

Total: 4 families × 3 levels × 1 layout × 2 noise × 2 seeds
     = 48 data cases × 4 solvers = 192 solver runs

Note: stress families use the SAME primary-axis parameterisation as in
benchmark_core, but levels are chosen from the hard regime only.

Output: reports/stress_track_raw.csv
"""

from __future__ import annotations

import argparse
import csv
import itertools
import logging
import sys
from pathlib import Path
from typing import Any

import numpy as np

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
_HERE         = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from experiments.benchmark.common import (   # noqa: E402
    SMatrixCache,
    build_raw_row,
    make_observation,
    make_sensor_positions,
    run_solver,
    setup_logging,
    RAW_COLUMNS,
    NY_Q, NT_Q, OBS_EVERY,
)
from src.forward.heat2d_simulator import HeatConduction2DFD  # noqa: E402
from src.heat_flux_families import get_family, FamilyDef    # noqa: E402

log = logging.getLogger("benchmark.stress")

# ---------------------------------------------------------------------------
# Stress-track family configurations
#
# Each entry defines which primary-axis values to use in the hard regime.
# These override the normal primary_axis_levels by specifying hard-regime
# primary values directly.
# ---------------------------------------------------------------------------

# Stress primary levels (explicit values, from difficult to very difficult)
STRESS_FAMILIES: dict[str, dict[str, Any]] = {
    "discontinuous_piecewise": {
        "primary_axis_values": [8.0, 20.0, 50.0],   # jump_sharpness: sharp to near-delta
        "primary_axis_labels": ["sharp", "very_sharp", "near_delta"],
        "secondary_override":  {"n_jumps": 2, "asymmetry": 0.2},   # added complexity
    },
    "moving_hotspot": {
        "primary_axis_values": [0.6, 0.85, 1.0],    # speed_frac: fast to very fast
        "primary_axis_labels": ["fast", "very_fast", "max_speed"],
        "secondary_override":  {"amplitude_modulation": 0.3, "direction_reversal": True},
    },
    "overlapping_multi_spot": {
        "primary_axis_values": [0.12, 0.05, 0.02],  # separation_frac: nearly merged
        "primary_axis_labels": ["marginal", "near_merged", "unresolvable"],
        "secondary_override":  {"amplitude_imbalance": 0.4, "width_mismatch": 0.3},
    },
    "matern_grf": {
        "primary_axis_values": [0.06, 0.03, 0.01],  # corr_length: very rough
        "primary_axis_labels": ["rough", "very_rough", "near_white_noise"],
        "secondary_override":  {"anisotropy_ratio": 0.5, "nonstationarity": 0.5},
    },
}

FAMILIES   = list(STRESS_FAMILIES.keys())
LAYOUT     = "sparse"
NOISES     = [0.5, 1.0]
SEEDS      = [0, 1]
SOLVERS    = ["tikhonov_2d", "tsvd_2d", "fast_bayesian", "deepxde_pinn"]


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def run_stress_track(
    output_csv: Path,
    simulator: HeatConduction2DFD,
    overwrite: bool = False,
    limit: int | None = None,
    solvers: list[str] | None = None,
) -> None:
    if solvers is None:
        solvers = SOLVERS

    output_csv.parent.mkdir(parents=True, exist_ok=True)

    done_keys: set[tuple] = set()
    if not overwrite and output_csv.exists():
        with output_csv.open(newline="") as fh:
            for row in csv.DictReader(fh):
                done_keys.add((
                    row.get("family_name", ""),
                    row.get("primary_axis_level", ""),
                    row.get("solver_name", ""),
                    row.get("sensor_config", ""),
                    row.get("noise_sigma", ""),
                    row.get("seed", ""),
                ))
        log.info("Resuming: skipping %d completed runs", len(done_keys))

    write_header = not output_csv.exists() or overwrite
    if overwrite and output_csv.exists():
        output_csv.unlink()

    sensor_positions = make_sensor_positions(LAYOUT)
    s_cache = SMatrixCache(simulator)
    S, obs_times, y_q_grid, t_q_grid = s_cache.get(
        cache_key=LAYOUT,
        sensor_positions=sensor_positions,
    )

    # Stress combinations
    all_cases: list[tuple] = []
    for family_name, cfg in STRESS_FAMILIES.items():
        for level_idx, (prim_val, label) in enumerate(
            zip(cfg["primary_axis_values"], cfg["primary_axis_labels"])
        ):
            for noise in NOISES:
                for seed in SEEDS:
                    all_cases.append((family_name, level_idx, prim_val, label, noise, seed))

    if limit is not None:
        all_cases = all_cases[:limit]

    total_runs = len(all_cases) * len(solvers)
    log.info("stress_track: %d data cases × %d solvers = %d runs",
             len(all_cases), len(solvers), total_runs)

    completed = 0
    with output_csv.open("a", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=RAW_COLUMNS)
        if write_header:
            writer.writeheader()
            fh.flush()

        for family_name, level_idx, prim_val, label, noise, seed in all_cases:
            fam_cfg = STRESS_FAMILIES[family_name]
            secondary_override = dict(fam_cfg.get("secondary_override", {}))

            # Build a synthetic primary axis spec for the family generator
            # We pass explicit primary value via secondary_values with key override
            # The generator picks level index, so we need to inject the actual value.
            # Solution: pass it as a patched family call with override.
            obs_data = _make_stress_observation(
                simulator=simulator,
                family_name=family_name,
                primary_val=prim_val,
                secondary_override=secondary_override,
                noise_sigma=noise,
                sensor_positions=sensor_positions,
                seed=seed,
            )

            for solver_name in solvers:
                key = (family_name, str(level_idx), solver_name, LAYOUT, str(noise), str(seed))
                if key in done_keys:
                    completed += 1
                    continue

                log.info(
                    "  %s / %s / level=%d (%s) / noise=%.1f / seed=%d",
                    solver_name, family_name, level_idx, label, noise, seed,
                )

                result = run_solver(
                    solver_name=solver_name,
                    S=S,
                    y_q_grid=y_q_grid,
                    t_q_grid=t_q_grid,
                    obs_data=obs_data,
                    simulator=simulator,
                    sensor_positions=sensor_positions,
                    noise_sigma=noise,
                    seed=seed,
                )

                row = build_raw_row(
                    track_name="stress_track",
                    family_name=family_name,
                    primary_axis_level=level_idx,
                    primary_axis_value=prim_val,
                    secondary_axis_name="stress_level",
                    secondary_axis_level=label,
                    secondary_axis_value=label,
                    solver_name=solver_name,
                    sensor_config=LAYOUT,
                    noise_sigma=noise,
                    seed=seed,
                    result=result,
                )
                writer.writerow(row)
                fh.flush()

                log.info(
                    "    rmse=%.1f  ssim=%.3f  t=%.1fs  [%s]",
                    _get(row, "rmse_flux"),
                    _get(row, "ssim_flux"),
                    _get(row, "runtime_seconds"),
                    "ok" if row.get("success") else "FAIL",
                )
                completed += 1

    log.info("stress_track complete.  %d runs → %s", completed, output_csv)


def _make_stress_observation(
    simulator: HeatConduction2DFD,
    family_name: str,
    primary_val: float,
    secondary_override: dict[str, Any],
    noise_sigma: float,
    sensor_positions: list[tuple[float, float]],
    seed: int,
) -> dict[str, Any]:
    """Generate observation for a stress case with explicit primary_val.

    Since the family generator uses a level index, we directly call the
    internal generator with the explicit primary value.
    """
    from src.forward.heat2d_simulator import DEFAULT_T_TOTAL, DEFAULT_T0, DEFAULT_Q_MAX
    from src.heat_flux_families import generate_family_flux, get_family
    import numpy as np

    y_q = np.linspace(0.0, simulator.Ly, NY_Q)
    t_q = np.linspace(0.0, DEFAULT_T_TOTAL, NT_Q)

    # Build a patched primary_axis_levels so level 0 = primary_val
    fam = get_family(family_name)

    # Inject primary value at level 0 by monkey-patching a temp override dict
    # We accomplish this by calling the generator directly.
    q_true = _call_generator_with_primary(
        family_name, y_q, t_q, primary_val, secondary_override, DEFAULT_Q_MAX, seed
    )
    y_fine = simulator.y_centers
    q_fine = _call_generator_with_primary(
        family_name, y_fine, t_q, primary_val, secondary_override, DEFAULT_Q_MAX, seed
    )

    rng = np.random.default_rng(seed)
    T_clean, obs_times = simulator.simulate(
        q_flux_2d=q_fine, T0=DEFAULT_T0,
        sensor_positions=sensor_positions,
        t_end=DEFAULT_T_TOTAL, obs_every=OBS_EVERY,
    )
    noise = rng.normal(0.0, noise_sigma, size=T_clean.shape)
    T_noisy = T_clean + noise

    return {
        "q_true_coarse": q_true,
        "T_obs_noisy":   T_noisy,
        "T_obs_clean":   T_clean,
        "obs_times":     obs_times,
        "primary_axis_name":  fam.primary_axis_name,
        "primary_axis_value": primary_val,
    }


def _call_generator_with_primary(
    family_name: str,
    y_grid: np.ndarray,
    t_grid: np.ndarray,
    primary_val: float,
    secondary_values: dict[str, Any],
    q_max: float,
    seed: int,
) -> np.ndarray:
    """Call the family generator with an explicit primary axis value."""
    import sys
    # Import the internal generators
    from src.heat_flux_families import (
        _gen_fourier_kl_smooth,
        _gen_gaussian_localized,
        _gen_overlapping_multi_spot,
        _gen_moving_hotspot,
        _gen_matern_grf,
        _gen_discontinuous_piecewise,
    )
    kwargs = dict(q_max=q_max, seed=seed)

    if family_name == "fourier_kl_smooth":
        kwargs["n_modes"]             = int(primary_val)
        kwargs["temporal_anisotropy"] = float(secondary_values.get("temporal_anisotropy", 1.0))
        kwargs["amplitude_contrast"]  = float(secondary_values.get("amplitude_contrast", 1.0))
        kwargs["phase_skew"]          = float(secondary_values.get("phase_skew", 0.0))
        return _gen_fourier_kl_smooth(y_grid, t_grid, **kwargs)

    elif family_name == "gaussian_localized":
        kwargs["sigma_y_frac"]           = float(primary_val)
        kwargs["anisotropy_ratio"]       = float(secondary_values.get("anisotropy_ratio", 1.0))
        kwargs["temporal_duration_frac"] = float(secondary_values.get("temporal_duration_frac", 0.2))
        kwargs["peak_amplitude"]         = float(secondary_values.get("peak_amplitude", 1.0))
        return _gen_gaussian_localized(y_grid, t_grid, **kwargs)

    elif family_name == "overlapping_multi_spot":
        kwargs["separation_frac"]      = float(primary_val)
        kwargs["amplitude_imbalance"]  = float(secondary_values.get("amplitude_imbalance", 0.0))
        kwargs["width_mismatch"]       = float(secondary_values.get("width_mismatch", 0.0))
        kwargs["temporal_offset_frac"] = float(secondary_values.get("temporal_offset_frac", 0.0))
        return _gen_overlapping_multi_spot(y_grid, t_grid, **kwargs)

    elif family_name == "moving_hotspot":
        kwargs["speed_frac"]           = float(primary_val)
        kwargs["amplitude_modulation"] = float(secondary_values.get("amplitude_modulation", 0.0))
        kwargs["width_modulation"]     = float(secondary_values.get("width_modulation", 0.0))
        kwargs["direction_reversal"]   = bool(secondary_values.get("direction_reversal", False))
        return _gen_moving_hotspot(y_grid, t_grid, **kwargs)

    elif family_name == "matern_grf":
        kwargs["corr_length_frac"] = float(primary_val)
        kwargs["anisotropy_ratio"] = float(secondary_values.get("anisotropy_ratio", 1.0))
        kwargs["orientation_deg"]  = float(secondary_values.get("orientation_deg", 0.0))
        kwargs["nonstationarity"]  = float(secondary_values.get("nonstationarity", 0.0))
        return _gen_matern_grf(y_grid, t_grid, **kwargs)

    elif family_name == "discontinuous_piecewise":
        kwargs["jump_sharpness"]     = float(primary_val)
        kwargs["plateau_width_frac"] = float(secondary_values.get("plateau_width_frac", 0.3))
        kwargs["n_jumps"]            = int(secondary_values.get("n_jumps", 1))
        kwargs["asymmetry"]          = float(secondary_values.get("asymmetry", 0.0))
        return _gen_discontinuous_piecewise(y_grid, t_grid, **kwargs)

    else:
        raise ValueError(f"Unknown family: {family_name}")


def _get(row: dict, key: str) -> Any:
    v = row.get(key, float("nan"))
    try:
        return float(v)
    except (TypeError, ValueError):
        return float("nan")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="stress_track — failure regime + primary-axis study",
    )
    p.add_argument("--output-csv", default="reports/stress_track_raw.csv")
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--solvers", nargs="+", default=SOLVERS)
    p.add_argument("--log-level", default="INFO")
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    setup_logging(args.log_level)

    output_csv = (_PROJECT_ROOT / args.output_csv).resolve()
    solvers = args.solvers

    simulator = HeatConduction2DFD()
    log.info("Simulator: dt=%.4fs", simulator.dt)

    run_stress_track(
        output_csv=output_csv,
        simulator=simulator,
        overwrite=args.overwrite,
        limit=args.limit,
        solvers=solvers,
    )


if __name__ == "__main__":
    main()
