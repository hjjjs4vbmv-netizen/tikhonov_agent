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
- Lambda: `1.6542e-05`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `77.797898`
- Regularisation norm: `1580.468120`
- Objective value: `6093.831775`

### Estimated Parameters

```
  x[  0] = +37667.1574
  x[  1] = +37674.3277
  x[  2] = +37694.0911
  x[  3] = +37709.1659
  x[  4] = +37708.1549
  x[  5] = +37678.0891
  x[  6] = +37622.8313
  x[  7] = +37510.5916
  x[  8] = +37337.2656
  x[  9] = +37101.8797
  x[ 10] = +36800.2177
  x[ 11] = +36435.3047
  x[ 12] = +35993.7812
  x[ 13] = +35476.3667
  x[ 14] = +34899.8350
  x[ 15] = +34307.8055
  x[ 16] = +33741.9835
  x[ 17] = +33229.0998
  x[ 18] = +32781.2996
  x[ 19] = +32422.5061
  x[ 20] = +32153.2530
  x[ 21] = +31972.5285
  x[ 22] = +31885.6297
  x[ 23] = +31867.6374
```

## Iteration Trace

**Iter 0** | λ=1.654e-05 | RMSE=5.0010 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=5883.5369
  - Fit failed: rmse=5.0010 > threshold 2.0

**Iter 1** | λ=3.308e-06 | RMSE=4.9429 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=18590.4171
  - Fit failed: rmse=4.9429 > threshold 2.0

**Iter 2** | λ=1.654e-05 | RMSE=5.0010 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=5883.5369
  - Fit failed: rmse=5.0010 > threshold 2.0

**Iter 3** | λ=3.308e-06 | RMSE=4.9429 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=18590.4171
  - Fit failed: rmse=4.9429 > threshold 2.0

**Iter 4** | λ=1.654e-05 | RMSE=5.0010 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=5883.5369
  - Fit failed: rmse=5.0010 > threshold 2.0

**Iter 5** | λ=3.308e-06 | RMSE=4.9429 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=18590.4171
  - Fit failed: rmse=4.9429 > threshold 2.0

**Iter 6** | λ=1.654e-05 | RMSE=5.0010 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=5883.5369
  - Fit failed: rmse=5.0010 > threshold 2.0

**Iter 7** | λ=3.308e-06 | RMSE=4.9429 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=18590.4171
  - Fit failed: rmse=4.9429 > threshold 2.0

**Iter 8** | λ=1.654e-05 | RMSE=5.0010 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.00, L1_rough=5883.5369
  - Fit failed: rmse=5.0010 > threshold 2.0

## Notes

- Completed in 9 iteration(s)
