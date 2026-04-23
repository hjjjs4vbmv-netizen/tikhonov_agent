# IHCP Inversion Report

**Date:** 2026-04-20 17:04  
**Status:** `weak_pass`  
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
- Regularisation order: 0
- Lambda: `4.9335e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.849381`
- Regularisation norm: `203808.097817`
- Objective value: `266.538546`

### Estimated Parameters

```
  x[  0] = +1157.7573
  x[  1] = +8452.7018
  x[  2] = +7839.1773
  x[  3] = +11482.4154
  x[  4] = +16449.2423
  x[  5] = +18911.9481
  x[  6] = +20055.3553
  x[  7] = +25475.9226
  x[  8] = +28730.5098
  x[  9] = +28959.9397
  x[ 10] = +33023.2834
  x[ 11] = +38345.6991
  x[ 12] = +41195.0481
  x[ 13] = +41620.3163
  x[ 14] = +49388.3311
  x[ 15] = +49909.6992
  x[ 16] = +54073.5403
  x[ 17] = +56031.8648
  x[ 18] = +56414.6826
  x[ 19] = +66649.1693
  x[ 20] = +66071.1714
  x[ 21] = +67221.9657
  x[ 22] = +60330.4794
  x[ 23] = +28203.7442
```

## Iteration Trace

**Iter 0** | λ=4.933e-09 | RMSE=0.5046 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.03, L1_rough=107465.4749
  - Fit marginal: rmse=0.5046, rel_err=0.0224

## Notes

- Completed in 1 iteration(s)
