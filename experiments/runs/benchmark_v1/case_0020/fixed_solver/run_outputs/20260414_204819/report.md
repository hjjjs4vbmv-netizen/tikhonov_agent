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
- Residual norm: `15.122738`
- Regularisation norm: `0.022762`
- Objective value: `228.697717`

### Estimated Parameters

```
  x[  0] = +32796.3949
  x[  1] = +32796.3965
  x[  2] = +32796.3998
  x[  3] = +32796.4049
  x[  4] = +32796.4112
  x[  5] = +32796.4183
  x[  6] = +32796.4259
  x[  7] = +32796.4336
  x[  8] = +32796.4412
  x[  9] = +32796.4486
  x[ 10] = +32796.4554
  x[ 11] = +32796.4616
  x[ 12] = +32796.4670
  x[ 13] = +32796.4714
  x[ 14] = +32796.4750
  x[ 15] = +32796.4777
  x[ 16] = +32796.4796
  x[ 17] = +32796.4807
  x[ 18] = +32796.4812
  x[ 19] = +32796.4810
  x[ 20] = +32796.4806
  x[ 21] = +32796.4801
  x[ 22] = +32796.4798
  x[ 23] = +32796.4797
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=0.9721 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.1227 is above target=1.5556 (rel_dev=8.72)
  - Fit marginal: rmse=0.9721, rel_err=0.0640

## Notes

- Completed in 1 iteration(s)
