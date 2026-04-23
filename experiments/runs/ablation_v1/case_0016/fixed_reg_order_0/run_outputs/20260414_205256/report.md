# IHCP Inversion Report

**Date:** 2026-04-14 20:52  
**Status:** `weak_pass`  
**Iterations:** 1  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 0
- Lambda: `6.7414e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.772278`
- Regularisation norm: `170637.961640`
- Objective value: `256.698320`

### Estimated Parameters

```
  x[  0] = +13241.5950
  x[  1] = +16603.7927
  x[  2] = +22522.6459
  x[  3] = +27988.5023
  x[  4] = +34771.7546
  x[  5] = +37570.4289
  x[  6] = +48130.7133
  x[  7] = +51769.1757
  x[  8] = +54175.6339
  x[  9] = +55923.7569
  x[ 10] = +53961.8788
  x[ 11] = +54228.4829
  x[ 12] = +51106.3935
  x[ 13] = +45907.8485
  x[ 14] = +36266.2721
  x[ 15] = +27572.3771
  x[ 16] = +21509.8596
  x[ 17] = +18027.9901
  x[ 18] = +11208.9539
  x[ 19] = +9208.1128
  x[ 20] = +6779.2464
  x[ 21] = +1322.3397
  x[ 22] = -227.4570
  x[ 23] = +1617.1263
```

## Iteration Trace

**Iter 0** | λ=6.741e-09 | RMSE=0.4996 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.18, L1_rough=101211.1674
  - Fit marginal: rmse=0.4996, rel_err=0.0313

## Notes

- Completed in 1 iteration(s)
