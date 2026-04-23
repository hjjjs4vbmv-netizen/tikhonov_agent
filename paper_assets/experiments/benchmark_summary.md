# Benchmark v1 — Key Results Summary

**Source:** `experiments/runs/benchmark_v1/`  
**Cases:** 30 synthetic cases (5 flux families × 3 noise levels × 2 seeds)  
**Flux families:** step, ramp, single_pulse, multi_pulse, smooth_sinusoid  
**Noise levels:** σ = 0.1 K, 0.5 K, 1.0 K  
**Variants compared:** fixed_solver, auto_solver, solver_plus_verifier, full_agent

---

## Key numbers

| Variant | Success rate | Flux RMSE mean [W/m²] | Flux correlation | Iterations (mean) |
|---------|-------------|----------------------|-----------------|-------------------|
| `full_agent` | **100%** | 5,491 ± 3,086 | 0.952 | 1.93 |
| `solver_plus_verifier` | 86.7% | 5,391 ± 2,818 | 0.955 | 1.00 |
| `auto_solver` | 86.7% | 5,391 ± 2,818 | 0.955 | 1.00 |
| `fixed_solver` (λ=1.0) | 10% | 20,120 ± 3,934 | 0.634 | 1.00 |

*Success rate = fraction of cases with `final_decision ∈ {pass, weak_pass}`.*
*All 30 cases × 4 variants = 120 runs.*

## Main finding
The full agent (verifier + replanner loop) achieves 100% acceptance rate vs
86.7% for single-iteration auto-lambda solve. The 4× improvement in RMSE
over fixed-lambda baseline confirms that automatic lambda selection is critical.
The replanner recovery step (absent in auto_solver/solver_plus_verifier)
accounts for the 13.3 percentage-point difference in success rate.

## Figure assets available
- `experiments/runs/benchmark_v1/figures/success_failure_barplot.png`
- `experiments/runs/benchmark_v1/figures/flux_error_by_variant_boxplot.png`
- `experiments/runs/benchmark_v1/figures/qualitative_flux_reconstruction_examples.png`
- `experiments/runs/benchmark_v1/figures/replay_error_by_noise_lineplot.png`
- `experiments/runs/benchmark_v1/figures/replanning_action_histogram.png`
- `experiments/runs/benchmark_v1/figures/lambda_vs_error_scatter.png`
