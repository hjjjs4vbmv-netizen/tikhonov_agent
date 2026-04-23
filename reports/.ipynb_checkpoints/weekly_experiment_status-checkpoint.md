# Weekly Experiment Status — 2026-04-14

## Summary

All benchmark and core ablation experiments are complete and results are clean.

---

## 1. Benchmark (benchmark_v1)

| Metric | Value |
|--------|-------|
| Total cases | 30 (5 flux families × 3 noise levels × 2 seeds) |
| Variants run | 4 (fixed_solver, auto_solver, solver_plus_verifier, full_agent) |
| Total result rows | **120** (30 × 4, 0 duplicates) |
| Status | **Complete** |

### Success Rates and Median Flux RMSE

| Variant | n | Success Rate | Median Flux RMSE (W/m²) |
|---------|---|-------------|------------------------|
| fixed_solver | 30 | 10% | 21,284 |
| auto_solver | 30 | 63% | 4,825 |
| solver_plus_verifier | 30 | 63% | 4,825 |
| full_agent | 30 | **100%** | 6,004 |

**Key finding:** `full_agent` achieves 100% success rate across all 30 cases.
`fixed_solver` (naive λ=1) fails on 90% of cases. `auto_solver` and
`solver_plus_verifier` are identical in success rate — the verifier alone (without
replanning) does not improve success rate, but full replanning loop achieves full
coverage.

---

## 2. Ablation (ablation_v1)

| Metric | Value |
|--------|-------|
| Cases used | 30 benchmark cases (all families × noise levels × seeds) |
| Variants run | 6 (full_agent_baseline, no_replanner, no_bounds, fixed_reg_order_0, fixed_reg_order_2, fixed_lambda_ablation) |
| Total result rows | **180** (30 × 6, 0 duplicates) |
| Status | **Complete** |

### Ablation Results

| Variant | n | Success Rate | Median Flux RMSE (W/m²) | vs Baseline |
|---------|---|-------------|------------------------|-------------|
| full_agent_baseline | 30 | 100% | 6,004 | — |
| no_bounds | 30 | 100% | 6,004 | no change |
| fixed_reg_order_2 | 30 | 100% | 6,028 | +0.4% |
| fixed_reg_order_0 | 30 | 100% | 6,383 | +6.3% |
| no_replanner | 30 | 63% | 4,825 | success ↓37pp †|
| fixed_lambda_ablation | 30 | 60% | 21,277 | success ↓40pp |

**Answers to ablation questions:**
- **Is replanner necessary?** Yes — removing it drops success from 100% → 63%. Note: the median flux RMSE for `no_replanner` (4,825) is lower than the baseline (6,004) because the 11 failed cases are not excluded from the median — they just happen to have moderate RMSE values (median ~4,886 even for failures). The correct reliability metric is success rate, where the replanner is clearly necessary.
- **Do physical bounds matter?** No — `no_bounds` produces identical results (the test problem's flux is well-behaved within bounds).
- **Does reg_order adaptation matter?** Moderately — fixed order 0 adds +6.3% RMSE vs adaptive, fixed order 2 adds only +0.4%.
- **Is adaptive lambda necessary?** Yes — fixed λ=1 drops success to 60% with 3.5× higher RMSE.

† `no_replanner` has a lower median flux RMSE (4,825) than the baseline (6,004) because it uses a single-shot solve (iteration_budget=1), which is identical to `auto_solver`. The 37% failure rate means those cases produce unreliable results with no recovery path. Compare on success rate, not median RMSE alone.

---

## 3. Result Files

### Benchmark
| File | Status |
|------|--------|
| `experiments/runs/benchmark_v1/results_raw.csv` | ✓ 120 rows, 0 duplicates |
| `experiments/runs/benchmark_v1/results_summary_by_variant.csv` | ✓ 4 rows |
| `experiments/runs/benchmark_v1/results_summary_by_noise.csv` | ✓ 12 rows |
| `experiments/runs/benchmark_v1/results_summary_by_flux_family.csv` | ✓ 20 rows |

### Ablation
| File | Status |
|------|--------|
| `experiments/runs/ablation_v1/results_raw.csv` | ✓ 180 rows, 0 duplicates |
| `experiments/runs/ablation_v1/ablation_summary.csv` | ✓ 6 rows |

---

## 4. Figures

All 8 required figures generated in `experiments/runs/benchmark_v1/figures/`:

| Figure | File |
|--------|------|
| Success/failure rates | `success_failure_barplot.png` |
| Flux error by variant | `flux_error_by_variant_boxplot.png` |
| Replay error vs noise | `replay_error_by_noise_lineplot.png` |
| Flux reconstruction examples | `qualitative_flux_reconstruction_examples.png` |
| Temperature replay examples | `qualitative_temperature_replay_examples.png` |
| Replanning action counts | `replanning_action_histogram.png` |
| λ vs flux error scatter | `lambda_vs_error_scatter.png` |
| Ablation comparison | `ablation_comparison_barplot.png` |

Ablation-specific figures also generated in `experiments/runs/ablation_v1/figures/`.

---

## 5. Code Patches Applied

### `experiments/utils.py` — `save_result_row()`
**Problem:** The original implementation blindly appended rows, causing duplicates
when experiments were re-run.

**Fix:** Changed to an upsert pattern — reads existing CSV, removes any row with the
same `(case_id, variant_name)` key, then writes the updated DataFrame back.
Prevents silent accumulation of duplicate rows in all future runs.

---

## 6. Known Issues / Caveats

| Issue | Severity | Notes |
|-------|----------|-------|
| `oscillation_score` column is structurally fixed at 0.3866 for **all 120 benchmark rows** and all 180 ablation rows | Medium | Root cause: the metric is computed on the piecewise-constant expanded flux (N_t=121, n_params=24), where segment boundaries always produce 46 sign-change pairs out of 119 differences (46/119 = 0.3866). This is a geometric property of the parametrization, not of solution quality. The column carries zero information and must be excluded from any supervisor table or figure. |
| `verifier._diagnose_tradeoff()` uses placeholder denominator `1.0` | Low | Affects tradeoff label classification but not final RMSE metrics |
| `no_verifier` ablation not in ablation_v1.yaml | Low | The task spec listed it as a priority, but `ablation_v1.yaml` was never updated to include it. All 6 variants that *are* in the config have been run. Adding `no_verifier` requires an edit to `ablation_v1.yaml` and a re-run. |
| `stress_v1` not yet generated or run | — | Deferred to next week as planned |

---

## 7. Recommended Next Step

**stress_v1:** Generate the 6 stress-test scenarios (high_noise, few_sensors,
distant_sensors, low_time_resolution, high_dimension, wrong_noise_estimate) using
`generate_cases.py --config experiments/configs/stress_v1.yaml`, then run with
`run_benchmark.py --config experiments/configs/stress_v1.yaml`.

These cases test edge cases beyond the standard benchmark and will complete the
planned experimental coverage before final write-up.
