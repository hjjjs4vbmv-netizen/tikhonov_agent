"""
run_benchmark.py
================
Run one or more solver variants across all benchmark cases and collect metrics.

Outputs
-------
  experiments/runs/<exp_name>/
    results_raw.csv          one row per (case × variant)
    case_<XXXX>/
      <variant>/
        run_outputs/         timestamped reporter output (summary.json, etc.)
        run_summary.npz      extracted arrays for plotting

Usage
-----
    # Run all variants on all cases
    python experiments/run_benchmark.py \\
        --config experiments/configs/benchmark_v1.yaml \\
        --variant all

    # Run only one variant with a case limit
    python experiments/run_benchmark.py \\
        --config experiments/configs/benchmark_v1.yaml \\
        --variant full_agent \\
        --limit 10

    # Repeat with a fixed seed (for deterministic lambda selection)
    python experiments/run_benchmark.py \\
        --config experiments/configs/benchmark_v1.yaml \\
        --seed 0 --overwrite
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
    load_manifest,
    load_truth,
    save_result_row,
    setup_logging,
)
from src.agent import IHCPAgent  # noqa: E402
from src.sensitivity import params_to_flux  # noqa: E402

log = logging.getLogger("run_benchmark")

# ---------------------------------------------------------------------------
# Run a single (case, variant) pair
# ---------------------------------------------------------------------------

def run_one(
    *,
    case_row: pd.Series,
    variant_name: str,
    variant_overrides: dict,
    run_dir: Path,
    output_csv: Path,
) -> dict | None:
    """Execute the agent on one case with one variant and return the result row.

    Parameters
    ----------
    case_row         : row from the manifest DataFrame
    variant_name     : e.g. 'full_agent'
    variant_overrides: planner overrides for this variant
    run_dir          : per-(case, variant) directory for agent outputs
    output_csv       : master results CSV path

    Returns
    -------
    dict of metric columns, or None on hard failure.
    """
    case_id: str = case_row["case_id"]
    config_path = Path(case_row["config_path"])
    truth_path = Path(case_row["truth_path"])

    log.info("[%s / %s] starting", case_id, variant_name)

    # Load ground truth
    truth = load_truth(truth_path)
    q_true: np.ndarray = truth["q_true"]
    time_grid: np.ndarray = truth["time_grid"]
    N_t = len(time_grid)

    # Prepare output directory for agent
    agent_out_dir = run_dir / "run_outputs"
    agent_out_dir.mkdir(parents=True, exist_ok=True)

    # Run the agent
    agent = IHCPAgent(output_dir=agent_out_dir)
    t0 = time.perf_counter()
    try:
        summary = agent.run(
            config_path=config_path,
            planner_overrides=variant_overrides,
        )
    except Exception as exc:
        log.error("[%s / %s] agent.run() raised: %s", case_id, variant_name, exc)
        return None
    runtime_sec = time.perf_counter() - t0

    # Expand estimated parameters to full time series
    x_est = np.array(summary.final_result.estimated_x)
    n_params = len(x_est)
    if n_params == 0:
        log.warning("[%s / %s] empty estimated_x; skipping metrics", case_id, variant_name)
        return None

    q_est_full = params_to_flux(x_est, N_t)

    # Flatten observations
    from src.parser import parse_problem  # noqa: E402 (local import for clarity)
    try:
        problem = parse_problem(config_path)
        y_obs = np.array(problem.observations).flatten()
    except Exception as exc:
        log.error("[%s / %s] parse_problem failed: %s", case_id, variant_name, exc)
        return None

    y_fit = np.array(summary.final_result.fitted_y)

    # Save arrays for plotting
    npz_path = run_dir / "run_summary.npz"
    np.savez(
        npz_path,
        q_true=q_true,
        q_est=q_est_full,
        y_obs=y_obs,
        y_fit=y_fit,
        time_grid=time_grid,
    )

    # Physical bounds from overrides (if provided)
    pb = variant_overrides.get("physical_bounds")
    physical_bounds = (float(pb[0]), float(pb[1])) if pb is not None else None

    # Build case metadata for the row
    case_meta = {
        "case_id": case_id,
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
        "[%s / %s] done | status=%s | flux_rmse=%.2e | replay_rmse=%.4f | t=%.1fs",
        case_id, variant_name,
        row["final_decision"],
        row["flux_rmse"],
        row["replay_rmse"],
        runtime_sec,
    )
    return row


# ---------------------------------------------------------------------------
# Main benchmark driver
# ---------------------------------------------------------------------------

def run_benchmark(
    exp_config: dict,
    variants: list[str],
    limit: int | None = None,
    overwrite: bool = False,
) -> None:
    """Run the full benchmark loop.

    Parameters
    ----------
    exp_config : loaded experiment config dict
    variants   : list of variant names to run (subset of exp_config["variants"])
    limit      : if set, only process this many cases (for quick smoke tests)
    overwrite  : if False, skip (case, variant) pairs that already exist in
                 results_raw.csv
    """
    exp = exp_config["experiment"]
    output_dir = Path(exp["output_dir"])
    cases_dir = Path(exp["cases_dir"])
    output_csv = output_dir / "results_raw.csv"

    output_dir.mkdir(parents=True, exist_ok=True)

    # Load manifest
    manifest = load_manifest(cases_dir)
    if limit is not None:
        manifest = manifest.head(limit)
    log.info("Cases to process: %d", len(manifest))

    # Load variant configs
    variant_cfgs: dict[str, dict] = exp_config.get("variants", {})
    for v in variants:
        if v not in variant_cfgs:
            raise ValueError(
                f"Variant '{v}' not in experiment config. "
                f"Available: {sorted(variant_cfgs)}"
            )

    # Load existing results to skip already-done pairs
    done_pairs: set[tuple[str, str]] = set()
    if not overwrite and output_csv.exists():
        existing = pd.read_csv(output_csv)
        for _, row in existing.iterrows():
            done_pairs.add((str(row["case_id"]), str(row["variant_name"])))
        log.info("Skipping %d already-completed (case, variant) pairs", len(done_pairs))

    total_runs = len(manifest) * len(variants)
    completed = 0
    failed = 0

    for _, case_row in manifest.iterrows():
        case_id = case_row["case_id"]
        for variant_name in variants:
            if (str(case_id), variant_name) in done_pairs:
                log.debug("Skipping %s / %s (already done)", case_id, variant_name)
                completed += 1
                continue

            run_dir = output_dir / str(case_id) / variant_name
            run_dir.mkdir(parents=True, exist_ok=True)

            overrides = get_variant_overrides(variant_name, variant_cfgs[variant_name])
            result = run_one(
                case_row=case_row,
                variant_name=variant_name,
                variant_overrides=overrides,
                run_dir=run_dir,
                output_csv=output_csv,
            )
            if result is None:
                failed += 1
            completed += 1
            log.info(
                "Progress: %d / %d  (failed: %d)", completed, total_runs, failed
            )

    log.info(
        "Benchmark complete. Results: %s  (total=%d, failed=%d)",
        output_csv, completed, failed
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run tikhonov_agent benchmark variants across all cases.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--config",
        default="experiments/configs/benchmark_v1.yaml",
        help="Experiment config YAML",
    )
    parser.add_argument(
        "--variant",
        default="all",
        help=(
            "Variant to run: 'all', 'fixed_solver', 'auto_solver', "
            "'solver_plus_verifier', or 'full_agent'"
        ),
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="Process at most N cases (for quick tests)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Re-run even if (case, variant) result already exists",
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

    exp_config = load_config(args.config)
    variant_cfgs: dict = exp_config.get("variants", {})

    if args.variant == "all":
        variants = sorted(variant_cfgs.keys())
    else:
        variants = [args.variant]

    log.info("Running variants: %s", variants)
    run_benchmark(exp_config, variants=variants, limit=args.limit, overwrite=args.overwrite)


if __name__ == "__main__":
    main()
