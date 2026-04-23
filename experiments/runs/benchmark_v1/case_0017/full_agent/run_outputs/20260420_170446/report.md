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
- Lambda: `1.5248e-09`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `13.700707`
- Regularisation norm: `37856.683218`
- Objective value: `189.894641`

### Estimated Parameters

```
  x[  0] = +4472.3024
  x[  1] = +19651.4579
  x[  2] = +19134.3209
  x[  3] = +25947.9964
  x[  4] = +37568.7244
  x[  5] = +42789.5535
  x[  6] = +45148.0234
  x[  7] = +56226.3616
  x[  8] = +60220.4964
  x[  9] = +54371.0063
  x[ 10] = +55314.3852
  x[ 11] = +57762.2421
  x[ 12] = +50590.9835
  x[ 13] = +37994.9826
  x[ 14] = +39674.4948
  x[ 15] = +28222.2280
  x[ 16] = +21760.3849
  x[ 17] = +11224.8988
  x[ 18] = +1673.5366
  x[ 19] = +12969.0160
  x[ 20] = +4441.3647
  x[ 21] = +2667.2706
  x[ 22] = +6211.0674
  x[ 23] = +4130.2532
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

**Iter 6** | λ=6.099e-09 | RMSE=0.8852 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.01, L1_rough=106784.8699
  - Fit marginal: rmse=0.8852, rel_err=0.0514

**Iter 7** | λ=3.050e-09 | RMSE=0.8834 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.02, L1_rough=120386.1754
  - Fit marginal: rmse=0.8834, rel_err=0.0513

**Iter 8** | λ=1.525e-09 | RMSE=0.8807 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.07, L1_rough=152692.7593
  - Fit marginal: rmse=0.8807, rel_err=0.0512

## Notes

- Completed in 9 iteration(s)
