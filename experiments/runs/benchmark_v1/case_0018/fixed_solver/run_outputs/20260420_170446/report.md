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
- Lambda: `1.0000e+00`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `26.652223`
- Regularisation norm: `0.028415`
- Objective value: `710.341814`

### Estimated Parameters

```
  x[  0] = +35610.8506
  x[  1] = +35610.8510
  x[  2] = +35610.8518
  x[  3] = +35610.8527
  x[  4] = +35610.8536
  x[  5] = +35610.8540
  x[  6] = +35610.8536
  x[  7] = +35610.8522
  x[  8] = +35610.8494
  x[  9] = +35610.8450
  x[ 10] = +35610.8392
  x[ 11] = +35610.8318
  x[ 12] = +35610.8231
  x[ 13] = +35610.8134
  x[ 14] = +35610.8031
  x[ 15] = +35610.7928
  x[ 16] = +35610.7829
  x[ 17] = +35610.7739
  x[ 18] = +35610.7662
  x[ 19] = +35610.7601
  x[ 20] = +35610.7557
  x[ 21] = +35610.7529
  x[ 22] = +35610.7515
  x[ 23] = +35610.7512
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.7133 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=26.6522 is above target=15.5563 (rel_dev=0.71)
  - Fit marginal: rmse=1.7133, rel_err=0.0989

## Notes

- Completed in 1 iteration(s)
