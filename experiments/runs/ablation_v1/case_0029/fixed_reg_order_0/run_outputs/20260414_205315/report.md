# IHCP Inversion Report

**Date:** 2026-04-14 20:53  
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
- Regularisation order: 0
- Lambda: `1.7200e-08`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.173566`
- Regularisation norm: `191149.750416`
- Objective value: `858.691896`

### Estimated Parameters

```
  x[  0] = +39681.1190
  x[  1] = +54678.5162
  x[  2] = +53715.2528
  x[  3] = +53111.8252
  x[  4] = +50831.2309
  x[  5] = +44764.4909
  x[  6] = +36991.9764
  x[  7] = +32590.0211
  x[  8] = +28864.0516
  x[  9] = +26195.3127
  x[ 10] = +29204.3696
  x[ 11] = +35543.8006
  x[ 12] = +41183.7480
  x[ 13] = +44720.1572
  x[ 14] = +50644.9093
  x[ 15] = +49113.6194
  x[ 16] = +46395.4102
  x[ 17] = +39950.7180
  x[ 18] = +31882.9827
  x[ 19] = +30347.6050
  x[ 20] = +23583.9840
  x[ 21] = +19933.3389
  x[ 22] = +16070.8866
  x[ 23] = +6554.9745
```

## Iteration Trace

**Iter 0** | λ=1.720e-08 | RMSE=0.9754 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.14, L1_rough=112020.1319
  - Fit marginal: rmse=0.9754, rel_err=0.0482

## Notes

- Completed in 1 iteration(s)
