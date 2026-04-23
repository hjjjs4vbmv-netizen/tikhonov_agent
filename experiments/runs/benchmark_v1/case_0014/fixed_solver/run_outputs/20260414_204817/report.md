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
- Residual norm: `22.237924`
- Regularisation norm: `0.027422`
- Objective value: `494.526031`

### Estimated Parameters

```
  x[  0] = +35475.7930
  x[  1] = +35475.7935
  x[  2] = +35475.7945
  x[  3] = +35475.7958
  x[  4] = +35475.7971
  x[  5] = +35475.7980
  x[  6] = +35475.7982
  x[  7] = +35475.7973
  x[  8] = +35475.7950
  x[  9] = +35475.7911
  x[ 10] = +35475.7856
  x[ 11] = +35475.7785
  x[ 12] = +35475.7701
  x[ 13] = +35475.7607
  x[ 14] = +35475.7507
  x[ 15] = +35475.7407
  x[ 16] = +35475.7311
  x[ 17] = +35475.7224
  x[ 18] = +35475.7149
  x[ 19] = +35475.7090
  x[ 20] = +35475.7048
  x[ 21] = +35475.7021
  x[ 22] = +35475.7008
  x[ 23] = +35475.7005
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.4295 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=22.2379 is above target=1.5556 (rel_dev=13.30)
  - Fit marginal: rmse=1.4295, rel_err=0.0959

## Notes

- Completed in 1 iteration(s)
