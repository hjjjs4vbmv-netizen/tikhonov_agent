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
- Residual norm: `35.511597`
- Regularisation norm: `0.086759`
- Objective value: `1261.081053`

### Estimated Parameters

```
  x[  0] = +32172.9261
  x[  1] = +32172.9292
  x[  2] = +32172.9361
  x[  3] = +32172.9467
  x[  4] = +32172.9610
  x[  5] = +32172.9785
  x[  6] = +32172.9989
  x[  7] = +32173.0216
  x[  8] = +32173.0463
  x[  9] = +32173.0722
  x[ 10] = +32173.0988
  x[ 11] = +32173.1255
  x[ 12] = +32173.1516
  x[ 13] = +32173.1766
  x[ 14] = +32173.1999
  x[ 15] = +32173.2210
  x[ 16] = +32173.2396
  x[ 17] = +32173.2554
  x[ 18] = +32173.2682
  x[ 19] = +32173.2779
  x[ 20] = +32173.2846
  x[ 21] = +32173.2887
  x[ 22] = +32173.2906
  x[ 23] = +32173.2912
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=2.2828 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.5116 is above target=7.7782 (rel_dev=3.57)
  - Fit failed: rmse=2.2828 > threshold 2.0

## Notes

- Completed in 1 iteration(s)
