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
- Residual norm: `20.931974`
- Regularisation norm: `0.021269`
- Objective value: `438.148000`

### Estimated Parameters

```
  x[  0] = +32931.4527
  x[  1] = +32931.4541
  x[  2] = +32931.4572
  x[  3] = +32931.4619
  x[  4] = +32931.4678
  x[  5] = +32931.4744
  x[  6] = +32931.4815
  x[  7] = +32931.4886
  x[  8] = +32931.4957
  x[  9] = +32931.5026
  x[ 10] = +32931.5091
  x[ 11] = +32931.5151
  x[ 12] = +32931.5202
  x[ 13] = +32931.5243
  x[ 14] = +32931.5275
  x[ 15] = +32931.5299
  x[ 16] = +32931.5315
  x[ 17] = +32931.5324
  x[ 18] = +32931.5326
  x[ 19] = +32931.5322
  x[ 20] = +32931.5316
  x[ 21] = +32931.5310
  x[ 22] = +32931.5306
  x[ 23] = +32931.5305
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.3456 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=20.9320 is above target=15.5563 (rel_dev=0.35)
  - Fit marginal: rmse=1.3456, rel_err=0.0729

## Notes

- Completed in 1 iteration(s)
