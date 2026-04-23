# IHCP Inversion Report

**Date:** 2026-04-14 20:53  
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
- Regularisation order: 2
- Lambda: `1.2587e-08`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.533468`
- Regularisation norm: `15853.317242`
- Objective value: `5.515068`

### Estimated Parameters

```
  x[  0] = +48255.0762
  x[  1] = +53683.1464
  x[  2] = +57574.6169
  x[  3] = +58062.4135
  x[  4] = +54076.6679
  x[  5] = +46103.5468
  x[  6] = +36195.4277
  x[  7] = +27161.3168
  x[  8] = +21478.7347
  x[  9] = +20748.6821
  x[ 10] = +25287.0201
  x[ 11] = +33831.8351
  x[ 12] = +43972.8655
  x[ 13] = +52972.1596
  x[ 14] = +58444.4256
  x[ 15] = +58778.4401
  x[ 16] = +53969.6500
  x[ 17] = +45470.4518
  x[ 18] = +35845.1760
  x[ 19] = +27810.3562
  x[ 20] = +23003.5569
  x[ 21] = +21842.6585
  x[ 22] = +23215.0960
  x[ 23] = +25427.1269
```

## Iteration Trace

**Iter 0** | λ=1.259e-08 | RMSE=0.0986 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.18, L1_rough=125671.0767
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
