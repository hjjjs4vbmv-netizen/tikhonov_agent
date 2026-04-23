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
- Residual norm: `20.192617`
- Regularisation norm: `0.015838`
- Objective value: `407.742037`

### Estimated Parameters

```
  x[  0] = +42115.4952
  x[  1] = +42115.4942
  x[  2] = +42115.4922
  x[  3] = +42115.4890
  x[  4] = +42115.4847
  x[  5] = +42115.4798
  x[  6] = +42115.4745
  x[  7] = +42115.4692
  x[  8] = +42115.4642
  x[  9] = +42115.4599
  x[ 10] = +42115.4561
  x[ 11] = +42115.4530
  x[ 12] = +42115.4502
  x[ 13] = +42115.4476
  x[ 14] = +42115.4448
  x[ 15] = +42115.4419
  x[ 16] = +42115.4389
  x[ 17] = +42115.4358
  x[ 18] = +42115.4329
  x[ 19] = +42115.4305
  x[ 20] = +42115.4285
  x[ 21] = +42115.4273
  x[ 22] = +42115.4266
  x[ 23] = +42115.4265
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.2980 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=20.1926 is above target=15.5563 (rel_dev=0.30)
  - Fit marginal: rmse=1.2980, rel_err=0.0639

## Notes

- Completed in 1 iteration(s)
