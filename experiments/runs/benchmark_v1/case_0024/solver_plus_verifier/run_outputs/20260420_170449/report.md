# IHCP Inversion Report

**Date:** 2026-04-20 17:04  
**Status:** `fail`  
**Iterations:** 1  

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
- Regularisation order: 1
- Lambda: `4.3884e-08`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.542077`
- Regularisation norm: `18891.440269`
- Objective value: `257.217777`

### Estimated Parameters

```
  x[  0] = +7453.4056
  x[  1] = +10020.5772
  x[  2] = +15977.7086
  x[  3] = +23534.9285
  x[  4] = +30885.1521
  x[  5] = +36062.0999
  x[  6] = +39186.3416
  x[  7] = +39136.1804
  x[  8] = +37964.1527
  x[  9] = +37811.2137
  x[ 10] = +39252.2416
  x[ 11] = +41903.6738
  x[ 12] = +43482.2113
  x[ 13] = +43026.0096
  x[ 14] = +41106.2567
  x[ 15] = +39822.9284
  x[ 16] = +39870.9997
  x[ 17] = +39772.5958
  x[ 18] = +37148.9199
  x[ 19] = +32101.2959
  x[ 20] = +25102.5144
  x[ 21] = +18076.0841
  x[ 22] = +13945.1945
  x[ 23] = +13062.5216
```

## Iteration Trace

**Iter 0** | λ=4.388e-08 | RMSE=0.9991 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=69294.8938
  - Fit marginal: rmse=0.9991, rel_err=0.0541

## Notes

- Completed in 1 iteration(s)
