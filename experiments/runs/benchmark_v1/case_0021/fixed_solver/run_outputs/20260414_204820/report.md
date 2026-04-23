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
- Residual norm: `15.997338`
- Regularisation norm: `0.021274`
- Objective value: `255.915272`

### Estimated Parameters

```
  x[  0] = +32590.9707
  x[  1] = +32590.9722
  x[  2] = +32590.9755
  x[  3] = +32590.9803
  x[  4] = +32590.9863
  x[  5] = +32590.9931
  x[  6] = +32591.0003
  x[  7] = +32591.0075
  x[  8] = +32591.0146
  x[  9] = +32591.0214
  x[ 10] = +32591.0278
  x[ 11] = +32591.0335
  x[ 12] = +32591.0384
  x[ 13] = +32591.0424
  x[ 14] = +32591.0456
  x[ 15] = +32591.0481
  x[ 16] = +32591.0497
  x[ 17] = +32591.0507
  x[ 18] = +32591.0510
  x[ 19] = +32591.0509
  x[ 20] = +32591.0504
  x[ 21] = +32591.0500
  x[ 22] = +32591.0496
  x[ 23] = +32591.0495
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.0283 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.9973 is above target=7.7782 (rel_dev=1.06)
  - Fit marginal: rmse=1.0283, rel_err=0.0620

## Notes

- Completed in 1 iteration(s)
