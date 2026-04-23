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
- Noise std: 1.0

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `1.3609e-06`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.332633`
- Regularisation norm: `11082.542132`
- Objective value: `402.241201`

### Estimated Parameters

```
  x[  0] = +11845.7372
  x[  1] = +12290.3532
  x[  2] = +13237.8230
  x[  3] = +14676.5233
  x[  4] = +16547.8584
  x[  5] = +18774.1477
  x[  6] = +21299.5940
  x[  7] = +24081.8157
  x[  8] = +27046.8023
  x[  9] = +30142.9860
  x[ 10] = +33346.0122
  x[ 11] = +36596.1726
  x[ 12] = +39818.7014
  x[ 13] = +42960.7346
  x[ 14] = +45987.9199
  x[ 15] = +48808.0923
  x[ 16] = +51388.6961
  x[ 17] = +53676.6829
  x[ 18] = +55639.8200
  x[ 19] = +57256.5468
  x[ 20] = +58437.2124
  x[ 21] = +59202.9859
  x[ 22] = +59593.0717
  x[ 23] = +59699.0788
```

## Iteration Trace

**Iter 0** | λ=1.361e-06 | RMSE=0.9856 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=47853.3416
  - Fit marginal: rmse=0.9856, rel_err=0.0403

## Notes

- Completed in 1 iteration(s)
