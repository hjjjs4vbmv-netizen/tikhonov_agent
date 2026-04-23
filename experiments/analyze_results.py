"""
analyze_results.py
==================
Aggregate raw benchmark results into summary tables for publication.

Input
-----
  experiments/runs/<exp_name>/results_raw.csv

Outputs (written to the same directory)
----------------------------------------
  results_summary_by_variant.csv
  results_summary_by_noise.csv
  results_summary_by_flux_family.csv
  ablation_summary.csv             (if ablation run detected)

Usage
-----
    python experiments/analyze_results.py \\
        --input experiments/runs/benchmark_v1/results_raw.csv

    # Specify output directory explicitly
    python experiments/analyze_results.py \\
        --input experiments/runs/benchmark_v1/results_raw.csv \\
        --output experiments/runs/benchmark_v1/
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from experiments.utils import setup_logging  # noqa: E402

log = logging.getLogger("analyze_results")

# Columns to aggregate (numeric metrics)
_FLUX_METRICS = [
    "flux_l2_error", "flux_relative_l2_error", "flux_rmse",
    "flux_peak_error", "flux_correlation",
]
_REPLAY_METRICS = [
    "replay_rmse", "replay_relative_error", "replay_max_abs_error",
]
_REGULARITY_METRICS = [
    "roughness_l1", "roughness_l2", "oscillation_score",
    "sign_flip_count", "physical_violation_count",
]
_AGENT_METRICS = [
    "iteration_count", "replanning_count", "runtime_sec",
    "initial_to_final_improvement", "final_lambda",
]
_RATE_METRICS = [
    "success_flag", "weak_pass_flag", "manual_review_flag", "failure_flag",
]
_ALL_NUMERIC = (
    _FLUX_METRICS + _REPLAY_METRICS + _REGULARITY_METRICS
    + _AGENT_METRICS + _RATE_METRICS
)


def _safe_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce all expected numeric columns to float, ignoring non-numeric."""
    for col in _ALL_NUMERIC:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def _agg_group(
    df: pd.DataFrame,
    group_key: str | list[str],
    metrics: list[str],
) -> pd.DataFrame:
    """Group ``df`` by ``group_key`` and compute mean ± std for ``metrics``."""
    available = [m for m in metrics if m in df.columns]
    if not available:
        log.warning("No metric columns found in dataframe for aggregation.")
        return pd.DataFrame()

    agg_fns: dict[str, list[str]] = {m: ["mean", "std", "count"] for m in available}
    grouped = df.groupby(group_key).agg(agg_fns)
    # Flatten multi-level column names
    grouped.columns = ["_".join(c).strip("_") for c in grouped.columns]
    return grouped.reset_index()


def summarize_by_variant(df: pd.DataFrame) -> pd.DataFrame:
    """Summary table grouped by variant_name."""
    all_metrics = _FLUX_METRICS + _REPLAY_METRICS + _AGENT_METRICS + _RATE_METRICS
    return _agg_group(df, "variant_name", all_metrics)


def summarize_by_noise(df: pd.DataFrame) -> pd.DataFrame:
    """Summary table grouped by (variant_name, noise_level)."""
    all_metrics = _FLUX_METRICS + _REPLAY_METRICS + _RATE_METRICS
    return _agg_group(df, ["variant_name", "noise_level"], all_metrics)


def summarize_by_flux_family(df: pd.DataFrame) -> pd.DataFrame:
    """Summary table grouped by (variant_name, flux_family)."""
    all_metrics = _FLUX_METRICS + _REPLAY_METRICS + _RATE_METRICS
    return _agg_group(df, ["variant_name", "flux_family"], all_metrics)


def compute_ablation_summary(df: pd.DataFrame) -> pd.DataFrame | None:
    """Compute ablation summary if ablation variants are present.

    Ablation variants are identified by names containing 'ablation' or
    'no_' prefixes, 'fixed_' prefixes, plus a 'full_agent_baseline' reference column.
    Returns None if no ablation variants are found.
    """
    ablation_variants = [
        v for v in df["variant_name"].unique()
        if ("ablation" in str(v)
            or str(v).startswith("no_")
            or str(v).startswith("fixed_")
            or v == "full_agent_baseline")
    ]
    if not ablation_variants:
        return None

    df_abl = df[df["variant_name"].isin(ablation_variants)].copy()
    return _agg_group(df_abl, "variant_name", _FLUX_METRICS + _REPLAY_METRICS + _RATE_METRICS)


def run_analysis(raw_csv: Path, output_dir: Path) -> None:
    """Load raw results and write all summary tables.

    Parameters
    ----------
    raw_csv    : path to results_raw.csv
    output_dir : directory where summary CSVs are written
    """
    if not raw_csv.exists():
        raise FileNotFoundError(f"Raw results not found: {raw_csv}")

    df = pd.read_csv(raw_csv)
    df = _safe_numeric(df)
    log.info("Loaded %d rows from %s", len(df), raw_csv)

    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. By variant
    tbl = summarize_by_variant(df)
    path = output_dir / "results_summary_by_variant.csv"
    tbl.to_csv(path, index=False)
    log.info("Written: %s  (%d rows)", path, len(tbl))

    # 2. By noise level
    if "noise_level" in df.columns:
        tbl = summarize_by_noise(df)
        path = output_dir / "results_summary_by_noise.csv"
        tbl.to_csv(path, index=False)
        log.info("Written: %s  (%d rows)", path, len(tbl))

    # 3. By flux family
    if "flux_family" in df.columns:
        tbl = summarize_by_flux_family(df)
        path = output_dir / "results_summary_by_flux_family.csv"
        tbl.to_csv(path, index=False)
        log.info("Written: %s  (%d rows)", path, len(tbl))

    # 4. Ablation (if applicable)
    abl = compute_ablation_summary(df)
    if abl is not None:
        path = output_dir / "ablation_summary.csv"
        abl.to_csv(path, index=False)
        log.info("Written: %s  (%d rows)", path, len(abl))

    # 5. Print quick summary to stdout
    _print_quick_summary(df)


def _print_quick_summary(df: pd.DataFrame) -> None:
    """Log a brief human-readable summary."""
    log.info("=== Quick Summary ===")
    if "variant_name" in df.columns:
        for variant, grp in df.groupby("variant_name"):
            n = len(grp)
            success_rate = grp.get("success_flag", pd.Series(dtype=float)).mean()
            rmse = grp.get("flux_rmse", pd.Series(dtype=float)).median()
            log.info(
                "  %-30s  n=%3d  success=%.1f%%  flux_rmse_median=%.2e",
                variant, n,
                100 * success_rate if not np.isnan(success_rate) else float("nan"),
                rmse if not np.isnan(rmse) else float("nan"),
            )
    log.info("=== End Summary ===")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Aggregate benchmark results into summary tables.",
    )
    parser.add_argument(
        "--input",
        required=True,
        metavar="CSV",
        help="Path to results_raw.csv",
    )
    parser.add_argument(
        "--output",
        default=None,
        metavar="DIR",
        help="Output directory (default: same directory as --input)",
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

    raw_csv = Path(args.input)
    output_dir = Path(args.output) if args.output else raw_csv.parent

    run_analysis(raw_csv, output_dir)
    log.info("Analysis complete.")


if __name__ == "__main__":
    main()
