"""
plot_benchmark_2d_v2.py
=======================
Visualisation for the 2D IHCP benchmark_2d_v2 (3-solver comparison).

Figures produced
----------------
Main benchmark (from benchmark_2d_v2_results.csv):
  1. rmse_vs_sensor_count.png
        RMSE vs number of sensors, one panel per noise level,
        one line per solver.  Shows how each solver scales with data density.

  2. rmse_vs_noise.png
        RMSE vs noise level, one panel per sensor_config,
        one line per solver.  Highlights TSVD instability at high noise.

  3. qualitative_reconstruction.png
        True vs predicted q(y, t) for each solver (one column per solver,
        two rows: ground truth + reconstruction).  Uses the medium/0.1K/seed=0
        case with the "smooth" target.

Layout note (from benchmark_2d_layout_note.csv):
  4. rmse_vs_layout.png
        RMSE vs sensor layout, one line per solver.

  5. layout_comparison.png
        Scatter plot of sensor positions for all three layouts, illustrating
        where the sensors are placed.

Usage
-----
    cd tikhonov_agent
    python scripts/plot_benchmark_2d_v2.py

    python scripts/plot_benchmark_2d_v2.py \\
        --main  reports/benchmark_2d_v2_results.csv \\
        --layout reports/benchmark_2d_layout_note.csv \\
        --output reports/figures_v2/

    python scripts/plot_benchmark_2d_v2.py --pdf --skip-qualitative
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

_HERE         = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

log = logging.getLogger("plot_benchmark_2d_v2")

# ---------------------------------------------------------------------------
# Style constants
# ---------------------------------------------------------------------------

_SOLVER_STYLES: dict[str, dict[str, Any]] = {
    "tikhonov_2d": {
        "color": "#4e79a7", "marker": "o", "linestyle": "-",
        "label": "Tikhonov",
    },
    "tsvd_2d": {
        "color": "#e15759", "marker": "s", "linestyle": "--",
        "label": "TSVD",
    },
    "deepxde_2d": {
        "color": "#59a14f", "marker": "^", "linestyle": "-.",
        "label": "DeepXDE (Adam)",
    },
}

_SENSOR_CONFIG_LABELS = {
    "sparse":  "sparse (4 sensors)",
    "medium":  "medium (9 sensors)",
    "dense":   "dense (16 sensors)",
}

_LAYOUT_LABELS = {
    "uniform_grid":    "Uniform grid",
    "boundary_biased": "Boundary-biased",
    "clustered":       "Clustered (centre)",
}

_LAYOUT_COLORS = {
    "uniform_grid":    "#4e79a7",
    "boundary_biased": "#f28e2b",
    "clustered":       "#e15759",
}

_DPI = 150

_SENSOR_COUNTS = {"sparse": 4, "medium": 9, "dense": 16}


# ---------------------------------------------------------------------------
# Save helper
# ---------------------------------------------------------------------------

def _save(fig: plt.Figure, path: Path, pdf: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=_DPI, bbox_inches="tight")
    log.info("Saved: %s", path)
    if pdf:
        fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 1 — RMSE vs sensor count (one panel per noise level)
# ---------------------------------------------------------------------------

def plot_rmse_vs_sensor_count(
    df: pd.DataFrame, output_dir: Path, pdf: bool,
) -> None:
    """Mean flux RMSE vs sensor count for each solver, split by noise level."""
    df = df.copy()
    df["sensor_count"] = df["sensor_config"].map(_SENSOR_COUNTS)
    noise_levels = sorted(df["noise"].dropna().unique())
    sensor_counts = sorted(df["sensor_count"].dropna().unique())

    n_panels = len(noise_levels)
    fig, axes = plt.subplots(1, n_panels, figsize=(5.5 * n_panels, 4.5),
                              sharey=True)
    if n_panels == 1:
        axes = [axes]

    for ax, nl in zip(axes, noise_levels):
        sub = df[df["noise"] == nl]
        for solver, style in _SOLVER_STYLES.items():
            vals = []
            for sc in sensor_counts:
                rows = sub.loc[
                    sub["solver_name"] == solver,
                    # --- filter by sensor_count not sensor_config key
                ].query(f"sensor_count == {sc}")["flux_rmse"].dropna()
                vals.append(rows.mean() if len(rows) > 0 else np.nan)

            ax.plot(sensor_counts, vals,
                    color=style["color"], marker=style["marker"],
                    linestyle=style["linestyle"], linewidth=1.8, markersize=7,
                    label=style["label"])

        ax.set_title(f"Noise σ = {nl} K", fontsize=11)
        ax.set_xlabel("Number of sensors", fontsize=10)
        ax.set_xticks(sensor_counts)
        ax.tick_params(labelsize=9)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        if ax is axes[0]:
            ax.set_ylabel("Flux RMSE [W/m²]", fontsize=10)

    axes[-1].legend(fontsize=10, loc="upper right")
    fig.suptitle("RMSE vs Sensor Count — Three Solvers", fontsize=12, y=1.02)
    fig.tight_layout()
    _save(fig, output_dir / "rmse_vs_sensor_count.png", pdf)


# ---------------------------------------------------------------------------
# Figure 2 — RMSE vs noise level (one panel per sensor_config)
# ---------------------------------------------------------------------------

def plot_rmse_vs_noise(
    df: pd.DataFrame, output_dir: Path, pdf: bool,
) -> None:
    """Mean flux RMSE vs noise level for each solver, split by sensor_config."""
    sensor_configs = ["sparse", "medium", "dense"]
    noise_levels   = sorted(df["noise"].dropna().unique())

    fig, axes = plt.subplots(1, len(sensor_configs), figsize=(16, 4.5),
                              sharey=False)

    for ax, sc in zip(axes, sensor_configs):
        sub = df[df["sensor_config"] == sc]
        for solver, style in _SOLVER_STYLES.items():
            vals = []
            for nl in noise_levels:
                rows = sub.loc[
                    (sub["solver_name"] == solver) & (sub["noise"] == nl),
                    "flux_rmse",
                ].dropna()
                vals.append(rows.mean() if len(rows) > 0 else np.nan)

            ax.plot(noise_levels, vals,
                    color=style["color"], marker=style["marker"],
                    linestyle=style["linestyle"], linewidth=1.8, markersize=7,
                    label=style["label"])

        ax.set_title(f"{_SENSOR_CONFIG_LABELS[sc]}", fontsize=11)
        ax.set_xlabel("Noise σ [K]", fontsize=10)
        ax.tick_params(labelsize=9)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        if ax is axes[0]:
            ax.set_ylabel("Flux RMSE [W/m²]", fontsize=10)

    axes[-1].legend(fontsize=10, loc="upper left")
    fig.suptitle("RMSE vs Noise Level — Three Solvers", fontsize=12, y=1.02)
    fig.tight_layout()
    _save(fig, output_dir / "rmse_vs_noise.png", pdf)


# ---------------------------------------------------------------------------
# Figure 3 — Qualitative reconstruction (true vs predicted per solver)
# ---------------------------------------------------------------------------

def plot_qualitative_reconstruction(
    output_dir: Path,
    pdf: bool,
    noise: float = 0.1,
    sensor_config: str = "medium",
    seed: int = 0,
    target_type: str = "smooth",
) -> None:
    """Run one inversion per solver and show q(y,t) side by side."""
    from src.forward.heat2d_simulator import (
        DEFAULT_LY, DEFAULT_T_TOTAL, DEFAULT_Q_MAX,
        HeatConduction2DFD, generate_flux_2d, generate_sensor_grid,
    )
    from src.tikhonov_solver_2d import solve_2d_tikhonov
    from src.tsvd_solver_2d import solve_2d_tsvd
    from src.deepxde_solver_2d import solve_2d

    NY_Q, NT_Q, OBS_EVERY = 10, 20, 5
    LAM_TIK, TSVD_TOL     = 1e-3, 0.01
    LAM_DXE, N_ITER, LR   = 1e-4, 500, 10.0

    simulator        = HeatConduction2DFD()
    sensor_positions = generate_sensor_grid(sensor_config)
    rng              = np.random.default_rng(seed)

    y_q_grid = np.linspace(0.0, DEFAULT_LY,     NY_Q)
    t_q_grid = np.linspace(0.0, DEFAULT_T_TOTAL, NT_Q)

    q_true = generate_flux_2d(target_type, y_grid=y_q_grid, t_grid=t_q_grid)

    # Forward run with fine q
    y_fine = simulator.y_centers
    t_fine = np.linspace(0.0, DEFAULT_T_TOTAL, NT_Q)
    q_fine = generate_flux_2d(target_type, y_grid=y_fine, t_grid=t_fine)

    T_clean, _ = simulator.simulate(
        q_flux_2d=q_fine, T0=300.0,
        sensor_positions=sensor_positions,
        t_end=DEFAULT_T_TOTAL, obs_every=OBS_EVERY,
    )
    T_noisy = T_clean + rng.normal(0.0, noise, size=T_clean.shape)

    # Build S once
    S, _, yqg, tqg = simulator.build_sensitivity_matrix(
        sensor_positions=sensor_positions,
        t_end=DEFAULT_T_TOTAL, ny_q=NY_Q, nt_q=NT_Q,
        obs_every=OBS_EVERY,
    )

    base_spec = {
        "simulator":        simulator,
        "sensor_positions": sensor_positions,
        "T_obs_noisy":      T_noisy,
        "obs_every":        OBS_EVERY,
        "t_end":            DEFAULT_T_TOTAL,
        "ny_q": NY_Q, "nt_q": NT_Q,
        "T0": 300.0,
        "q_true": q_true,
        "S": S, "y_q_grid": yqg, "t_q_grid": tqg,
    }

    solvers = [
        ("tikhonov_2d",
         lambda sp: solve_2d_tikhonov({**sp, "lam": LAM_TIK, "reg_order": 1})),
        ("tsvd_2d",
         lambda sp: solve_2d_tsvd({**sp, "tsvd_tol": TSVD_TOL})),
        ("deepxde_2d",
         lambda sp: solve_2d({**sp, "lam": LAM_DXE, "n_iter": N_ITER,
                               "lr": LR, "reg_order": 1})),
    ]

    n_solvers = len(solvers)
    fig, axes = plt.subplots(
        n_solvers + 1, 1,
        figsize=(10, 3.2 * (n_solvers + 1)),
        squeeze=True,
    )
    # Convert to 2-column layout: column 0 = truth, columns 1-3 = solvers
    # Use a grid layout instead: 2 rows × (n_solvers+1) columns
    plt.close(fig)

    fig, axes = plt.subplots(
        2, n_solvers + 1,
        figsize=(4.5 * (n_solvers + 1), 7),
        squeeze=False,
    )

    extent = [t_q_grid[0], t_q_grid[-1],
              y_q_grid[0] * 100, y_q_grid[-1] * 100]

    vmin_t = q_true.min()
    vmax_t = q_true.max()

    # Column 0: ground truth (same in both rows)
    for row in range(2):
        ax = axes[row, 0]
        im = ax.imshow(q_true, origin="lower", aspect="auto",
                       extent=extent, vmin=vmin_t, vmax=vmax_t,
                       cmap="RdYlBu_r")
        ax.set_ylabel("y [cm]", fontsize=9)
        ax.set_xlabel("t [s]",  fontsize=9)
        ax.tick_params(labelsize=8)
        if row == 0:
            ax.set_title("Ground truth", fontsize=10, fontweight="bold")
        else:
            ax.set_title("Ground truth", fontsize=10, fontweight="bold")
    fig.colorbar(im, ax=axes[:, 0], label="q [W/m²]",
                 fraction=0.04, pad=0.02, aspect=30)

    # Columns 1–3: one solver per column
    for col_idx, (solver_name, solver_fn) in enumerate(solvers):
        col = col_idx + 1
        style = _SOLVER_STYLES[solver_name]

        try:
            result = solver_fn(base_spec)
            q_pred = result["flux_pred"]
            flux_rmse = result.get("flux_rmse") or result.get("rmse")
        except Exception as exc:
            log.warning("Solver %s failed: %s", solver_name, exc)
            q_pred = np.zeros_like(q_true)
            flux_rmse = None

        vmin = min(vmin_t, q_pred.min())
        vmax = max(vmax_t, q_pred.max())

        # Row 0: truth column (already drawn), so use row 0 for predicted
        ax0 = axes[0, col]
        im0 = ax0.imshow(q_true, origin="lower", aspect="auto",
                         extent=extent, vmin=vmin, vmax=vmax, cmap="RdYlBu_r")
        ax0.set_title(f"{style['label']}\nGround truth", fontsize=10)
        ax0.set_ylabel("y [cm]", fontsize=9)
        ax0.set_xlabel("t [s]",  fontsize=9)
        ax0.tick_params(labelsize=8)

        ax1 = axes[1, col]
        im1 = ax1.imshow(q_pred, origin="lower", aspect="auto",
                         extent=extent, vmin=vmin, vmax=vmax, cmap="RdYlBu_r")
        rmse_str = f"{flux_rmse:.1f}" if flux_rmse is not None else "N/A"
        ax1.set_title(f"Predicted  (RMSE = {rmse_str} W/m²)", fontsize=9)
        ax1.set_ylabel("y [cm]", fontsize=9)
        ax1.set_xlabel("t [s]",  fontsize=9)
        ax1.tick_params(labelsize=8)
        fig.colorbar(im1, ax=axes[:, col], label="q [W/m²]",
                     fraction=0.04, pad=0.02, aspect=30)

    # Hide the duplicate column-0 bottom row (already labelled)
    fig.suptitle(
        f"Qualitative Reconstruction  |  target={target_type}  "
        f"|  σ={noise} K  |  {sensor_config} sensors  |  seed={seed}",
        fontsize=11, y=1.01,
    )
    fig.tight_layout()
    _save(fig, output_dir / "qualitative_reconstruction.png", pdf)


# ---------------------------------------------------------------------------
# Figure 4 — RMSE vs sensor layout
# ---------------------------------------------------------------------------

def plot_rmse_vs_layout(
    dl: pd.DataFrame, output_dir: Path, pdf: bool,
) -> None:
    """Mean flux RMSE vs sensor layout for each solver."""
    layouts = ["uniform_grid", "boundary_biased", "clustered"]
    x       = np.arange(len(layouts))

    fig, ax = plt.subplots(figsize=(7.5, 4.5))

    for solver, style in _SOLVER_STYLES.items():
        means, stds = [], []
        for lay in layouts:
            vals = dl.loc[
                (dl["solver_name"] == solver) & (dl["layout"] == lay),
                "flux_rmse",
            ].dropna()
            means.append(vals.mean() if len(vals) > 0 else np.nan)
            stds.append(vals.std()   if len(vals) > 0 else np.nan)

        m = np.array(means, dtype=float)
        s = np.array(stds,  dtype=float)
        ax.plot(x, m,
                color=style["color"], marker=style["marker"],
                linestyle=style["linestyle"], linewidth=1.8, markersize=8,
                label=style["label"])
        ax.fill_between(x,
                         np.maximum(0, m - s), m + s,
                         color=style["color"], alpha=0.12)

    ax.set_xticks(x)
    ax.set_xticklabels(
        [_LAYOUT_LABELS[lay] for lay in layouts], fontsize=10,
    )
    ax.set_ylabel("Flux RMSE [W/m²]", fontsize=11)
    ax.set_title("RMSE vs Sensor Layout\n(9 sensors, averaged over targets and noise levels)",
                 fontsize=11)
    ax.legend(fontsize=10)
    ax.tick_params(labelsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    _save(fig, output_dir / "rmse_vs_layout.png", pdf)


# ---------------------------------------------------------------------------
# Figure 5 — Illustrative sensor layout comparison
# ---------------------------------------------------------------------------

def plot_layout_comparison(output_dir: Path, pdf: bool) -> None:
    """Show the three sensor layouts in a 1×3 panel of scatter plots."""
    from src.forward.heat2d_simulator import DEFAULT_LX, DEFAULT_LY

    def _uniform_grid() -> list[tuple[float, float]]:
        xs = np.linspace(0.1, 0.9, 3) * DEFAULT_LX
        ys = np.linspace(0.1, 0.9, 3) * DEFAULT_LY
        return [(x, y) for x in xs for y in ys]

    def _boundary_biased() -> list[tuple[float, float]]:
        xs = np.array([0.10, 0.20, 0.35]) * DEFAULT_LX
        ys = np.linspace(0.1, 0.9, 3) * DEFAULT_LY
        return [(x, y) for x in xs for y in ys]

    def _clustered() -> list[tuple[float, float]]:
        xs = np.linspace(0.35, 0.65, 3) * DEFAULT_LX
        ys = np.linspace(0.35, 0.65, 3) * DEFAULT_LY
        return [(x, y) for x in xs for y in ys]

    layouts = {
        "uniform_grid":    _uniform_grid(),
        "boundary_biased": _boundary_biased(),
        "clustered":       _clustered(),
    }

    fig, axes = plt.subplots(1, 3, figsize=(11, 3.8))

    for ax, (name, positions) in zip(axes, layouts.items()):
        xs = [p[0] * 100 for p in positions]   # cm
        ys = [p[1] * 100 for p in positions]
        ax.scatter(xs, ys, s=80, color=_LAYOUT_COLORS[name],
                   edgecolors="k", linewidths=0.6, zorder=3)
        ax.set_xlim(-0.5, DEFAULT_LX * 100 + 0.5)
        ax.set_ylim(-0.5, DEFAULT_LY * 100 + 0.5)
        ax.set_aspect("equal")
        ax.set_xlabel("x [cm]", fontsize=10)
        ax.set_ylabel("y [cm]", fontsize=10)
        ax.set_title(_LAYOUT_LABELS[name], fontsize=11, color=_LAYOUT_COLORS[name],
                     fontweight="bold")
        ax.tick_params(labelsize=8)
        ax.grid(linestyle="--", alpha=0.35)
        # Shade the left boundary (flux boundary at x=0)
        ax.axvspan(-0.5, 0.5, color="#aaddff", alpha=0.4, zorder=1)
        ax.text(0.25, DEFAULT_LY * 100 * 0.5, "q(y,t)\nboundary",
                ha="center", va="center", fontsize=7, color="#005599",
                rotation=90)

    fig.suptitle("Sensor Layout Comparison  (9 sensors each)", fontsize=12)
    fig.tight_layout()
    _save(fig, output_dir / "layout_comparison.png", pdf)


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------

def run_plots(
    main_csv:     Path,
    layout_csv:   Path,
    output_dir:   Path,
    pdf:          bool,
    skip_qualitative: bool = False,
) -> None:
    """Load benchmark CSVs and generate all five figures."""
    if not main_csv.exists():
        raise FileNotFoundError(f"Main results CSV not found: {main_csv}")
    if not layout_csv.exists():
        raise FileNotFoundError(f"Layout note CSV not found: {layout_csv}")

    df = pd.read_csv(main_csv)
    dl = pd.read_csv(layout_csv)

    df["flux_rmse"] = pd.to_numeric(df["flux_rmse"], errors="coerce")
    df["noise"]     = pd.to_numeric(df["noise"],     errors="coerce")
    dl["flux_rmse"] = pd.to_numeric(dl["flux_rmse"], errors="coerce")
    dl["noise"]     = pd.to_numeric(dl["noise"],     errors="coerce")

    log.info("Main benchmark: %d rows", len(df))
    log.info("Layout note:    %d rows", len(dl))

    output_dir.mkdir(parents=True, exist_ok=True)

    log.info("Plotting Figure 1: RMSE vs sensor count…")
    plot_rmse_vs_sensor_count(df, output_dir, pdf)

    log.info("Plotting Figure 2: RMSE vs noise…")
    plot_rmse_vs_noise(df, output_dir, pdf)

    log.info("Plotting Figure 4: RMSE vs layout…")
    plot_rmse_vs_layout(dl, output_dir, pdf)

    log.info("Plotting Figure 5: Layout comparison…")
    plot_layout_comparison(output_dir, pdf)

    if not skip_qualitative:
        log.info("Plotting Figure 3: Qualitative reconstruction…")
        try:
            plot_qualitative_reconstruction(output_dir, pdf)
        except Exception as exc:
            log.warning("Qualitative reconstruction failed: %s", exc)
    else:
        log.info("Skipping qualitative reconstruction (--skip-qualitative).")

    log.info("All figures written to %s", output_dir)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate figures for benchmark_2d_v2.",
    )
    p.add_argument("--main",    default="reports/benchmark_2d_v2_results.csv",  metavar="CSV")
    p.add_argument("--layout",  default="reports/benchmark_2d_layout_note.csv", metavar="CSV")
    p.add_argument("--output",  default="reports/figures_v2",                   metavar="DIR")
    p.add_argument("--pdf",    action="store_true", help="Also save PDF copies")
    p.add_argument("--skip-qualitative", action="store_true",
                   help="Skip qualitative reconstruction (faster)")
    p.add_argument("--log-level", default="INFO",
                   choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout,
        force=True,
    )

    main_csv   = Path(args.main)
    layout_csv = Path(args.layout)
    output_dir = Path(args.output)

    if not main_csv.is_absolute():
        main_csv   = _PROJECT_ROOT / main_csv
    if not layout_csv.is_absolute():
        layout_csv = _PROJECT_ROOT / layout_csv
    if not output_dir.is_absolute():
        output_dir = _PROJECT_ROOT / output_dir

    run_plots(main_csv, layout_csv, output_dir, args.pdf, args.skip_qualitative)


if __name__ == "__main__":
    main()
