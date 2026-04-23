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
- Noise std: 0.1

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 2
- Lambda: `3.3028e-07`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `3.612405`
- Regularisation norm: `4454.609544`
- Objective value: `19.603320`

### Estimated Parameters

```
  x[  0] = -1216.7621
  x[  1] = +7407.0994
  x[  2] = +15857.6232
  x[  3] = +23752.3980
  x[  4] = +30554.8950
  x[  5] = +35759.2421
  x[  6] = +39130.5449
  x[  7] = +40840.5099
  x[  8] = +41390.4113
  x[  9] = +41372.7819
  x[ 10] = +41219.7912
  x[ 11] = +41103.7091
  x[ 12] = +41033.8357
  x[ 13] = +41002.0467
  x[ 14] = +41004.3289
  x[ 15] = +40920.4796
  x[ 16] = +40420.2278
  x[ 17] = +39002.0751
  x[ 18] = +36213.7145
  x[ 19] = +31890.2015
  x[ 20] = +26233.7641
  x[ 21] = +19710.7842
  x[ 22] = +12798.5285
  x[ 23] = +5794.1256
```

## Iteration Trace

**Iter 0** | λ=2.642e-09 | RMSE=0.1024 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=0.23, L1_rough=143533.7107
  - Fit is good but regularisation balance is uncertain

**Iter 1** | λ=2.642e-09 | RMSE=0.1016 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.23, L1_rough=154161.6794
  - Fit is good but regularisation balance is uncertain

**Iter 2** | λ=1.321e-08 | RMSE=0.1410 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=2.1935 is above target=1.5556 (rel_dev=0.41)
  - Under-regularisation suspected: osc=0.23, L1_rough=123936.9292
  - Fit is good but regularisation balance is uncertain

**Iter 3** | λ=6.606e-08 | RMSE=0.1810 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=2.8152 is above target=1.5556 (rel_dev=0.81)
  - Under-regularisation suspected: osc=0.23, L1_rough=96534.5500
  - Fit is good but regularisation balance is uncertain

**Iter 4** | λ=3.303e-07 | RMSE=0.2322 | under_regularized | → stop_success_weak_pass
  - Discrepancy principle: ||r||=3.6124 is above target=1.5556 (rel_dev=1.32)
  - Under-regularisation suspected: osc=0.14, L1_rough=78208.0235
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 5 iteration(s)
