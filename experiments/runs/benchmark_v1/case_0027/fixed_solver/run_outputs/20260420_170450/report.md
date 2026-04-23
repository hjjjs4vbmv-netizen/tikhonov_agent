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
- Lambda: `1.0000e+00`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `14.187769`
- Regularisation norm: `0.015682`
- Objective value: `201.293043`

### Estimated Parameters

```
  x[  0] = +41775.0129
  x[  1] = +41775.0120
  x[  2] = +41775.0100
  x[  3] = +41775.0070
  x[  4] = +41775.0029
  x[  5] = +41774.9982
  x[  6] = +41774.9930
  x[  7] = +41774.9877
  x[  8] = +41774.9828
  x[  9] = +41774.9783
  x[ 10] = +41774.9744
  x[ 11] = +41774.9710
  x[ 12] = +41774.9681
  x[ 13] = +41774.9653
  x[ 14] = +41774.9626
  x[ 15] = +41774.9597
  x[ 16] = +41774.9567
  x[ 17] = +41774.9538
  x[ 18] = +41774.9510
  x[ 19] = +41774.9487
  x[ 20] = +41774.9469
  x[ 21] = +41774.9458
  x[ 22] = +41774.9453
  x[ 23] = +41774.9452
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=0.9120 | well_regularized | → stop_success_weak_pass
  - Discrepancy principle: ||r||=14.1878 is above target=7.7782 (rel_dev=0.82)
  - Fit marginal: rmse=0.9120, rel_err=0.0490

## Notes

- Completed in 1 iteration(s)
