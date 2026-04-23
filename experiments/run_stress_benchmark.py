"""
run_stress_benchmark.py
=======================
Run the stress_v1 benchmark suite.

Extends run_benchmark.py with per-case planner overrides drawn from the
stress manifest (e.g. num_parameters for the high_dimension scenario).

Usage
-----
    python experiments/run_stress_benchmark.py \\
        --config experiments/configs/stress_v1.yaml \\
        [--overwrite]
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from experiments.utils import (  # noqa: E402
    compute_all_metrics,
    get_variant_overrides,
    load_config,
    load_truth,
    save_result_row,
    setup_logging,
)
from src.agent import IHCPAgent  # noqa: E402
from src.sensitivity import params_to_flux  # noqa: E402
from src.parser import parse_problem  # noqa: E402

log = logging.getLogger("run_stress_benchmark")


def run_one_stress(
    *,
    case_row: pd.Series,
    variant_name: str,
    variant_overrides: dict,
    run_dir: Path,
    output_csv: Path,
) -> dict | None:
    """Execute the agent on one stress case."""
    case_id: str = case_row["case_id"]
    config_path = Path(case_row["config_path"])
    truth_path = Path(case_row["truth_path"])

    log.info("[%s / %s] starting", case_id, variant_name)

    truth = load_truth(truth_path)
    q_true: np.ndarray = truth["q_true"]
    time_grid: np.ndarray = truth["time_grid"]
    N_t = len(time_grid)

    agent_out_dir = run_dir / "run_outputs"
    agent_out_dir.mkdir(parents=True, exist_ok=True)

    # Merge per-case overrides (e.g. num_parameters for high_dimension)
    case_overrides = dict(variant_overrides)
    # high_dimension: num_parameters_override in manifest → pass as num_parameters
    if "num_parameters_override" in case_row and not pd.isna(case_row.get("num_parameters_override", float("nan"))):
        case_overrides["num_parameters"] = int(case_row["num_parameters_override"])

    agent = IHCPAgent(output_dir=agent_out_dir)
    t0 = time.perf_counter()
    try:
        summary = agent.run(config_path=config_path, planner_overrides=case_overrides)
    except Exception as exc:
        log.error("[%s / %s] agent.run() raised: %s", case_id, variant_name, exc)
        return None
    runtime_sec = time.perf_counter() - t0

    x_est = np.array(summary.final_result.estimated_x)
    if len(x_est) == 0:
        log.warning("[%s / %s] empty estimated_x", case_id, variant_name)
        return None

    q_est_full = params_to_flux(x_est, N_t)

    try:
        problem = parse_problem(config_path)
        y_obs = np.array(problem.observations).flatten()
    except Exception as exc:
        log.error("[%s / %s] parse_problem failed: %s", case_id, variant_name, exc)
        return None

    y_fit = np.array(summary.final_result.fitted_y)

    npz_path = run_dir / "run_summary.npz"
    np.savez(npz_path, q_true=q_true, q_est=q_est_full,
             y_obs=y_obs, y_fit=y_fit, time_grid=time_grid)

    pb = case_overrides.get("physical_bounds")
    physical_bounds = (float(pb[0]), float(pb[1])) if pb is not None else None

    case_meta = {
        "case_id": case_id,
        "scenario": str(case_row.get("scenario", "unknown")),
        "flux_family": case_row.get("flux_family", "unknown"),
        "noise_level": float(case_row.get("noise_level", 0.0)),
        "sensor_count": int(case_row.get("sensor_count", 0)),
        "sensor_layout": str(case_row.get("sensor_layout", "")),
        "time_resolution": float(case_row.get("time_resolution", 1.0)),
        "seed": int(case_row.get("seed", 0)),
    }

    row = compute_all_metrics(
        case_meta=case_meta,
        q_true=q_true,
        q_est_full=q_est_full,
        y_obs=y_obs,
        y_fit=y_fit,
        summary=summary,
        variant_name=variant_name,
        runtime_sec=runtime_sec,
        physical_bounds=physical_bounds,
        x_params=x_est,
    )

    save_result_row(row, output_csv)
    log.info(
        "[%s / %s] done | status=%s | flux_rmse=%.2e | t=%.1fs",
        case_id, variant_name, row["final_decision"], row["flux_rmse"], runtime_sec,
    )
    return row


def run_stress_benchmark(exp_config: dict, overwrite: bool = False) -> None:
    """Run the stress benchmark loop."""
    exp = exp_config["experiment"]
    output_dir = Path(exp["output_dir"])
    cases_dir = Path(exp["cases_dir"])
    output_csv = output_dir / "results_raw.csv"

    output_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = cases_dir / "manifest.csv"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}. Run generate_stress_cases.py first.")
    manifest = pd.read_csv(manifest_path)
    log.info("Cases to process: %d", len(manifest))

    variant_cfgs: dict = exp_config.get("variants", {})
    variants = sorted(variant_cfgs.keys())

    done_pairs: set[tuple[str, str]] = set()
    if not overwrite and output_csv.exists():
        existing = pd.read_csv(output_csv)
        for _, row in existing.iterrows():
            done_pairs.add((str(row["case_id"]), str(row["variant_name"])))
        log.info("Skipping %d already-completed pairs", len(done_pairs))

    total = len(manifest) * len(variants)
    completed = failed = 0

    for _, case_row in manifest.iterrows():
        case_id = case_row["case_id"]
        for variant_name in variants:
            if (str(case_id), variant_name) in done_pairs:
                completed += 1
                continue

            run_dir = output_dir / str(case_id) / variant_name
            run_dir.mkdir(parents=True, exist_ok=True)

            overrides = get_variant_overrides(variant_name, variant_cfgs[variant_name])
            result = run_one_stress(
                case_row=case_row,
                variant_name=variant_name,
                variant_overrides=overrides,
                run_dir=run_dir,
                output_csv=output_csv,
            )
            if result is None:
                failed += 1
            completed += 1
            log.info("Progress: %d / %d  (failed: %d)", completed, total, failed)

    log.info("Stress benchmark complete. Results: %s", output_csv)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run tikhonov_agent stress benchmark.")
    parser.add_argument("--config", default="experiments/configs/stress_v1.yaml")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--log-level", default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    setup_logging(args.log_level)
    exp_config = load_config(args.config)
    run_stress_benchmark(exp_config, overwrite=args.overwrite)


if __name__ == "__main__":
    main()
