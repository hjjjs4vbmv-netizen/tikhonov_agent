# IHCP Inversion Report

**Date:** 2026-04-20 17:21  
**Status:** `weak_pass`  
**Iterations:** 8  

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
- Lambda: `9.6355e-09`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `4.329726`
- Regularisation norm: `16026.581069`
- Objective value: `21.221413`

### Estimated Parameters

```
  x[  0] = +20209.0150
  x[  1] = +21592.8664
  x[  2] = +24516.0604
  x[  3] = +28620.7695
  x[  4] = +33480.8595
  x[  5] = +38634.7158
  x[  6] = +43535.6401
  x[  7] = +47641.7934
  x[  8] = +50532.1405
  x[  9] = +51868.6453
  x[ 10] = +51420.7627
  x[ 11] = +49236.0678
  x[ 12] = +45628.0518
  x[ 13] = +41031.3260
  x[ 14] = +35977.1125
  x[ 15] = +31065.5681
  x[ 16] = +26763.0929
  x[ 17] = +23360.8359
  x[ 18] = +20898.8389
  x[ 19] = +19295.9247
  x[ 20] = +18452.7001
  x[ 21] = +18116.7620
  x[ 22] = +18021.9941
  x[ 23] = +18009.0071
```

## Iteration Trace

**Iter 0** | λ=1.233e-06 | RMSE=0.5000 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=2154.1667
  - Fit marginal: rmse=0.5000, rel_err=0.0617

**Iter 1** | λ=6.167e-07 | RMSE=0.4945 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=4047.8330
  - Fit marginal: rmse=0.4945, rel_err=0.0611

**Iter 2** | λ=3.083e-07 | RMSE=0.4858 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=7412.8032
  - Fit marginal: rmse=0.4858, rel_err=0.0600

**Iter 3** | λ=1.542e-07 | RMSE=0.4723 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=13366.9382
  - Fit marginal: rmse=0.4723, rel_err=0.0583

**Iter 4** | λ=7.708e-08 | RMSE=0.4528 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=22857.7884
  - Fit marginal: rmse=0.4528, rel_err=0.0559

**Iter 5** | λ=3.854e-08 | RMSE=0.4291 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=36215.1005
  - Fit marginal: rmse=0.4291, rel_err=0.0530

**Iter 6** | λ=1.927e-08 | RMSE=0.4076 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=51592.5006
  - Fit marginal: rmse=0.4076, rel_err=0.0503

**Iter 7** | λ=9.635e-09 | RMSE=0.3936 | under_regularized | → stop_success_weak_pass
  - Discrepancy principle: ||r||=4.3297 is below target=5.5000 (rel_dev=0.21)
  - Under-regularisation suspected: osc=0.00, L1_rough=65519.2684
  - Fit marginal: rmse=0.3936, rel_err=0.0486

## Notes

- Completed in 8 iteration(s)
