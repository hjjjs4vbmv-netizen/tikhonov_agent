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
- Regularisation order: 2
- Lambda: `1.7200e-08`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.791555`
- Regularisation norm: `13208.895564`
- Objective value: `63.709278`

### Estimated Parameters

```
  x[  0] = -4845.1330
  x[  1] = +4738.8706
  x[  2] = +15048.7795
  x[  3] = +25784.0001
  x[  4] = +35362.1610
  x[  5] = +41454.2084
  x[  6] = +43006.6839
  x[  7] = +40355.1990
  x[  8] = +36831.4886
  x[  9] = +35934.5860
  x[ 10] = +38465.0427
  x[ 11] = +42293.0906
  x[ 12] = +43885.8728
  x[ 13] = +42007.1706
  x[ 14] = +38742.4316
  x[ 15] = +37649.8997
  x[ 16] = +39887.4864
  x[ 17] = +42882.3611
  x[ 18] = +42597.5886
  x[ 19] = +37161.9951
  x[ 20] = +27021.6942
  x[ 21] = +14510.1921
  x[ 22] = +2155.4954
  x[ 23] = -9503.4845
```

## Iteration Trace

**Iter 0** | λ=1.720e-08 | RMSE=0.5009 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.01, L1_rough=126729.4817
  - Fit marginal: rmse=0.5009, rel_err=0.0302

## Notes

- Completed in 1 iteration(s)
