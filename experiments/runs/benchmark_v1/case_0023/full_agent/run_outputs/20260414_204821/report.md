# IHCP Inversion Report

**Date:** 2026-04-14 20:48  
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
- Lambda: `1.6669e-07`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `14.051556`
- Regularisation norm: `5555.677766`
- Objective value: `202.591107`

### Estimated Parameters

```
  x[  0] = -3414.0277
  x[  1] = +6740.2914
  x[  2] = +16552.2869
  x[  3] = +25559.5838
  x[  4] = +33016.3415
  x[  5] = +38181.5550
  x[  6] = +40820.0704
  x[  7] = +41374.6976
  x[  8] = +40693.6514
  x[  9] = +39744.8037
  x[ 10] = +39185.8854
  x[ 11] = +39047.3399
  x[ 12] = +39045.4593
  x[ 13] = +39067.7293
  x[ 14] = +39212.9605
  x[ 15] = +39377.9248
  x[ 16] = +39290.4642
  x[ 17] = +38349.4577
  x[ 18] = +35980.9339
  x[ 19] = +31920.3958
  x[ 20] = +26199.3328
  x[ 21] = +19430.9771
  x[ 22] = +12220.8796
  x[ 23] = +4891.2896
```

## Iteration Trace

**Iter 0** | λ=5.334e-07 | RMSE=0.9981 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=31180.0288
  - Fit marginal: rmse=0.9981, rel_err=0.0545

**Iter 1** | λ=2.667e-07 | RMSE=0.9643 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=39922.8229
  - Fit marginal: rmse=0.9643, rel_err=0.0527

**Iter 2** | λ=1.333e-07 | RMSE=0.9397 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=47603.1736
  - Fit marginal: rmse=0.9397, rel_err=0.0513

**Iter 3** | λ=6.667e-08 | RMSE=0.9209 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.14, L1_rough=56017.6279
  - Fit marginal: rmse=0.9209, rel_err=0.0503

**Iter 4** | λ=3.334e-08 | RMSE=0.9069 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=0.23, L1_rough=69096.8175
  - Fit marginal: rmse=0.9069, rel_err=0.0495

**Iter 5** | λ=3.334e-08 | RMSE=0.8951 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.23, L1_rough=103063.3241
  - Fit marginal: rmse=0.8951, rel_err=0.0489

**Iter 6** | λ=1.667e-07 | RMSE=0.9033 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.14, L1_rough=81937.0644
  - Fit marginal: rmse=0.9033, rel_err=0.0493

## Notes

- Completed in 7 iteration(s)
