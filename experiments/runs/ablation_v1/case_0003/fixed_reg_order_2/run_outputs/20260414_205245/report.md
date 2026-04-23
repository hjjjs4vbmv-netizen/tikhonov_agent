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
- Regularisation order: 2
- Lambda: `5.3340e-07`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.771791`
- Regularisation norm: `3522.776012`
- Objective value: `67.020182`

### Estimated Parameters

```
  x[  0] = -9391.4045
  x[  1] = -5651.7274
  x[  2] = -1762.0949
  x[  3] = +2605.7308
  x[  4] = +7784.9363
  x[  5] = +13946.0964
  x[  6] = +20970.0190
  x[  7] = +28387.2034
  x[  8] = +35474.2843
  x[  9] = +41557.5742
  x[ 10] = +46229.5438
  x[ 11] = +49368.2762
  x[ 12] = +51094.5192
  x[ 13] = +51702.1806
  x[ 14] = +51557.4580
  x[ 15] = +50994.1691
  x[ 16] = +50311.3242
  x[ 17] = +49722.6333
  x[ 18] = +49355.5101
  x[ 19] = +49242.3691
  x[ 20] = +49315.9127
  x[ 21] = +49512.8975
  x[ 22] = +49768.2939
  x[ 23] = +50034.3844
```

## Iteration Trace

**Iter 0** | λ=5.334e-07 | RMSE=0.4996 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.09, L1_rough=64345.4119
  - Fit marginal: rmse=0.4996, rel_err=0.0253

## Notes

- Completed in 1 iteration(s)
