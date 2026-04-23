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
- Noise std: 2.0

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `2.0836e-01`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `37.203427`
- Regularisation norm: `0.141964`
- Objective value: `1384.099182`

### Estimated Parameters

```
  x[  0] = +35761.0176
  x[  1] = +35761.0188
  x[  2] = +35761.0213
  x[  3] = +35761.0239
  x[  4] = +35761.0256
  x[  5] = +35761.0247
  x[  6] = +35761.0203
  x[  7] = +35761.0105
  x[  8] = +35760.9943
  x[  9] = +35760.9713
  x[ 10] = +35760.9412
  x[ 11] = +35760.9045
  x[ 12] = +35760.8615
  x[ 13] = +35760.8134
  x[ 14] = +35760.7621
  x[ 15] = +35760.7104
  x[ 16] = +35760.6612
  x[ 17] = +35760.6168
  x[ 18] = +35760.5786
  x[ 19] = +35760.5483
  x[ 20] = +35760.5262
  x[ 21] = +35760.5120
  x[ 22] = +35760.5052
  x[ 23] = +35760.5035
```

## Iteration Trace

**Iter 0** | λ=5.334e-07 | RMSE=2.0077 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=57180.8592
  - Fit failed: rmse=2.0077 > threshold 2.0

**Iter 1** | λ=2.667e-06 | RMSE=2.1814 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=22454.5594
  - Fit failed: rmse=2.1814 > threshold 2.0

**Iter 2** | λ=1.333e-05 | RMSE=2.3128 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=6465.7951
  - Fit failed: rmse=2.3128 > threshold 2.0

**Iter 3** | λ=6.667e-05 | RMSE=2.3708 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=1550.6923
  - Fit failed: rmse=2.3708 > threshold 2.0

**Iter 4** | λ=3.334e-04 | RMSE=2.3871 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=326.4745
  - Fit failed: rmse=2.3871 > threshold 2.0

**Iter 5** | λ=1.667e-03 | RMSE=2.3906 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=66.0554
  - Fit failed: rmse=2.3906 > threshold 2.0

**Iter 6** | λ=8.334e-03 | RMSE=2.3914 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=13.2420
  - Fit failed: rmse=2.3914 > threshold 2.0

**Iter 7** | λ=4.167e-02 | RMSE=2.3915 | well_regularized | → increase_lambda
  - Fit failed: rmse=2.3915 > threshold 2.0

**Iter 8** | λ=2.084e-01 | RMSE=2.3915 | well_regularized | → stop_with_failure
  - Fit failed: rmse=2.3915 > threshold 2.0

## Notes

- Completed in 9 iteration(s)
