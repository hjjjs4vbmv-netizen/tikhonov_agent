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
- Noise std: 0.1

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `1.0000e+00`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `22.243101`
- Regularisation norm: `0.027536`
- Objective value: `494.756315`

### Estimated Parameters

```
  x[  0] = +35422.7033
  x[  1] = +35422.7038
  x[  2] = +35422.7047
  x[  3] = +35422.7060
  x[  4] = +35422.7073
  x[  5] = +35422.7082
  x[  6] = +35422.7084
  x[  7] = +35422.7074
  x[  8] = +35422.7051
  x[  9] = +35422.7011
  x[ 10] = +35422.6955
  x[ 11] = +35422.6883
  x[ 12] = +35422.6799
  x[ 13] = +35422.6704
  x[ 14] = +35422.6604
  x[ 15] = +35422.6504
  x[ 16] = +35422.6407
  x[ 17] = +35422.6320
  x[ 18] = +35422.6246
  x[ 19] = +35422.6187
  x[ 20] = +35422.6144
  x[ 21] = +35422.6118
  x[ 22] = +35422.6105
  x[ 23] = +35422.6102
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.4298 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=22.2431 is above target=1.5556 (rel_dev=13.30)
  - Fit marginal: rmse=1.4298, rel_err=0.0965

## Notes

- Completed in 1 iteration(s)
