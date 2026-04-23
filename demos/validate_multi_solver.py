"""
validate_multi_solver.py
========================
Validation script for Part B: Solver Registry + TSVD.

Runs both Tikhonov and TSVD solvers on a small representative subset of
benchmark cases and produces a compact comparison table.

Cases selected: 3 cases from benchmark_v1 (step/ramp/sine flux families,
medium noise level) to cover representative scenarios without re-running
the full 30-case benchmark.

Run from the tikhonov_agent/ directory:
    python demos/validate_multi_solver.py

Outputs:
    demos/outputs/multi_solver_comparison.csv
    demos/outputs/multi_solver_comparison.json
"""

from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))

import numpy as np

from src.agent import IHCPAgent
from src.parser import parse_problem
from src.solver_registry import get_registry

OUTPUT_DIR = REPO_ROOT / "demos" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Case selection: pick representative cases from benchmark_v1
# step flux / low noise, ramp flux / medium noise, step flux / high noise
# ---------------------------------------------------------------------------

CASES_DIR = REPO_ROOT / "experiments" / "cases" / "benchmark_v1"

SELECTED_CASES = [
    # (case_id, label)
    ("case_0001", "step, low-noise"),
    ("case_0007", "step, med-noise"),
    ("case_0013", "step, high-noise"),
    ("case_0006", "ramp, low-noise"),
    ("case_0012", "ramp, med-noise"),
]


def run_solver(case_dir: Path, solver_name: str) -> dict:
    """Run one solver on one case and return a result record."""
    config_path = case_dir / "config.yaml"
    obs_path = case_dir / "observations.csv"
    truth_path = case_dir / "truth.npz"

    # Load ground-truth flux for RMSE computation
    truth_data = np.load(truth_path)
    q_true = truth_data["q_true"]          # shape (N_t,)

    # Build planner overrides — enforce single-iteration, fixed lambda for fair comparison
    planner_overrides = {
        "solver_name": solver_name,
        "iteration_budget": 1,   # single iteration for clean comparison
        "max_retries": 1,
    }
    if solver_name == "tsvd":
        # Use fixed truncation threshold for TSVD (1% of max singular value)
        planner_overrides["lambda_strategy"] = "fixed"
        planner_overrides["lambda_value"] = 0.01
    else:
        # Auto-select lambda for Tikhonov (discrepancy or L-curve)
        pass  # planner picks automatically

    output_dir = OUTPUT_DIR / "agent_runs" / case_dir.name / solver_name
    agent = IHCPAgent(output_dir=output_dir)

    t0 = time.perf_counter()
    summary = agent.run(
        config_path=config_path,
        observations_path=obs_path,
        planner_overrides=planner_overrides,
    )
    runtime_s = time.perf_counter() - t0

    # Compute flux RMSE vs ground truth
    x_est = np.array(summary.final_result.estimated_x)
    # Expand from n_params to N_t using the same segment scheme
    from src.sensitivity import params_to_flux
    n_t = len(q_true)
    q_est = params_to_flux(x_est, n_t)
    flux_rmse = float(np.sqrt(np.mean((q_est - q_true) ** 2)))

    final_trace = summary.traces[-1] if summary.traces else None
    replay_rmse = final_trace.verification.replay_rmse if final_trace else float("nan")
    decision = final_trace.verification.decision if final_trace else "unknown"

    return {
        "case": case_dir.name,
        "solver": solver_name,
        "decision": decision,
        "flux_rmse": flux_rmse,
        "replay_rmse": replay_rmse,
        "runtime_s": runtime_s,
        "final_status": summary.final_status,
        "n_iter": len(summary.traces),
        "lambda_used": summary.final_result.lambda_used,
        "solver_status": summary.final_result.status,
    }


def main() -> None:
    print("=" * 70)
    print("Multi-Solver Validation: Tikhonov vs TSVD")
    print("=" * 70)

    # Verify solver registry
    registry = get_registry()
    print(f"\nRegistered solvers: {registry.available()}")

    # Check which cases exist
    available_cases = []
    for case_id, label in SELECTED_CASES:
        case_dir = CASES_DIR / case_id
        if case_dir.exists():
            available_cases.append((case_id, label, case_dir))
        else:
            print(f"  [SKIP] {case_id} not found at {case_dir}")

    if not available_cases:
        print("\nNo benchmark cases found. Run experiments/generate_cases.py first.")
        print("Falling back to synthetic demo case...")
        _run_synthetic_demo()
        return

    print(f"\nRunning {len(available_cases)} cases × 2 solvers = {len(available_cases)*2} runs...\n")

    results = []
    for case_id, label, case_dir in available_cases:
        for solver_name in ["tikhonov", "tsvd"]:
            print(f"  [{case_id}] [{label}] [{solver_name}]...", end=" ", flush=True)
            try:
                rec = run_solver(case_dir, solver_name)
                rec["label"] = label
                results.append(rec)
                print(f"verif={rec['decision']}, agent={rec['final_status']}, flux_rmse={rec['flux_rmse']:.0f}, runtime={rec['runtime_s']:.2f}s")
            except Exception as exc:
                print(f"ERROR: {exc}")
                results.append({
                    "case": case_id, "label": label, "solver": solver_name,
                    "decision": "error", "flux_rmse": float("nan"),
                    "replay_rmse": float("nan"), "runtime_s": float("nan"),
                    "final_status": "error", "n_iter": 0,
                    "lambda_used": float("nan"), "solver_status": "failed",
                    "error": str(exc),
                })

    # --- Print compact comparison table ---
    # Note: 'Verif' = verification decision (per-iteration, from verifier);
    #        'Agent' = final agent status (from replanner + loop exit logic).
    # These can differ: verifier may say "weak_pass" but if max_retries is
    # exhausted the agent exits with "fail".  Both columns are shown here to
    # avoid misleading interpretation.
    print("\n" + "=" * 100)
    print("Comparison Table")
    print("=" * 100)
    header = (f"{'Case':<12} {'Label':<22} {'Solver':<12} {'Verif':<12} {'Agent':<12}"
              f" {'Flux RMSE':>10} {'Replay RMSE':>12} {'Runtime':>8}")
    print(header)
    print("-" * 100)
    for r in results:
        flux_r = f"{r['flux_rmse']:.0f}" if r['flux_rmse'] == r['flux_rmse'] else "N/A"
        rep_r = f"{r['replay_rmse']:.4f}" if r['replay_rmse'] == r['replay_rmse'] else "N/A"
        run_r = f"{r['runtime_s']:.2f}s" if r['runtime_s'] == r['runtime_s'] else "N/A"
        label = r.get("label", "")
        print(f"{r['case']:<12} {label:<22} {r['solver']:<12} {r['decision']:<12} {r['final_status']:<12}"
              f" {flux_r:>10} {rep_r:>12} {run_r:>8}")

    # --- Per-case ratio ---
    print("\nFlux RMSE ratio (TSVD / Tikhonov) per case:")
    for case_id, label, _ in available_cases:
        tik = next((r for r in results if r["case"] == case_id and r["solver"] == "tikhonov"), None)
        tsv = next((r for r in results if r["case"] == case_id and r["solver"] == "tsvd"), None)
        if tik and tsv and tik["flux_rmse"] > 0:
            ratio = tsv["flux_rmse"] / tik["flux_rmse"]
            print(f"  {case_id} [{label}]: {ratio:.2f}x (lower=better for TSVD)")

    # --- Save outputs ---
    csv_path = OUTPUT_DIR / "multi_solver_comparison.csv"
    json_path = OUTPUT_DIR / "multi_solver_comparison.json"

    fieldnames = ["case", "label", "solver", "decision", "final_status",
                  "flux_rmse", "replay_rmse", "runtime_s", "n_iter",
                  "lambda_used", "solver_status"]
    with csv_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)

    with json_path.open("w") as fh:
        json.dump(results, fh, indent=2)

    print(f"\nSaved: {csv_path}")
    print(f"Saved: {json_path}")
    print("\nValidation complete.")


def _run_synthetic_demo() -> None:
    """Fallback: run Tikhonov and TSVD on the example_case.yaml config."""
    import numpy as np

    from src.forward_model import HeatConductionFD
    from src.parser import parse_problem
    from src.planner import make_initial_plan
    from src.sensitivity import build_sensitivity_matrix
    from src.solver_registry import get_registry
    from src.verifier import VerifierThresholds, verify

    config_path = REPO_ROOT / "configs" / "example_case.yaml"
    obs_path = REPO_ROOT / "data" / "demo_temperature.csv"

    print("\nRunning synthetic demo on example_case.yaml...")
    problem = parse_problem(config_path, obs_path)
    model = HeatConductionFD(
        geometry=problem.geometry,
        material=problem.material,
        bc=problem.boundary_conditions,
        time_grid=problem.time_grid,
    )
    sensor_indices = model.sensor_indices_from_positions(problem.sensor_positions)
    y_obs = np.array(problem.observations).flatten()

    registry = get_registry()
    results = []

    for solver_name, lam in [("tikhonov", None), ("tsvd", 0.01)]:
        config = make_initial_plan(problem, {"solver_name": solver_name, "iteration_budget": 1})
        G, y_0 = build_sensitivity_matrix(problem, config, model, sensor_indices)
        y = y_obs - y_0

        if lam is None:
            from src.lambda_selector import select_lambda
            from src.regularization import build_regularization_matrix
            L = build_regularization_matrix(G.shape[1], config.reg_order)
            lam = select_lambda("discrepancy", G, L, y, problem.noise_std, None, None)

        t0 = time.perf_counter()
        result = registry.solve_single(solver_name, G, y, config, lam)
        runtime = time.perf_counter() - t0
        result.fitted_y = (y_0 + np.array(result.fitted_y)).tolist()

        v = verify(problem, config, result, thresholds=VerifierThresholds())
        results.append({
            "solver": solver_name, "lambda": lam, "decision": v.decision,
            "replay_rmse": v.replay_rmse, "runtime_s": runtime,
        })

    print(f"\n{'Solver':<12} {'Lambda':>10} {'Decision':<14} {'Replay RMSE':>12} {'Runtime':>8}")
    print("-" * 60)
    for r in results:
        print(f"{r['solver']:<12} {r['lambda']:>10.4e} {r['decision']:<14} {r['replay_rmse']:>12.4f} {r['runtime_s']:>7.3f}s")

    out_path = OUTPUT_DIR / "multi_solver_comparison.json"
    with out_path.open("w") as fh:
        json.dump(results, fh, indent=2)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
