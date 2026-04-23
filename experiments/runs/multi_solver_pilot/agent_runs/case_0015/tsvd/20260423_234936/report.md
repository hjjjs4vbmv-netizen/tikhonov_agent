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
- Noise std: 0.5

## Final Inversion Configuration

- Solver: `tsvd`
- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 2
- Lambda: `5.0000e-02`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `6.893850`
- Regularisation norm: `9234.132945`
- Objective value: `47.525164`

### Estimated Parameters

```
  x[  0] = +8172.4202
  x[  1] = +14211.4622
  x[  2] = +20971.8700
  x[  3] = +27347.6036
  x[  4] = +33438.3212
  x[  5] = +40962.5924
  x[  6] = +49101.2336
  x[  7] = +54920.0569
  x[  8] = +57389.8474
  x[  9] = +58203.9634
  x[ 10] = +58248.2640
  x[ 11] = +55903.4252
  x[ 12] = +50084.7902
  x[ 13] = +42712.2986
  x[ 14] = +36148.5686
  x[ 15] = +29783.3188
  x[ 16] = +21736.0934
  x[ 17] = +13144.8149
  x[ 18] = +7732.4782
  x[ 19] = +6702.5387
  x[ 20] = +6833.0170
  x[ 21] = +4931.4114
  x[ 22] = +1855.0110
  x[ 23] = +185.8286
```

## Iteration Trace

**Iter 0** | λ=1.000e-02 | RMSE=0.4261 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=3.00, L1_rough=706536.4589
  - Fit marginal: rmse=0.4261, rel_err=0.0269

**Iter 1** | λ=1.000e-02 | RMSE=0.4261 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=3.00, L1_rough=706536.4589
  - Fit marginal: rmse=0.4261, rel_err=0.0269

**Iter 2** | λ=5.000e-02 | RMSE=0.4432 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=108399.2356
  - Fit marginal: rmse=0.4432, rel_err=0.0280

## Notes

- Completed in 3 iteration(s)
