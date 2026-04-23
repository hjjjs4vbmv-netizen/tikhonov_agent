# IHCP Inversion Report

**Date:** 2026-04-14 20:53  
**Status:** `weak_pass`  
**Iterations:** 6  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 0.1

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 2
- Lambda: `1.2945e-07`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `3.228161`
- Regularisation norm: `6085.653997`
- Objective value: `15.215177`

### Estimated Parameters

```
  x[  0] = -3854.1493
  x[  1] = +5946.7112
  x[  2] = +15592.0123
  x[  3] = +24606.0485
  x[  4] = +32221.6036
  x[  5] = +37664.6659
  x[  6] = +40606.1901
  x[  7] = +41406.7075
  x[  8] = +41016.5116
  x[  9] = +40436.5166
  x[ 10] = +40199.1111
  x[ 11] = +40272.0186
  x[ 12] = +40379.8698
  x[ 13] = +40440.9861
  x[ 14] = +40643.8702
  x[ 15] = +41113.1567
  x[ 16] = +41487.5453
  x[ 17] = +40883.8663
  x[ 18] = +38340.9529
  x[ 19] = +33399.1459
  x[ 20] = +26313.9776
  x[ 21] = +17846.4692
  x[ 22] = +8800.1817
  x[ 23] = -358.6515
```

## Iteration Trace

**Iter 0** | λ=1.036e-09 | RMSE=0.1015 | under_regularized | → switch_reg_order_to_1
  - Under-regularisation suspected: osc=0.23, L1_rough=165250.3258
  - Fit is good but regularisation balance is uncertain

**Iter 1** | λ=1.415e-09 | RMSE=0.1010 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=0.23, L1_rough=160438.9950
  - Fit is good but regularisation balance is uncertain

**Iter 2** | λ=1.036e-09 | RMSE=0.0992 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.23, L1_rough=170501.1871
  - Fit is good but regularisation balance is uncertain

**Iter 3** | λ=5.178e-09 | RMSE=0.1236 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=1.9227 is above target=1.5556 (rel_dev=0.24)
  - Under-regularisation suspected: osc=0.23, L1_rough=145683.8412
  - Fit is good but regularisation balance is uncertain

**Iter 4** | λ=2.589e-08 | RMSE=0.1676 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=2.6076 is above target=1.5556 (rel_dev=0.68)
  - Under-regularisation suspected: osc=0.23, L1_rough=113160.3809
  - Fit is good but regularisation balance is uncertain

**Iter 5** | λ=1.294e-07 | RMSE=0.2075 | under_regularized | → stop_success_weak_pass
  - Discrepancy principle: ||r||=3.2282 is above target=1.5556 (rel_dev=1.08)
  - Under-regularisation suspected: osc=0.14, L1_rough=89603.0842
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 6 iteration(s)
