# IHCP Inversion Report

**Date:** 2026-04-20 17:04  
**Status:** `fail`  
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
- Residual norm: `16.616428`
- Regularisation norm: `0.022097`
- Objective value: `276.106170`

### Estimated Parameters

```
  x[  0] = +32856.4206
  x[  1] = +32856.4221
  x[  2] = +32856.4254
  x[  3] = +32856.4303
  x[  4] = +32856.4364
  x[  5] = +32856.4433
  x[  6] = +32856.4506
  x[  7] = +32856.4581
  x[  8] = +32856.4655
  x[  9] = +32856.4726
  x[ 10] = +32856.4793
  x[ 11] = +32856.4854
  x[ 12] = +32856.4907
  x[ 13] = +32856.4950
  x[ 14] = +32856.4984
  x[ 15] = +32856.5009
  x[ 16] = +32856.5027
  x[ 17] = +32856.5037
  x[ 18] = +32856.5040
  x[ 19] = +32856.5038
  x[ 20] = +32856.5033
  x[ 21] = +32856.5028
  x[ 22] = +32856.5024
  x[ 23] = +32856.5023
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.0681 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=16.6164 is above target=7.7782 (rel_dev=1.14)
  - Fit marginal: rmse=1.0681, rel_err=0.0645

## Notes

- Completed in 1 iteration(s)
