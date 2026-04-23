# IHCP Inversion Report

**Date:** 2026-04-14 20:48  
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
- Residual norm: `18.796339`
- Regularisation norm: `0.017315`
- Objective value: `353.302678`

### Estimated Parameters

```
  x[  0] = +41584.5948
  x[  1] = +41584.5939
  x[  2] = +41584.5918
  x[  3] = +41584.5885
  x[  4] = +41584.5841
  x[  5] = +41584.5790
  x[  6] = +41584.5733
  x[  7] = +41584.5675
  x[  8] = +41584.5620
  x[  9] = +41584.5569
  x[ 10] = +41584.5525
  x[ 11] = +41584.5486
  x[ 12] = +41584.5451
  x[ 13] = +41584.5419
  x[ 14] = +41584.5388
  x[ 15] = +41584.5356
  x[ 16] = +41584.5324
  x[ 17] = +41584.5292
  x[ 18] = +41584.5264
  x[ 19] = +41584.5240
  x[ 20] = +41584.5222
  x[ 21] = +41584.5211
  x[ 22] = +41584.5206
  x[ 23] = +41584.5204
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.2083 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=18.7963 is above target=15.5563 (rel_dev=0.21)
  - Fit marginal: rmse=1.2083, rel_err=0.0597

## Notes

- Completed in 1 iteration(s)
