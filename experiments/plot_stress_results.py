"""
plot_stress_results.py
======================
Generate figures specific to the stress_v1 experiment.

Produces:
  1. stress_success_barplot.png  — success rate per scenario
  2. stress_flux_rmse_boxplot.png — flux RMSE distribution per scenario

Usage
-----
    python experiments/plot_stress_results.py \\
        --input experiments/runs/stress_v1/results_raw.csv
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from experiments.utils import setup_logging  # noqa: E402

log = logging.getLogger("plot_stress_results")

_DPI = 150
_SCENARIO_ORDER = [
    "high_noise", "few_sensors", "distant_sensors",
    "low_time_resolution", "high_dimension", "wrong_noise_estimate",
]
_SCENARIO_COLORS = {
    "high_noise": "#d62728",
    "few_sensors": "#ff7f0e",
    "distant_sensors": "#9467bd",
    "low_time_resolution": "#8c564b",
    "high_dimension": "#e377c2",
    "wrong_noise_estimate": "#17becf",
}


def _save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=_DPI, bbox_inches="tight")
    log.info("Saved: %s", path)
    plt.close(fig)


def _ordered_scenarios(scenarios: list[str]) -> list[str]:
    known = [s for s in _SCENARIO_ORDER if s in scenarios]
    extra = sorted(s for s in scenarios if s not in _SCENARIO_ORDER)
    return known + extra


def plot_stress_success_barplot(df: pd.DataFrame, output_dir: Path) -> None:
    """Grouped bar chart of success rate and flux RMSE per scenario."""
    if "scenario" not in df.columns:
        log.warning("No 'scenario' column; skipping stress success barplot.")
        return

    scenarios = _ordered_scenarios(list(df["scenario"].unique()))
    success_rates = [df.loc[df["scenario"] == s, "success_flag"].mean() * 100
                     for s in scenarios]

    fig, ax = plt.subplots(figsize=(9, 4))
    x = np.arange(len(scenarios))
    colors = [_SCENARIO_COLORS.get(s, "#7f7f7f") for s in scenarios]
    bars = ax.bar(x, success_rates, color=colors, edgecolor="white", linewidth=0.5)

    # Add value labels on bars
    for bar, val in zip(bars, success_rates):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
                f"{val:.0f}%", ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels([s.replace("_", "\n") for s in scenarios], fontsize=9)
    ax.set_ylabel("Success rate [%]", fontsize=9)
    ax.set_title("stress_v1: Success Rate per Scenario (full_agent)", fontsize=10)
    ax.set_ylim(0, 115)
    ax.axhline(100, color="green", lw=1, ls="--", alpha=0.4, label="100% target")
    ax.legend(fontsize=8)
    fig.tight_layout()
    _save(fig, output_dir / "stress_success_barplot.png")


def plot_stress_flux_rmse_boxplot(df: pd.DataFrame, output_dir: Path) -> None:
    """Boxplot of flux RMSE per scenario."""
    if "scenario" not in df.columns or "flux_rmse" not in df.columns:
        log.warning("Missing columns for stress RMSE boxplot.")
        return

    scenarios = _ordered_scenarios(list(df["scenario"].unique()))
    data_groups = [df.loc[df["scenario"] == s, "flux_rmse"].dropna().values
                   for s in scenarios]

    fig, ax = plt.subplots(figsize=(9, 4))
    bp = ax.boxplot(
        data_groups,
        patch_artist=True,
        notch=False,
        medianprops={"color": "black", "linewidth": 1.5},
    )
    for patch, scenario in zip(bp["boxes"], scenarios):
        patch.set_facecolor(_SCENARIO_COLORS.get(scenario, "#cccccc"))
        patch.set_alpha(0.8)

    ax.set_xticks(range(1, len(scenarios) + 1))
    ax.set_xticklabels([s.replace("_", "\n") for s in scenarios], fontsize=9)
    ax.set_ylabel("Flux RMSE [W/m²]", fontsize=9)
    ax.set_title("stress_v1: Flux Reconstruction Error per Scenario", fontsize=10)
    ax.set_yscale("log")
    fig.tight_layout()
    _save(fig, output_dir / "stress_flux_rmse_boxplot.png")


def plot_stress_oscillation_by_scenario(df: pd.DataFrame, output_dir: Path) -> None:
    """Boxplot of oscillation_score per scenario."""
    if "scenario" not in df.columns or "oscillation_score" not in df.columns:
        log.warning("Missing columns for oscillation score plot.")
        return

    scenarios = _ordered_scenarios(list(df["scenario"].unique()))
    data_groups = [df.loc[df["scenario"] == s, "oscillation_score"].dropna().values
                   for s in scenarios]

    fig, ax = plt.subplots(figsize=(9, 4))
    bp = ax.boxplot(
        data_groups,
        patch_artist=True,
        notch=False,
        medianprops={"color": "black", "linewidth": 1.5},
    )
    for patch, scenario in zip(bp["boxes"], scenarios):
        patch.set_facecolor(_SCENARIO_COLORS.get(scenario, "#cccccc"))
        patch.set_alpha(0.8)

    ax.set_xticks(range(1, len(scenarios) + 1))
    ax.set_xticklabels([s.replace("_", "\n") for s in scenarios], fontsize=9)
    ax.set_ylabel("Oscillation score (norm. 2nd-diff energy)", fontsize=9)
    ax.set_title("stress_v1: Solution Oscillation per Scenario", fontsize=10)
    fig.tight_layout()
    _save(fig, output_dir / "stress_oscillation_score_boxplot.png")


def run_stress_plots(raw_csv: Path, output_dir: Path) -> None:
    df = pd.read_csv(raw_csv)
    for col in ["flux_rmse", "success_flag", "oscillation_score"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    log.info("Loaded %d stress rows; generating plots into %s", len(df), output_dir)
    plot_stress_success_barplot(df, output_dir)
    plot_stress_flux_rmse_boxplot(df, output_dir)
    plot_stress_oscillation_by_scenario(df, output_dir)
    log.info("Stress figures written.")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate stress_v1 figures.")
    parser.add_argument("--input", required=True, metavar="CSV",
                        help="Path to stress results_raw.csv")
    parser.add_argument("--output", default=None, metavar="DIR",
                        help="Output directory (default: <input_dir>/figures/)")
    parser.add_argument("--log-level", default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    setup_logging(args.log_level)
    raw_csv = Path(args.input)
    output_dir = Path(args.output) if args.output else raw_csv.parent / "figures"
    run_stress_plots(raw_csv, output_dir)


if __name__ == "__main__":
    main()
