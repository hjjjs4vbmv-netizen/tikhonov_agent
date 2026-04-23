# IHCP Inversion Report

**Date:** 2026-04-20 17:21  
**Status:** `weak_pass`  
**Iterations:** 1  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 1 at positions [0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `2.6919e-02`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `5.046988`
- Regularisation norm: `0.036061`
- Objective value: `25.472121`

### Estimated Parameters

```
  x[  0] = +42287.4146
  x[  1] = +42287.4116
  x[  2] = +42287.4051
  x[  3] = +42287.3957
  x[  4] = +42287.3841
  x[  5] = +42287.3711
  x[  6] = +42287.3576
  x[  7] = +42287.3442
  x[  8] = +42287.3318
  x[  9] = +42287.3207
  x[ 10] = +42287.3114
  x[ 11] = +42287.3038
  x[ 12] = +42287.2978
  x[ 13] = +42287.2934
  x[ 14] = +42287.2902
  x[ 15] = +42287.2880
  x[ 16] = +42287.2865
  x[ 17] = +42287.2855
  x[ 18] = +42287.2848
  x[ 19] = +42287.2844
  x[ 20] = +42287.2842
  x[ 21] = +42287.2841
  x[ 22] = +42287.2841
  x[ 23] = +42287.2841
```

## Iteration Trace

**Iter 0** | λ=2.692e-02 | RMSE=0.4588 | well_regularized | → stop_success_weak_pass
  - Fit marginal: rmse=0.4588, rel_err=0.0490

## Notes

- Completed in 1 iteration(s)
