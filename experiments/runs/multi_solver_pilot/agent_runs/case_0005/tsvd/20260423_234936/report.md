# IHCP Inversion Report

**Date:** 2026-04-23 23:49  
**Status:** `weak_pass`  
**Iterations:** 3  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 1.0

## Final Inversion Configuration

- Solver: `tsvd`
- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 2
- Lambda: `5.0000e-02`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `13.896434`
- Regularisation norm: `41951.716164`
- Objective value: `193.110891`

### Estimated Parameters

```
  x[  0] = -3836.1032
  x[  1] = +188.9228
  x[  2] = +5443.3302
  x[  3] = +3485.5257
  x[  4] = -3076.3580
  x[  5] = -2899.9796
  x[  6] = +11046.0690
  x[  7] = +32747.8091
  x[  8] = +48887.2884
  x[  9] = +52280.6117
  x[ 10] = +47943.4105
  x[ 11] = +45620.1115
  x[ 12] = +48398.8453
  x[ 13] = +51300.9750
  x[ 14] = +50328.8299
  x[ 15] = +48157.6181
  x[ 16] = +48305.7355
  x[ 17] = +48361.7240
  x[ 18] = +45091.8529
  x[ 19] = +43476.9946
  x[ 20] = +51195.7474
  x[ 21] = +62134.5727
  x[ 22] = +55651.5202
  x[ 23] = +23281.1375
```

## Iteration Trace

**Iter 0** | λ=1.000e-02 | RMSE=0.8523 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=6.15, L1_rough=1477037.2050
  - Fit marginal: rmse=0.8523, rel_err=0.0394

**Iter 1** | λ=1.000e-02 | RMSE=0.8523 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=6.15, L1_rough=1477037.2050
  - Fit marginal: rmse=0.8523, rel_err=0.0394

**Iter 2** | λ=5.000e-02 | RMSE=0.8933 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.04, L1_rough=151240.6608
  - Fit marginal: rmse=0.8933, rel_err=0.0413

## Notes

- Completed in 3 iteration(s)
