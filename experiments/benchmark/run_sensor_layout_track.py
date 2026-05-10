"""
run_sensor_layout_track.py
==========================
Track 2: sensor_layout_track — observability / layout effects study,
WITH primary-axis sweeps inside each family.

Design
------
This track studies how sensor layout affects reconstruction quality
ACROSS the full primary-axis range of each family.  Layout is the
track-level variable, but the primary-axis sweep is mandatory.

Families  : gaussian_localized, overlapping_multi_spot,
            moving_hotspot, matern_grf
Primary axis: 3 levels per family
Layouts   : uniform (3×3=9), boundary_biased (9), clustered (9)
            — total sensor count fixed at 9 across all layouts
Noise     : 0.1, 1.0 K
Seeds     : 0

Total: 4 families × 3 levels × 3 layouts × 2 noise × 1 seed
     = 72 data cases × 4 solvers = 288 solver runs

Secondary axis: fixed at mid level throughout.

Output: reports/sensor_layout_track_raw.csv
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
from src.heat_flux_families import get_family               # noqa: E402

log = logging.getLogger("benchmark.sensor_layout")

# ---------------------------------------------------------------------------
# Track parameters
# ---------------------------------------------------------------------------

FAMILIES   = ["gaussian_localized", "overlapping_multi_spot",
               "moving_hotspot", "matern_grf"]
N_LEVELS   = 3
LAYOUTS    = ["uniform", "boundary_biased", "clustered"]   # all have ~9 sensors
NOISES     = [0.1, 1.0]
SEEDS      = [0]
SOLVERS    = ["tikhonov_2d", "tsvd_2d", "fast_bayesian", "deepxde_pinn"]


def get_secondary_values(family_name: str) -> dict[str, Any]:
    fam = get_family(family_name)
    result: dict[str, Any] = {}
    for ax_name, ax_vals in fam.secondary_axis_levels.items():
        mid_idx = min(1, len(ax_vals) - 1)
        result[ax_name] = ax_vals[mid_idx]
    return result


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def run_sensor_layout_track(
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

    s_cache = SMatrixCache(simulator)

    combinations = list(itertools.product(
        FAMILIES, range(N_LEVELS), LAYOUTS, NOISES, SEEDS
    ))
    if limit is not None:
        combinations = combinations[:limit]

    total_runs = len(combinations) * len(solvers)
    log.info("sensor_layout_track: %d data cases × %d solvers = %d runs",
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

            S, obs_times, y_q_grid, t_q_grid = s_cache.get(
                cache_key=f"layout_{layout}",
                sensor_positions=sensor_positions,
            )

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
                    "  %s / %s / level=%d / layout=%s / noise=%.1f / seed=%d",
                    solver_name, family_name, level, layout, noise, seed,
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
                    track_name="sensor_layout_track",
                    family_name=family_name,
                    primary_axis_level=level,
                    primary_axis_value=prim_val,
                    secondary_axis_name="sensor_layout",
                    secondary_axis_level=layout,
                    secondary_axis_value=len(sensor_positions),
                    solver_name=solver_name,
                    sensor_config=layout,
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

    log.info("sensor_layout_track complete.  %d runs → %s", completed, output_csv)


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
        description="sensor_layout_track — layout × primary-axis study",
    )
    p.add_argument("--output-csv", default="reports/sensor_layout_track_raw.csv")
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

    run_sensor_layout_track(
        output_csv=output_csv,
        simulator=simulator,
        overwrite=args.overwrite,
        limit=args.limit,
        solvers=solvers,
    )


if __name__ == "__main__":
    main()
