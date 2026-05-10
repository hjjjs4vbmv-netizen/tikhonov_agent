"""
generate_figures.py
===================
Generate benchmark figures from raw results.

Figures
-------
    figures/rmse_vs_primary_axis.png
    figures/ssim_vs_primary_axis.png
    figures/peak_error_vs_primary_axis.png
    figures/band_energy_error_vs_primary_axis.png
    figures/support_overlap_vs_primary_axis.png
    figures/layout_sensitivity_vs_primary_axis.png
    figures/stress_failure_map.png
    figures/solver_ranking_heatmap.png
    figures/qualitative_gallery_main.png
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from collections import defaultdict

import numpy as np

_HERE         = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

# ---------------------------------------------------------------------------
# Try to import matplotlib; emit meaningful error if unavailable
# ---------------------------------------------------------------------------
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("WARNING: matplotlib not available; skipping figure generation")


def load_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def safe_float(v: str) -> float:
    try:
        f = float(v)
        return f if np.isfinite(f) else float("nan")
    except (ValueError, TypeError):
        return float("nan")


SOLVER_COLORS = {
    "tikhonov_2d":   "#1f77b4",
    "tsvd_2d":       "#ff7f0e",
    "fast_bayesian": "#2ca02c",
    "deepxde_pinn":  "#d62728",
}
SOLVER_MARKERS = {
    "tikhonov_2d":   "o",
    "tsvd_2d":       "s",
    "fast_bayesian": "^",
    "deepxde_pinn":  "D",
}
FAMILY_ORDER = [
    "fourier_kl_smooth", "gaussian_localized",
    "overlapping_multi_spot", "matern_grf",
    "discontinuous_piecewise", "moving_hotspot",
]
SOLVER_ORDER = ["tikhonov_2d", "tsvd_2d", "fast_bayesian", "deepxde_pinn"]
PRIMARY_AXIS_LABELS = {
    "fourier_kl_smooth":       ["2 modes", "4 modes", "8 modes"],
    "gaussian_localized":      ["σ=0.05", "σ=0.15", "σ=0.30"],
    "overlapping_multi_spot":  ["sep=0.45", "sep=0.20", "sep=0.07"],
    "matern_grf":              ["ℓ=0.30", "ℓ=0.12", "ℓ=0.04"],
    "moving_hotspot":          ["v=0.2", "v=0.5", "v=1.0"],
    "discontinuous_piecewise": ["sharp=2", "sharp=8", "sharp=30"],
}


def _group_by(rows: list[dict], keys: list[str]) -> dict[tuple, list[dict]]:
    g: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        k = tuple(r.get(kk, "") for kk in keys)
        g[k].append(r)
    return g


def _mean_of(rows: list[dict], metric: str) -> float:
    vals = [safe_float(r.get(metric, "nan")) for r in rows]
    vals = [v for v in vals if np.isfinite(v)]
    return float(np.mean(vals)) if vals else float("nan")


def _std_of(rows: list[dict], metric: str) -> float:
    vals = [safe_float(r.get(metric, "nan")) for r in rows]
    vals = [v for v in vals if np.isfinite(v)]
    return float(np.std(vals)) if len(vals) > 1 else 0.0


# ---------------------------------------------------------------------------
# 1. Metric vs primary axis (one panel per family)
# ---------------------------------------------------------------------------

def plot_metric_vs_primary_axis(
    core_rows: list[dict],
    metric: str,
    ylabel: str,
    title: str,
    out_path: Path,
    noise_filter: str = "0.1",
) -> None:
    """One subplot per family, x = primary axis level, y = metric, lines = solver."""
    rows = [r for r in core_rows if r.get("noise_sigma", "") == noise_filter
            and r.get("track_name", "") == "benchmark_core"]
    if not rows:
        rows = [r for r in core_rows if r.get("noise_sigma", "") == noise_filter]

    families = [f for f in FAMILY_ORDER if any(r.get("family_name") == f for r in rows)]
    if not families:
        families = sorted(set(r.get("family_name", "") for r in rows))

    n_fam = len(families)
    if n_fam == 0:
        return

    fig, axes = plt.subplots(1, n_fam, figsize=(4 * n_fam, 4), squeeze=False)
    fig.suptitle(f"{title} (noise={noise_filter} K)", fontsize=12)

    for col, fam in enumerate(families):
        ax = axes[0][col]
        fam_rows = [r for r in rows if r.get("family_name") == fam]
        solvers = [s for s in SOLVER_ORDER if any(r.get("solver_name") == s for r in fam_rows)]

        for solver in solvers:
            sol_rows = [r for r in fam_rows if r.get("solver_name") == solver]
            # Group by level
            by_level = _group_by(sol_rows, ["primary_axis_level"])
            levels = sorted(by_level.keys(), key=lambda k: int(k[0]) if k[0].isdigit() else 0)
            x = list(range(len(levels)))
            y = [_mean_of(by_level[lev], metric) for lev in levels]
            e = [_std_of(by_level[lev], metric) for lev in levels]
            y = [float("nan") if not np.isfinite(v) else v for v in y]

            valid = [(xi, yi, ei) for xi, yi, ei in zip(x, y, e) if np.isfinite(yi)]
            if valid:
                xv, yv, ev = zip(*valid)
                ax.errorbar(
                    xv, yv, yerr=ev,
                    color=SOLVER_COLORS.get(solver, "gray"),
                    marker=SOLVER_MARKERS.get(solver, "o"),
                    label=solver.replace("_", " "),
                    capsize=3, linewidth=1.5, markersize=6,
                )

        axis_labels = PRIMARY_AXIS_LABELS.get(fam, [str(i) for i in range(3)])
        ax.set_xticks(range(min(3, len(axis_labels))))
        ax.set_xticklabels(axis_labels[:3], rotation=30, ha="right", fontsize=7)
        ax.set_title(fam.replace("_", "\n"), fontsize=9)
        ax.set_xlabel("Primary axis level", fontsize=8)
        if col == 0:
            ax.set_ylabel(ylabel, fontsize=9)
        ax.legend(fontsize=6, loc="upper left")
        ax.grid(alpha=0.3)

    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"  Saved {out_path.name}")


# ---------------------------------------------------------------------------
# 2. Layout sensitivity vs primary axis
# ---------------------------------------------------------------------------

def plot_layout_sensitivity(layout_rows: list[dict], out_path: Path) -> None:
    rows = [r for r in layout_rows if r.get("noise_sigma", "") == "0.1"]
    families = sorted(set(r.get("family_name", "") for r in rows))
    layouts  = ["uniform", "boundary_biased", "clustered"]
    layout_colors = {"uniform": "#1f77b4", "boundary_biased": "#2ca02c", "clustered": "#d62728"}

    n_fam = len(families)
    if not n_fam:
        return

    fig, axes = plt.subplots(1, n_fam, figsize=(4 * n_fam, 4), squeeze=False)
    fig.suptitle("RMSE vs Primary Axis by Layout (noise=0.1 K, Tikhonov)", fontsize=11)

    for col, fam in enumerate(families):
        ax = axes[0][col]
        fam_rows = [r for r in rows if r.get("family_name") == fam
                    and r.get("solver_name") == "tikhonov_2d"]

        for layout in layouts:
            lay_rows = [r for r in fam_rows if r.get("sensor_config") == layout]
            by_level = _group_by(lay_rows, ["primary_axis_level"])
            levels   = sorted(by_level.keys(), key=lambda k: int(k[0]) if k[0].isdigit() else 0)
            x = list(range(len(levels)))
            y = [_mean_of(by_level[lev], "rmse_flux") for lev in levels]
            valid = [(xi, yi) for xi, yi in zip(x, y) if np.isfinite(yi)]
            if valid:
                xv, yv = zip(*valid)
                ax.plot(xv, yv, color=layout_colors.get(layout, "gray"),
                        marker="o", label=layout, linewidth=1.5, markersize=6)

        ax.set_title(fam.replace("_", "\n"), fontsize=9)
        ax.set_xlabel("Primary axis level", fontsize=8)
        if col == 0:
            ax.set_ylabel("RMSE [W/m²]", fontsize=9)
        ax.legend(fontsize=7)
        ax.grid(alpha=0.3)

    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"  Saved {out_path.name}")


# ---------------------------------------------------------------------------
# 3. Stress failure map
# ---------------------------------------------------------------------------

def plot_stress_failure_map(stress_rows: list[dict], out_path: Path) -> None:
    families = sorted(set(r.get("family_name", "") for r in stress_rows))
    solvers  = [s for s in SOLVER_ORDER if any(r.get("solver_name") == s for r in stress_rows)]
    if not families or not solvers:
        return

    # For each (family, solver): mean RMSE at hardest level (level=2)
    n_fam = len(families)
    n_sol = len(solvers)
    Z = np.full((n_sol, n_fam), float("nan"))

    for fi, fam in enumerate(families):
        for si, sol in enumerate(solvers):
            subset = [r for r in stress_rows
                      if r.get("family_name") == fam
                      and r.get("solver_name") == sol
                      and r.get("primary_axis_level") == "2"]
            if subset:
                Z[si, fi] = _mean_of(subset, "rmse_flux")

    fig, ax = plt.subplots(figsize=(max(4, n_fam * 1.5), max(3, n_sol * 0.8)))
    # Normalise per family for colour
    Z_norm = np.copy(Z)
    for col in range(n_fam):
        col_vals = Z_norm[:, col]
        finite = col_vals[np.isfinite(col_vals)]
        if len(finite) > 0:
            vmax = np.max(finite)
            if vmax > 0:
                Z_norm[:, col] /= vmax

    im = ax.imshow(Z_norm, cmap="RdYlGn_r", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(n_fam))
    ax.set_xticklabels([f.replace("_", "\n") for f in families], fontsize=8)
    ax.set_yticks(range(n_sol))
    ax.set_yticklabels(solvers, fontsize=8)
    ax.set_title("Stress Track — Normalised RMSE (hardest level)", fontsize=10)

    # Annotate with actual RMSE
    for si in range(n_sol):
        for fi in range(n_fam):
            val = Z[si, fi]
            if np.isfinite(val):
                ax.text(fi, si, f"{val:.0f}", ha="center", va="center",
                        fontsize=7, color="black")

    plt.colorbar(im, ax=ax, label="Normalised RMSE")
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"  Saved {out_path.name}")


# ---------------------------------------------------------------------------
# 4. Solver ranking heatmap
# ---------------------------------------------------------------------------

def plot_solver_ranking_heatmap(core_rows: list[dict], out_path: Path) -> None:
    """Show solver rankings by family and metric."""
    metrics_to_rank = ["rmse_flux", "ssim_flux", "band_error_scalar", "support_overlap"]
    metric_labels   = ["RMSE↓", "SSIM↑", "BandErr↓", "Support↑"]
    families = [f for f in FAMILY_ORDER if any(r.get("family_name") == f for r in core_rows)]
    solvers  = [s for s in SOLVER_ORDER if any(r.get("solver_name") == s for r in core_rows)]
    if not families or not solvers:
        return

    rows_lo = [r for r in core_rows if r.get("noise_sigma", "") in ("0.1", "")]

    # For each (family, solver, metric): mean value
    # Then rank solvers within each (family, metric)
    n_row = len(families) * len(metrics_to_rank)
    n_col = len(solvers)
    rank_matrix = np.full((n_row, n_col), float("nan"))
    y_labels: list[str] = []

    row_idx = 0
    for fam in families:
        for mi, metric in enumerate(metrics_to_rank):
            y_labels.append(f"{fam[:12]}\n{metric_labels[mi]}")
            vals: dict[str, float] = {}
            for sol in solvers:
                subset = [r for r in rows_lo
                          if r.get("family_name") == fam
                          and r.get("solver_name") == sol]
                vals[sol] = _mean_of(subset, metric)

            # Rank: lower is better for RMSE/band, higher is better for SSIM/support
            higher_is_better = metric in ("ssim_flux", "support_overlap")
            finite_vals = {k: v for k, v in vals.items() if np.isfinite(v)}
            if finite_vals:
                sorted_solvers = sorted(
                    finite_vals.keys(),
                    key=lambda s: -finite_vals[s] if higher_is_better else finite_vals[s],
                )
                for rank, sol in enumerate(sorted_solvers):
                    sol_idx = solvers.index(sol)
                    rank_matrix[row_idx, sol_idx] = rank + 1   # 1 = best
            row_idx += 1

    fig, ax = plt.subplots(figsize=(max(5, n_col * 1.5), max(4, n_row * 0.5)))
    im = ax.imshow(rank_matrix, cmap="RdYlGn_r", vmin=1, vmax=max(4, n_col), aspect="auto")

    for ri in range(n_row):
        for ci in range(n_col):
            val = rank_matrix[ri, ci]
            if np.isfinite(val):
                ax.text(ci, ri, str(int(val)), ha="center", va="center",
                        fontsize=9, fontweight="bold",
                        color="white" if val > n_col / 2 else "black")

    ax.set_xticks(range(n_col))
    ax.set_xticklabels(solvers, rotation=20, ha="right", fontsize=8)
    ax.set_yticks(range(n_row))
    ax.set_yticklabels(y_labels, fontsize=7)
    ax.set_title("Solver Rankings by Family × Metric (1=best)", fontsize=10)
    plt.colorbar(im, ax=ax, label="Rank")
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"  Saved {out_path.name}")


# ---------------------------------------------------------------------------
# 5. Qualitative gallery (ground-truth flux visualisations)
# ---------------------------------------------------------------------------

def plot_qualitative_gallery(out_path: Path) -> None:
    """Show the 6 flux families across 3 primary-axis levels as a gallery."""
    try:
        from src.heat_flux_families import generate_family_flux, list_families, FAMILY_REGISTRY
    except ImportError:
        print("  Cannot import heat_flux_families; skipping gallery")
        return

    import numpy as np
    families = ["fourier_kl_smooth", "gaussian_localized", "overlapping_multi_spot",
                "matern_grf", "moving_hotspot", "discontinuous_piecewise"]
    n_fam = len(families)
    n_levels = 3

    y = np.linspace(0.0, 0.1, 20)
    t = np.linspace(0.0, 100.0, 20)

    fig, axes = plt.subplots(n_fam, n_levels, figsize=(n_levels * 2.5, n_fam * 2.0))
    fig.suptitle("Heat-flux Family Taxonomy — Primary Axis Levels", fontsize=11)

    for row, fam in enumerate(families):
        fam_meta = FAMILY_REGISTRY.get(fam)
        for col in range(n_levels):
            ax = axes[row][col]
            try:
                q = generate_family_flux(fam, y, t, primary_axis_level=col, seed=0)
                vmax = max(abs(q.min()), abs(q.max())) or 1.0
                ax.imshow(q, origin="lower", aspect="auto",
                          cmap="RdBu_r", vmin=-vmax, vmax=vmax,
                          extent=[0, 100, 0, 0.1])
            except Exception as e:
                ax.text(0.5, 0.5, str(e)[:20], transform=ax.transAxes,
                        ha="center", fontsize=6, color="red")

            if row == 0 and fam_meta:
                levels = fam_meta.primary_axis_levels
                label = str(levels[col]) if col < len(levels) else str(col)
                ax.set_title(f"{fam_meta.primary_axis_name}={label}", fontsize=7)

            if col == 0:
                ax.set_ylabel(fam.replace("_", "\n"), fontsize=7)
            else:
                ax.set_yticks([])

            if row == n_fam - 1:
                ax.set_xlabel("t [s]", fontsize=7)
            else:
                ax.set_xticks([])

    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"  Saved {out_path.name}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if not HAS_MPL:
        print("matplotlib not available; install with: pip install matplotlib")
        return

    reports = _PROJECT_ROOT / "reports"
    figures = _PROJECT_ROOT / "figures"
    figures.mkdir(parents=True, exist_ok=True)

    core_rows   = load_csv(reports / "benchmark_core_raw.csv")
    layout_rows = load_csv(reports / "sensor_layout_track_raw.csv")
    stress_rows = load_csv(reports / "stress_track_raw.csv")

    print(f"Loaded {len(core_rows)} core / {len(layout_rows)} layout / {len(stress_rows)} stress rows")

    # 1. Metric vs primary axis plots
    for metric, ylabel, title, fname in [
        ("rmse_flux",              "RMSE [W/m²]",         "RMSE vs Primary Axis",             "rmse_vs_primary_axis.png"),
        ("ssim_flux",              "SSIM",                 "SSIM vs Primary Axis",              "ssim_vs_primary_axis.png"),
        ("peak_localization_error","Peak Loc. Error",      "Peak Localization Error vs Primary", "peak_error_vs_primary_axis.png"),
        ("band_error_scalar",      "Band Energy Error",    "Band Energy Error vs Primary Axis",  "band_energy_error_vs_primary_axis.png"),
        ("support_overlap",        "Support Overlap (Dice)","Support Overlap vs Primary Axis",  "support_overlap_vs_primary_axis.png"),
    ]:
        for noise in ["0.1", "1.0"]:
            sfx = f"_noise{noise.replace('.','p')}" if noise != "0.1" else ""
            plot_metric_vs_primary_axis(
                core_rows, metric, ylabel, title,
                figures / fname.replace(".png", f"{sfx}.png"),
                noise_filter=noise,
            )

    # 2. Layout sensitivity
    plot_layout_sensitivity(layout_rows, figures / "layout_sensitivity_vs_primary_axis.png")

    # 3. Stress failure map
    plot_stress_failure_map(stress_rows, figures / "stress_failure_map.png")

    # 4. Solver ranking heatmap
    plot_solver_ranking_heatmap(core_rows, figures / "solver_ranking_heatmap.png")

    # 5. Qualitative gallery
    plot_qualitative_gallery(figures / "qualitative_gallery_main.png")

    print("Figure generation complete.")


if __name__ == "__main__":
    main()
