# PINN Recovery Pilot v2 — Admission Test Report

*Generated: 2026-05-04 11:35:27*

## 1. Environment

- Python: 3.12.3
- PyTorch: 2.10.0+cu128
- CUDA: 12.8
- GPU: NVIDIA GeForce RTX 5090
- DeepXDE: 1.15.0  backend=pytorch
- GPU actually used: True

## 2. Training Schedule

- Stage 1: Adam 20000 iters, lr=0.001 (cosine decay)
- Stage 2: L-BFGS ≤400 closures, strong-Wolfe
- Network: [64, 64, 64, 64]  (tanh activations, Xavier init)
- Collocation: 900 PDE, 120 BC, 200 IC

## 3. Recovery Strategies

| Strategy | Status | Details |
|----------|--------|---------|
| A: Boundary-biased sensors | **Enabled** | x ∈ {0.01, 0.05, 0.10}·Lx, 9 sensors |
| B: Stronger flux BC weight | **Enabled** | w_bc_flux = 500.0 |
| C: Normalized loss balancing | **Enabled** | divide each component by initial scale |
| D: Tikhonov warm start | **Enabled** | λ=1e-3, fit via normal equations |
| E: Fourier basis q | **Enabled** | 8×8 cosine modes = 64 coefficients |
| F: Two-stage training | **Enabled** | Adam 20000k + L-BFGS |

## 4. Sensor Layouts Used

- `medium`: standard 3×3 grid, x ∈ [0.1·Lx, 0.9·Lx]
- `boundary_biased`: 3×3 grid, x ∈ {0.01, 0.05, 0.10}·Lx

## 5. Case-by-Case Metrics

### Previous pilot (v1 — failed)
| Case | flux_rmse | replay_rmse | ssim_flux | support_overlap |
|------|-----------|-------------|-----------|-----------------|
| gaussian_localized   | 272.39 | 0.0822 | 0.000658 | 0.0000 |
| overlapping_multi_spot | 339.83 | 0.0813 | 0.001097 | 0.0000 |

### Recovery pilot v2
| Case | Layout | flux_rmse | replay_rmse | ssim_flux | support_overlap | q_max | collapsed | runtime |
|------|--------|-----------|-------------|-----------|-----------------|-------|-----------|---------|
| case1_gaussian_boundary_biased | boundary_biased | 143.29 | 0.2035 | 0.784755 | 0.756757 | 603.6 | False | 574s |
| case2_multi_spot_boundary_bias | boundary_biased | 203.88 | 0.7808 | 0.713156 | 0.746269 | 770.5 | False | 635s |

## 6. Comparison vs Benchmark-Ready Solvers

*(On gaussian_localized medium, σ=0.1 K — from benchmark_2d_v2_results.csv)*
| Solver | flux_rmse | notes |
|--------|-----------|-------|
| tikhonov_2d | ~224 | benchmark-ready |
| tsvd_2d | ~134 | benchmark-ready |
| deepxde_2d (sensitivity) | ~164 | benchmark-ready |
| **deepxde_pinn (v1)** | **272** | **failed — q≈0** |
| **deepxde_pinn (v2)** | **143.3** | **recovery pilot** |

## 7. Admission Decision

**Verdict: ADMITTED**

```
======================================================================
PINN ADMISSION DECISION
======================================================================
Case results:
  case1_gaussian_boundary_biased (boundary_biased): flux_rmse=143.3 (prev 272.4)  SSIM=0.7848  supp=0.7568  q_max=603.6  collapsed=False → FULL
  case2_multi_spot_boundary_biased (boundary_biased): flux_rmse=203.9 (prev 339.8)  SSIM=0.7132  supp=0.7463  q_max=770.5  collapsed=False → FULL

Admitted cases:     2/2
Conditional cases:  0/2
Failed cases:       0/2

VERDICT: ADMITTED

Reasoning: PINN recovers nontrivial q(y,t) with material structure. Flux metrics are in a credible range and performance exceeds temperature-replay-only trivial solution.
======================================================================
```

## 8. Next Recommended Actions

- Include deepxde_pinn in full benchmark suite with recovery config
- Run stress-track cases (noise=0.5K, harder families)
- Document required hyperparameters in solver registry

## 9. Output Files

- `reports/pinn_recovery_pilot_v2/raw_results.csv`
- `reports/pinn_recovery_pilot_v2/config_used.yaml`
- `reports/pinn_recovery_pilot_v2/training_log_case1.txt`
- `reports/pinn_recovery_pilot_v2/training_log_case2.txt`
- `figures/pinn_recovery_pilot_v2/` (all figures)