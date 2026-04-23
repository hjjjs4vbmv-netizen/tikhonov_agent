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
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `1.0000e+00`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `23.214792`
- Regularisation norm: `0.028442`
- Objective value: `538.927387`

### Estimated Parameters

```
  x[  0] = +35270.3686
  x[  1] = +35270.3690
  x[  2] = +35270.3699
  x[  3] = +35270.3710
  x[  4] = +35270.3720
  x[  5] = +35270.3726
  x[  6] = +35270.3723
  x[  7] = +35270.3710
  x[  8] = +35270.3681
  x[  9] = +35270.3637
  x[ 10] = +35270.3577
  x[ 11] = +35270.3501
  x[ 12] = +35270.3412
  x[ 13] = +35270.3314
  x[ 14] = +35270.3211
  x[ 15] = +35270.3108
  x[ 16] = +35270.3010
  x[ 17] = +35270.2921
  x[ 18] = +35270.2845
  x[ 19] = +35270.2786
  x[ 20] = +35270.2743
  x[ 21] = +35270.2717
  x[ 22] = +35270.2704
  x[ 23] = +35270.2701
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.4923 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=23.2148 is above target=7.7782 (rel_dev=1.98)
  - Fit marginal: rmse=1.4923, rel_err=0.0942

## Notes

- Completed in 1 iteration(s)
