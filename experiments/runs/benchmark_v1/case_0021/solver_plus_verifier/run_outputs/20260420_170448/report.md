# IHCP Inversion Report

**Date:** 2026-04-20 17:04  
**Status:** `weak_pass`  
**Iterations:** 1  

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
- Regularisation order: 1
- Lambda: `4.3884e-08`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.696039`
- Regularisation norm: `18424.668671`
- Objective value: `74.126245`

### Estimated Parameters

```
  x[  0] = +5288.5289
  x[  1] = +8419.6154
  x[  2] = +14400.1433
  x[  3] = +22477.2969
  x[  4] = +30750.1186
  x[  5] = +36988.1816
  x[  6] = +40097.7096
  x[  7] = +40634.6945
  x[  8] = +39836.4218
  x[  9] = +39298.8222
  x[ 10] = +39940.6214
  x[ 11] = +40945.2077
  x[ 12] = +41038.8493
  x[ 13] = +40127.2152
  x[ 14] = +39365.5877
  x[ 15] = +39033.7288
  x[ 16] = +39283.7298
  x[ 17] = +38780.1934
  x[ 18] = +36328.0365
  x[ 19] = +31906.8514
  x[ 20] = +25743.8515
  x[ 21] = +20187.4197
  x[ 22] = +16805.8409
  x[ 23] = +15664.7537
```

## Iteration Trace

**Iter 0** | λ=4.388e-08 | RMSE=0.4947 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=64296.1627
  - Fit marginal: rmse=0.4947, rel_err=0.0298

## Notes

- Completed in 1 iteration(s)
