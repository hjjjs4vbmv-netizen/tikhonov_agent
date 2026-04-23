# IHCP Inversion Report

**Date:** 2026-04-14 20:52  
**Status:** `weak_pass`  
**Iterations:** 3  

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
- Lambda: `1.1197e-07`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.788140`
- Regularisation norm: `6551.146018`
- Objective value: `65.460427`

### Estimated Parameters

```
  x[  0] = -1522.3140
  x[  1] = -1749.4752
  x[  2] = -1574.6885
  x[  3] = -293.1136
  x[  4] = +2974.5159
  x[  5] = +8873.0844
  x[  6] = +17368.6009
  x[  7] = +27258.3799
  x[  8] = +36786.5121
  x[  9] = +44489.5697
  x[ 10] = +49714.8222
  x[ 11] = +52559.6454
  x[ 12] = +53437.9090
  x[ 13] = +52948.1497
  x[ 14] = +51765.8060
  x[ 15] = +50568.1119
  x[ 16] = +49777.6630
  x[ 17] = +49449.3347
  x[ 18] = +49389.7336
  x[ 19] = +49422.8260
  x[ 20] = +49361.1798
  x[ 21] = +49172.8222
  x[ 22] = +49000.6524
  x[ 23] = +48897.1025
```

## Iteration Trace

**Iter 0** | λ=3.610e-09 | RMSE=0.5012 | under_regularized | → switch_reg_order_to_1
  - Under-regularisation suspected: osc=0.55, L1_rough=121316.6026
  - Fit marginal: rmse=0.5012, rel_err=0.0257

**Iter 1** | λ=4.388e-08 | RMSE=0.5018 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=0.23, L1_rough=57543.0104
  - Fit marginal: rmse=0.5018, rel_err=0.0257

**Iter 2** | λ=1.120e-07 | RMSE=0.5006 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.18, L1_rough=60021.5367
  - Fit marginal: rmse=0.5006, rel_err=0.0256

## Notes

- Completed in 3 iteration(s)
