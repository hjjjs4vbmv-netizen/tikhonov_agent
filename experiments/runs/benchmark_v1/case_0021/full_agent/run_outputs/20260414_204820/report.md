# IHCP Inversion Report

**Date:** 2026-04-14 20:48  
**Status:** `weak_pass`  
**Iterations:** 2  

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
- Lambda: `5.3340e-07`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.786359`
- Regularisation norm: `3670.117653`
- Objective value: `67.812146`

### Estimated Parameters

```
  x[  0] = +826.9244
  x[  1] = +8738.0185
  x[  2] = +16474.7431
  x[  3] = +23709.9996
  x[  4] = +30000.1155
  x[  5] = +34933.3422
  x[  6] = +38317.8789
  x[  7] = +40269.5275
  x[  8] = +41142.7469
  x[  9] = +41386.4758
  x[ 10] = +41365.9934
  x[ 11] = +41253.2649
  x[ 12] = +41080.7682
  x[ 13] = +40848.3089
  x[ 14] = +40538.2261
  x[ 15] = +40030.1445
  x[ 16] = +39095.1373
  x[ 17] = +37412.3131
  x[ 18] = +34716.7051
  x[ 19] = +30933.1158
  x[ 20] = +26199.2403
  x[ 21] = +20851.5567
  x[ 22] = +15227.5736
  x[ 23] = +9534.4290
```

## Iteration Trace

**Iter 0** | λ=4.388e-08 | RMSE=0.4947 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=0.23, L1_rough=64296.1627
  - Fit marginal: rmse=0.4947, rel_err=0.0298

**Iter 1** | λ=5.334e-07 | RMSE=0.5005 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.05, L1_rough=72411.5982
  - Fit marginal: rmse=0.5005, rel_err=0.0302

## Notes

- Completed in 2 iteration(s)
