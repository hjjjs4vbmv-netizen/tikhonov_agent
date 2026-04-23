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
- Regularisation order: 1
- Lambda: `2.3503e-08`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.808282`
- Regularisation norm: `25615.354191`
- Objective value: `76.390546`

### Estimated Parameters

```
  x[  0] = +54397.9221
  x[  1] = +55330.5752
  x[  2] = +56525.5687
  x[  3] = +55480.1411
  x[  4] = +51142.3230
  x[  5] = +43764.6928
  x[  6] = +35968.3130
  x[  7] = +28434.2566
  x[  8] = +23558.4639
  x[  9] = +23064.2434
  x[ 10] = +27191.0138
  x[ 11] = +35353.6665
  x[ 12] = +44619.7626
  x[ 13] = +52137.1069
  x[ 14] = +55736.7526
  x[ 15] = +55336.6470
  x[ 16] = +51583.8829
  x[ 17] = +45318.0323
  x[ 18] = +37502.1413
  x[ 19] = +30590.5918
  x[ 20] = +25439.2648
  x[ 21] = +22370.7600
  x[ 22] = +21766.2172
  x[ 23] = +22294.9259
```

## Iteration Trace

**Iter 0** | λ=2.350e-08 | RMSE=0.5019 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=102760.7252
  - Fit marginal: rmse=0.5019, rel_err=0.0268

## Notes

- Completed in 1 iteration(s)
