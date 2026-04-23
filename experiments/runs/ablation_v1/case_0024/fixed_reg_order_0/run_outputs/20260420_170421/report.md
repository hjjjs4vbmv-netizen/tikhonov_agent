# IHCP Inversion Report

**Date:** 2026-04-20 17:04  
**Status:** `weak_pass`  
**Iterations:** 9  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 1.0

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 2
- Lambda: `1.9668e-10`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `14.798073`
- Regularisation norm: `104636.412061`
- Objective value: `221.136337`

### Estimated Parameters

```
  x[  0] = +8028.4100
  x[  1] = -3696.8205
  x[  2] = +12494.6658
  x[  3] = +27422.8283
  x[  4] = +40114.7893
  x[  5] = +32370.9299
  x[  6] = +58019.5775
  x[  7] = +43780.0647
  x[  8] = +26696.8089
  x[  9] = +26720.7319
  x[ 10] = +27298.1313
  x[ 11] = +49551.5677
  x[ 12] = +59177.5579
  x[ 13] = +54467.0846
  x[ 14] = +30091.6696
  x[ 15] = +20179.9459
  x[ 16] = +35737.6627
  x[ 17] = +55903.3445
  x[ 18] = +42589.0400
  x[ 19] = +43039.3236
  x[ 20] = +33247.3320
  x[ 21] = -2435.7033
  x[ 22] = -10813.3134
  x[ 23] = +23308.0356
```

## Iteration Trace

**Iter 0** | λ=1.259e-08 | RMSE=1.0030 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.02, L1_rough=109800.9775
  - Fit marginal: rmse=1.0030, rel_err=0.0543

**Iter 1** | λ=6.294e-09 | RMSE=0.9750 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.06, L1_rough=147521.2032
  - Fit marginal: rmse=0.9750, rel_err=0.0528

**Iter 2** | λ=3.147e-09 | RMSE=0.9614 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.17, L1_rough=212136.3419
  - Fit marginal: rmse=0.9614, rel_err=0.0521

**Iter 3** | λ=1.573e-09 | RMSE=0.9533 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.45, L1_rough=306414.6188
  - Fit marginal: rmse=0.9533, rel_err=0.0516

**Iter 4** | λ=7.867e-10 | RMSE=0.9471 | under_regularized | → switch_reg_order_to_1
  - Under-regularisation suspected: osc=1.09, L1_rough=441637.4301
  - Fit marginal: rmse=0.9471, rel_err=0.0513

**Iter 5** | λ=7.867e-10 | RMSE=0.9537 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.24, L1_rough=273371.4491
  - Fit marginal: rmse=0.9537, rel_err=0.0517

**Iter 6** | λ=3.934e-10 | RMSE=0.9495 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.55, L1_rough=366074.8462
  - Fit marginal: rmse=0.9495, rel_err=0.0514

**Iter 7** | λ=1.967e-10 | RMSE=0.9450 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=1.22, L1_rough=496214.4797
  - Fit marginal: rmse=0.9450, rel_err=0.0512

**Iter 8** | λ=1.967e-10 | RMSE=0.9513 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.35, L1_rough=329192.4493
  - Fit marginal: rmse=0.9513, rel_err=0.0515

## Notes

- Completed in 9 iteration(s)
