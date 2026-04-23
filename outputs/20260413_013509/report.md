# IHCP Inversion Report

**Date:** 2026-04-13 01:35  
**Status:** `weak_pass`  
**Iterations:** 9  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 60 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 0.3

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 2
- Lambda: `3.9891e-02`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.351872`
- Regularisation norm: `0.356513`
- Objective value: `54.055089`

### Estimated Parameters

```
  x[  0] = +63003.0732
  x[  1] = +59658.3090
  x[  2] = +56313.5370
  x[  3] = +52968.7405
  x[  4] = +49623.8969
  x[  5] = +46278.9802
  x[  6] = +42933.9650
  x[  7] = +39588.8296
  x[  8] = +36243.5594
  x[  9] = +32898.1484
  x[ 10] = +29552.6004
  x[ 11] = +26206.9279
  x[ 12] = +22861.1504
  x[ 13] = +19515.2915
  x[ 14] = +16169.3758
  x[ 15] = +12823.4261
  x[ 16] = +9477.4618
  x[ 17] = +6131.4967
  x[ 18] = +2785.5384
  x[ 19] = -560.4109
  x[ 20] = -3906.3524
  x[ 21] = -7252.2891
  x[ 22] = -10598.2237
  x[ 23] = -13944.1578
```

## Iteration Trace

**Iter 0** | λ=7.844e-08 | RMSE=0.2995 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=0.05, L1_rough=53709.0165
  - Fit marginal: rmse=0.2995, rel_err=0.0226

**Iter 1** | λ=5.106e-07 | RMSE=0.3001 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=57911.4516
  - Fit marginal: rmse=0.3001, rel_err=0.0226

**Iter 2** | λ=2.553e-06 | RMSE=0.3510 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=65249.8327
  - Fit marginal: rmse=0.3510, rel_err=0.0264

**Iter 3** | λ=1.277e-05 | RMSE=0.4167 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=6.4827 is above target=4.6669 (rel_dev=0.39)
  - Under-regularisation suspected: osc=0.00, L1_rough=74474.0375
  - Fit marginal: rmse=0.4167, rel_err=0.0314

**Iter 4** | λ=6.383e-05 | RMSE=0.4525 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=7.0388 is above target=4.6669 (rel_dev=0.51)
  - Under-regularisation suspected: osc=0.00, L1_rough=76745.0028
  - Fit marginal: rmse=0.4525, rel_err=0.0341

**Iter 5** | λ=3.191e-04 | RMSE=0.4675 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=7.2726 is above target=4.6669 (rel_dev=0.56)
  - Under-regularisation suspected: osc=0.00, L1_rough=76943.4495
  - Fit marginal: rmse=0.4675, rel_err=0.0352

**Iter 6** | λ=1.596e-03 | RMSE=0.4715 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=7.3356 is above target=4.6669 (rel_dev=0.57)
  - Under-regularisation suspected: osc=0.00, L1_rough=76948.4525
  - Fit marginal: rmse=0.4715, rel_err=0.0355

**Iter 7** | λ=7.978e-03 | RMSE=0.4724 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=7.3491 is above target=4.6669 (rel_dev=0.57)
  - Under-regularisation suspected: osc=0.00, L1_rough=76947.5046
  - Fit marginal: rmse=0.4724, rel_err=0.0356

**Iter 8** | λ=3.989e-02 | RMSE=0.4726 | under_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=7.3519 is above target=4.6669 (rel_dev=0.58)
  - Under-regularisation suspected: osc=0.00, L1_rough=76947.2310
  - Fit marginal: rmse=0.4726, rel_err=0.0356

## Notes

- Completed in 9 iteration(s)
