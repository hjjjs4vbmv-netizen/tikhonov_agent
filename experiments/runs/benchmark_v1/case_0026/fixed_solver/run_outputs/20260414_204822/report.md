# IHCP Inversion Report

**Date:** 2026-04-14 20:48  
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
- Regularisation order: 1
- Lambda: `1.0000e+00`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `12.313892`
- Regularisation norm: `0.014244`
- Objective value: `151.632150`

### Estimated Parameters

```
  x[  0] = +41980.4373
  x[  1] = +41980.4365
  x[  2] = +41980.4346
  x[  3] = +41980.4317
  x[  4] = +41980.4280
  x[  5] = +41980.4236
  x[  6] = +41980.4188
  x[  7] = +41980.4141
  x[  8] = +41980.4096
  x[  9] = +41980.4056
  x[ 10] = +41980.4022
  x[ 11] = +41980.3994
  x[ 12] = +41980.3969
  x[ 13] = +41980.3945
  x[ 14] = +41980.3921
  x[ 15] = +41980.3895
  x[ 16] = +41980.3868
  x[ 17] = +41980.3840
  x[ 18] = +41980.3814
  x[ 19] = +41980.3791
  x[ 20] = +41980.3773
  x[ 21] = +41980.3762
  x[ 22] = +41980.3756
  x[ 23] = +41980.3755
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=0.7916 | well_regularized | → stop_success_weak_pass
  - Discrepancy principle: ||r||=12.3139 is above target=1.5556 (rel_dev=6.92)
  - Fit marginal: rmse=0.7916, rel_err=0.0450

## Notes

- Completed in 1 iteration(s)
