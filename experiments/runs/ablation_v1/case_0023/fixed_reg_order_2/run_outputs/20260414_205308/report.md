# IHCP Inversion Report

**Date:** 2026-04-14 20:53  
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

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 2
- Lambda: `3.5318e-07`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `14.159391`
- Regularisation norm: `4287.270806`
- Objective value: `206.979968`

### Estimated Parameters

```
  x[  0] = -532.2783
  x[  1] = +8254.0164
  x[  2] = +16787.6146
  x[  3] = +24674.2253
  x[  4] = +31358.2151
  x[  5] = +36322.1028
  x[  6] = +39371.8663
  x[  7] = +40738.6907
  x[  8] = +40938.9369
  x[  9] = +40602.8576
  x[ 10] = +40224.1466
  x[ 11] = +39966.4955
  x[ 12] = +39782.1279
  x[ 13] = +39629.9537
  x[ 14] = +39500.6342
  x[ 15] = +39241.4347
  x[ 16] = +38601.8180
  x[ 17] = +37192.5232
  x[ 18] = +34685.0498
  x[ 19] = +30963.6704
  x[ 20] = +26117.4376
  x[ 21] = +20551.1223
  x[ 22] = +14667.6901
  x[ 23] = +8699.6685
```

## Iteration Trace

**Iter 0** | λ=2.260e-05 | RMSE=0.9950 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=35656.4586
  - Fit marginal: rmse=0.9950, rel_err=0.0543

**Iter 1** | λ=1.130e-05 | RMSE=0.9644 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=45806.9734
  - Fit marginal: rmse=0.9644, rel_err=0.0527

**Iter 2** | λ=5.651e-06 | RMSE=0.9473 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=53763.8139
  - Fit marginal: rmse=0.9473, rel_err=0.0517

**Iter 3** | λ=2.825e-06 | RMSE=0.9370 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=59410.6347
  - Fit marginal: rmse=0.9370, rel_err=0.0512

**Iter 4** | λ=1.413e-06 | RMSE=0.9281 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=63645.6155
  - Fit marginal: rmse=0.9281, rel_err=0.0507

**Iter 5** | λ=7.064e-07 | RMSE=0.9189 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=67927.8273
  - Fit marginal: rmse=0.9189, rel_err=0.0502

**Iter 6** | λ=3.532e-07 | RMSE=0.9102 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.05, L1_rough=73710.4835
  - Fit marginal: rmse=0.9102, rel_err=0.0497

## Notes

- Completed in 7 iteration(s)
