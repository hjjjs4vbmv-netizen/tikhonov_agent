# IHCP Inversion Report

**Date:** 2026-04-23 19:57  
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

- Solver: `tsvd`
- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `1.0000e-02`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `1.324616`
- Regularisation norm: `40828.575897`
- Objective value: `16669727.851991`

### Estimated Parameters

```
  x[  0] = -3176.9334
  x[  1] = +11225.5630
  x[  2] = +3914.9755
  x[  3] = +12497.6456
  x[  4] = +14910.9574
  x[  5] = +19507.4579
  x[  6] = +18794.9475
  x[  7] = +25904.8150
  x[  8] = +29438.8070
  x[  9] = +28977.6396
  x[ 10] = +34941.1950
  x[ 11] = +37422.3712
  x[ 12] = +44648.5186
  x[ 13] = +38083.0353
  x[ 14] = +54583.6200
  x[ 15] = +46992.7152
  x[ 16] = +55768.8075
  x[ 17] = +60727.2795
  x[ 18] = +53025.8264
  x[ 19] = +73278.6337
  x[ 20] = +63104.0209
  x[ 21] = +72231.1667
  x[ 22] = +76295.6098
  x[ 23] = +76883.8683
```

## Iteration Trace

**Iter 0** | λ=1.000e-02 | RMSE=0.0851 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.09, L1_rough=161094.2400
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
