# IHCP Inversion Report

**Date:** 2026-04-13 11:20  
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
- Residual norm: `35.739873`
- Regularisation norm: `0.083486`
- Objective value: `1277.345477`

### Estimated Parameters

```
  x[  0] = +30554.1023
  x[  1] = +30554.1057
  x[  2] = +30554.1134
  x[  3] = +30554.1253
  x[  4] = +30554.1412
  x[  5] = +30554.1607
  x[  6] = +30554.1833
  x[  7] = +30554.2080
  x[  8] = +30554.2341
  x[  9] = +30554.2607
  x[ 10] = +30554.2870
  x[ 11] = +30554.3124
  x[ 12] = +30554.3363
  x[ 13] = +30554.3582
  x[ 14] = +30554.3780
  x[ 15] = +30554.3954
  x[ 16] = +30554.4101
  x[ 17] = +30554.4221
  x[ 18] = +30554.4316
  x[ 19] = +30554.4386
  x[ 20] = +30554.4434
  x[ 21] = +30554.4462
  x[ 22] = +30554.4475
  x[ 23] = +30554.4478
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=2.2974 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.7399 is above target=7.7782 (rel_dev=3.59)
  - Fit failed: rmse=2.2974 > threshold 2.0

## Notes

- Completed in 1 iteration(s)
