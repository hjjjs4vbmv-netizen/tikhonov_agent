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
- Residual norm: `36.997441`
- Regularisation norm: `0.081787`
- Objective value: `1368.817362`

### Estimated Parameters

```
  x[  0] = +30363.6843
  x[  1] = +30363.6876
  x[  2] = +30363.6951
  x[  3] = +30363.7068
  x[  4] = +30363.7224
  x[  5] = +30363.7415
  x[  6] = +30363.7636
  x[  7] = +30363.7878
  x[  8] = +30363.8133
  x[  9] = +30363.8393
  x[ 10] = +30363.8651
  x[ 11] = +30363.8899
  x[ 12] = +30363.9133
  x[ 13] = +30363.9349
  x[ 14] = +30363.9543
  x[ 15] = +30363.9713
  x[ 16] = +30363.9857
  x[ 17] = +30363.9976
  x[ 18] = +30364.0069
  x[ 19] = +30364.0139
  x[ 20] = +30364.0186
  x[ 21] = +30364.0214
  x[ 22] = +30364.0227
  x[ 23] = +30364.0231
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=2.3783 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=36.9974 is above target=15.5563 (rel_dev=1.38)
  - Fit failed: rmse=2.3783 > threshold 2.0

## Notes

- Completed in 1 iteration(s)
