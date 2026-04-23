# IHCP Inversion Report

**Date:** 2026-04-20 17:04  
**Status:** `weak_pass`  
**Iterations:** 1  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 0.1

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 2
- Lambda: `1.5300e-07`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.556874`
- Regularisation norm: `5362.585836`
- Objective value: `6.823603`

### Estimated Parameters

```
  x[  0] = +6512.5747
  x[  1] = +13576.0769
  x[  2] = +20673.9580
  x[  3] = +27851.9567
  x[  4] = +35043.7291
  x[  5] = +42009.0677
  x[  6] = +48347.7699
  x[  7] = +53556.6851
  x[  8] = +57118.2864
  x[  9] = +58630.6805
  x[ 10] = +57900.2833
  x[ 11] = +54969.4978
  x[ 12] = +50123.5858
  x[ 13] = +43860.5234
  x[ 14] = +36804.0370
  x[ 15] = +29582.6257
  x[ 16] = +22763.8072
  x[ 17] = +16757.7049
  x[ 18] = +11774.5174
  x[ 19] = +7806.8677
  x[ 20] = +4649.4192
  x[ 21] = +2025.7557
  x[ 22] = -341.0399
  x[ 23] = -2643.6708
```

## Iteration Trace

**Iter 0** | λ=1.530e-07 | RMSE=0.1001 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=113392.4571
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
