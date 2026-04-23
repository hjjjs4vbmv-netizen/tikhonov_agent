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
- Noise std: 1.0

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 2
- Lambda: `2.0906e-07`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.514345`
- Regularisation norm: `8535.487612`
- Objective value: `255.925918`

### Estimated Parameters

```
  x[  0] = +62368.9410
  x[  1] = +59562.0347
  x[  2] = +56403.5814
  x[  3] = +52272.9289
  x[  4] = +46852.1687
  x[  5] = +40439.3946
  x[  6] = +34004.5734
  x[  7] = +28708.7742
  x[  8] = +25827.0995
  x[  9] = +26232.1493
  x[ 10] = +29982.6069
  x[ 11] = +36228.6500
  x[ 12] = +43310.1839
  x[ 13] = +49390.3425
  x[ 14] = +53050.0169
  x[ 15] = +53683.9517
  x[ 16] = +51396.9803
  x[ 17] = +46758.9807
  x[ 18] = +40592.2215
  x[ 19] = +33824.1519
  x[ 20] = +27079.7760
  x[ 21] = +20667.6936
  x[ 22] = +14657.8283
  x[ 23] = +8857.9704
```

## Iteration Trace

**Iter 0** | λ=2.091e-07 | RMSE=0.9973 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=109224.6750
  - Fit marginal: rmse=0.9973, rel_err=0.0491

## Notes

- Completed in 1 iteration(s)
