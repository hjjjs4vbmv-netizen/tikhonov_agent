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
- Residual norm: `26.099798`
- Regularisation norm: `0.029624`
- Objective value: `681.200357`

### Estimated Parameters

```
  x[  0] = +35079.9506
  x[  1] = +35079.9509
  x[  2] = +35079.9516
  x[  3] = +35079.9525
  x[  4] = +35079.9532
  x[  5] = +35079.9534
  x[  6] = +35079.9527
  x[  7] = +35079.9507
  x[  8] = +35079.9474
  x[  9] = +35079.9423
  x[ 10] = +35079.9357
  x[ 11] = +35079.9277
  x[ 12] = +35079.9183
  x[ 13] = +35079.9080
  x[ 14] = +35079.8974
  x[ 15] = +35079.8867
  x[ 16] = +35079.8766
  x[ 17] = +35079.8676
  x[ 18] = +35079.8599
  x[ 19] = +35079.8539
  x[ 20] = +35079.8496
  x[ 21] = +35079.8470
  x[ 22] = +35079.8457
  x[ 23] = +35079.8454
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.6778 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=26.0998 is above target=15.5563 (rel_dev=0.68)
  - Fit marginal: rmse=1.6778, rel_err=0.0974

## Notes

- Completed in 1 iteration(s)
