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
- Residual norm: `19.501200`
- Regularisation norm: `0.019629`
- Objective value: `380.297175`

### Estimated Parameters

```
  x[  0] = +32400.5526
  x[  1] = +32400.5541
  x[  2] = +32400.5572
  x[  3] = +32400.5617
  x[  4] = +32400.5674
  x[  5] = +32400.5738
  x[  6] = +32400.5805
  x[  7] = +32400.5872
  x[  8] = +32400.5937
  x[  9] = +32400.6000
  x[ 10] = +32400.6057
  x[ 11] = +32400.6109
  x[ 12] = +32400.6154
  x[ 13] = +32400.6190
  x[ 14] = +32400.6218
  x[ 15] = +32400.6239
  x[ 16] = +32400.6253
  x[ 17] = +32400.6261
  x[ 18] = +32400.6263
  x[ 19] = +32400.6261
  x[ 20] = +32400.6256
  x[ 21] = +32400.6251
  x[ 22] = +32400.6248
  x[ 23] = +32400.6247
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.2536 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=19.5012 is above target=15.5563 (rel_dev=0.25)
  - Fit marginal: rmse=1.2536, rel_err=0.0685

## Notes

- Completed in 1 iteration(s)
