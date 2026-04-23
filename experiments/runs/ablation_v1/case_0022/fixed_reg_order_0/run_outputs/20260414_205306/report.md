# IHCP Inversion Report

**Date:** 2026-04-14 20:53  
**Status:** `weak_pass`  
**Iterations:** 5  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 2
- Lambda: `4.3000e-07`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `8.448579`
- Regularisation norm: `3969.262494`
- Objective value: `78.153127`

### Estimated Parameters

```
  x[  0] = +1279.6173
  x[  1] = +9089.3697
  x[  2] = +16748.3595
  x[  3] = +23893.5000
  x[  4] = +30056.0996
  x[  5] = +34824.5725
  x[  6] = +38038.8374
  x[  7] = +39834.3256
  x[  8] = +40654.7624
  x[  9] = +41021.9333
  x[ 10] = +41296.7415
  x[ 11] = +41594.2685
  x[ 12] = +41835.1810
  x[ 13] = +41922.9673
  x[ 14] = +41811.0572
  x[ 15] = +41435.2399
  x[ 16] = +40568.0100
  x[ 17] = +38813.0590
  x[ 18] = +35788.2740
  x[ 19] = +31368.0980
  x[ 20] = +25731.3991
  x[ 21] = +19294.4677
  x[ 22] = +12516.9694
  x[ 23] = +5676.2844
```

## Iteration Trace

**Iter 0** | λ=4.933e-09 | RMSE=0.4991 | under_regularized | → switch_reg_order_to_1
  - Under-regularisation suspected: osc=0.23, L1_rough=138372.7642
  - Fit marginal: rmse=0.4991, rel_err=0.0301

**Iter 1** | λ=9.212e-09 | RMSE=0.4975 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=0.23, L1_rough=119710.6082
  - Fit marginal: rmse=0.4975, rel_err=0.0300

**Iter 2** | λ=1.720e-08 | RMSE=0.5009 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.23, L1_rough=126729.4817
  - Fit marginal: rmse=0.5009, rel_err=0.0302

**Iter 3** | λ=8.600e-08 | RMSE=0.5184 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.23, L1_rough=94209.9177
  - Fit marginal: rmse=0.5184, rel_err=0.0313

**Iter 4** | λ=4.300e-07 | RMSE=0.5431 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.05, L1_rough=76890.0329
  - Fit marginal: rmse=0.5431, rel_err=0.0328

## Notes

- Completed in 5 iteration(s)
