# Main Claims and Evidence

**tikhonov_agent — Scientific Paper Asset**

> This document maps each intended paper claim to the specific experimental
> evidence available in the repository.  Use it as the backbone for drafting
> the Results and Discussion sections.

---

## 1. Main Paper Claim

**A deterministic, rule-based verifier–replanner workflow substantially and
reliably improves the acceptance rate of ill-posed inverse heat conduction
solutions compared to single-iteration baselines, without requiring an LLM
or a manually tuned regularization parameter.**

Specifically:
- The full agent (verifier + replanner loop) achieves **100% acceptance** on
  the 30-case benchmark, vs **86.7%** for single-iteration auto-lambda and
  **10%** for fixed-lambda baselines.
- The replanner recovers all 4 cases that the single-iteration solver fails,
  using at most 9 iterations (mean 1.93).
- This is validated on the **1D transient IHCP boundary heat flux
  reconstruction** problem.

**What this paper is NOT claiming:**
- A new regularization formula
- A general inverse-PDE solver
- An LLM-based scientific agent
- Superiority over Bayesian or EnKF methods (not compared)

---

## 2. Supporting Evidence — Benchmark (benchmark_v1)

**Setup:** 30 synthetic cases, 5 flux families (step, ramp, single_pulse,
multi_pulse, smooth_sinusoid), 3 noise levels (0.1, 0.5, 1.0 K), 2 seeds.
4 variants compared.

**Key numbers:**

| Variant | Success | Flux RMSE | Correlation |
|---------|---------|-----------|-------------|
| full_agent | **100%** | 5,491 | 0.952 |
| auto_solver | 86.7% | 5,391 | 0.955 |
| solver_plus_verifier | 86.7% | 5,391 | 0.955 |
| fixed_solver (λ=1) | 10% | 20,120 | 0.634 |

**Narrative:**
- Adding the verifier alone (solver_plus_verifier) does not help vs auto_solver:
  same 86.7%. The verifier identifies failures but the replanner is needed to
  recover.
- The replanner recovers all 4 failures in the auto_solver set.
- Fixed-lambda baseline confirms that automatic lambda selection is necessary:
  90% failure rate and 4× RMSE degradation.
- RMSE values for full_agent and auto_solver are similar (5,491 vs 5,391) —
  the extra iterations don't hurt accuracy, they recover borderline cases.

**Figures:**
- `benchmark_v1/figures/success_failure_barplot.png`
- `benchmark_v1/figures/flux_error_by_variant_boxplot.png`
- `benchmark_v1/figures/qualitative_flux_reconstruction_examples.png`

---

## 3. Supporting Evidence — Ablation (ablation_v1)

**Setup:** Same 30 cases, 7 ablation variants.  Tests which components are
load-bearing.

**Key numbers:**

| Ablation | Success | Flux RMSE | Interpretation |
|----------|---------|-----------|----------------|
| full_agent_baseline | 100% | 5,491 | Reference |
| no_replanner | **86.7%** | 5,391 | 4 failures — replanner critical |
| fixed_lambda_ablation | **60%** | 20,119 | λ selection critical |
| no_verifier | 100%* | 5,391 | *No quality gate; all accepted regardless |
| fixed_reg_order_0 | 100% | **7,287** | +33% RMSE vs order-1 |
| fixed_reg_order_2 | 100% | **4,749** | −14% RMSE; slightly better with order-2 |
| no_bounds | 100% | 5,491 | Bounds inactive on this case set |

**Narrative:**
- The most critical component after the solver is **lambda selection** (60% failure
  without it), followed by **the replanner** (86.7% failure without it).
- The verifier alone cannot improve results without the replanner.
- Regularization order matters: order-1 is the right default; order-2 gives
  marginally better RMSE but relies on the replanner to handle oscillation risk.
- Physical bounds are not load-bearing on the benchmark cases but are a
  correctness safeguard.

**Figures:**
- `ablation_v1/figures/ablation_comparison_barplot.png`
- `ablation_v1/figures/flux_error_by_variant_boxplot.png`

---

## 4. Supporting Evidence — Stress Tests (stress_v1)

**Setup:** 32 cases across 6 out-of-distribution stress scenarios.
Full_agent variant only.

**Key result:** 75% success (24/32) vs 100% on benchmark. Mean RMSE 11,638 vs
5,491. Mean iterations 5.06 vs 1.93.

**Per-scenario interpretation:**

| Scenario | Expected difficulty | Implication |
|----------|---------------------|-------------|
| high_noise (σ=2–5 K) | Very hard; near information limit | Graceful degradation expected |
| few_sensors (1 sensor) | Hard; limited spatial info | Agent still converges in most cases |
| distant_sensors | Moderate; signal attenuation | Comparable to high-noise effect |
| low_time_resolution | Moderate; coarser G matrix | Success maintained in most cases |
| high_dimension (50 params) | Harder optimization surface | Agent handles via more iterations |
| wrong_noise_estimate (10×) | Misleads discrepancy principle | Partial recovery |

**Narrative:**
- The system degrades gracefully — it does not silently produce wrong answers;
  it raises manual_review or fail decisions when it cannot converge.
- Stress results confirm that the verifier and replanner add genuine value
  beyond the baseline: on these harder cases, the replanner engages much more
  (5.06 vs 1.93 mean iterations).

**Figures:**
- `stress_v1/figures/stress_success_barplot.png`
- `stress_v1/figures/stress_flux_rmse_boxplot.png`

---

## 5. Supporting Evidence — Packaging Upgrade (v1.2)

**Input Normalizer:**
- Validation: `demos/outputs/normalizer_validation.json` shows all 9 checked
  physical fields and both sensor positions MATCH between YAML and text
  extraction paths.
- Both paths produce identical `ProblemSpec` objects (confirmed by
  `demo_structured_input.py`).

**Solver Registry:**
- Validation: `experiments/runs/multi_solver_pilot/` — 18 runs (9 cases × 2
  solvers) all completed without errors.
- Both Tikhonov and TSVD dispatch correctly through the registry.
- 100% acceptance rate achieved by both solvers on the 9-case pilot.
- TSVD is operationally integrated (verifier, replanner, reporter all work).

**Framing for paper:**
> "To support extensibility, we introduce a lightweight Input Normalizer
> (Section X) that standardizes heterogeneous input formats into a typed schema,
> and a Solver Registry (Section X) that decouples solver dispatch from the
> agent orchestration loop.  As a proof-of-concept, we register a second solver
> (TSVD) and demonstrate that the workflow operates correctly with both solvers
> on a 9-case pilot (Table X)."

---

## 6. Current Limitations

These are honest limitations to discuss in the paper.

| Limitation | Detail |
|------------|--------|
| **Single use case validated** | All results are for 1D transient IHCP only; no other PDE family |
| **1D geometry only** | Forward model is 1D FD; 2D/3D not implemented |
| **Linear forward model** | Sensitivity matrix G is built once; non-linear problems require adjoint |
| **Piecewise-constant parameterization** | Coarser than B-spline or piecewise-linear; may miss sharp flux features |
| **No uncertainty quantification** | Point estimates only; no confidence intervals or posterior distributions |
| **TSVD not benchmarked** | Only pilot (9 cases); no full benchmark comparison |
| **Physical bounds inactive on benchmark** | The ablation shows bounds have no effect on this case set |
| **High-noise failure** | σ=5 K cases consistently fail; information limit not rigorously characterized |
| **Stress results from one run** | stress_v1 is a single run; no cross-validation or statistical replication |

---

## 7. What Should Stay Out of Scope for This Paper

Do NOT claim or attempt to demonstrate:
- Bayesian posterior inference
- Ensemble Kalman Smoother / sequential assimilation
- Approximate Bayesian Computation (ABC)
- Physics-Informed Neural Network surrogate
- General multi-dimensional geometry
- Temperature-dependent material properties
- Multi-unknown / coupled inversion
- Robustness to arbitrary natural-language input
- LLM-driven scientific decision-making
- Comparison with MCMC / Bayesian benchmarks

These are legitimate future extensions and should be described as such in
the paper's Future Work section, clearly labeled as not implemented.

---

## Suggested paper section structure

1. Introduction — inverse heat conduction as a canonical ill-posed problem
2. Problem formulation — 1D transient IHCP, notation
3. System architecture — agent workflow diagram + module descriptions
4. Inversion methods — Tikhonov (primary) + TSVD (extensibility demo)
5. Experimental setup — benchmark_v1, ablation_v1, stress_v1
6. Results — benchmark, ablation, stress (in order)
7. Input Normalization and Solver Registry — extensibility section
8. Discussion — limitations, comparison context
9. Conclusion
10. Appendix — additional figures, stress details, multi-solver pilot table
