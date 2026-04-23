# Multi-Solver Pilot Note

**Purpose:** Demonstrate that the Solver Registry (v1.2) is functional and that
the same agent workflow dispatches cleanly to both Tikhonov and TSVD solvers.
This is NOT a comparative benchmark — the goal is to show multi-solver capability.

**Date:** 2026-04-23  
**Cases:** 9 benchmark_v1 cases (step, single_pulse, smooth_sinusoid; 3 noise levels each)  
**Solvers:** Tikhonov (primary, validated) and TSVD (secondary, v1.2 addition)  
**Agent configuration:** Full iteration budget (max_retries=6, iteration_budget=10)  
**TSVD settings:** fixed threshold λ=0.01 (keep singular values ≥ 1% of s_max)

---

## Results Table

| Case | Flux family | Noise [K] | Difficulty | Solver | Verif | Agent | Flux RMSE | Replay RMSE | Iters |
|------|------------|-----------|------------|--------|-------|-------|-----------|-------------|-------|
| case_0001 | step | 0.1 | easy | tikhonov | weak_pass | weak_pass | 4,886 | 0.100 | 1 |
| case_0001 | step | 0.1 | easy | tsvd | weak_pass | weak_pass | 6,044 | 0.086 | 1 |
| case_0003 | step | 0.5 | moderate | tikhonov | weak_pass | weak_pass | 7,901 | 0.505 | 1 |
| case_0003 | step | 0.5 | moderate | tsvd | weak_pass | weak_pass | 8,296 | 0.452 | 3 |
| case_0005 | step | 1.0 | hard | tikhonov | weak_pass | weak_pass | 9,853 | 1.003 | 1 |
| case_0005 | step | 1.0 | hard | tsvd | weak_pass | weak_pass | 8,615 | 0.893 | 3 |
| case_0013 | single_pulse | 0.1 | easy | tikhonov | weak_pass | weak_pass | 1,697 | 0.101 | 1 |
| case_0013 | single_pulse | 0.1 | easy | tsvd | weak_pass | weak_pass | 4,308 | 0.085 | 1 |
| case_0015 | single_pulse | 0.5 | moderate | tikhonov | weak_pass | weak_pass | 4,040 | 0.507 | 1 |
| case_0015 | single_pulse | 0.5 | moderate | tsvd | weak_pass | weak_pass | 1,993 | 0.443 | 3 |
| case_0017 | single_pulse | 1.0 | hard | tikhonov | weak_pass | weak_pass | 2,522 | 0.885 | 7 |
| case_0017 | single_pulse | 1.0 | hard | tsvd | weak_pass | weak_pass | 15,631 | 0.876 | 7 |
| case_0025 | smooth_sinusoid | 0.1 | easy | tikhonov | weak_pass | weak_pass | 3,210 | 0.100 | 1 |
| case_0025 | smooth_sinusoid | 0.1 | easy | tsvd | weak_pass | weak_pass | 4,611 | 0.085 | 1 |
| case_0027 | smooth_sinusoid | 0.5 | moderate | tikhonov | weak_pass | weak_pass | 6,126 | 0.503 | 1 |
| case_0027 | smooth_sinusoid | 0.5 | moderate | tsvd | weak_pass | weak_pass | 5,656 | 0.445 | 3 |
| case_0029 | smooth_sinusoid | 1.0 | hard | tikhonov | weak_pass | weak_pass | 9,613 | 0.998 | 1 |
| case_0029 | smooth_sinusoid | 1.0 | hard | tsvd | weak_pass | weak_pass | 6,145 | 0.887 | 3 |

*Verif = verification decision (per-iteration verifier output).*  
*Agent = final agent status after replanning loop.*  
*Flux RMSE [W/m²] vs ground-truth; Replay RMSE [K] vs observations.*

---

## Summary by Flux Family

| Flux family | Solver | Success | Flux RMSE mean | Flux RMSE std |
|-------------|--------|---------|---------------|--------------|
| step | tikhonov | 100% | 7,546 | 2,044 |
| step | tsvd | 100% | 7,651 | 1,144 |
| single_pulse | tikhonov | 100% | 2,753 | 970 |
| single_pulse | tsvd | 100% | 7,311 | 5,959 |
| smooth_sinusoid | tikhonov | 100% | 6,316 | 2,618 |
| smooth_sinusoid | tsvd | 100% | 5,471 | 640 |

---

## Observations

### Registry dispatch works correctly (primary goal)
All 18 runs completed without errors. Both solvers were dispatched through
the same `SolverRegistry` and produced `SolverResult` objects consumed by
the same verifier, replanner, and reporter. The agent framework is
solver-agnostic at the dispatch level.

### Both solvers achieve 100% acceptance rate on this pilot
Both Tikhonov and TSVD received `agent=weak_pass` on all 9 cases.
This confirms the verifier and replanner work with TSVD results.

### TSVD uses more iterations on moderate/hard cases
- Easy cases (noise=0.1): both solvers converge in 1 iteration
- Moderate/hard cases: TSVD typically takes 3 iterations, Tikhonov takes 1–7

This is expected: TSVD with a fixed threshold does not benefit from the
discrepancy-principle lambda selection, so the replanner needs more iterations
to find an acceptable truncation level.

### Flux RMSE comparison (not the primary purpose; interpret cautiously)
Mixed results — neither solver dominates uniformly:
- Tikhonov better on step (easy/moderate) and single_pulse (easy/hard)
- TSVD competitive or better on single_pulse (moderate) and smooth_sinusoid (high noise)
- High variance for TSVD on single_pulse suggests sensitivity to the fixed threshold

This comparison uses TSVD at a single fixed threshold (0.01) without tuning.
A fair comparison would require per-case threshold optimization, which is
outside the scope of this packaging pilot.

### Replay RMSE is consistent between solvers
Both solvers achieve similar replay RMSE (sensor-fit quality). This confirms
they both fit the observation data adequately; differences in flux RMSE
reflect different regularization behaviour, not observation fit failure.

---

## Interpretation for paper

This pilot demonstrates:
1. **Solver Registry pattern is functional:** `get_registry().solve_single(name, ...)` dispatches to the correct solver without changes to the agent loop.
2. **Workflow reuse is complete:** the same forward model, sensitivity matrix, verifier, replanner, and reporter work with both solvers.
3. **TSVD is a working secondary solver:** not yet tuned or benchmarked at scale, but operationally integrated.

This should be presented in the paper as an *extensibility demonstration*, not
as a comparative performance study. The validated solver remains Tikhonov.

---

## Raw data
- `experiments/runs/multi_solver_pilot/results_raw.csv` — 18 rows, per-run metrics
- `experiments/runs/multi_solver_pilot/results_summary.csv` — 6 rows, aggregated by family × solver
- `experiments/runs/multi_solver_pilot/results_raw.json` — full JSON with warnings and solver_method fields
