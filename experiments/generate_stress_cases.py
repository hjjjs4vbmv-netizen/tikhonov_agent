"""
generate_stress_cases.py
========================
Generate synthetic cases for the stress_v1 experiment.

stress_v1.yaml uses a ``stress_scenarios`` layout instead of the ``factors``
grid used by benchmark/ablation configs.  Each scenario stresses one problem
dimension at a time; cases are tagged with the scenario name.

Output layout
-------------
  experiments/cases/stress_v1/
    manifest.csv
    <scenario_name>_case_<NNNN>/
      config.yaml
      observations.csv
      truth.npz

Usage
-----
    python experiments/generate_stress_cases.py \\
        --config experiments/configs/stress_v1.yaml \\
        [--overwrite]
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from experiments.generate_cases import generate_case  # noqa: E402
from experiments.utils import (  # noqa: E402
    build_time_grid,
    load_config,
    setup_logging,
)
from src.types import BoundaryConditions, Geometry, Material  # noqa: E402

log = logging.getLogger("generate_stress_cases")


def run_stress_generation(exp_config: dict, overwrite: bool = False) -> None:
    """Generate all stress scenario cases and write the manifest."""
    exp = exp_config["experiment"]
    physics = exp_config["physics"]
    time_cfg = exp_config["time"]
    sensor_cfg = exp_config["sensors"]
    scenarios = exp_config["stress_scenarios"]
    flux_params_all = exp_config.get("flux_params", {})

    cases_dir = Path(exp["cases_dir"])
    cases_dir.mkdir(parents=True, exist_ok=True)

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

    manifest_rows: list[dict] = []
    case_counter = 0

    for scenario_name, scenario_cfg in scenarios.items():
        flux_families: list[str] = scenario_cfg.get("flux_families", ["step"])
        noise_levels: list[float] = [float(n) for n in scenario_cfg.get("noise_levels", [0.5])]
        seeds: list[int] = [int(s) for s in scenario_cfg.get("seeds", [42])]
        sensor_positions: list[float] = [float(x) for x in scenario_cfg.get(
            "sensor_positions", sensor_cfg["default_positions"]
        )]
        n_steps: int = int(scenario_cfg.get("n_steps", base_n_steps))
        reported_noise_std: float | None = scenario_cfg.get("reported_noise_std")
        num_parameters_override: int | None = scenario_cfg.get("num_parameters_override")

        for flux_family in flux_families:
            for noise_level in noise_levels:
                for seed in seeds:
                    case_counter += 1
                    case_id = f"{scenario_name}_case_{case_counter:04d}"
                    case_dir = cases_dir / case_id

                    if case_dir.exists() and not overwrite:
                        log.info("Skipping existing case %s", case_id)
                        # Re-add to manifest
                        manifest_rows.append({
                            "case_id": case_id,
                            "scenario": scenario_name,
                            "config_path": str((case_dir / "config.yaml").resolve()),
                            "obs_path": str((case_dir / "observations.csv").resolve()),
                            "truth_path": str((case_dir / "truth.npz").resolve()),
                            "flux_family": flux_family,
                            "noise_level": noise_level,
                            "sensor_count": len(sensor_positions),
                            "sensor_layout": ",".join(str(s) for s in sensor_positions),
                            "time_resolution": n_steps / base_n_steps,
                            "seed": seed,
                            "n_steps": n_steps,
                            "reported_noise_std": reported_noise_std if reported_noise_std is not None else noise_level,
                            "num_parameters_override": num_parameters_override,
                        })
                        continue

                    time_grid = build_time_grid(base_t_start, base_t_end, n_steps)
                    fp = dict(flux_params_all.get(flux_family, {}))
                    rng = np.random.default_rng(seed)

                    # noise_std written into config may differ from true noise
                    noise_std_in_config = (
                        float(reported_noise_std)
                        if reported_noise_std is not None
                        else None
                    )

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
                        noise_std_in_config=noise_std_in_config,
                        rng=rng,
                    )

                    manifest_rows.append({
                        "case_id": case_id,
                        "scenario": scenario_name,
                        "config_path": str((case_dir / "config.yaml").resolve()),
                        "obs_path": str((case_dir / "observations.csv").resolve()),
                        "truth_path": str((case_dir / "truth.npz").resolve()),
                        "flux_family": flux_family,
                        "noise_level": noise_level,
                        "sensor_count": len(sensor_positions),
                        "sensor_layout": ",".join(str(s) for s in sensor_positions),
                        "time_resolution": n_steps / base_n_steps,
                        "seed": seed,
                        "n_steps": n_steps,
                        "reported_noise_std": reported_noise_std if reported_noise_std is not None else noise_level,
                        "num_parameters_override": num_parameters_override,
                    })
                    log.info(
                        "Generated %s  (scenario=%s, family=%s, noise=%.2f, seed=%d)",
                        case_id, scenario_name, flux_family, noise_level, seed,
                    )

    if manifest_rows:
        manifest_path = cases_dir / "manifest.csv"
        manifest_df = pd.DataFrame(manifest_rows)
        manifest_df.to_csv(manifest_path, index=False)
        log.info("Manifest written: %s  (%d cases)", manifest_path, len(manifest_rows))
    else:
        log.warning("No new cases generated.")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate synthetic stress-test cases for tikhonov_agent.",
    )
    parser.add_argument(
        "--config",
        default="experiments/configs/stress_v1.yaml",
        help="Path to stress experiment config YAML",
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
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    setup_logging(args.log_level)
    log.info("Loading stress config: %s", args.config)
    exp_config = load_config(args.config)
    run_stress_generation(exp_config, overwrite=args.overwrite)
    log.info("Stress case generation complete.")


if __name__ == "__main__":
    main()
