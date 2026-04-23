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
- Noise std: 0.1

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 2
- Lambda: `8.1939e-08`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.567769`
- Regularisation norm: `5562.079391`
- Objective value: `4.992837`

### Estimated Parameters

```
  x[  0] = +7330.1390
  x[  1] = +13905.9515
  x[  2] = +20582.8018
  x[  3] = +27454.4805
  x[  4] = +34500.3829
  x[  5] = +41497.8672
  x[  6] = +48026.3363
  x[  7] = +53483.4474
  x[  8] = +57294.4065
  x[  9] = +59020.5933
  x[ 10] = +58433.6740
  x[ 11] = +55560.9301
  x[ 12] = +50656.7428
  x[ 13] = +44209.5725
  x[ 14] = +36886.0626
  x[ 15] = +29429.4856
  x[ 16] = +22485.4886
  x[ 17] = +16475.4378
  x[ 18] = +11564.7476
  x[ 19] = +7715.0984
  x[ 20] = +4703.5939
  x[ 21] = +2238.3824
  x[ 22] = +62.9875
  x[ 23] = -2017.6203
```

## Iteration Trace

**Iter 0** | λ=8.194e-08 | RMSE=0.1008 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=112728.6680
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
