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
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 0
- Lambda: `3.6104e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.796741`
- Regularisation norm: `192749.562270`
- Objective value: `194.925762`

### Estimated Parameters

```
  x[  0] = +2193.6844
  x[  1] = -686.4218
  x[  2] = +2234.1166
  x[  3] = +1537.7037
  x[  4] = +2507.1419
  x[  5] = -2561.6947
  x[  6] = +13912.9505
  x[  7] = +31240.3264
  x[  8] = +43636.9624
  x[  9] = +48004.0423
  x[ 10] = +45914.3092
  x[ 11] = +50578.4589
  x[ 12] = +52414.0869
  x[ 13] = +53936.2756
  x[ 14] = +49713.7597
  x[ 15] = +47353.4813
  x[ 16] = +48114.5429
  x[ 17] = +51814.7106
  x[ 18] = +47887.1161
  x[ 19] = +50910.1204
  x[ 20] = +51864.6079
  x[ 21] = +45553.3981
  x[ 22] = +39328.8039
  x[ 23] = +22709.8842
```

## Iteration Trace

**Iter 0** | λ=3.610e-09 | RMSE=0.5012 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.03, L1_rough=121316.6026
  - Fit marginal: rmse=0.5012, rel_err=0.0257

## Notes

- Completed in 1 iteration(s)
