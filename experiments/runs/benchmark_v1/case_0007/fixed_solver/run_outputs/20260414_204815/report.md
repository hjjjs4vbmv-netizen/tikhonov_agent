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
- Noise std: 0.1

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `1.0000e+00`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `34.964837`
- Regularisation norm: `0.087260`
- Objective value: `1222.547408`

### Estimated Parameters

```
  x[  0] = +32059.8105
  x[  1] = +32059.8136
  x[  2] = +32059.8205
  x[  3] = +32059.8314
  x[  4] = +32059.8458
  x[  5] = +32059.8635
  x[  6] = +32059.8841
  x[  7] = +32059.9071
  x[  8] = +32059.9319
  x[  9] = +32059.9579
  x[ 10] = +32059.9846
  x[ 11] = +32060.0113
  x[ 12] = +32060.0375
  x[ 13] = +32060.0626
  x[ 14] = +32060.0859
  x[ 15] = +32060.1072
  x[ 16] = +32060.1259
  x[ 17] = +32060.1418
  x[ 18] = +32060.1547
  x[ 19] = +32060.1645
  x[ 20] = +32060.1714
  x[ 21] = +32060.1755
  x[ 22] = +32060.1775
  x[ 23] = +32060.1780
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=2.2476 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=34.9648 is above target=1.5556 (rel_dev=21.48)
  - Fit failed: rmse=2.2476 > threshold 2.0

## Notes

- Completed in 1 iteration(s)
