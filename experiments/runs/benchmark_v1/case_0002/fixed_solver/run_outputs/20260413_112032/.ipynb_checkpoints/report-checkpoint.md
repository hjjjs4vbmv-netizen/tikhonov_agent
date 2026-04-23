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
- Noise std: 0.1

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `1.0000e+00`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `35.761782`
- Regularisation norm: `0.085015`
- Objective value: `1278.912263`

### Estimated Parameters

```
  x[  0] = +30759.5268
  x[  1] = +30759.5302
  x[  2] = +30759.5380
  x[  3] = +30759.5501
  x[  4] = +30759.5663
  x[  5] = +30759.5862
  x[  6] = +30759.6092
  x[  7] = +30759.6344
  x[  8] = +30759.6610
  x[  9] = +30759.6881
  x[ 10] = +30759.7149
  x[ 11] = +30759.7408
  x[ 12] = +30759.7651
  x[ 13] = +30759.7875
  x[ 14] = +30759.8077
  x[ 15] = +30759.8253
  x[ 16] = +30759.8402
  x[ 17] = +30759.8525
  x[ 18] = +30759.8620
  x[ 19] = +30759.8691
  x[ 20] = +30759.8738
  x[ 21] = +30759.8766
  x[ 22] = +30759.8779
  x[ 23] = +30759.8782
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=2.2989 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.7618 is above target=1.5556 (rel_dev=21.99)
  - Fit failed: rmse=2.2989 > threshold 2.0

## Notes

- Completed in 1 iteration(s)
