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
- Residual norm: `37.507464`
- Regularisation norm: `0.085925`
- Objective value: `1406.817213`

### Estimated Parameters

```
  x[  0] = +32247.9583
  x[  1] = +32247.9613
  x[  2] = +32247.9680
  x[  3] = +32247.9785
  x[  4] = +32247.9925
  x[  5] = +32248.0097
  x[  6] = +32248.0298
  x[  7] = +32248.0523
  x[  8] = +32248.0766
  x[  9] = +32248.1023
  x[ 10] = +32248.1287
  x[ 11] = +32248.1553
  x[ 12] = +32248.1813
  x[ 13] = +32248.2061
  x[ 14] = +32248.2291
  x[ 15] = +32248.2501
  x[ 16] = +32248.2685
  x[ 17] = +32248.2842
  x[ 18] = +32248.2968
  x[ 19] = +32248.3064
  x[ 20] = +32248.3131
  x[ 21] = +32248.3171
  x[ 22] = +32248.3189
  x[ 23] = +32248.3195
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=2.4111 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=37.5075 is above target=15.5563 (rel_dev=1.41)
  - Fit failed: rmse=2.4111 > threshold 2.0

## Notes

- Completed in 1 iteration(s)
