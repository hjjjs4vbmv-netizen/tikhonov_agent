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
- Residual norm: `38.094931`
- Regularisation norm: `0.083489`
- Objective value: `1451.230739`

### Estimated Parameters

```
  x[  0] = +30894.5844
  x[  1] = +30894.5877
  x[  2] = +30894.5953
  x[  3] = +30894.6071
  x[  4] = +30894.6228
  x[  5] = +30894.6421
  x[  6] = +30894.6646
  x[  7] = +30894.6893
  x[  8] = +30894.7154
  x[  9] = +30894.7421
  x[ 10] = +30894.7685
  x[ 11] = +30894.7941
  x[ 12] = +30894.8182
  x[ 13] = +30894.8403
  x[ 14] = +30894.8601
  x[ 15] = +30894.8773
  x[ 16] = +30894.8920
  x[ 17] = +30894.9040
  x[ 18] = +30894.9133
  x[ 19] = +30894.9201
  x[ 20] = +30894.9247
  x[ 21] = +30894.9274
  x[ 22] = +30894.9286
  x[ 23] = +30894.9289
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=2.4488 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=38.0949 is above target=15.5563 (rel_dev=1.45)
  - Fit failed: rmse=2.4488 > threshold 2.0

## Notes

- Completed in 1 iteration(s)
