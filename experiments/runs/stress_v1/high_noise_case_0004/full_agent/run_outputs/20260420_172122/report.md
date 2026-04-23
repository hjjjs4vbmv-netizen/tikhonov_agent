# IHCP Inversion Report

**Date:** 2026-04-20 17:21  
**Status:** `fail`  
**Iterations:** 9  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 5.0

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `8.8591e-06`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `77.911113`
- Regularisation norm: `5115.411815`
- Objective value: `6301.962200`

### Estimated Parameters

```
  x[  0] = +21727.8321
  x[  1] = +21920.9722
  x[  2] = +22376.1171
  x[  3] = +23078.8065
  x[  4] = +24024.2518
  x[  5] = +25198.0003
  x[  6] = +26603.9998
  x[  7] = +28160.3264
  x[  8] = +29816.9105
  x[  9] = +31523.0120
  x[ 10] = +33222.1503
  x[ 11] = +34869.7161
  x[ 12] = +36387.1701
  x[ 13] = +37718.9958
  x[ 14] = +38838.0950
  x[ 15] = +39768.8474
  x[ 16] = +40537.0299
  x[ 17] = +41149.2852
  x[ 18] = +41597.5714
  x[ 19] = +41911.7739
  x[ 20] = +42097.0377
  x[ 21] = +42177.2383
  x[ 22] = +42212.1083
  x[ 23] = +42230.6607
```

## Iteration Trace

**Iter 0** | λ=8.859e-06 | RMSE=5.0083 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=20502.8285
  - Fit failed: rmse=5.0083 > threshold 2.0

**Iter 1** | λ=1.772e-06 | RMSE=4.8799 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=37641.0806
  - Fit failed: rmse=4.8799 > threshold 2.0

**Iter 2** | λ=8.859e-06 | RMSE=5.0083 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=20502.8285
  - Fit failed: rmse=5.0083 > threshold 2.0

**Iter 3** | λ=1.772e-06 | RMSE=4.8799 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=37641.0806
  - Fit failed: rmse=4.8799 > threshold 2.0

**Iter 4** | λ=8.859e-06 | RMSE=5.0083 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=20502.8285
  - Fit failed: rmse=5.0083 > threshold 2.0

**Iter 5** | λ=1.772e-06 | RMSE=4.8799 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=37641.0806
  - Fit failed: rmse=4.8799 > threshold 2.0

**Iter 6** | λ=8.859e-06 | RMSE=5.0083 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=20502.8285
  - Fit failed: rmse=5.0083 > threshold 2.0

**Iter 7** | λ=1.772e-06 | RMSE=4.8799 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=37641.0806
  - Fit failed: rmse=4.8799 > threshold 2.0

**Iter 8** | λ=8.859e-06 | RMSE=5.0083 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.00, L1_rough=20502.8285
  - Fit failed: rmse=5.0083 > threshold 2.0

## Notes

- Completed in 9 iteration(s)
