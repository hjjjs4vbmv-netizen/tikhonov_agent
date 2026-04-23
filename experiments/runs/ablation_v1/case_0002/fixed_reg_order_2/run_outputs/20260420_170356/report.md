# IHCP Inversion Report

**Date:** 2026-04-20 17:03  
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
- Lambda: `7.5787e-10`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.544643`
- Regularisation norm: `23867.237695`
- Objective value: `2.817637`

### Estimated Parameters

```
  x[  0] = +49.0732
  x[  1] = +143.5149
  x[  2] = +1004.9199
  x[  3] = +498.7947
  x[  4] = -2240.5255
  x[  5] = -2939.6179
  x[  6] = +9385.5563
  x[  7] = +32493.5675
  x[  8] = +49234.7982
  x[  9] = +52466.6613
  x[ 10] = +49983.4866
  x[ 11] = +49469.1927
  x[ 12] = +50498.4231
  x[ 13] = +51023.8002
  x[ 14] = +50106.5149
  x[ 15] = +49331.1457
  x[ 16] = +49593.9762
  x[ 17] = +50178.3045
  x[ 18] = +49985.2481
  x[ 19] = +50402.3237
  x[ 20] = +50320.1268
  x[ 21] = +49180.6974
  x[ 22] = +49207.8833
  x[ 23] = +50948.3293
```

## Iteration Trace

**Iter 0** | λ=7.579e-10 | RMSE=0.0993 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.01, L1_rough=70997.9434
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
