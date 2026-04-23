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
- Residual norm: `14.800146`
- Regularisation norm: `96051.031442`
- Objective value: `220.858813`

### Estimated Parameters

```
  x[  0] = +17049.5196
  x[  1] = +7530.3716
  x[  2] = +23497.5324
  x[  3] = +33386.5558
  x[  4] = +37844.4652
  x[  5] = +25356.4156
  x[  6] = +56409.4631
  x[  7] = +56700.6041
  x[  8] = +53489.6977
  x[  9] = +56420.9913
  x[ 10] = +47586.3184
  x[ 11] = +56806.3750
  x[ 12] = +59974.8585
  x[ 13] = +57138.8220
  x[ 14] = +35020.4398
  x[ 15] = +18729.1104
  x[ 16] = +18750.6438
  x[ 17] = +23254.3217
  x[ 18] = +4430.8381
  x[ 19] = +11843.1704
  x[ 20] = +14993.3084
  x[ 21] = -9893.2477
  x[ 22] = -12683.8303
  x[ 23] = +24231.3907
```

## Iteration Trace

**Iter 0** | λ=1.259e-08 | RMSE=0.9923 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.01, L1_rough=96549.2967
  - Fit marginal: rmse=0.9923, rel_err=0.0573

**Iter 1** | λ=6.294e-09 | RMSE=0.9681 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.04, L1_rough=113640.9892
  - Fit marginal: rmse=0.9681, rel_err=0.0559

**Iter 2** | λ=3.147e-09 | RMSE=0.9583 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.13, L1_rough=159499.6405
  - Fit marginal: rmse=0.9583, rel_err=0.0553

**Iter 3** | λ=1.573e-09 | RMSE=0.9523 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.38, L1_rough=252883.9803
  - Fit marginal: rmse=0.9523, rel_err=0.0550

**Iter 4** | λ=7.867e-10 | RMSE=0.9469 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.99, L1_rough=406619.7765
  - Fit marginal: rmse=0.9469, rel_err=0.0547

**Iter 5** | λ=3.934e-10 | RMSE=0.9418 | under_regularized | → switch_reg_order_to_1
  - Under-regularisation suspected: osc=2.12, L1_rough=623906.6800
  - Fit marginal: rmse=0.9418, rel_err=0.0544

**Iter 6** | λ=3.934e-10 | RMSE=0.9496 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.48, L1_rough=296990.9413
  - Fit marginal: rmse=0.9496, rel_err=0.0548

**Iter 7** | λ=1.967e-10 | RMSE=0.9451 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=1.12, L1_rough=451633.2950
  - Fit marginal: rmse=0.9451, rel_err=0.0546

**Iter 8** | λ=1.967e-10 | RMSE=0.9514 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.28, L1_rough=250780.1659
  - Fit marginal: rmse=0.9514, rel_err=0.0549

## Notes

- Completed in 9 iteration(s)
