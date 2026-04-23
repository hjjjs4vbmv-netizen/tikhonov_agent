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
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `1.0000e+00`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `35.117476`
- Regularisation norm: `0.085925`
- Objective value: `1233.244525`

### Estimated Parameters

```
  x[  0] = +31907.4761
  x[  1] = +31907.4791
  x[  2] = +31907.4860
  x[  3] = +31907.4966
  x[  4] = +31907.5108
  x[  5] = +31907.5282
  x[  6] = +31907.5484
  x[  7] = +31907.5709
  x[  8] = +31907.5952
  x[  9] = +31907.6208
  x[ 10] = +31907.6471
  x[ 11] = +31907.6734
  x[ 12] = +31907.6992
  x[ 13] = +31907.7239
  x[ 14] = +31907.7470
  x[ 15] = +31907.7680
  x[ 16] = +31907.7865
  x[ 17] = +31907.8022
  x[ 18] = +31907.8150
  x[ 19] = +31907.8248
  x[ 20] = +31907.8316
  x[ 21] = +31907.8357
  x[ 22] = +31907.8377
  x[ 23] = +31907.8382
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=2.2574 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.1175 is above target=7.7782 (rel_dev=3.51)
  - Fit failed: rmse=2.2574 > threshold 2.0

## Notes

- Completed in 1 iteration(s)
