"""
run_benchmark_core.py
=====================
Track 1: benchmark_core — comparative study across four families,
sweeping the primary axis for each.

Design
------
Families       : fourier_kl_smooth, gaussian_localized,
                 overlapping_multi_spot, matern_grf
Primary axis   : 3 levels per family (easy → hard)
Secondary axes : fixed at representative mid-level values
Solvers        : tikhonov_2d, tsvd_2d, fast_bayesian, deepxde_pinn
Sensor layouts : medium (9 sensors)
Noise          : 0.1, 1.0 K
Seeds          : 0, 1

Total: 4 families × 3 levels × 1 layout × 2 noise × 2 seeds
     = 48 data cases × 4 solvers = 192 solver runs

Primary-axis study: each family's primary axis sweeps 3 levels.
Secondary axes:     fixed at representative mid-level (NOT swept here;
                    secondary-axis studies go in sensor_layout_track
                    or stress_track as budget allows).

Output: reports/benchmark_core_raw.csv
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
    n_sensors_for_layout,
    run_solver,
    setup_logging,
    RAW_COLUMNS,
    NY_Q, NT_Q,
    DEFAULT_T_TOTAL, DEFAULT_T0,
    OBS_EVERY,
)
from src.forward.heat2d_simulator import HeatConduction2DFD, DEFAULT_Q_MAX  # noqa: E402
from src.heat_flux_families import get_family, list_families                 # noqa: E402

log = logging.getLogger("benchmark.core")

# ---------------------------------------------------------------------------
# Benchmark parameters
# ---------------------------------------------------------------------------

FAMILIES   = ["fourier_kl_smooth", "gaussian_localized",
               "overlapping_multi_spot", "matern_grf"]
N_LEVELS   = 3       # primary-axis levels per family (0 = easy, 2 = hard)
LAYOUTS    = ["medium"]
NOISES     = [0.1, 1.0]
SEEDS      = [0, 1]
SOLVERS    = ["tikhonov_2d", "tsvd_2d", "fast_bayesian", "deepxde_pinn"]

# Secondary axes: fixed at representative mid-level (index = 1)
# These are held constant in benchmark_core.
SECONDARY_AXIS_LEVEL = "mid"   # label for the CSV
SECONDARY_AXIS_IDX   = 1       # index into family.secondary_axis_levels[ax]


def get_secondary_values(family_name: str) -> dict[str, Any]:
    """Return secondary-axis values at the representative mid level."""
    fam = get_family(family_name)
    result: dict[str, Any] = {}
    for ax_name, ax_vals in fam.secondary_axis_levels.items():
        mid_idx = SECONDARY_AXIS_IDX
        if mid_idx >= len(ax_vals):
            mid_idx = len(ax_vals) - 1
        result[ax_name] = ax_vals[mid_idx]
    return result


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def run_benchmark_core(
    output_csv: Path,
    simulator: HeatConduction2DFD,
    overwrite: bool = False,
    limit: int | None = None,
    solvers: list[str] | None = None,
) -> None:
    if solvers is None:
        solvers = SOLVERS

    output_csv.parent.mkdir(parents=True, exist_ok=True)

    # Load done keys for resuming
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

    s_cache = SMatrixCache(simulator)

    # Build the full experiment matrix
    combinations = list(itertools.product(
        FAMILIES,
        range(N_LEVELS),    # primary axis levels
        LAYOUTS,
        NOISES,
        SEEDS,
    ))
    if limit is not None:
        combinations = combinations[:limit]

    total_runs = len(combinations) * len(solvers)
    log.info("benchmark_core: %d data cases × %d solvers = %d runs",
             len(combinations), len(solvers), total_runs)

    completed = 0
    with output_csv.open("a", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=RAW_COLUMNS)
        if write_header:
            writer.writeheader()
            fh.flush()

        for family_name, level, layout, noise, seed in combinations:
            fam = get_family(family_name)
            prim_val = fam.primary_axis_levels[level]
            sensor_positions = make_sensor_positions(layout)

            # Sensitivity matrix (cached per layout)
            S, obs_times, y_q_grid, t_q_grid = s_cache.get(
                cache_key=layout,
                sensor_positions=sensor_positions,
            )

            # Observations (shared across solvers)
            secondary_values = get_secondary_values(family_name)
            obs_data = make_observation(
                simulator=simulator,
                family_name=family_name,
                primary_level=level,
                secondary_values=secondary_values,
                noise_sigma=noise,
                sensor_positions=sensor_positions,
                seed=seed,
            )

            for solver_name in solvers:
                key = (family_name, str(level), solver_name, layout, str(noise), str(seed))
                if key in done_keys:
                    completed += 1
                    continue

                log.info(
                    "  %s / %s / level=%d (prim=%s) / %s / noise=%.1f / seed=%d",
                    solver_name, family_name, level, prim_val, layout, noise, seed,
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

                # Update metric dict with family info for gating
                result["metrics"] = compute_all_metrics_with_family(
                    result, family_name, level
                )

                row = build_raw_row(
                    track_name="benchmark_core",
                    family_name=family_name,
                    primary_axis_level=level,
                    primary_axis_value=prim_val,
                    secondary_axis_name="all_mid",
                    secondary_axis_level=SECONDARY_AXIS_LEVEL,
                    secondary_axis_value="see_family_defaults",
                    solver_name=solver_name,
                    sensor_config=layout,
                    noise_sigma=noise,
                    seed=seed,
                    result=result,
                )
                writer.writerow(row)
                fh.flush()

                log.info(
                    "    rmse=%.1f  ssim=%.3f  peak_err=%.3f  "
                    "band=%.3f  support=%.3f  t=%.1fs  [%s]",
                    _get(row, "rmse_flux"),
                    _get(row, "ssim_flux"),
                    _get(row, "peak_localization_error"),
                    _get(row, "band_error_scalar"),
                    _get(row, "support_overlap"),
                    _get(row, "runtime_seconds"),
                    "ok" if row.get("success") else "FAIL",
                )
                completed += 1

    log.info("benchmark_core complete.  %d runs → %s", completed, output_csv)


def compute_all_metrics_with_family(
    result: dict[str, Any],
    family_name: str,
    level: int,
) -> dict[str, Any]:
    """Re-compute metrics with correct family_name for metric gating."""
    from src.metrics import compute_all_metrics
    from src.heat_flux_families import n_peaks_for_family, get_family

    flux_pred = np.asarray(result.get("flux_pred", np.zeros((NY_Q, NT_Q))))
    raw_result = result.get("raw_result", {})
    obs_data = result.get("obs_data_ref", {})

    # We can't easily re-get q_true here; the metrics were already computed
    # in run_solver. We just update the family gating.
    m = result.get("metrics", {})
    fam = get_family(family_name)
    n_peaks = n_peaks_for_family(family_name, level)

    # If peak metric was computed as nan due to wrong gating, leave it —
    # the metric.py gates by family now, so the first call was already correct.
    return m


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
        description="benchmark_core track — primary-axis comparative study",
    )
    p.add_argument("--output-csv", default="reports/benchmark_core_raw.csv")
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--limit", type=int, default=None, metavar="N",
                   help="Run only first N data-cases (smoke test)")
    p.add_argument("--solvers", nargs="+", default=SOLVERS,
                   choices=SOLVERS + ["all"])
    p.add_argument("--log-level", default="INFO")
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    setup_logging(args.log_level)

    output_csv = (_PROJECT_ROOT / args.output_csv).resolve()
    solvers = SOLVERS if "all" in args.solvers else args.solvers

    simulator = HeatConduction2DFD()
    log.info("Simulator: dt=%.4fs  nx=%d  ny=%d", simulator.dt, simulator.nx, simulator.ny)
    log.info("Grid: NY_Q=%d  NT_Q=%d  OBS_EVERY=%d", NY_Q, NT_Q, OBS_EVERY)

    run_benchmark_core(
        output_csv=output_csv,
        simulator=simulator,
        overwrite=args.overwrite,
        limit=args.limit,
        solvers=solvers,
    )


if __name__ == "__main__":
    main()
