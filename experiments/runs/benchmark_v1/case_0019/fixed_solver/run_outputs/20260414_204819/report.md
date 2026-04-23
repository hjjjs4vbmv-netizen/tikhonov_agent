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
- Residual norm: `15.035177`
- Regularisation norm: `0.022598`
- Objective value: `226.057054`

### Estimated Parameters

```
  x[  0] = +32743.3051
  x[  1] = +32743.3066
  x[  2] = +32743.3100
  x[  3] = +32743.3150
  x[  4] = +32743.3213
  x[  5] = +32743.3284
  x[  6] = +32743.3360
  x[  7] = +32743.3436
  x[  8] = +32743.3512
  x[  9] = +32743.3584
  x[ 10] = +32743.3652
  x[ 11] = +32743.3713
  x[ 12] = +32743.3766
  x[ 13] = +32743.3810
  x[ 14] = +32743.3846
  x[ 15] = +32743.3872
  x[ 16] = +32743.3891
  x[ 17] = +32743.3902
  x[ 18] = +32743.3907
  x[ 19] = +32743.3906
  x[ 20] = +32743.3901
  x[ 21] = +32743.3897
  x[ 22] = +32743.3893
  x[ 23] = +32743.3892
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=0.9665 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.0352 is above target=1.5556 (rel_dev=8.66)
  - Fit marginal: rmse=0.9665, rel_err=0.0635

## Notes

- Completed in 1 iteration(s)
