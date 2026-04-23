"""
run_multi_solver_pilot.py
=========================
Run the small multi-solver pilot for the paper asset package.

9 representative cases × 2 solvers = 18 runs.

Cases selected:
  step:             case_0001 (noise=0.1), case_0003 (noise=0.5), case_0005 (noise=1.0)
  single_pulse:     case_0013 (noise=0.1), case_0015 (noise=0.5), case_0017 (noise=1.0)
  smooth_sinusoid:  case_0025 (noise=0.1), case_0027 (noise=0.5), case_0029 (noise=1.0)

Solvers:
  tikhonov — auto lambda (discrepancy or L-curve per planner rule)
  tsvd     — fixed threshold 0.01 (1% of max singular value)

The agent runs with the FULL iteration budget so results are comparable
to the benchmark_v1 full_agent variant (not the single-iteration compare).
"""

from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import numpy as np

from src.agent import IHCPAgent
from src.sensitivity import params_to_flux

CASES_DIR = REPO_ROOT / "experiments" / "cases" / "benchmark_v1"
OUT_DIR = REPO_ROOT / "experiments" / "runs" / "multi_solver_pilot"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 9 representative cases
PILOT_CASES = [
    # (case_id, flux_family, noise_level, difficulty)
    ("case_0001", "step",            0.1, "easy"),
    ("case_0003", "step",            0.5, "moderate"),
    ("case_0005", "step",            1.0, "hard"),
    ("case_0013", "single_pulse",    0.1, "easy"),
    ("case_0015", "single_pulse",    0.5, "moderate"),
    ("case_0017", "single_pulse",    1.0, "hard"),
    ("case_0025", "smooth_sinusoid", 0.1, "easy"),
    ("case_0027", "smooth_sinusoid", 0.5, "moderate"),
    ("case_0029", "smooth_sinusoid", 1.0, "hard"),
]

SOLVERS = ["tikhonov", "tsvd"]

# Full budget — same as benchmark full_agent
FULL_BUDGET_OVERRIDES = {
    "max_retries": 6,
    "iteration_budget": 10,
}


def run_one(case_id: str, flux_family: str, noise_level: float,
            difficulty: str, solver_name: str) -> dict:
    case_dir = CASES_DIR / case_id
    config_path = case_dir / "config.yaml"
    obs_path = case_dir / "observations.csv"
    truth_path = case_dir / "truth.npz"

    truth = np.load(truth_path)
    q_true = truth["q_true"]

    overrides = {**FULL_BUDGET_OVERRIDES, "solver_name": solver_name}
    if solver_name == "tsvd":
        overrides["lambda_strategy"] = "fixed"
        overrides["lambda_value"] = 0.01

    agent = IHCPAgent(
        output_dir=OUT_DIR / "agent_runs" / case_id / solver_name,
    )
    t0 = time.perf_counter()
    summary = agent.run(
        config_path=config_path,
        observations_path=obs_path,
        planner_overrides=overrides,
    )
    runtime_s = time.perf_counter() - t0

    # Flux RMSE vs ground truth
    x_est = np.array(summary.final_result.estimated_x)
    q_est = params_to_flux(x_est, len(q_true))
    flux_rmse = float(np.sqrt(np.mean((q_est - q_true) ** 2)))
    flux_corr = float(np.corrcoef(q_est, q_true)[0, 1]) if len(q_true) > 1 else float("nan")

    final_trace = summary.traces[-1] if summary.traces else None
    replay_rmse = final_trace.verification.replay_rmse if final_trace else float("nan")
    verif_decision = final_trace.verification.decision if final_trace else "unknown"
    tradeoff = final_trace.verification.tradeoff_label if final_trace else "unknown"

    warnings = []
    if summary.final_result.diagnostics and summary.final_result.diagnostics.warnings:
        warnings = summary.final_result.diagnostics.warnings

    return {
        "case_id": case_id,
        "flux_family": flux_family,
        "noise_level": noise_level,
        "difficulty": difficulty,
        "solver_name": solver_name,
        "verif_decision": verif_decision,
        "agent_status": summary.final_status,
        "flux_rmse": round(flux_rmse, 1),
        "flux_correlation": round(flux_corr, 4),
        "replay_rmse": round(replay_rmse, 5),
        "n_iterations": len(summary.traces),
        "runtime_s": round(runtime_s, 3),
        "lambda_used": summary.final_result.lambda_used,
        "tradeoff_label": tradeoff,
        "solver_method": (
            summary.final_result.diagnostics.solve_method
            if summary.final_result.diagnostics else "unknown"
        ),
        "warnings": "; ".join(warnings[:2]) if warnings else "",
    }


def main():
    print("=" * 72)
    print("Multi-Solver Pilot: Tikhonov vs TSVD on 9 benchmark cases")
    print("=" * 72)

    results = []
    for (case_id, flux_family, noise_level, difficulty) in PILOT_CASES:
        for solver_name in SOLVERS:
            tag = f"[{case_id}][{flux_family}][noise={noise_level}][{solver_name}]"
            print(f"  {tag}...", end=" ", flush=True)
            try:
                rec = run_one(case_id, flux_family, noise_level, difficulty, solver_name)
                results.append(rec)
                print(
                    f"verif={rec['verif_decision']}, agent={rec['agent_status']}, "
                    f"flux_rmse={rec['flux_rmse']:.0f}, n_iter={rec['n_iterations']}, "
                    f"t={rec['runtime_s']:.2f}s"
                )
            except Exception as exc:
                print(f"ERROR: {exc}")
                results.append({
                    "case_id": case_id, "flux_family": flux_family,
                    "noise_level": noise_level, "difficulty": difficulty,
                    "solver_name": solver_name,
                    "verif_decision": "error", "agent_status": "error",
                    "flux_rmse": float("nan"), "flux_correlation": float("nan"),
                    "replay_rmse": float("nan"), "n_iterations": 0,
                    "runtime_s": float("nan"), "lambda_used": float("nan"),
                    "tradeoff_label": "error", "solver_method": "error",
                    "warnings": str(exc),
                })

    # Save raw results
    raw_path = OUT_DIR / "results_raw.csv"
    fieldnames = [
        "case_id", "flux_family", "noise_level", "difficulty",
        "solver_name", "verif_decision", "agent_status",
        "flux_rmse", "flux_correlation", "replay_rmse",
        "n_iterations", "runtime_s", "lambda_used",
        "tradeoff_label", "solver_method", "warnings",
    ]
    with raw_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"\nRaw results: {raw_path}")

    # Build summary: aggregate by flux_family, difficulty, solver
    summary_rows = []
    for flux_family in ["step", "single_pulse", "smooth_sinusoid"]:
        for solver_name in SOLVERS:
            subset = [
                r for r in results
                if r["flux_family"] == flux_family and r["solver_name"] == solver_name
                and r["agent_status"] not in ("error",)
            ]
            if not subset:
                continue
            flux_rmses = [r["flux_rmse"] for r in subset if r["flux_rmse"] == r["flux_rmse"]]
            replay_rmses = [r["replay_rmse"] for r in subset if r["replay_rmse"] == r["replay_rmse"]]
            successes = [
                1 for r in subset if r["agent_status"] in ("pass", "weak_pass")
            ]
            summary_rows.append({
                "flux_family": flux_family,
                "solver_name": solver_name,
                "n_cases": len(subset),
                "success_rate": round(len(successes) / len(subset), 3),
                "flux_rmse_mean": round(float(np.mean(flux_rmses)), 1) if flux_rmses else float("nan"),
                "flux_rmse_std": round(float(np.std(flux_rmses)), 1) if flux_rmses else float("nan"),
                "replay_rmse_mean": round(float(np.mean(replay_rmses)), 5) if replay_rmses else float("nan"),
                "runtime_mean_s": round(float(np.mean([r["runtime_s"] for r in subset])), 3),
            })

    summary_path = OUT_DIR / "results_summary.csv"
    sum_fields = ["flux_family", "solver_name", "n_cases", "success_rate",
                  "flux_rmse_mean", "flux_rmse_std", "replay_rmse_mean", "runtime_mean_s"]
    with summary_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=sum_fields)
        writer.writeheader()
        writer.writerows(summary_rows)
    print(f"Summary:     {summary_path}")

    # Print comparison table
    print("\n" + "=" * 100)
    print(f"{'Case':<12} {'Family':<18} {'Noise':>6} {'Solver':<12} {'Verif':<12} "
          f"{'Agent':<12} {'FluxRMSE':>10} {'RepRMSE':>9} {'Iters':>5} {'Time':>6}")
    print("-" * 100)
    for r in results:
        flux_r = f"{r['flux_rmse']:.0f}" if r["flux_rmse"] == r["flux_rmse"] else "ERR"
        rep_r = f"{r['replay_rmse']:.4f}" if r["replay_rmse"] == r["replay_rmse"] else "ERR"
        print(
            f"{r['case_id']:<12} {r['flux_family']:<18} {r['noise_level']:>6.1f} "
            f"{r['solver_name']:<12} {r['verif_decision']:<12} {r['agent_status']:<12} "
            f"{flux_r:>10} {rep_r:>9} {r['n_iterations']:>5} {r['runtime_s']:>5.2f}s"
        )

    print("\nSummary by flux family:")
    print(f"{'Family':<18} {'Solver':<12} {'Success':>8} {'FluxRMSE mean':>14} {'FluxRMSE std':>13}")
    print("-" * 70)
    for r in summary_rows:
        print(
            f"{r['flux_family']:<18} {r['solver_name']:<12} "
            f"{r['success_rate']:>8.1%} {r['flux_rmse_mean']:>14.0f} {r['flux_rmse_std']:>13.0f}"
        )

    # Save JSON for note generation
    with (OUT_DIR / "results_raw.json").open("w") as fh:
        json.dump(results, fh, indent=2)


if __name__ == "__main__":
    main()
