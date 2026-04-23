# IHCP Inversion Report

**Date:** 2026-04-20 17:21  
**Status:** `weak_pass`  
**Iterations:** 9  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 1 at positions [0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `6.0889e-11`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `5.173122`
- Regularisation norm: `53338.503285`
- Objective value: `26.934417`

### Estimated Parameters

```
  x[  0] = +28201.1457
  x[  1] = +24564.5404
  x[  2] = +18006.7618
  x[  3] = +15841.8124
  x[  4] = +24158.6113
  x[  5] = +35459.7375
  x[  6] = +37975.5652
  x[  7] = +43015.2172
  x[  8] = +56035.5971
  x[  9] = +73557.9088
  x[ 10] = +83131.0678
  x[ 11] = +71913.4333
  x[ 12] = +46219.6194
  x[ 13] = +25674.8025
  x[ 14] = +24396.0422
  x[ 15] = +31929.0909
  x[ 16] = +32781.4691
  x[ 17] = +23585.8932
  x[ 18] = +9144.3981
  x[ 19] = -6919.5556
  x[ 20] = -13308.9076
  x[ 21] = -4796.4184
  x[ 22] = +2628.3534
  x[ 23] = +3317.8328
```

## Iteration Trace

**Iter 0** | λ=1.559e-08 | RMSE=0.4975 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=66806.6145
  - Fit marginal: rmse=0.4975, rel_err=0.0593

**Iter 1** | λ=7.794e-09 | RMSE=0.4840 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=82829.2121
  - Fit marginal: rmse=0.4840, rel_err=0.0576

**Iter 2** | λ=3.897e-09 | RMSE=0.4776 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=94788.9808
  - Fit marginal: rmse=0.4776, rel_err=0.0569

**Iter 3** | λ=1.948e-09 | RMSE=0.4749 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=103058.4189
  - Fit marginal: rmse=0.4749, rel_err=0.0566

**Iter 4** | λ=9.742e-10 | RMSE=0.4735 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=110700.8917
  - Fit marginal: rmse=0.4735, rel_err=0.0564

**Iter 5** | λ=4.871e-10 | RMSE=0.4726 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.01, L1_rough=121742.3019
  - Fit marginal: rmse=0.4726, rel_err=0.0563

**Iter 6** | λ=2.436e-10 | RMSE=0.4719 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.01, L1_rough=137117.2764
  - Fit marginal: rmse=0.4719, rel_err=0.0562

**Iter 7** | λ=1.218e-10 | RMSE=0.4711 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.02, L1_rough=162008.2966
  - Fit marginal: rmse=0.4711, rel_err=0.0561

**Iter 8** | λ=6.089e-11 | RMSE=0.4703 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.06, L1_rough=209486.1584
  - Fit marginal: rmse=0.4703, rel_err=0.0560

## Notes

- Completed in 9 iteration(s)
