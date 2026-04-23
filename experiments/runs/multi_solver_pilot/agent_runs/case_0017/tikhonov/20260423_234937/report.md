# IHCP Inversion Report

**Date:** 2026-04-23 23:49  
**Status:** `weak_pass`  
**Iterations:** 7  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 1.0

## Final Inversion Configuration

- Solver: `tikhonov`
- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `6.0993e-09`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `13.770656`
- Regularisation norm: `26177.985450`
- Objective value: `193.810732`

### Estimated Parameters

```
  x[  0] = +9236.2496
  x[  1] = +15699.5660
  x[  2] = +19974.7569
  x[  3] = +27068.3290
  x[  4] = +35773.0952
  x[  5] = +42410.1645
  x[  6] = +47742.8436
  x[  7] = +54551.4677
  x[  8] = +57860.4078
  x[  9] = +56790.9419
  x[ 10] = +56374.6143
  x[ 11] = +55160.9076
  x[ 12] = +49721.1163
  x[ 13] = +41741.7842
  x[ 14] = +37019.9267
  x[ 15] = +28343.7428
  x[ 16] = +20499.9776
  x[ 17] = +12294.4688
  x[ 18] = +6451.7608
  x[ 19] = +8008.2397
  x[ 20] = +5100.5064
  x[ 21] = +4134.2993
  x[ 22] = +4951.3393
  x[ 23] = +4446.7338
```

## Iteration Trace

**Iter 0** | λ=3.904e-07 | RMSE=1.0045 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=65866.2527
  - Fit marginal: rmse=1.0045, rel_err=0.0583

**Iter 1** | λ=1.952e-07 | RMSE=0.9352 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=79742.4640
  - Fit marginal: rmse=0.9352, rel_err=0.0543

**Iter 2** | λ=9.759e-08 | RMSE=0.9040 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=89255.3921
  - Fit marginal: rmse=0.9040, rel_err=0.0525

**Iter 3** | λ=4.879e-08 | RMSE=0.8923 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=94831.6210
  - Fit marginal: rmse=0.8923, rel_err=0.0518

**Iter 4** | λ=2.440e-08 | RMSE=0.8883 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=97765.4407
  - Fit marginal: rmse=0.8883, rel_err=0.0516

**Iter 5** | λ=1.220e-08 | RMSE=0.8865 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=99890.6447
  - Fit marginal: rmse=0.8865, rel_err=0.0515

**Iter 6** | λ=6.099e-09 | RMSE=0.8852 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.01, L1_rough=106784.8699
  - Fit marginal: rmse=0.8852, rel_err=0.0514

## Notes

- Completed in 7 iteration(s)
