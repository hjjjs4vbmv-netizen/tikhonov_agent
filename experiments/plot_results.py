"""
plot_results.py
===============
Generate publication-quality figures from benchmark results.

Figures produced
----------------
1.  qualitative_flux_reconstruction_examples.png
2.  qualitative_temperature_replay_examples.png
3.  success_failure_barplot.png
4.  flux_error_by_variant_boxplot.png
5.  replay_error_by_noise_lineplot.png
6.  replanning_action_histogram.png
7.  lambda_vs_error_scatter.png
8.  ablation_comparison_barplot.png  (only if ablation variants detected)

Usage
-----
    python experiments/plot_results.py \\
        --input experiments/runs/benchmark_v1/results_raw.csv

    # Save PDF as well
    python experiments/plot_results.py \\
        --input experiments/runs/benchmark_v1/results_raw.csv \\
        --pdf
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")          # non-interactive backend for scripts
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from experiments.utils import setup_logging  # noqa: E402

log = logging.getLogger("plot_results")

# ---------------------------------------------------------------------------
# Style constants
# ---------------------------------------------------------------------------

_VARIANT_ORDER = ["fixed_solver", "auto_solver", "solver_plus_verifier", "full_agent"]
_VARIANT_COLORS = {
    "fixed_solver": "#4e79a7",
    "auto_solver": "#f28e2b",
    "solver_plus_verifier": "#59a14f",
    "full_agent": "#e15759",
}
_FIGSIZE_WIDE = (10, 4)
_FIGSIZE_SQUARE = (6, 5)
_DPI = 150


def _save(fig: plt.Figure, path: Path, pdf: bool) -> None:
    """Save figure as PNG and optionally as PDF."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=_DPI, bbox_inches="tight")
    log.info("Saved: %s", path)
    if pdf:
        pdf_path = path.with_suffix(".pdf")
        fig.savefig(pdf_path, bbox_inches="tight")
        log.info("Saved: %s", pdf_path)
    plt.close(fig)


def _ordered_variants(variants: list[str]) -> list[str]:
    """Return variants in canonical order; unknowns appended alphabetically."""
    known = [v for v in _VARIANT_ORDER if v in variants]
    extra = sorted(v for v in variants if v not in _VARIANT_ORDER)
    return known + extra


# ---------------------------------------------------------------------------
# Figure 1: Qualitative flux reconstruction examples
# ---------------------------------------------------------------------------

def plot_flux_reconstruction_examples(
    df: pd.DataFrame,
    run_dir: Path,
    output_dir: Path,
    pdf: bool = False,
    n_examples: int = 4,
) -> None:
    """Plot true vs estimated flux for representative cases.

    Picks one case per flux_family × 'full_agent' (or first available variant).
    """
    families = df["flux_family"].dropna().unique() if "flux_family" in df.columns else []
    if len(families) == 0:
        log.warning("No flux_family column; skipping flux reconstruction plot.")
        return

    fig, axes = plt.subplots(
        1, min(len(families), n_examples),
        figsize=(4 * min(len(families), n_examples), 3.5),
        squeeze=False,
    )
    axes = axes[0]

    for ax, family in zip(axes, list(families)[:n_examples]):
        # Pick one case from this family (prefer full_agent)
        sub = df[df["flux_family"] == family]
        if "variant_name" in sub.columns:
            fa = sub[sub["variant_name"] == "full_agent"]
            row = fa.iloc[0] if len(fa) > 0 else sub.iloc[0]
        else:
            row = sub.iloc[0]

        npz_path = (
            run_dir / str(row["case_id"])
            / str(row.get("variant_name", "full_agent"))
            / "run_summary.npz"
        )
        if not npz_path.exists():
            ax.set_title(f"{family}\n(no data)")
            continue

        data = np.load(npz_path)
        tg = data["time_grid"]
        ax.plot(tg, data["q_true"], "k-", lw=1.5, label="truth")
        ax.plot(tg, data["q_est"], "--", lw=1.5,
                color=_VARIANT_COLORS.get(str(row.get("variant_name", "")), "#888"),
                label="estimate")
        ax.set_title(family, fontsize=9)
        ax.set_xlabel("t [s]", fontsize=8)
        ax.set_ylabel("q [W/m²]", fontsize=8)
        ax.tick_params(labelsize=7)
        ax.legend(fontsize=7)

    fig.suptitle("Flux Reconstruction Examples (full_agent)", fontsize=10)
    fig.tight_layout()
    _save(fig, output_dir / "qualitative_flux_reconstruction_examples.png", pdf)


# ---------------------------------------------------------------------------
# Figure 2: Qualitative temperature replay examples
# ---------------------------------------------------------------------------

def plot_temperature_replay_examples(
    df: pd.DataFrame,
    run_dir: Path,
    output_dir: Path,
    pdf: bool = False,
    n_examples: int = 3,
) -> None:
    """Plot observed vs fitted temperatures for a few representative cases."""
    sub = df.copy()
    if "variant_name" in sub.columns:
        sub = sub[sub["variant_name"] == "full_agent"]
    if len(sub) == 0:
        sub = df.copy()

    n = min(n_examples, len(sub))
    if n == 0:
        log.warning("No rows available for temperature replay plot.")
        return

    fig, axes = plt.subplots(1, n, figsize=(4 * n, 3.5), squeeze=False)
    axes = axes[0]

    for ax, (_, row) in zip(axes, sub.head(n).iterrows()):
        variant = str(row.get("variant_name", "full_agent"))
        npz_path = run_dir / str(row["case_id"]) / variant / "run_summary.npz"
        if not npz_path.exists():
            ax.set_title("no data")
            continue

        data = np.load(npz_path)
        tg = data["time_grid"]
        y_obs = data["y_obs"]
        y_fit = data["y_fit"]
        n_t = len(tg)

        # Determine number of sensors
        n_sensors = len(y_obs) // n_t
        for k in range(n_sensors):
            obs_k = y_obs[k * n_t:(k + 1) * n_t]
            fit_k = y_fit[k * n_t:(k + 1) * n_t]
            ax.plot(tg, obs_k, ".", ms=2, alpha=0.5,
                    color=f"C{k}", label=f"obs s{k+1}")
            ax.plot(tg, fit_k, "-", lw=1.2,
                    color=f"C{k}", label=f"fit s{k+1}")

        title = f"{row.get('case_id', '')} ({row.get('flux_family', '')})"
        ax.set_title(title, fontsize=8)
        ax.set_xlabel("t [s]", fontsize=8)
        ax.set_ylabel("T [K]", fontsize=8)
        ax.tick_params(labelsize=7)
        ax.legend(fontsize=6, ncol=2)

    fig.suptitle("Temperature Replay Examples", fontsize=10)
    fig.tight_layout()
    _save(fig, output_dir / "qualitative_temperature_replay_examples.png", pdf)


# ---------------------------------------------------------------------------
# Figure 3: Success / failure bar plot
# ---------------------------------------------------------------------------

def plot_success_failure_barplot(
    df: pd.DataFrame,
    output_dir: Path,
    pdf: bool = False,
) -> None:
    """Stacked bar chart: pass / weak_pass / manual_review / fail rates per variant."""
    if "final_decision" not in df.columns or "variant_name" not in df.columns:
        log.warning("Missing columns for success/failure barplot.")
        return

    variants = _ordered_variants(list(df["variant_name"].unique()))
    decision_labels = ["pass", "weak_pass", "manual_review", "fail"]
    colors = ["#2ca02c", "#98df8a", "#ffbb78", "#d62728"]

    data_matrix = np.zeros((len(variants), len(decision_labels)))
    for i, v in enumerate(variants):
        sub = df[df["variant_name"] == v]
        total = max(len(sub), 1)
        for j, dec in enumerate(decision_labels):
            data_matrix[i, j] = (sub["final_decision"] == dec).sum() / total * 100

    fig, ax = plt.subplots(figsize=_FIGSIZE_WIDE)
    x = np.arange(len(variants))
    bottom = np.zeros(len(variants))
    for j, (label, color) in enumerate(zip(decision_labels, colors)):
        ax.bar(x, data_matrix[:, j], bottom=bottom, label=label,
               color=color, edgecolor="white", linewidth=0.5)
        bottom += data_matrix[:, j]

    ax.set_xticks(x)
    ax.set_xticklabels(variants, rotation=20, ha="right", fontsize=9)
    ax.set_ylabel("Percentage of cases [%]", fontsize=9)
    ax.set_title("Success / Failure Rates by Variant", fontsize=10)
    ax.legend(loc="upper right", fontsize=8)
    ax.set_ylim(0, 105)
    fig.tight_layout()
    _save(fig, output_dir / "success_failure_barplot.png", pdf)


# ---------------------------------------------------------------------------
# Figure 4: Flux error boxplot by variant
# ---------------------------------------------------------------------------

def plot_flux_error_by_variant_boxplot(
    df: pd.DataFrame,
    output_dir: Path,
    pdf: bool = False,
    metric: str = "flux_rmse",
) -> None:
    """Boxplot of flux reconstruction RMSE grouped by variant."""
    if metric not in df.columns or "variant_name" not in df.columns:
        log.warning("Missing columns for flux error boxplot.")
        return

    variants = _ordered_variants(list(df["variant_name"].unique()))
    data_groups = [df.loc[df["variant_name"] == v, metric].dropna().values
                   for v in variants]

    fig, ax = plt.subplots(figsize=_FIGSIZE_WIDE)
    bp = ax.boxplot(
        data_groups,
        patch_artist=True,
        notch=False,
        medianprops={"color": "black", "linewidth": 1.5},
    )
    for patch, variant in zip(bp["boxes"], variants):
        patch.set_facecolor(_VARIANT_COLORS.get(variant, "#cccccc"))
        patch.set_alpha(0.8)

    ax.set_xticks(range(1, len(variants) + 1))
    ax.set_xticklabels(variants, rotation=20, ha="right", fontsize=9)
    ax.set_ylabel(metric, fontsize=9)
    ax.set_title(f"Flux Reconstruction Error ({metric}) by Variant", fontsize=10)
    ax.set_yscale("log")
    fig.tight_layout()
    _save(fig, output_dir / "flux_error_by_variant_boxplot.png", pdf)


# ---------------------------------------------------------------------------
# Figure 5: Replay error vs noise level (line plot)
# ---------------------------------------------------------------------------

def plot_replay_error_by_noise_lineplot(
    df: pd.DataFrame,
    output_dir: Path,
    pdf: bool = False,
) -> None:
    """Mean replay RMSE vs noise level, one line per variant."""
    needed = {"variant_name", "noise_level", "replay_rmse"}
    if not needed.issubset(df.columns):
        log.warning("Missing columns for replay error lineplot.")
        return

    variants = _ordered_variants(list(df["variant_name"].unique()))
    noise_levels = sorted(df["noise_level"].dropna().unique())

    fig, ax = plt.subplots(figsize=_FIGSIZE_WIDE)
    for variant in variants:
        sub = df[df["variant_name"] == variant]
        means = []
        stds = []
        for nl in noise_levels:
            vals = sub.loc[sub["noise_level"] == nl, "replay_rmse"].dropna()
            means.append(vals.mean() if len(vals) > 0 else float("nan"))
            stds.append(vals.std() if len(vals) > 0 else float("nan"))

        means_arr = np.array(means, dtype=float)
        stds_arr = np.array(stds, dtype=float)
        color = _VARIANT_COLORS.get(variant, None)
        ax.plot(noise_levels, means_arr, "o-", label=variant, color=color, lw=1.5, ms=5)
        ax.fill_between(
            noise_levels,
            np.maximum(0, means_arr - stds_arr),
            means_arr + stds_arr,
            alpha=0.15, color=color,
        )

    ax.set_xlabel("Noise level [K]", fontsize=9)
    ax.set_ylabel("Mean replay RMSE [K]", fontsize=9)
    ax.set_title("Replay Error vs Noise Level", fontsize=10)
    ax.legend(fontsize=8)
    fig.tight_layout()
    _save(fig, output_dir / "replay_error_by_noise_lineplot.png", pdf)


# ---------------------------------------------------------------------------
# Figure 6: Replanning action histogram
# ---------------------------------------------------------------------------

def plot_replanning_action_histogram(
    df: pd.DataFrame,
    run_dir: Path,
    output_dir: Path,
    pdf: bool = False,
) -> None:
    """Bar chart of replanning action frequencies (from trace JSONs).

    Falls back to 'replanning_count' from the CSV if trace JSONs are not found.
    """
    if "replanning_count" not in df.columns or "variant_name" not in df.columns:
        log.warning("Missing columns for replanning histogram.")
        return

    variants = _ordered_variants(list(df["variant_name"].unique()))
    mean_replanning = [
        df.loc[df["variant_name"] == v, "replanning_count"].mean()
        for v in variants
    ]

    fig, ax = plt.subplots(figsize=_FIGSIZE_WIDE)
    x = np.arange(len(variants))
    colors = [_VARIANT_COLORS.get(v, "#cccccc") for v in variants]
    ax.bar(x, mean_replanning, color=colors, edgecolor="white", linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(variants, rotation=20, ha="right", fontsize=9)
    ax.set_ylabel("Mean replanning count per case", fontsize=9)
    ax.set_title("Replanning Actions by Variant", fontsize=10)
    fig.tight_layout()
    _save(fig, output_dir / "replanning_action_histogram.png", pdf)


# ---------------------------------------------------------------------------
# Figure 7: Lambda vs flux error scatter
# ---------------------------------------------------------------------------

def plot_lambda_vs_error_scatter(
    df: pd.DataFrame,
    output_dir: Path,
    pdf: bool = False,
) -> None:
    """Scatter: final lambda vs flux_rmse, coloured by variant."""
    needed = {"final_lambda", "flux_rmse", "variant_name"}
    if not needed.issubset(df.columns):
        log.warning("Missing columns for lambda vs error scatter.")
        return

    variants = _ordered_variants(list(df["variant_name"].unique()))
    fig, ax = plt.subplots(figsize=_FIGSIZE_WIDE)

    for variant in variants:
        sub = df[(df["variant_name"] == variant) &
                 df["final_lambda"].notna() &
                 df["flux_rmse"].notna()]
        if len(sub) == 0:
            continue
        ax.scatter(
            sub["final_lambda"], sub["flux_rmse"],
            label=variant, alpha=0.6, s=20,
            color=_VARIANT_COLORS.get(variant, None),
        )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Final regularization parameter λ", fontsize=9)
    ax.set_ylabel("Flux RMSE [W/m²]", fontsize=9)
    ax.set_title("λ vs Flux Reconstruction Error", fontsize=10)
    ax.legend(fontsize=8)
    fig.tight_layout()
    _save(fig, output_dir / "lambda_vs_error_scatter.png", pdf)


# ---------------------------------------------------------------------------
# Figure 8: Ablation comparison bar plot
# ---------------------------------------------------------------------------

def plot_ablation_comparison_barplot(
    df: pd.DataFrame,
    output_dir: Path,
    pdf: bool = False,
) -> None:
    """Horizontal bar plot comparing ablation variants on flux_rmse."""
    ablation_variants = [
        v for v in df["variant_name"].unique()
        if ("ablation" in str(v)
            or str(v).startswith("no_")
            or str(v).startswith("fixed_")
            or v == "full_agent_baseline")
    ]
    if not ablation_variants:
        log.debug("No ablation variants found; skipping ablation barplot.")
        return

    medians = {
        v: df.loc[df["variant_name"] == v, "flux_rmse"].median()
        for v in ablation_variants
    }
    sorted_variants = sorted(medians, key=lambda v: medians[v])
    values = [medians[v] for v in sorted_variants]

    fig, ax = plt.subplots(figsize=(7, max(3, len(sorted_variants) * 0.6)))
    y = np.arange(len(sorted_variants))
    ax.barh(y, values, color="#4e79a7", edgecolor="white")
    ax.set_yticks(y)
    ax.set_yticklabels(sorted_variants, fontsize=9)
    ax.set_xlabel("Median flux RMSE [W/m²]", fontsize=9)
    ax.set_title("Ablation Comparison (lower is better)", fontsize=10)
    ax.set_xscale("log")
    fig.tight_layout()
    _save(fig, output_dir / "ablation_comparison_barplot.png", pdf)


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------

def run_plots(raw_csv: Path, run_dir: Path, output_dir: Path, pdf: bool) -> None:
    """Load raw results and produce all figures."""
    if not raw_csv.exists():
        raise FileNotFoundError(f"Raw results not found: {raw_csv}")

    df = pd.read_csv(raw_csv)
    for col in ["flux_rmse", "replay_rmse", "final_lambda", "noise_level",
                "replanning_count", "success_flag", "failure_flag",
                "weak_pass_flag", "manual_review_flag"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    log.info("Loaded %d rows; generating plots into %s", len(df), output_dir)

    plot_flux_reconstruction_examples(df, run_dir, output_dir, pdf=pdf)
    plot_temperature_replay_examples(df, run_dir, output_dir, pdf=pdf)
    plot_success_failure_barplot(df, output_dir, pdf=pdf)
    plot_flux_error_by_variant_boxplot(df, output_dir, pdf=pdf)
    plot_replay_error_by_noise_lineplot(df, output_dir, pdf=pdf)
    plot_replanning_action_histogram(df, run_dir, output_dir, pdf=pdf)
    plot_lambda_vs_error_scatter(df, output_dir, pdf=pdf)
    plot_ablation_comparison_barplot(df, output_dir, pdf=pdf)

    log.info("All figures written.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate publication figures from benchmark results.",
    )
    parser.add_argument(
        "--input",
        required=True,
        metavar="CSV",
        help="Path to results_raw.csv",
    )
    parser.add_argument(
        "--run-dir",
        default=None,
        metavar="DIR",
        help=(
            "Base directory containing per-case run summaries "
            "(default: parent directory of --input)"
        ),
    )
    parser.add_argument(
        "--output",
        default=None,
        metavar="DIR",
        help="Directory for output figures (default: <run-dir>/figures/)",
    )
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Also save figures as PDF",
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
    run_dir = Path(args.run_dir) if args.run_dir else raw_csv.parent
    output_dir = Path(args.output) if args.output else run_dir / "figures"

    run_plots(raw_csv, run_dir, output_dir, pdf=args.pdf)
    log.info("Plotting complete.")


if __name__ == "__main__":
    main()
