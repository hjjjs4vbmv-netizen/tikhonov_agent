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
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `1.0000e+00`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `14.824910`
- Regularisation norm: `0.014952`
- Objective value: `219.778193`

### Estimated Parameters

```
  x[  0] = +42040.4629
  x[  1] = +42040.4620
  x[  2] = +42040.4601
  x[  3] = +42040.4571
  x[  4] = +42040.4531
  x[  5] = +42040.4484
  x[  6] = +42040.4435
  x[  7] = +42040.4384
  x[  8] = +42040.4338
  x[  9] = +42040.4296
  x[ 10] = +42040.4261
  x[ 11] = +42040.4231
  x[ 12] = +42040.4205
  x[ 13] = +42040.4180
  x[ 14] = +42040.4154
  x[ 15] = +42040.4127
  x[ 16] = +42040.4098
  x[ 17] = +42040.4069
  x[ 18] = +42040.4042
  x[ 19] = +42040.4018
  x[ 20] = +42040.4000
  x[ 21] = +42040.3988
  x[ 22] = +42040.3982
  x[ 23] = +42040.3980
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=0.9530 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=14.8249 is above target=7.7782 (rel_dev=0.91)
  - Fit marginal: rmse=0.9530, rel_err=0.0510

## Notes

- Completed in 1 iteration(s)
