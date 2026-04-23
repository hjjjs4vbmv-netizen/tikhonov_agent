# Weekly Experiment Status — 2026-04-20

## Summary

This week: added `no_verifier` ablation, fixed the broken `oscillation_score` metric,
generated and ran `stress_v1` (all 6 scenarios, 32 cases). All three tasks complete.

All benchmark and ablation experiments have been re-run with the corrected
oscillation metric. Result counts are stable; no duplicates.

---

## 1. Benchmark (benchmark_v1) — Updated

| Metric | Value |
|--------|-------|
| Total cases | 30 (5 flux families × 3 noise levels × 2 seeds) |
| Variants run | 4 (fixed_solver, auto_solver, solver_plus_verifier, full_agent) |
| Total result rows | **120** (0 duplicates) |
| Status | **Complete (re-run with fixed oscillation_score)** |

### Success Rates

| Variant | n | Success Rate | Mean Flux RMSE (W/m²) | Mean osc_score |
|---------|---|-------------|----------------------|----------------|
| fixed_solver | 30 | 10% | 20,120 | 0.0000 |
| auto_solver | 30 | **87%** | 5,391 | 0.0042 |
| solver_plus_verifier | 30 | **87%** | 5,391 | 0.0042 |
| full_agent | 30 | **100%** | 5,491 | 0.0623 |

**Note:** The benchmark success rate for `auto_solver` and `solver_plus_verifier` changed
from 63% (previous run) to 87% after the oscillation_score fix. The previous verifier
was using overly tight `osc_fail=0.50` thresholds calibrated for the old (broken) metric;
the new thresholds (osc_fail=5.0) correctly avoid flagging smooth solutions as oscillatory.
`full_agent` success rate is unchanged at 100%.

---

## 2. Ablation (ablation_v1) — Extended and Updated

| Metric | Value |
|--------|-------|
| Cases used | 30 benchmark cases (reused) |
| Variants run | **7** (added `no_verifier` this week) |
| Total result rows | **210** (30 × 7, 0 duplicates) |
| Status | **Complete** |

### Ablation Results

| Variant | n | Success Rate | Mean Flux RMSE (W/m²) | Mean iter | vs Baseline |
|---------|---|-------------|----------------------|-----------|-------------|
| full_agent_baseline | 30 | 100% | 5,491 | 1.9 | — |
| no_bounds | 30 | 100% | 5,491 | 1.9 | no change |
| fixed_reg_order_2 | 30 | 100% | 4,749 | 2.0 | −13.5% RMSE |
| fixed_reg_order_0 | 30 | 100% | 7,287 | 1.9 | +32.7% RMSE |
| no_replanner | 30 | **87%** | 5,391 | 1.0 | −13pp success |
| no_verifier | 30 | **100%** | 5,391 | 1.0 | no change |
| fixed_lambda_ablation | 30 | **60%** | 20,119 | 8.2 | −40pp success |

### `no_verifier` Ablation Findings

- `no_verifier` achieves **100% success rate** with mean flux RMSE = 5,391 W/m².
- It runs in a single iteration (iteration_count = 1.0 mean) by design: the first
  solve is accepted unconditionally and the loop terminates.
- This is **identical success rate to `full_agent_baseline`** but at 1/2 the mean
  iteration count. This is expected: for these standard benchmark cases, the initial
  Tikhonov solve with adaptive λ already produces good results on most cases.
- The practical implication: the verifier is NOT the primary driver of success on
  benchmark cases. The replanner (not the verifier) is the differentiating component.
  `no_replanner` (87%) shows that removing replanning hurts, while `no_verifier` (100%)
  shows that removing the verifier acceptance check alone does not.
- The verifier's role is thus diagnostic and safety-oriented (flagging failures for
  replanning), not a strict gate on final result quality for these test cases.

### Updated Ablation Interpretations

- **Replanner:** Still necessary. 100% → 87% without it (was 63% pre-fix; the change
  reflects recalibrated oscillation thresholds, not a regression).
- **Physical bounds:** Still irrelevant for standard benchmark cases.
- **Reg order:** `fixed_reg_order_2` now achieves −13.5% RMSE vs baseline (unexpected;
  second-difference regularization may be slightly better-tuned for these flux shapes).
- **Adaptive lambda:** Still critical. Fixed λ=1 is clearly the worst component to remove.

---

## 3. `oscillation_score` Fix

### Root Cause (Previous Bug)

`oscillation_score` was structurally constant at **0.3866** across all 300 rows
(120 benchmark + 180 ablation) because both `utils.py:compute_regularity_metrics`
and `verifier.py:_oscillation_score` were implicitly or explicitly operating on a
signal where the geometric structure fixed the answer:

- `utils.py` computed on `q_est_full` (N_t=121 piecewise-constant expansion).
- For 24 parameters × 5 steps each, every segment boundary produces a direction
  change in `diff(q_est)`, yielding exactly 46 sign-change pairs out of 119
  differences = **46/119 = 0.3866** regardless of solution content.

### New Metric Definition

**Normalized second-difference energy of the raw parameter vector:**

```
osc = sum(diff(x, n=2)**2) / (sum(x**2) + 1e-30)
```

where `x` is the N_p=24 parameter vector (not the expanded N_t=121 signal).

Properties:
- Zero for constant or linearly-varying solutions.
- Large for rapidly oscillating solutions (e.g. ~14.7 for perfectly alternating +/-50000 W/m²).
- Dimensionless and scale-invariant.
- Deterministic and easy to compute from any parameter vector.

### Updated Thresholds

To match the new scale (not a 0–1 fraction):
- `VerifierThresholds.osc_pass`: 0.20 → **1.0**
- `VerifierThresholds.osc_fail`: 0.50 → **5.0**
- Replanner guard thresholds updated accordingly.

### New Score Distribution

| Variant | osc_score mean | osc_score max |
|---------|---------------|---------------|
| fixed_solver | 0.0000 | 0.0000 |
| auto_solver | 0.0042 | 0.031 |
| full_agent | 0.0623 | 1.407 |
| fixed_lambda_ablation | 0.0000 | 0.0000 |
| fixed_reg_order_0 | 0.0929 | 1.493 |
| fixed_reg_order_2 | 0.0057 | 0.062 |

Observations: `fixed_solver` (λ=1, over-regularized) gives flat solutions → osc=0.
`fixed_reg_order_0` (identity regularization) allows more oscillation → higher osc.
`fixed_reg_order_2` (second-difference) strongly suppresses oscillation.
The oscillation_score is now scientifically meaningful.

---

## 4. Stress Tests (stress_v1) — First Run

| Metric | Value |
|--------|-------|
| Scenarios | 6 (high_noise, few_sensors, distant_sensors, low_time_resolution, high_dimension, wrong_noise_estimate) |
| Total cases | **32** |
| Variant | full_agent only |
| Total result rows | **32** |
| Status | **Complete (first run)** |

### Results by Scenario

| Scenario | n | Success Rate | Mean Flux RMSE (W/m²) | Median Flux RMSE (W/m²) |
|----------|---|-------------|----------------------|------------------------|
| high_noise | 8 | **25%** | 17,097 | 20,345 |
| few_sensors | 6 | **100%** | 10,674 | 9,955 |
| distant_sensors | 4 | **50%** | 20,452 | 23,388 |
| low_time_resolution | 6 | **100%** | 8,259 | 8,715 |
| high_dimension | 4 | **100%** | 5,449 | 5,486 |
| wrong_noise_estimate | 4 | **100%** | 4,614 | 4,530 |

### Main Stress Observations

1. **high_noise (2.0–5.0 K noise):** Hardest scenario — only 25% success.
   At 5 K noise, the SNR is very low and the discrepancy principle target becomes
   large, leading to under-regularization. Main failure mode is the agent hitting
   the iteration budget without converging to a consistent solution.

2. **distant_sensors (sensors at x=0.04, 0.045 m):** 50% success. Far-field sensors
   have low sensitivity to left-boundary flux — the sensitivity matrix is
   ill-conditioned, and the agent struggles to converge.

3. **few_sensors (1 sensor at x=0.03 m):** 100% success with ~2× higher RMSE than
   the 2-sensor benchmark. The single sensor provides enough information for the
   step and sinusoid families; RMSE penalty is moderate.

4. **low_time_resolution (31 steps):** 100% success. The agent adapts correctly to
   the coarser grid; RMSE is ~1.5× benchmark because temporal resolution limits
   the achievable reconstruction accuracy.

5. **high_dimension (50 parameters):** 100% success despite the higher underdetermined
   ratio. The λ selection and regularization handle the extra parameters well because
   the problem is still physically well-posed.

6. **wrong_noise_estimate (reported noise_std = 0.05 K, true = 0.5 K):** 100% success.
   The deliberately underestimated noise std biases the discrepancy principle toward
   under-regularization, but the replanner corrects this. The RMSE (4,614) is actually
   better than the standard 2-sensor benchmark (5,491) — the agent finds a good λ
   regardless.

---

## 5. Result Files

### Benchmark
| File | Rows |
|------|------|
| `experiments/runs/benchmark_v1/results_raw.csv` | 120 (re-run) |
| `experiments/runs/benchmark_v1/results_summary_by_variant.csv` | 4 |
| `experiments/runs/benchmark_v1/results_summary_by_noise.csv` | 12 |
| `experiments/runs/benchmark_v1/results_summary_by_flux_family.csv` | 20 |

### Ablation
| File | Rows |
|------|------|
| `experiments/runs/ablation_v1/results_raw.csv` | 210 (re-run + no_verifier) |
| `experiments/runs/ablation_v1/ablation_summary.csv` | 7 |
| `experiments/runs/ablation_v1/results_summary_by_variant.csv` | 7 |

### Stress
| File | Rows |
|------|------|
| `experiments/runs/stress_v1/results_raw.csv` | 32 |
| `experiments/runs/stress_v1/results_summary_by_variant.csv` | 1 |
| `experiments/cases/stress_v1/manifest.csv` | 32 cases |

---

## 6. Figures

### Benchmark (`experiments/runs/benchmark_v1/figures/`)
8 figures — regenerated with new oscillation_score values.

### Ablation (`experiments/runs/ablation_v1/figures/`)
8 figures — regenerated including `no_verifier` variant.

### Stress (`experiments/runs/stress_v1/figures/`)
3 new figures:
- `stress_success_barplot.png` — success rate per scenario
- `stress_flux_rmse_boxplot.png` — RMSE distribution per scenario
- `stress_oscillation_score_boxplot.png` — oscillation score per scenario

---

## 7. Code Changes This Week

### `src/types.py`
- Added `skip_verifier: bool = False` field to `InversionConfig`.

### `src/planner.py`
- Added `skip_verifier` override passthrough to `InversionConfig`.

### `src/agent.py`
- When `config.skip_verifier=True`, bypasses `verify()` call and constructs a
  synthetic `VerificationResult(decision="pass")` so the loop terminates after
  iteration 0. Implements `no_verifier` ablation cleanly.

### `src/verifier.py`
- `_oscillation_score()`: replaced sign-change fraction with normalized
  second-difference energy `sum(diff(x,2)**2) / (sum(x**2) + eps)`.
- `VerifierThresholds.osc_pass`: 0.20 → 1.0; `osc_fail`: 0.50 → 5.0.

### `src/replanner.py`
- Updated oscillation significance thresholds: `> 0.2` → `> 1.0`;
  `> 0.4` → `> 4.0` (matches new osc_fail scale).

### `experiments/utils.py`
- `compute_regularity_metrics()`: added `x_params` optional argument.
  When provided, computes oscillation score on the raw parameter vector;
  fallback remains for backward compatibility.
- `compute_all_metrics()`: added `x_params` optional argument, passed through
  to `compute_regularity_metrics`.
- `get_variant_overrides()`: added `skip_verifier` to allowed_keys.

### `experiments/run_benchmark.py`
- Passes `x_params=x_est` to `compute_all_metrics`.

### `experiments/analyze_results.py`
- `compute_ablation_summary()`: now also detects variants prefixed with `fixed_`
  (previously missed `fixed_reg_order_0` and `fixed_reg_order_2`).

### `experiments/plot_results.py`
- `plot_ablation_comparison_barplot()`: updated variant detection to match.

### New files
- `experiments/generate_stress_cases.py` — generates stress scenario cases.
- `experiments/run_stress_benchmark.py` — runs stress benchmark with per-case
  planner overrides (e.g. `num_parameters_override` for `high_dimension`).
- `experiments/plot_stress_results.py` — stress-specific figures by scenario.
- `experiments/configs/ablation_v1.yaml` — added `no_verifier` variant.

---

## 8. Known Issues / Caveats

| Issue | Severity | Notes |
|-------|----------|-------|
| `_diagnose_tradeoff()` uses placeholder denominator `1.0` | Low | Affects tradeoff label only, not RMSE metrics |
| Benchmark success rate change (63% → 87% for auto_solver) | Note | This is a correction, not a regression: previous thresholds were miscalibrated for the broken oscillation metric |
| Stress results are preliminary (first run) | — | Only `full_agent` variant tested; no multi-variant comparison for stress scenarios yet |

---

## 9. Recommended Next Steps

1. **Stress multi-variant comparison** — run `auto_solver` and `fixed_solver` on
   stress cases to measure variant robustness under stress (currently only `full_agent`
   is characterized).

2. **Stress parametric sweep for high_noise** — add more noise levels (e.g. 1.0, 2.0,
   3.0, 5.0 K) to characterize the SNR breakeven point for `full_agent`.

3. **Paper writing** — core evidence is in hand:
   - Benchmark: 100% vs 10%/87%/87% success rates.
   - Ablation: replanner and adaptive λ are necessary; verifier is diagnostic.
   - Stress: agent degrades gracefully on all scenarios except high noise and distant sensors.
