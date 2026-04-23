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
- Noise std: 1.0

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `7.2886e-07`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.522390`
- Regularisation norm: `12308.763782`
- Objective value: `351.371299`

### Estimated Parameters

```
  x[  0] = +10354.1457
  x[  1] = +10804.9787
  x[  2] = +11840.0017
  x[  3] = +13375.7918
  x[  4] = +15355.1524
  x[  5] = +17718.6744
  x[  6] = +20488.0991
  x[  7] = +23523.5920
  x[  8] = +26803.9524
  x[  9] = +30307.0430
  x[ 10] = +33973.4912
  x[ 11] = +37748.7540
  x[ 12] = +41473.0133
  x[ 13] = +45019.7384
  x[ 14] = +48308.5477
  x[ 15] = +51361.7204
  x[ 16] = +54184.2917
  x[ 17] = +56717.5386
  x[ 18] = +58854.9914
  x[ 19] = +60578.0028
  x[ 20] = +61814.5256
  x[ 21] = +62560.2373
  x[ 22] = +62940.6455
  x[ 23] = +63073.2890
```

## Iteration Trace

**Iter 0** | λ=7.289e-07 | RMSE=0.9978 | well_regularized | → stop_success
  - skip_verifier=True: verification bypassed (ablation)

## Notes

- Completed in 1 iteration(s)
