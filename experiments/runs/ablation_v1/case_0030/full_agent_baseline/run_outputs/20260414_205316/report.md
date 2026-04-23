# IHCP Inversion Report

**Date:** 2026-04-14 20:53  
**Status:** `weak_pass`  
**Iterations:** 1  

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
- Lambda: `5.9965e-08`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.519320`
- Regularisation norm: `21473.132193`
- Objective value: `268.498987`

### Estimated Parameters

```
  x[  0] = +56804.0082
  x[  1] = +56670.7657
  x[  2] = +56077.8823
  x[  3] = +53641.9340
  x[  4] = +48946.2419
  x[  5] = +42349.6004
  x[  6] = +35876.2239
  x[  7] = +29933.0496
  x[  8] = +26277.1890
  x[  9] = +26180.0930
  x[ 10] = +29764.9192
  x[ 11] = +36490.4256
  x[ 12] = +43963.5951
  x[ 13] = +49902.9269
  x[ 14] = +52658.8547
  x[ 15] = +52282.2994
  x[ 16] = +49355.0046
  x[ 17] = +44483.6990
  x[ 18] = +38258.9229
  x[ 19] = +32427.3170
  x[ 20] = +27598.8853
  x[ 21] = +24193.4423
  x[ 22] = +22884.7994
  x[ 23] = +22953.1749
```

## Iteration Trace

**Iter 0** | λ=5.997e-08 | RMSE=0.9976 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.14, L1_rough=86945.1077
  - Fit marginal: rmse=0.9976, rel_err=0.0491

## Notes

- Completed in 1 iteration(s)
