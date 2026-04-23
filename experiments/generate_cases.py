"""
generate_cases.py
=================
Generate synthetic benchmark cases for the tikhonov_agent experiment pipeline.

Each case consists of:
  - config.yaml  : problem spec compatible with src/parser.py
  - observations.csv : noisy temperature time series (rows=time, cols=sensors)
  - truth.npz    : ground-truth arrays (q_true, time_grid)

Cases are written to:
  experiments/cases/<experiment_name>/
    manifest.csv
    case_0001/
      config.yaml
      observations.csv
      truth.npz
    case_0002/
      ...

Usage
-----
    python experiments/generate_cases.py \\
        --config experiments/configs/benchmark_v1.yaml \\
        [--overwrite]
"""

from __future__ import annotations

import argparse
import itertools
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

# ---------------------------------------------------------------------------
# Path setup: allow running from the project root or this directory
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from experiments.utils import (  # noqa: E402
    build_time_grid,
    generate_flux,
    load_config,
    setup_logging,
)
from src.forward_model import HeatConductionFD  # noqa: E402
from src.types import BoundaryConditions, Geometry, Material  # noqa: E402

log = logging.getLogger("generate_cases")


# ---------------------------------------------------------------------------
# Case generation
# ---------------------------------------------------------------------------

def generate_case(
    case_dir: Path,
    *,
    time_grid: np.ndarray,
    geometry: Geometry,
    material: Material,
    bc: BoundaryConditions,
    initial_condition: float,
    sensor_positions: list[float],
    flux_family: str,
    flux_params: dict,
    noise_level: float,
    noise_std_in_config: float | None,
    rng: np.random.Generator,
) -> None:
    """Generate a single synthetic case and write it to ``case_dir``.

    Parameters
    ----------
    case_dir           : target directory (will be created)
    time_grid          : uniform time grid [s]
    geometry/material/bc/initial_condition : physical setup
    sensor_positions   : list of sensor x-coordinates [m]
    flux_family        : name of flux family (e.g. 'step')
    flux_params        : kwargs for the flux generator
    noise_level        : std-dev of Gaussian observation noise [K]
    noise_std_in_config: noise_std written into config.yaml (may differ for
                         stress-test "wrong estimate" scenario; if None uses
                         noise_level)
    rng                : numpy Generator for reproducible noise
    """
    case_dir.mkdir(parents=True, exist_ok=True)

    N_t = len(time_grid)

    # --- 1. Build forward model ---
    model = HeatConductionFD(
        geometry=geometry,
        material=material,
        bc=bc,
        time_grid=time_grid.tolist(),
    )
    sensor_indices = model.sensor_indices_from_positions(sensor_positions)

    # --- 2. Generate true flux ---
    q_true = generate_flux(flux_family, time_grid, flux_params)

    # --- 3. Simulate clean observations ---
    T_clean = model.simulate(q_true, initial_condition, sensor_indices)
    # T_clean shape: (n_sensors, N_t)

    # --- 4. Add Gaussian noise ---
    noise = rng.normal(0.0, noise_level, size=T_clean.shape)
    T_noisy = T_clean + noise

    # --- 5. Write observations.csv (rows=time, cols=sensors) ---
    obs_path = case_dir / "observations.csv"
    n_sensors = len(sensor_positions)
    header = ",".join(f"sensor_{k+1}_K" for k in range(n_sensors))
    # T_noisy shape (n_sensors, N_t) → transpose to (N_t, n_sensors)
    np.savetxt(
        obs_path,
        T_noisy.T,
        delimiter=",",
        header=header,
        comments="",
        fmt="%.6f",
    )

    # --- 6. Write truth.npz ---
    truth_path = case_dir / "truth.npz"
    np.savez(truth_path, q_true=q_true, time_grid=time_grid)

    # --- 7. Write config.yaml ---
    _write_case_config(
        path=case_dir / "config.yaml",
        obs_path=obs_path,
        time_grid=time_grid,
        geometry=geometry,
        material=material,
        bc=bc,
        sensor_positions=sensor_positions,
        initial_condition=initial_condition,
        noise_std=noise_std_in_config if noise_std_in_config is not None else noise_level,
        flux_family=flux_family,
    )

    log.debug("Case written to %s (flux=%s, noise=%.2f K)", case_dir, flux_family, noise_level)


def _write_case_config(
    path: Path,
    obs_path: Path,
    time_grid: np.ndarray,
    geometry: Geometry,
    material: Material,
    bc: BoundaryConditions,
    sensor_positions: list[float],
    initial_condition: float,
    noise_std: float,
    flux_family: str,
) -> None:
    """Write a parser-compatible YAML config for one case."""
    config: dict = {
        "problem_type": "1D_transient_IHCP",
        "dimension": 1,
        "transient": True,
        "target_name": "boundary_heat_flux",
        "time": {
            "start": float(time_grid[0]),
            "end": float(time_grid[-1]),
            "n_steps": len(time_grid),
        },
        "geometry": {
            "length": geometry.length,
            "n_cells": geometry.n_cells,
        },
        "material": {
            "density": material.density,
            "specific_heat": material.specific_heat,
            "conductivity": material.conductivity,
        },
        "boundary_conditions": {
            "right_type": bc.right_type,
            "right_value": bc.right_value,
        },
        "sensor_positions": sensor_positions,
        "initial_condition": initial_condition,
        "noise_std": float(noise_std),
        # Use absolute path so agent can be run from any directory
        "observations_file": str(obs_path.resolve()),
        "metadata": {
            "flux_family": flux_family,
            "generated_by": "experiments/generate_cases.py",
        },
    }
    with path.open("w", encoding="utf-8") as fh:
        yaml.dump(config, fh, default_flow_style=False, allow_unicode=True)


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------

def run_generation(exp_config: dict, overwrite: bool = False) -> None:
    """Generate all cases described by ``exp_config`` and write the manifest."""
    exp = exp_config["experiment"]
    physics = exp_config["physics"]
    time_cfg = exp_config["time"]
    sensor_cfg = exp_config["sensors"]
    factors = exp_config["factors"]
    flux_params_all = exp_config.get("flux_params", {})

    cases_dir = Path(exp["cases_dir"])

    # Build base physical objects
    geometry = Geometry(
        length=float(physics["geometry"]["length"]),
        n_cells=int(physics["geometry"]["n_cells"]),
    )
    material = Material(
        density=float(physics["material"]["density"]),
        specific_heat=float(physics["material"]["specific_heat"]),
        conductivity=float(physics["material"]["conductivity"]),
    )
    bc = BoundaryConditions(
        right_type=physics["boundary_conditions"]["right_type"],
        right_value=float(physics["boundary_conditions"]["right_value"]),
    )
    initial_condition = float(physics["initial_condition"])

    base_t_start = float(time_cfg["start"])
    base_t_end = float(time_cfg["end"])
    base_n_steps = int(time_cfg["n_steps"])
    default_sensor_positions: list[float] = [
        float(x) for x in sensor_cfg["default_positions"]
    ]

    flux_families: list[str] = factors["flux_families"]
    noise_levels: list[float] = [float(n) for n in factors["noise_levels"]]
    seeds: list[int] = [int(s) for s in factors["seeds"]]
    time_resolutions: list[float] = [float(r) for r in factors.get("time_resolutions", [1.0])]
    sensor_counts: list[int] = [int(c) for c in factors.get("sensor_counts", [len(default_sensor_positions)])]

    manifest_rows: list[dict] = []
    case_counter = 0

    combinations = list(itertools.product(
        flux_families, noise_levels, time_resolutions, sensor_counts, seeds
    ))
    log.info("Generating %d cases into %s", len(combinations), cases_dir)

    for flux_family, noise_level, time_res, sensor_count, seed in combinations:
        case_counter += 1
        case_id = f"case_{case_counter:04d}"
        case_dir = cases_dir / case_id

        if case_dir.exists() and not overwrite:
            log.info("Skipping existing case %s (use --overwrite to regenerate)", case_id)
            # Still need to load manifest row; skip for simplicity — user must
            # regenerate all or none when modifying factors.
            log.warning(
                "Manifest may be incomplete if not all cases exist. "
                "Run with --overwrite to regenerate everything."
            )
            continue

        # Adapt time grid for resolution multiplier
        n_steps = max(3, int(base_n_steps * time_res))
        time_grid = build_time_grid(base_t_start, base_t_end, n_steps)

        # Adapt sensor positions for sensor count
        if sensor_count == 1:
            sensor_positions = [default_sensor_positions[0]]
        elif sensor_count >= len(default_sensor_positions):
            sensor_positions = default_sensor_positions[:]
        else:
            sensor_positions = default_sensor_positions[:sensor_count]

        # Flux parameters for this family
        fp = dict(flux_params_all.get(flux_family, {}))

        # Reproducible RNG per case
        rng = np.random.default_rng(seed)

        generate_case(
            case_dir=case_dir,
            time_grid=time_grid,
            geometry=geometry,
            material=material,
            bc=bc,
            initial_condition=initial_condition,
            sensor_positions=sensor_positions,
            flux_family=flux_family,
            flux_params=fp,
            noise_level=noise_level,
            noise_std_in_config=None,
            rng=rng,
        )

        manifest_rows.append({
            "case_id": case_id,
            "config_path": str((case_dir / "config.yaml").resolve()),
            "obs_path": str((case_dir / "observations.csv").resolve()),
            "truth_path": str((case_dir / "truth.npz").resolve()),
            "flux_family": flux_family,
            "noise_level": noise_level,
            "sensor_count": sensor_count,
            "sensor_layout": ",".join(str(s) for s in sensor_positions),
            "time_resolution": time_res,
            "seed": seed,
            "n_steps": n_steps,
        })

    if manifest_rows:
        manifest_path = cases_dir / "manifest.csv"
        manifest_df = pd.DataFrame(manifest_rows)
        manifest_df.to_csv(manifest_path, index=False)
        log.info(
            "Manifest written: %s  (%d cases)", manifest_path, len(manifest_rows)
        )
    else:
        log.warning("No new cases generated (all exist or no combinations).")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate synthetic benchmark cases for tikhonov_agent.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--config",
        default="experiments/configs/benchmark_v1.yaml",
        help="Path to experiment config YAML (default: experiments/configs/benchmark_v1.yaml)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing case directories",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity (default: INFO)",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    setup_logging(args.log_level)

    log.info("Loading experiment config: %s", args.config)
    exp_config = load_config(args.config)

    run_generation(exp_config, overwrite=args.overwrite)
    log.info("Case generation complete.")


if __name__ == "__main__":
    main()
