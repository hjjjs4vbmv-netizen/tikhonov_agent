# IHCP Inversion Report

**Date:** 2026-04-14 20:53  
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
- Regularisation order: 1
- Lambda: `1.0000e+00`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `12.220165`
- Regularisation norm: `0.014388`
- Objective value: `149.332646`

### Estimated Parameters

```
  x[  0] = +41927.3474
  x[  1] = +41927.3466
  x[  2] = +41927.3447
  x[  3] = +41927.3419
  x[  4] = +41927.3381
  x[  5] = +41927.3337
  x[  6] = +41927.3289
  x[  7] = +41927.3240
  x[  8] = +41927.3195
  x[  9] = +41927.3155
  x[ 10] = +41927.3120
  x[ 11] = +41927.3091
  x[ 12] = +41927.3065
  x[ 13] = +41927.3041
  x[ 14] = +41927.3017
  x[ 15] = +41927.2991
  x[ 16] = +41927.2963
  x[ 17] = +41927.2935
  x[ 18] = +41927.2909
  x[ 19] = +41927.2886
  x[ 20] = +41927.2869
  x[ 21] = +41927.2857
  x[ 22] = +41927.2852
  x[ 23] = +41927.2851
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=0.7855 | well_regularized | → stop_success_weak_pass
  - Discrepancy principle: ||r||=12.2202 is above target=1.5556 (rel_dev=6.86)
  - Fit marginal: rmse=0.7855, rel_err=0.0447

## Notes

- Completed in 1 iteration(s)
