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
- Noise std: 0.1

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `1.0000e+00`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `35.024413`
- Regularisation norm: `0.087427`
- Objective value: `1226.717163`

### Estimated Parameters

```
  x[  0] = +32112.9005
  x[  1] = +32112.9036
  x[  2] = +32112.9106
  x[  3] = +32112.9214
  x[  4] = +32112.9358
  x[  5] = +32112.9536
  x[  6] = +32112.9742
  x[  7] = +32112.9972
  x[  8] = +32113.0221
  x[  9] = +32113.0482
  x[ 10] = +32113.0749
  x[ 11] = +32113.1018
  x[ 12] = +32113.1280
  x[ 13] = +32113.1531
  x[ 14] = +32113.1765
  x[ 15] = +32113.1978
  x[ 16] = +32113.2166
  x[ 17] = +32113.2325
  x[ 18] = +32113.2453
  x[ 19] = +32113.2551
  x[ 20] = +32113.2620
  x[ 21] = +32113.2661
  x[ 22] = +32113.2681
  x[ 23] = +32113.2686
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=2.2515 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.0244 is above target=1.5556 (rel_dev=21.51)
  - Fit failed: rmse=2.2515 > threshold 2.0

## Notes

- Completed in 1 iteration(s)
