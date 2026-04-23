# IHCP Inversion Report

**Date:** 2026-04-14 20:52  
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
- Lambda: `1.5300e-07`
- Lambda strategy: `discrepancy`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `7.891809`
- Regularisation norm: `20130.769615`
- Objective value: `124.281814`

### Estimated Parameters

```
  x[  0] = +18632.4832
  x[  1] = +20286.2374
  x[  2] = +23661.9215
  x[  3] = +28480.7656
  x[  4] = +34176.2677
  x[  5] = +40053.9885
  x[  6] = +45511.6590
  x[  7] = +50046.7671
  x[  8] = +53106.7313
  x[  9] = +54377.3494
  x[ 10] = +53840.8953
  x[ 11] = +51514.6898
  x[ 12] = +47531.4953
  x[ 13] = +42268.5842
  x[ 14] = +36279.8680
  x[ 15] = +29895.3548
  x[ 16] = +23682.9478
  x[ 17] = +18040.9365
  x[ 18] = +13341.3389
  x[ 19] = +9851.0175
  x[ 20] = +7344.8823
  x[ 21] = +5852.7698
  x[ 22] = +5181.3359
  x[ 23] = +4990.8012
```

## Iteration Trace

**Iter 0** | λ=1.530e-07 | RMSE=0.5073 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.05, L1_rough=85131.4145
  - Fit marginal: rmse=0.5073, rel_err=0.0320

## Notes

- Completed in 1 iteration(s)
