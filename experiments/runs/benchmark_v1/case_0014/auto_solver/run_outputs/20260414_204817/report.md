# IHCP Inversion Report

**Date:** 2026-04-14 20:48  
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
- Regularisation order: 1
- Lambda: `1.2587e-08`
- Lambda strategy: `discrepancy`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `1.555150`
- Regularisation norm: `24626.548635`
- Objective value: `10.052286`

### Estimated Parameters

```
  x[  0] = +12081.9615
  x[  1] = +14452.6362
  x[  2] = +19468.8078
  x[  3] = +26063.2907
  x[  4] = +33421.7635
  x[  5] = +40794.7506
  x[  6] = +47918.6120
  x[  7] = +53608.7657
  x[  8] = +57419.0272
  x[  9] = +59068.5703
  x[ 10] = +58384.1391
  x[ 11] = +55628.6182
  x[ 12] = +50815.0447
  x[ 13] = +44318.4236
  x[ 14] = +36734.7870
  x[ 15] = +29093.5967
  x[ 16] = +22176.8551
  x[ 17] = +16292.8957
  x[ 18] = +11355.1222
  x[ 19] = +7613.7232
  x[ 20] = +4794.8387
  x[ 21] = +2749.1880
  x[ 22] = +1753.0511
  x[ 23] = +1608.4193
```

## Iteration Trace

**Iter 0** | λ=1.259e-08 | RMSE=0.1000 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.05, L1_rough=104446.7598
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
