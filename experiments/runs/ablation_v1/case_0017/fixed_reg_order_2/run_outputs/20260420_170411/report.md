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
- Regularisation order: 2
- Lambda: `4.7287e-08`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `13.796458`
- Regularisation norm: `6001.231425`
- Objective value: `192.045281`

### Estimated Parameters

```
  x[  0] = +6706.8937
  x[  1] = +14279.5652
  x[  2] = +21494.4707
  x[  3] = +28669.3885
  x[  4] = +35816.1735
  x[  5] = +42573.3923
  x[  6] = +48624.8230
  x[  7] = +53612.0109
  x[  8] = +56827.4565
  x[  9] = +57940.4614
  x[ 10] = +57118.2788
  x[ 11] = +54315.7884
  x[ 12] = +49469.9638
  x[ 13] = +43010.0659
  x[ 14] = +35668.0765
  x[ 15] = +27751.4656
  x[ 16] = +20130.5842
  x[ 17] = +13595.2187
  x[ 18] = +8888.1522
  x[ 19] = +6231.7349
  x[ 20] = +4715.0065
  x[ 21] = +4026.9057
  x[ 22] = +3771.6501
  x[ 23] = +3543.7987
```

## Iteration Trace

**Iter 0** | λ=1.211e-05 | RMSE=1.0120 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=82347.4637
  - Fit marginal: rmse=1.0120, rel_err=0.0588

**Iter 1** | λ=6.053e-06 | RMSE=0.9558 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=96150.0279
  - Fit marginal: rmse=0.9558, rel_err=0.0555

**Iter 2** | λ=3.026e-06 | RMSE=0.9247 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=104859.6865
  - Fit marginal: rmse=0.9247, rel_err=0.0537

**Iter 3** | λ=1.513e-06 | RMSE=0.9067 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=109328.5221
  - Fit marginal: rmse=0.9067, rel_err=0.0527

**Iter 4** | λ=7.566e-07 | RMSE=0.8966 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=110732.9038
  - Fit marginal: rmse=0.8966, rel_err=0.0521

**Iter 5** | λ=3.783e-07 | RMSE=0.8912 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=110154.7020
  - Fit marginal: rmse=0.8912, rel_err=0.0518

**Iter 6** | λ=1.891e-07 | RMSE=0.8886 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=108618.9860
  - Fit marginal: rmse=0.8886, rel_err=0.0516

**Iter 7** | λ=9.457e-08 | RMSE=0.8874 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=106954.2402
  - Fit marginal: rmse=0.8874, rel_err=0.0515

**Iter 8** | λ=4.729e-08 | RMSE=0.8869 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.00, L1_rough=105630.2304
  - Fit marginal: rmse=0.8869, rel_err=0.0515

## Notes

- Completed in 9 iteration(s)
