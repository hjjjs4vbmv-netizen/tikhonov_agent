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
- Noise std: 0.1

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 0
- Lambda: `7.5787e-10`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.659174`
- Regularisation norm: `217411.150546`
- Objective value: `38.575531`

### Estimated Parameters

```
  x[  0] = +130.9818
  x[  1] = +7014.8054
  x[  2] = +7066.7785
  x[  3] = +11158.3224
  x[  4] = +15478.5088
  x[  5] = +18456.2579
  x[  6] = +20234.5667
  x[  7] = +25242.6991
  x[  8] = +28727.6945
  x[  9] = +30145.1498
  x[ 10] = +34149.2867
  x[ 11] = +38498.1796
  x[ 12] = +41846.3485
  x[ 13] = +42546.1204
  x[ 14] = +49832.3332
  x[ 15] = +50184.4653
  x[ 16] = +55011.4261
  x[ 17] = +58102.8724
  x[ 18] = +58352.5882
  x[ 19] = +67271.3955
  x[ 20] = +66726.4705
  x[ 21] = +71503.4366
  x[ 22] = +77744.2667
  x[ 23] = +50296.7329
```

## Iteration Trace

**Iter 0** | λ=7.579e-10 | RMSE=0.1067 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.03, L1_rough=106150.6686
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
