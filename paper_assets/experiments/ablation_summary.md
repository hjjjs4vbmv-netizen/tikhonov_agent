# Ablation v1 — Key Results Summary

**Source:** `experiments/runs/ablation_v1/`  
**Cases:** 30 benchmark_v1 cases reused  
**Variants:** 7 ablation conditions vs full_agent_baseline

---

## Key numbers

| Variant | Success rate | Flux RMSE mean [W/m²] | Note |
|---------|-------------|----------------------|------|
| `full_agent_baseline` | **100%** | 5,491 | Full system (reference) |
| `no_replanner` | 86.7% | 5,391 | Replanner removed — 4 failures |
| `no_verifier` | 100%* | 5,391 | *All "pass" but verifier is bypassed; no quality gate |
| `no_bounds` | 100% | 5,491 | Physical bounds had no effect on this case set |
| `fixed_reg_order_0` | 100% | 7,287 | Identity L; 33% higher RMSE |
| `fixed_reg_order_2` | 100% | 4,749 | Best RMSE; 2nd-difference regularization |
| `fixed_lambda_ablation` | 60% | 20,119 | Fixed λ=1.0; 40% failures, 4× RMSE |

## Main findings
1. **Replanner is critical for recovery:** removing it drops success from 100% to 86.7%.
2. **Lambda selection is the most sensitive component:** fixing λ=1.0 collapses success to 60% and quadruples RMSE.
3. **Regularization order matters:** order-0 (identity) inflates RMSE by 33% vs order-1; order-2 gives marginally better RMSE but depends on replanner to handle oscillation.
4. **Physical bounds are inactive on this case set:** no cases violate the specified bounds; removing bounds has no observable effect.

## Figure assets available
- `experiments/runs/ablation_v1/figures/ablation_comparison_barplot.png`
- `experiments/runs/ablation_v1/figures/flux_error_by_variant_boxplot.png`
- `experiments/runs/ablation_v1/figures/success_failure_barplot.png`
