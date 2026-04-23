# IHCP Inversion Report

**Date:** 2026-04-20 17:03  
**Status:** `pass`  
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
- Lambda: `1.5300e-07`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.850572`
- Regularisation norm: `17100.326650`
- Objective value: `106.370646`

### Estimated Parameters

```
  x[  0] = -2361.9598
  x[  1] = -1631.5900
  x[  2] = -64.7139
  x[  3] = +2670.4237
  x[  4] = +6807.9083
  x[  5] = +12436.3247
  x[  6] = +19452.6616
  x[  7] = +27267.4619
  x[  8] = +34628.4330
  x[  9] = +40631.3413
  x[ 10] = +45091.6452
  x[ 11] = +48074.7985
  x[ 12] = +49777.9309
  x[ 13] = +50552.8577
  x[ 14] = +50811.0885
  x[ 15] = +50647.4470
  x[ 16] = +50350.2759
  x[ 17] = +50045.4344
  x[ 18] = +49881.1942
  x[ 19] = +49976.1331
  x[ 20] = +50046.3099
  x[ 21] = +50159.6233
  x[ 22] = +50266.1271
  x[ 23] = +50286.8506
```

## Iteration Trace

**Iter 0** | λ=1.530e-07 | RMSE=0.5047 | well_regularized | → stop_success
  - skip_verifier=True: verification bypassed (ablation)

## Notes

- Completed in 1 iteration(s)
