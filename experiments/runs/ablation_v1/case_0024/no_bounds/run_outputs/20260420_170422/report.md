# IHCP Inversion Report

**Date:** 2026-04-20 17:04  
**Status:** `weak_pass`  
**Iterations:** 9  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 1.0

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `1.7142e-10`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `14.686580`
- Regularisation norm: `133810.061884`
- Objective value: `218.764975`

### Estimated Parameters

```
  x[  0] = +11962.7269
  x[  1] = -10066.4398
  x[  2] = +18389.4927
  x[  3] = +20453.1837
  x[  4] = +53117.5063
  x[  5] = +13869.2349
  x[  6] = +73442.1518
  x[  7] = +38294.8271
  x[  8] = +23031.6130
  x[  9] = +34635.0588
  x[ 10] = +19614.5367
  x[ 11] = +55123.4909
  x[ 12] = +54784.3954
  x[ 13] = +58253.9092
  x[ 14] = +28485.4137
  x[ 15] = +20490.6644
  x[ 16] = +31350.0251
  x[ 17] = +66442.1517
  x[ 18] = +32866.4553
  x[ 19] = +43755.3630
  x[ 20] = +39213.9172
  x[ 21] = -5821.2600
  x[ 22] = -13178.0797
  x[ 23] = +28048.9139
```

## Iteration Trace

**Iter 0** | λ=4.388e-08 | RMSE=0.9991 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=69294.8938
  - Fit marginal: rmse=0.9991, rel_err=0.0541

**Iter 1** | λ=2.194e-08 | RMSE=0.9852 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.01, L1_rough=93787.6548
  - Fit marginal: rmse=0.9852, rel_err=0.0534

**Iter 2** | λ=1.097e-08 | RMSE=0.9744 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.02, L1_rough=122359.5408
  - Fit marginal: rmse=0.9744, rel_err=0.0528

**Iter 3** | λ=5.486e-09 | RMSE=0.9665 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.03, L1_rough=154161.9614
  - Fit marginal: rmse=0.9665, rel_err=0.0523

**Iter 4** | λ=2.743e-09 | RMSE=0.9610 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.06, L1_rough=187954.1428
  - Fit marginal: rmse=0.9610, rel_err=0.0521

**Iter 5** | λ=1.371e-09 | RMSE=0.9569 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.13, L1_rough=228127.1950
  - Fit marginal: rmse=0.9569, rel_err=0.0518

**Iter 6** | λ=6.857e-10 | RMSE=0.9529 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.28, L1_rough=286919.8099
  - Fit marginal: rmse=0.9529, rel_err=0.0516

**Iter 7** | λ=3.428e-10 | RMSE=0.9486 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.65, L1_rough=388824.4063
  - Fit marginal: rmse=0.9486, rel_err=0.0514

**Iter 8** | λ=1.714e-10 | RMSE=0.9441 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=1.41, L1_rough=526726.1441
  - Fit marginal: rmse=0.9441, rel_err=0.0511

## Notes

- Completed in 9 iteration(s)
