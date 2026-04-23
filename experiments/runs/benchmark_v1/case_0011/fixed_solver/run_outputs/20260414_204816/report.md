# IHCP Inversion Report

**Date:** 2026-04-14 20:48  
**Status:** `fail`  
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
- Lambda: `1.0000e+00`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `36.519419`
- Regularisation norm: `0.084257`
- Objective value: `1333.675098`

### Estimated Parameters

```
  x[  0] = +31717.0580
  x[  1] = +31717.0610
  x[  2] = +31717.0677
  x[  3] = +31717.0781
  x[  4] = +31717.0920
  x[  5] = +31717.1089
  x[  6] = +31717.1286
  x[  7] = +31717.1506
  x[  8] = +31717.1744
  x[  9] = +31717.1994
  x[ 10] = +31717.2251
  x[ 11] = +31717.2509
  x[ 12] = +31717.2762
  x[ 13] = +31717.3005
  x[ 14] = +31717.3232
  x[ 15] = +31717.3439
  x[ 16] = +31717.3621
  x[ 17] = +31717.3776
  x[ 18] = +31717.3903
  x[ 19] = +31717.4000
  x[ 20] = +31717.4068
  x[ 21] = +31717.4110
  x[ 22] = +31717.4130
  x[ 23] = +31717.4135
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=2.3476 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=36.5194 is above target=15.5563 (rel_dev=1.35)
  - Fit failed: rmse=2.3476 > threshold 2.0

## Notes

- Completed in 1 iteration(s)
