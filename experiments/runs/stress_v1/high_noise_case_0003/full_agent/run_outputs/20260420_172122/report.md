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
- Lambda: `2.9604e+04`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `74.719221`
- Regularisation norm: `0.000002`
- Objective value: `5582.962014`

### Estimated Parameters

```
  x[  0] = +28840.9442
  x[  1] = +28840.9442
  x[  2] = +28840.9442
  x[  3] = +28840.9442
  x[  4] = +28840.9442
  x[  5] = +28840.9442
  x[  6] = +28840.9442
  x[  7] = +28840.9442
  x[  8] = +28840.9442
  x[  9] = +28840.9442
  x[ 10] = +28840.9442
  x[ 11] = +28840.9442
  x[ 12] = +28840.9442
  x[ 13] = +28840.9442
  x[ 14] = +28840.9442
  x[ 15] = +28840.9442
  x[ 16] = +28840.9442
  x[ 17] = +28840.9442
  x[ 18] = +28840.9442
  x[ 19] = +28840.9442
  x[ 20] = +28840.9442
  x[ 21] = +28840.9442
  x[ 22] = +28840.9442
  x[ 23] = +28840.9442
```

## Iteration Trace

**Iter 0** | λ=7.579e-02 | RMSE=4.8031 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=3.7633
  - Fit failed: rmse=4.8031 > threshold 2.0

**Iter 1** | λ=3.789e-01 | RMSE=4.8031 | well_regularized | → increase_lambda
  - Fit failed: rmse=4.8031 > threshold 2.0

**Iter 2** | λ=1.895e+00 | RMSE=4.8031 | well_regularized | → increase_lambda
  - Fit failed: rmse=4.8031 > threshold 2.0

**Iter 3** | λ=9.473e+00 | RMSE=4.8031 | well_regularized | → increase_lambda
  - Fit failed: rmse=4.8031 > threshold 2.0

**Iter 4** | λ=4.737e+01 | RMSE=4.8031 | well_regularized | → increase_lambda
  - Fit failed: rmse=4.8031 > threshold 2.0

**Iter 5** | λ=2.368e+02 | RMSE=4.8031 | well_regularized | → increase_lambda
  - Fit failed: rmse=4.8031 > threshold 2.0

**Iter 6** | λ=1.184e+03 | RMSE=4.8031 | well_regularized | → increase_lambda
  - Fit failed: rmse=4.8031 > threshold 2.0

**Iter 7** | λ=5.921e+03 | RMSE=4.8031 | well_regularized | → increase_lambda
  - Fit failed: rmse=4.8031 > threshold 2.0

**Iter 8** | λ=2.960e+04 | RMSE=4.8031 | well_regularized | → stop_with_failure
  - Fit failed: rmse=4.8031 > threshold 2.0

## Notes

- Completed in 9 iteration(s)
