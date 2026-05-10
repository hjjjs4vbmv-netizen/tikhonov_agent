"""
run_simple_multisolver_benchmark.py
====================================
Compact 3-solver benchmark for advisor discussion.

Selected cases: step / single_pulse / smooth_sinusoid  ×  0.1 / 0.5 / 1.0 K noise
Solvers: tikhonov, tsvd, deepxde
Total runs: 9 cases × 3 solvers = 27

Outputs:
  experiments/runs/simple_multisolver_benchmark/results_raw.csv
  experiments/runs/simple_multisolver_benchmark/results_summary.csv
  figures/simple_multisolver_benchmark.png

Run from the tikhonov_agent/ directory:
    DDE_BACKEND=pytorch python experiments/run_simple_multisolver_benchmark.py
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

# Ensure DDE_BACKEND is set before any deepxde import
os.environ.setdefault("DDE_BACKEND", "pytorch")

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import numpy as np
import pandas as pd

from src.agent import IHCPAgent
from src.sensitivity import params_to_flux

# ---------------------------------------------------------------------------
# Case selection table
# (case_id, flux_family, noise_level)
# One representative case per (family, noise) combination from benchmark_v1
# Noise 0.5 is used as the benchmark spec asks for 0.1/0.5/1.0, but the
# existing cases have 0.1/0.5/1.0 mapped as:
#   0.1 → case_0001, 0003, 0005 (step), 0013,15,17 (single_pulse), 0025,27,29 (sinusoid)
# ---------------------------------------------------------------------------

CASES_DIR = REPO_ROOT / "experiments" / "cases" / "benchmark_v1"

SELECTED_CASES = [
    # (case_id,      flux_family,      noise_level)
    ("case_0001", "step",            0.1),
    ("case_0003", "step",            0.5),
    ("case_0005", "step",            1.0),
    ("case_0013", "single_pulse",    0.1),
    ("case_0015", "single_pulse",    0.5),
    ("case_0017", "single_pulse",    1.0),
    ("case_0025", "smooth_sinusoid", 0.1),
    ("case_0027", "smooth_sinusoid", 0.5),
    ("case_0029", "smooth_sinusoid", 1.0),
]

SOLVERS = ["tikhonov", "tsvd", "deepxde"]

OUTPUT_DIR = REPO_ROOT / "experiments" / "runs" / "simple_multisolver_benchmark"
FIGURES_DIR = REPO_ROOT / "figures"


# ---------------------------------------------------------------------------
# Per-solver planner override presets
# ---------------------------------------------------------------------------

def _solver_overrides(solver_name: str) -> dict:
    """Return planner overrides for a given solver."""
    base = {
        "iteration_budget": 3,   # allow a couple of replanning iterations
        "max_retries": 3,
        "physical_bounds": [-1e6, 1e6],
    }
    if solver_name == "tsvd":
        base["lambda_strategy"] = "fixed"
        base["lambda_value"] = 0.01
    elif solver_name == "deepxde":
        # L-BFGS is scale-invariant: converges on heat-flux scale ~50 kW/m²
        # without lr tuning.  Adam warm-start (500 steps) then LBFGS (500 steps).
        base["deepxde_iterations"] = 1000
        base["deepxde_adam_iterations"] = 500
        base["deepxde_optimizer"] = "lbfgs"
        base["deepxde_init"] = "lstsq"      # warm start near Tikhonov solution
        base["deepxde_device"] = "cpu"
    base["solver_name"] = solver_name
    return base


# ---------------------------------------------------------------------------
# Single run
# ---------------------------------------------------------------------------

def run_one(case_id: str, flux_family: str, noise_level: float,
            solver_name: str) -> dict:
    """Run one (case, solver) pair and return a result record."""
    case_dir = CASES_DIR / case_id
    config_path = case_dir / "config.yaml"
    obs_path = case_dir / "observations.csv"
    truth_path = case_dir / "truth.npz"

    truth_data = np.load(truth_path)
    q_true: np.ndarray = truth_data["q_true"]
    n_t = len(q_true)

    overrides = _solver_overrides(solver_name)
    agent_out = OUTPUT_DIR / case_id / solver_name
    agent = IHCPAgent(output_dir=agent_out)

    t0 = time.perf_counter()
    error_msg = ""
    try:
        summary = agent.run(
            config_path=config_path,
            observations_path=obs_path,
            planner_overrides=overrides,
        )
    except Exception as exc:
        runtime_sec = time.perf_counter() - t0
        print(f"    ERROR: {exc}")
        return {
            "case_id": case_id,
            "flux_family": flux_family,
            "noise_level": noise_level,
            "solver_name": solver_name,
            "final_decision": "error",
            "flux_rmse": float("nan"),
            "replay_rmse": float("nan"),
            "runtime_sec": runtime_sec,
            "n_iterations": 0,
            "lambda_used": float("nan"),
            "warning_count": 0,
            "notes": str(exc)[:120],
        }

    runtime_sec = time.perf_counter() - t0

    x_est = np.array(summary.final_result.estimated_x)
    q_est = params_to_flux(x_est, n_t)
    flux_rmse = float(np.sqrt(np.mean((q_est - q_true) ** 2)))

    last_trace = summary.traces[-1] if summary.traces else None
    replay_rmse = last_trace.verification.replay_rmse if last_trace else float("nan")

    diag = summary.final_result.diagnostics
    warning_count = len(diag.warnings) if diag else 0

    return {
        "case_id": case_id,
        "flux_family": flux_family,
        "noise_level": noise_level,
        "solver_name": solver_name,
        "final_decision": summary.final_status,
        "flux_rmse": flux_rmse,
        "replay_rmse": replay_rmse,
        "runtime_sec": runtime_sec,
        "n_iterations": len(summary.traces),
        "lambda_used": summary.final_result.lambda_used,
        "warning_count": warning_count,
        "notes": error_msg,
    }


# ---------------------------------------------------------------------------
# Main benchmark loop
# ---------------------------------------------------------------------------

def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    raw_csv = OUTPUT_DIR / "results_raw.csv"
    summary_csv = OUTPUT_DIR / "results_summary.csv"

    total = len(SELECTED_CASES) * len(SOLVERS)
    print(f"\n{'='*70}")
    print(f"Simple 3-Solver Benchmark")
    print(f"  Cases: {len(SELECTED_CASES)}  |  Solvers: {SOLVERS}  |  Total runs: {total}")
    print(f"{'='*70}\n")

    records = []
    run_num = 0

    for case_id, flux_family, noise_level in SELECTED_CASES:
        case_dir = CASES_DIR / case_id
        if not case_dir.exists():
            print(f"[SKIP] {case_id} not found at {case_dir}")
            continue

        for solver_name in SOLVERS:
            run_num += 1
            print(f"[{run_num:2d}/{total}] {case_id} | {flux_family:<18} | "
                  f"noise={noise_level} | solver={solver_name:<10}", end=" ... ", flush=True)

            rec = run_one(case_id, flux_family, noise_level, solver_name)
            records.append(rec)

            flux_r = f"{rec['flux_rmse']:.0f}" if not _isnan(rec['flux_rmse']) else "N/A"
            rep_r  = f"{rec['replay_rmse']:.4f}" if not _isnan(rec['replay_rmse']) else "N/A"
            print(f"{rec['final_decision']:<12} flux_rmse={flux_r:<8} "
                  f"replay_rmse={rep_r:<8} t={rec['runtime_sec']:.1f}s")

    # --- Save raw CSV ---
    df_raw = pd.DataFrame(records)
    df_raw.to_csv(raw_csv, index=False)
    print(f"\nSaved: {raw_csv}")

    # --- Build summary ---
    df_summary = _build_summary(df_raw)
    df_summary.to_csv(summary_csv, index=False)
    print(f"Saved: {summary_csv}")

    # --- Print summary table ---
    print(f"\n{'='*90}")
    print("Summary Table  (mean flux RMSE ± std across noise levels, per flux family)")
    print(f"{'='*90}")
    _print_pivot(df_raw)

    # --- Generate figure ---
    fig_path = FIGURES_DIR / "simple_multisolver_benchmark.png"
    _make_figure(df_raw, fig_path)
    print(f"\nFigure saved: {fig_path}")

    # --- Final stats ---
    _print_final_stats(df_raw)


def _isnan(x: float) -> bool:
    return x != x  # NaN check compatible with plain floats


def _build_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate mean/std over cases per (flux_family, noise_level, solver)."""
    numeric_cols = ["flux_rmse", "replay_rmse", "runtime_sec", "n_iterations"]
    agg: dict = {c: ["mean", "std"] for c in numeric_cols if c in df.columns}
    agg["final_decision"] = lambda x: ",".join(sorted(set(x.astype(str))))  # type: ignore[assignment]

    grouped = df.groupby(["flux_family", "noise_level", "solver_name"])
    rows = []
    for (family, noise, solver), grp in grouped:
        row: dict = {
            "flux_family": family,
            "noise_level": noise,
            "solver_name": solver,
            "n_runs": len(grp),
            "decisions": ",".join(sorted(set(grp["final_decision"].astype(str)))),
        }
        for col in numeric_cols:
            if col in grp.columns:
                row[f"{col}_mean"] = float(grp[col].mean())
                row[f"{col}_std"] = float(grp[col].std(ddof=0))
        rows.append(row)
    return pd.DataFrame(rows)


def _print_pivot(df: pd.DataFrame) -> None:
    pivot = df.pivot_table(
        index=["flux_family", "noise_level"],
        columns="solver_name",
        values="flux_rmse",
        aggfunc="mean",
    )
    solver_cols = [c for c in ["tikhonov", "tsvd", "deepxde"] if c in pivot.columns]
    pivot = pivot[solver_cols]
    print(pivot.to_string(float_format="{:,.0f}".format))


def _make_figure(df: pd.DataFrame, out_path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    import numpy as np_

    families = ["step", "single_pulse", "smooth_sinusoid"]
    noise_levels = sorted(df["noise_level"].unique())
    solvers = ["tikhonov", "tsvd", "deepxde"]
    colors = {"tikhonov": "#1f77b4", "tsvd": "#ff7f0e", "deepxde": "#2ca02c"}

    n_families = len(families)
    n_noise = len(noise_levels)
    n_solvers = len(solvers)
    bar_width = 0.22
    group_gap = 0.15

    fig, axes = plt.subplots(1, n_families, figsize=(5.5 * n_families, 4.5), sharey=False)
    if n_families == 1:
        axes = [axes]

    for ax, family in zip(axes, families):
        grp = df[df["flux_family"] == family]
        x_positions = np_.arange(n_noise)

        for si, solver in enumerate(solvers):
            vals = []
            for noise in noise_levels:
                sub = grp[(grp["solver_name"] == solver) & (grp["noise_level"] == noise)]
                vals.append(float(sub["flux_rmse"].mean()) if len(sub) > 0 else 0.0)

            offset = (si - (n_solvers - 1) / 2) * bar_width
            bars = ax.bar(
                x_positions + offset, vals,
                width=bar_width,
                label=solver,
                color=colors[solver],
                alpha=0.85,
                edgecolor="white",
                linewidth=0.5,
            )

        ax.set_title(family.replace("_", " ").title(), fontsize=12, fontweight="bold")
        ax.set_xlabel("Noise level [K]", fontsize=10)
        ax.set_ylabel("Flux RMSE [W/m²]", fontsize=10)
        ax.set_xticks(x_positions)
        ax.set_xticklabels([str(n) for n in noise_levels])
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
        ax.grid(axis="y", alpha=0.3, linestyle="--")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    axes[-1].legend(title="Solver", fontsize=9, title_fontsize=10, loc="upper left")

    fig.suptitle(
        "3-Solver Benchmark: Flux RMSE by Family and Noise Level\n"
        "(tikhonov | tsvd | deepxde  —  simple selected benchmark)",
        fontsize=12, y=1.02,
    )
    plt.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _print_final_stats(df: pd.DataFrame) -> None:
    print(f"\n{'='*70}")
    print("Final Run Statistics")
    print(f"{'='*70}")
    total = len(df)
    errors = int((df["final_decision"] == "error").sum())
    passes = int(df["final_decision"].isin(["pass", "weak_pass"]).sum())
    print(f"Total runs        : {total}")
    print(f"Successful runs   : {passes}  ({100*passes/total:.0f}%)")
    print(f"Error/failed runs : {errors}")
    print()

    for solver in SOLVERS:
        s = df[df["solver_name"] == solver]
        ok = s["final_decision"].isin(["pass", "weak_pass"]).sum()
        rmse_mean = s["flux_rmse"].mean()
        rt_mean = s["runtime_sec"].mean()
        print(f"  {solver:<12}: {ok}/{len(s)} runs OK"
              f"  |  mean flux RMSE = {rmse_mean:,.0f} W/m²"
              f"  |  mean runtime = {rt_mean:.1f}s")

    print(f"\nOutputs saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
