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
- Noise std: 1.0

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 0
- Lambda: `9.2117e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.490363`
- Regularisation norm: `199726.400406`
- Objective value: `607.412200`

### Estimated Parameters

```
  x[  0] = +44353.0158
  x[  1] = +54439.3626
  x[  2] = +58327.0207
  x[  3] = +57008.3790
  x[  4] = +53103.4414
  x[  5] = +40432.2349
  x[  6] = +38944.3812
  x[  7] = +29620.7990
  x[  8] = +23424.1421
  x[  9] = +23138.9909
  x[ 10] = +24810.0973
  x[ 11] = +36190.1736
  x[ 12] = +46492.9989
  x[ 13] = +54480.8395
  x[ 14] = +53956.5091
  x[ 15] = +51280.6012
  x[ 16] = +48396.9670
  x[ 17] = +45438.9638
  x[ 18] = +34821.3467
  x[ 19] = +30387.5120
  x[ 20] = +25765.7196
  x[ 21] = +17364.9049
  x[ 22] = +13550.4656
  x[ 23] = +9324.5676
```

## Iteration Trace

**Iter 0** | λ=9.212e-09 | RMSE=0.9958 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.02, L1_rough=125660.1553
  - Fit marginal: rmse=0.9958, rel_err=0.0490

## Notes

- Completed in 1 iteration(s)
