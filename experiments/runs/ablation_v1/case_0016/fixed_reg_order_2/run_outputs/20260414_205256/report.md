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
- Regularisation order: 2
- Lambda: `9.9595e-07`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.812106`
- Regularisation norm: `4187.668599`
- Objective value: `78.494586`

### Estimated Parameters

```
  x[  0] = +8481.3843
  x[  1] = +15606.1030
  x[  2] = +22693.2858
  x[  3] = +29635.9994
  x[  4] = +36263.3520
  x[  5] = +42343.2146
  x[  6] = +47601.9260
  x[  7] = +51731.1460
  x[  8] = +54464.6386
  x[  9] = +55612.4433
  x[ 10] = +55085.3043
  x[ 11] = +52913.7147
  x[ 12] = +49241.3079
  x[ 13] = +44333.0911
  x[ 14] = +38552.9191
  x[ 15] = +32314.3281
  x[ 16] = +25994.7539
  x[ 17] = +19867.5436
  x[ 18] = +14077.3083
  x[ 19] = +8658.0445
  x[ 20] = +3545.9257
  x[ 21] = -1363.8364
  x[ 22] = -6166.1966
  x[ 23] = -10933.2477
```

## Iteration Trace

**Iter 0** | λ=9.960e-07 | RMSE=0.5022 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.05, L1_rough=113676.7500
  - Fit marginal: rmse=0.5022, rel_err=0.0315

## Notes

- Completed in 1 iteration(s)
