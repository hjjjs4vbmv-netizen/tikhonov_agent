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
- Lambda: `5.9764e-10`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `14.811399`
- Regularisation norm: `62731.952749`
- Objective value: `221.729422`

### Estimated Parameters

```
  x[  0] = +16045.4328
  x[  1] = +8662.3406
  x[  2] = +24289.7025
  x[  3] = +31039.2794
  x[  4] = +39347.1840
  x[  5] = +25124.2633
  x[  6] = +57360.9850
  x[  7] = +55184.3914
  x[  8] = +53282.9330
  x[  9] = +57319.7003
  x[ 10] = +47523.2231
  x[ 11] = +57781.4983
  x[ 12] = +58642.9295
  x[ 13] = +56437.3747
  x[ 14] = +35320.1479
  x[ 15] = +20182.0289
  x[ 16] = +17829.9432
  x[ 17] = +23501.4013
  x[ 18] = +4669.5838
  x[ 19] = +11424.6033
  x[ 20] = +13301.5357
  x[ 21] = -7955.6810
  x[ 22] = -8468.0843
  x[ 23] = +13448.1046
```

## Iteration Trace

**Iter 0** | λ=1.530e-07 | RMSE=0.9942 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=83642.8295
  - Fit marginal: rmse=0.9942, rel_err=0.0574

**Iter 1** | λ=7.650e-08 | RMSE=0.9748 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=91547.8131
  - Fit marginal: rmse=0.9748, rel_err=0.0563

**Iter 2** | λ=3.825e-08 | RMSE=0.9678 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=96166.3309
  - Fit marginal: rmse=0.9678, rel_err=0.0559

**Iter 3** | λ=1.912e-08 | RMSE=0.9648 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=98798.9555
  - Fit marginal: rmse=0.9648, rel_err=0.0557

**Iter 4** | λ=9.562e-09 | RMSE=0.9627 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.01, L1_rough=102779.2471
  - Fit marginal: rmse=0.9627, rel_err=0.0556

**Iter 5** | λ=4.781e-09 | RMSE=0.9608 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.01, L1_rough=108421.6310
  - Fit marginal: rmse=0.9608, rel_err=0.0555

**Iter 6** | λ=2.391e-09 | RMSE=0.9585 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.03, L1_rough=118365.8543
  - Fit marginal: rmse=0.9585, rel_err=0.0554

**Iter 7** | λ=1.195e-09 | RMSE=0.9557 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.10, L1_rough=158731.1485
  - Fit marginal: rmse=0.9557, rel_err=0.0552

**Iter 8** | λ=5.976e-10 | RMSE=0.9521 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.27, L1_rough=231192.6039
  - Fit marginal: rmse=0.9521, rel_err=0.0550

## Notes

- Completed in 9 iteration(s)
