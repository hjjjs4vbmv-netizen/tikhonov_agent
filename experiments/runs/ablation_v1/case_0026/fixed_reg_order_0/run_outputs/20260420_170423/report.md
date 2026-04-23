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
- Regularisation order: 0
- Lambda: `7.5787e-10`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.580904`
- Regularisation norm: `206255.244734`
- Objective value: `34.739951`

### Estimated Parameters

```
  x[  0] = +44174.6210
  x[  1] = +53827.2230
  x[  2] = +59321.5208
  x[  3] = +59058.0659
  x[  4] = +56173.0221
  x[  5] = +43096.0747
  x[  6] = +37977.6572
  x[  7] = +26573.3524
  x[  8] = +20657.4384
  x[  9] = +21151.2451
  x[ 10] = +23712.1194
  x[ 11] = +34545.5082
  x[ 12] = +44475.9983
  x[ 13] = +54614.4099
  x[ 14] = +58330.3391
  x[ 15] = +58345.6739
  x[ 16] = +53777.7455
  x[ 17] = +47514.5372
  x[ 18] = +34518.9198
  x[ 19] = +27325.9543
  x[ 20] = +22548.0590
  x[ 21] = +19694.0684
  x[ 22] = +25311.2358
  x[ 23] = +22412.2433
```

## Iteration Trace

**Iter 0** | λ=7.579e-10 | RMSE=0.1016 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.02, L1_rough=138666.9832
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
