# IHCP Inversion Report

**Date:** 2026-04-14 20:53  
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
- Lambda: `1.9668e-09`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `14.931590`
- Regularisation norm: `22394.880848`
- Objective value: `223.938786`

### Estimated Parameters

```
  x[  0] = +11192.4752
  x[  1] = +14999.1913
  x[  2] = +22705.3976
  x[  3] = +29535.3973
  x[  4] = +34149.8476
  x[  5] = +38073.3644
  x[  6] = +49013.1192
  x[  7] = +54778.9620
  x[  8] = +55278.5566
  x[  9] = +53965.4164
  x[ 10] = +53041.3753
  x[ 11] = +56754.9816
  x[ 12] = +58175.1666
  x[ 13] = +51883.5427
  x[ 14] = +37307.7368
  x[ 15] = +24061.7902
  x[ 16] = +18069.7534
  x[ 17] = +16216.3518
  x[ 18] = +12394.8134
  x[ 19] = +10525.0990
  x[ 20] = +5838.4277
  x[ 21] = -2470.6617
  x[ 22] = -3870.0311
  x[ 23] = +3105.2825
```

## Iteration Trace

**Iter 0** | λ=1.259e-08 | RMSE=0.9923 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.18, L1_rough=96549.2967
  - Fit marginal: rmse=0.9923, rel_err=0.0573

**Iter 1** | λ=6.294e-09 | RMSE=0.9681 | under_regularized | → switch_reg_order_to_1
  - Under-regularisation suspected: osc=0.27, L1_rough=113640.9892
  - Fit marginal: rmse=0.9681, rel_err=0.0559

**Iter 2** | λ=6.294e-09 | RMSE=0.9616 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.18, L1_rough=105954.6492
  - Fit marginal: rmse=0.9616, rel_err=0.0555

**Iter 3** | λ=3.147e-09 | RMSE=0.9595 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.18, L1_rough=113744.0607
  - Fit marginal: rmse=0.9595, rel_err=0.0554

**Iter 4** | λ=1.573e-09 | RMSE=0.9569 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=0.59, L1_rough=139381.5074
  - Fit marginal: rmse=0.9569, rel_err=0.0553

**Iter 5** | λ=1.573e-09 | RMSE=0.9593 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.18, L1_rough=124514.3437
  - Fit marginal: rmse=0.9593, rel_err=0.0554

**Iter 6** | λ=7.867e-10 | RMSE=0.9572 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.27, L1_rough=139752.5666
  - Fit marginal: rmse=0.9572, rel_err=0.0553

**Iter 7** | λ=3.934e-09 | RMSE=0.9614 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.18, L1_rough=109338.1099
  - Fit marginal: rmse=0.9614, rel_err=0.0555

**Iter 8** | λ=1.967e-09 | RMSE=0.9598 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.18, L1_rough=120477.5652
  - Fit marginal: rmse=0.9598, rel_err=0.0554

## Notes

- Completed in 9 iteration(s)
