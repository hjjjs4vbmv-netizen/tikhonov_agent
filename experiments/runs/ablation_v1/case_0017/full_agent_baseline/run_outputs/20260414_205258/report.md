# IHCP Inversion Report

**Date:** 2026-04-14 20:52  
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
- Regularisation order: 2
- Lambda: `3.0496e-09`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `13.768295`
- Regularisation norm: `12263.069314`
- Objective value: `190.024569`

### Estimated Parameters

```
  x[  0] = +5273.8552
  x[  1] = +16020.9619
  x[  2] = +21744.6534
  x[  3] = +27820.9313
  x[  4] = +35472.6306
  x[  5] = +42076.2818
  x[  6] = +48040.3070
  x[  7] = +54731.4224
  x[  8] = +57952.7870
  x[  9] = +57107.9261
  x[ 10] = +56496.8674
  x[ 11] = +55095.8955
  x[ 12] = +49708.6803
  x[ 13] = +42274.4017
  x[ 14] = +36902.9008
  x[ 15] = +28865.3658
  x[ 16] = +20156.0358
  x[ 17] = +11439.2179
  x[ 18] = +6330.6703
  x[ 19] = +7283.1886
  x[ 20] = +5633.8823
  x[ 21] = +4549.0019
  x[ 22] = +4815.2207
  x[ 23] = +4251.2006
```

## Iteration Trace

**Iter 0** | λ=3.904e-07 | RMSE=1.0045 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=65866.2527
  - Fit marginal: rmse=1.0045, rel_err=0.0583

**Iter 1** | λ=1.952e-07 | RMSE=0.9352 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=79742.4640
  - Fit marginal: rmse=0.9352, rel_err=0.0543

**Iter 2** | λ=9.759e-08 | RMSE=0.9040 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=89255.3921
  - Fit marginal: rmse=0.9040, rel_err=0.0525

**Iter 3** | λ=4.879e-08 | RMSE=0.8923 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=94831.6210
  - Fit marginal: rmse=0.8923, rel_err=0.0518

**Iter 4** | λ=2.440e-08 | RMSE=0.8883 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.14, L1_rough=97765.4407
  - Fit marginal: rmse=0.8883, rel_err=0.0516

**Iter 5** | λ=1.220e-08 | RMSE=0.8865 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.14, L1_rough=99890.6447
  - Fit marginal: rmse=0.8865, rel_err=0.0515

**Iter 6** | λ=6.099e-09 | RMSE=0.8852 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=0.23, L1_rough=106784.8699
  - Fit marginal: rmse=0.8852, rel_err=0.0514

**Iter 7** | λ=6.099e-09 | RMSE=0.8858 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.14, L1_rough=104794.9331
  - Fit marginal: rmse=0.8858, rel_err=0.0514

**Iter 8** | λ=3.050e-09 | RMSE=0.8851 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.23, L1_rough=108817.9923
  - Fit marginal: rmse=0.8851, rel_err=0.0514

## Notes

- Completed in 9 iteration(s)
