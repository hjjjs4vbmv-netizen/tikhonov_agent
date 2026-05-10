"""
plot_benchmark_2d_v1.py
=======================
Visualisation for the 2D IHCP benchmark (benchmark_2d_v1).

Figures produced
----------------
1.  rmse_vs_noise_by_sensor_config.png
        RMSE vs noise level (σ), one line per sensor configuration.
        Reveals how data quality interacts with observability.

2.  rmse_vs_sensor_config_by_noise.png
        RMSE vs sensor configuration, one line per noise level.
        Shows the benefit of adding sensors as a function of noise.

3.  qualitative_reconstruction.png
        True vs predicted flux for one representative case per target_type.
        Uses the medium/0.1K/seed=0 case as the canonical example.

Usage
-----
    cd tikhonov_agent
    python scripts/plot_benchmark_2d_v1.py

    # Explicit input path
    python scripts/plot_benchmark_2d_v1.py \\
        --input  reports/benchmark_2d_v1_results.csv \\
        --output reports/figures/

    # Also save PDF
    python scripts/plot_benchmark_2d_v1.py --pdf
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")   # non-interactive backend

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.forward.heat2d_simulator import (   # noqa: E402
    DEFAULT_LX, DEFAULT_LY, DEFAULT_T_TOTAL, DEFAULT_Q_MAX,
    HeatConduction2DFD, generate_flux_2d,
    generate_sensor_grid,
)
from src.deepxde_solver_2d import solve_2d  # noqa: E402

log = logging.getLogger("plot_benchmark_2d_v1")

# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------

_SENSOR_STYLES = {
    "sparse":  {"color": "#4e79a7", "marker": "o", "label": "sparse (2×2)"},
    "medium":  {"color": "#f28e2b", "marker": "s", "label": "medium (3×3)"},
    "dense":   {"color": "#e15759", "marker": "^", "label": "dense (4×4)"},
}

_NOISE_STYLES = {
    0.1: {"color": "#59a14f", "linestyle": "-",  "label": "σ = 0.1 K"},
    0.5: {"color": "#f28e2b", "linestyle": "--", "label": "σ = 0.5 K"},
    1.0: {"color": "#e15759", "linestyle": ":",  "label": "σ = 1.0 K"},
}

_TARGET_LABELS = {
    "smooth":     "Smooth (sinusoidal)",
    "localized":  "Localized (Gaussian pulse)",
    "multi_spot": "Multi-spot (3 peaks)",
}

_DPI = 150


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _save(fig: plt.Figure, path: Path, pdf: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=_DPI, bbox_inches="tight")
    log.info("Saved: %s", path)
    if pdf:
        pdf_path = path.with_suffix(".pdf")
        fig.savefig(pdf_path, bbox_inches="tight")
        log.info("Saved: %s", pdf_path)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 1 — RMSE vs noise (per sensor_config)
# ---------------------------------------------------------------------------

def plot_rmse_vs_noise(df: pd.DataFrame, output_dir: Path, pdf: bool) -> None:
    """Mean RMSE ± std vs noise level, one line per sensor configuration."""
    sensor_configs = ["sparse", "medium", "dense"]
    noise_levels   = sorted(df["noise"].dropna().unique())

    fig, ax = plt.subplots(figsize=(7, 4.5))

    for sc in sensor_configs:
        style  = _SENSOR_STYLES[sc]
        means, stds = [], []
        for nl in noise_levels:
            vals = df.loc[
                (df["sensor_config"] == sc) & (df["noise"] == nl),
                "rmse",
            ].dropna()
            means.append(vals.mean() if len(vals) > 0 else np.nan)
            stds.append(vals.std()  if len(vals) > 0 else np.nan)

        m = np.array(means, dtype=float)
        s = np.array(stds,  dtype=float)
        ax.plot(noise_levels, m,
                color=style["color"], marker=style["marker"],
                linewidth=1.8, markersize=7, label=style["label"])
        ax.fill_between(noise_levels,
                         np.maximum(0, m - s), m + s,
                         color=style["color"], alpha=0.15)

    ax.set_xlabel("Noise level σ [K]", fontsize=11)
    ax.set_ylabel("Flux RMSE [W/m²]", fontsize=11)
    ax.set_title("RMSE vs Noise Level (averaged over target types and seeds)",
                 fontsize=11)
    ax.legend(fontsize=10)
    ax.tick_params(labelsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    _save(fig, output_dir / "rmse_vs_noise_by_sensor_config.png", pdf)


# ---------------------------------------------------------------------------
# Figure 2 — RMSE vs sensor_config (per noise level)
# ---------------------------------------------------------------------------

def plot_rmse_vs_sensor_config(
    df: pd.DataFrame, output_dir: Path, pdf: bool
) -> None:
    """Mean RMSE vs sensor configuration, one line per noise level."""
    sensor_configs = ["sparse", "medium", "dense"]
    noise_levels   = sorted(df["noise"].dropna().unique())

    x = np.arange(len(sensor_configs))
    fig, ax = plt.subplots(figsize=(7, 4.5))

    for nl in noise_levels:
        style  = _NOISE_STYLES.get(nl, {"color": "gray", "linestyle": "-",
                                        "label": f"σ={nl} K"})
        means = []
        for sc in sensor_configs:
            vals = df.loc[
                (df["sensor_config"] == sc) & (df["noise"] == nl),
                "rmse",
            ].dropna()
            means.append(vals.mean() if len(vals) > 0 else np.nan)

        ax.plot(x, means,
                color=style["color"], linestyle=style["linestyle"],
                marker="o", linewidth=1.8, markersize=7, label=style["label"])

    ax.set_xticks(x)
    ax.set_xticklabels(
        [_SENSOR_STYLES[sc]["label"] for sc in sensor_configs],
        fontsize=10,
    )
    ax.set_ylabel("Flux RMSE [W/m²]", fontsize=11)
    ax.set_title("RMSE vs Sensor Configuration (averaged over target types and seeds)",
                 fontsize=11)
    ax.legend(fontsize=10)
    ax.tick_params(labelsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    _save(fig, output_dir / "rmse_vs_sensor_config_by_noise.png", pdf)


# ---------------------------------------------------------------------------
# Figure 3 — Qualitative reconstruction (one per target_type)
# ---------------------------------------------------------------------------

def plot_qualitative_reconstruction(
    output_dir: Path,
    pdf: bool,
    noise: float = 0.1,
    sensor_config: str = "medium",
    seed: int = 0,
) -> None:
    """Re-run one case per target type and visualise the q(y, t) reconstruction.

    Shows ground truth and predicted flux as 2D heat maps side by side.
    """
    from src.scripts_config_2d import (   # graceful fallback below
        NY_Q, NT_Q, OBS_EVERY, LAM, N_ITER, LR,
    )

    target_types = ["smooth", "localized", "multi_spot"]
    n_col = len(target_types)

    fig, axes = plt.subplots(
        2, n_col,
        figsize=(4 * n_col, 7),
        squeeze=False,
    )

    rng = np.random.default_rng(seed)
    simulator = HeatConduction2DFD()
    sensor_positions = generate_sensor_grid(sensor_config)

    y_q_grid = np.linspace(0.0, DEFAULT_LY,    NY_Q)
    t_q_grid = np.linspace(0.0, DEFAULT_T_TOTAL, NT_Q)

    for col_idx, target_type in enumerate(target_types):
        # Ground truth on coarse grid
        q_true = generate_flux_2d(
            target_type=target_type,
            y_grid=y_q_grid, t_grid=t_q_grid,
        )

        # True flux on fine y-grid for forward run
        y_fine  = simulator.y_centers
        t_fine  = np.linspace(0.0, DEFAULT_T_TOTAL, NT_Q)
        q_fine  = generate_flux_2d(
            target_type=target_type,
            y_grid=y_fine, t_grid=t_fine,
        )

        # Forward simulation
        T_clean, _ = simulator.simulate(
            q_flux_2d=q_fine, T0=300.0,
            sensor_positions=sensor_positions,
            t_end=DEFAULT_T_TOTAL, obs_every=OBS_EVERY,
        )
        noise_arr = rng.normal(0.0, noise, size=T_clean.shape)
        T_noisy   = T_clean + noise_arr

        # Inversion
        try:
            result = solve_2d({
                "simulator":       simulator,
                "sensor_positions": sensor_positions,
                "T_obs_noisy":     T_noisy,
                "obs_every":       OBS_EVERY,
                "t_end":           DEFAULT_T_TOTAL,
                "ny_q": NY_Q, "nt_q": NT_Q,
                "T0": 300.0,
                "lam": LAM, "n_iter": N_ITER, "lr": LR,
                "reg_order": 1,
            })
            q_pred = result["flux_pred"]
        except Exception as exc:
            log.warning("Reconstruction failed for %s: %s", target_type, exc)
            q_pred = np.zeros_like(q_true)

        # Shared colour scale per column
        vmin = min(q_true.min(), q_pred.min())
        vmax = max(q_true.max(), q_pred.max())
        extent = [t_q_grid[0], t_q_grid[-1], y_q_grid[0] * 100, y_q_grid[-1] * 100]

        # Row 0: ground truth
        ax_true = axes[0, col_idx]
        im = ax_true.imshow(
            q_true, origin="lower", aspect="auto",
            extent=extent, vmin=vmin, vmax=vmax, cmap="RdYlBu_r",
        )
        ax_true.set_title(_TARGET_LABELS[target_type], fontsize=10)
        ax_true.set_ylabel("y [cm]", fontsize=9)
        ax_true.set_xlabel("t [s]",  fontsize=9)
        ax_true.tick_params(labelsize=8)
        if col_idx == n_col - 1:
            fig.colorbar(im, ax=ax_true, label="q [W/m²]", fraction=0.046)

        # Row 1: prediction
        ax_pred = axes[1, col_idx]
        im2 = ax_pred.imshow(
            q_pred, origin="lower", aspect="auto",
            extent=extent, vmin=vmin, vmax=vmax, cmap="RdYlBu_r",
        )
        ax_pred.set_ylabel("y [cm]", fontsize=9)
        ax_pred.set_xlabel("t [s]",  fontsize=9)
        ax_pred.tick_params(labelsize=8)
        rmse = np.sqrt(np.mean((q_pred - q_true) ** 2))
        ax_pred.set_title(f"Predicted  (RMSE = {rmse:.2f} W/m²)", fontsize=9)
        if col_idx == n_col - 1:
            fig.colorbar(im2, ax=ax_pred, label="q [W/m²]", fraction=0.046)

    axes[0, 0].annotate("Ground truth", xy=(-0.18, 0.5),
                         xycoords="axes fraction",
                         fontsize=10, rotation=90, va="center")
    axes[1, 0].annotate("Predicted",    xy=(-0.18, 0.5),
                         xycoords="axes fraction",
                         fontsize=10, rotation=90, va="center")

    fig.suptitle(
        f"Flux Reconstruction  |  σ={noise} K  |  {sensor_config} sensors  |  seed={seed}",
        fontsize=11, y=1.01,
    )
    fig.tight_layout()
    _save(fig, output_dir / "qualitative_reconstruction.png", pdf)


# ---------------------------------------------------------------------------
# Config import fallback for plot_qualitative_reconstruction
# ---------------------------------------------------------------------------

def _inject_scripts_config() -> None:
    """Make NY_Q, NT_Q, etc. available as src.scripts_config_2d."""
    import types
    mod = types.ModuleType("src.scripts_config_2d")
    mod.NY_Q      = 10
    mod.NT_Q      = 20
    mod.OBS_EVERY = 5
    mod.LAM       = 1e-4
    mod.N_ITER    = 500
    mod.LR        = 10.0
    sys.modules["src.scripts_config_2d"] = mod


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------

def run_plots(
    raw_csv: Path,
    output_dir: Path,
    pdf: bool,
    skip_qualitative: bool = False,
) -> None:
    """Load benchmark CSV and generate all figures."""
    if not raw_csv.exists():
        raise FileNotFoundError(f"Results CSV not found: {raw_csv}")

    df = pd.read_csv(raw_csv)
    df["rmse"]  = pd.to_numeric(df["rmse"], errors="coerce")
    df["noise"] = pd.to_numeric(df["noise"], errors="coerce")
    log.info("Loaded %d rows from %s", len(df), raw_csv)

    output_dir.mkdir(parents=True, exist_ok=True)

    plot_rmse_vs_noise(df, output_dir, pdf)
    plot_rmse_vs_sensor_config(df, output_dir, pdf)

    if not skip_qualitative:
        _inject_scripts_config()
        try:
            plot_qualitative_reconstruction(output_dir, pdf)
        except Exception as exc:
            log.warning("Qualitative reconstruction plot failed: %s", exc)

    log.info("All figures written to %s", output_dir)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate figures for benchmark_2d_v1.",
    )
    parser.add_argument(
        "--input",
        default="reports/benchmark_2d_v1_results.csv",
        metavar="CSV",
    )
    parser.add_argument(
        "--output",
        default="reports/figures",
        metavar="DIR",
        help="Output directory for figures",
    )
    parser.add_argument(
        "--pdf", action="store_true",
        help="Also save PDF copies",
    )
    parser.add_argument(
        "--skip-qualitative", action="store_true",
        help="Skip the qualitative reconstruction plot (faster)",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout,
        force=True,
    )

    raw_csv    = Path(args.input)
    output_dir = Path(args.output)

    if not raw_csv.is_absolute():
        raw_csv = _PROJECT_ROOT / raw_csv
    if not output_dir.is_absolute():
        output_dir = _PROJECT_ROOT / output_dir

    run_plots(raw_csv, output_dir, args.pdf, args.skip_qualitative)


if __name__ == "__main__":
    main()
