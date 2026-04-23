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
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `1.0000e+00`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `23.340154`
- Regularisation norm: `0.027856`
- Objective value: `544.763569`

### Estimated Parameters

```
  x[  0] = +35535.8188
  x[  1] = +35535.8192
  x[  2] = +35535.8201
  x[  3] = +35535.8213
  x[  4] = +35535.8224
  x[  5] = +35535.8231
  x[  6] = +35535.8230
  x[  7] = +35535.8219
  x[  8] = +35535.8193
  x[  9] = +35535.8153
  x[ 10] = +35535.8096
  x[ 11] = +35535.8024
  x[ 12] = +35535.7938
  x[ 13] = +35535.7843
  x[ 14] = +35535.7742
  x[ 15] = +35535.7640
  x[ 16] = +35535.7543
  x[ 17] = +35535.7455
  x[ 18] = +35535.7379
  x[ 19] = +35535.7319
  x[ 20] = +35535.7276
  x[ 21] = +35535.7248
  x[ 22] = +35535.7235
  x[ 23] = +35535.7232
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.5004 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=23.3402 is above target=7.7782 (rel_dev=2.00)
  - Fit marginal: rmse=1.5004, rel_err=0.0941

## Notes

- Completed in 1 iteration(s)
