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
- Noise std: 0.1

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `4.3884e-08`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.545522`
- Regularisation norm: `14641.885199`
- Objective value: `11.796702`

### Estimated Parameters

```
  x[  0] = +4459.8019
  x[  1] = +5588.1526
  x[  2] = +7774.6708
  x[  3] = +10729.2187
  x[  4] = +14092.9667
  x[  5] = +17570.3096
  x[  6] = +21040.4163
  x[  7] = +24495.3495
  x[  8] = +27866.6503
  x[  9] = +31168.8137
  x[ 10] = +34503.4656
  x[ 11] = +37864.7975
  x[ 12] = +41202.9936
  x[ 13] = +44537.8459
  x[ 14] = +47947.5705
  x[ 15] = +51328.6178
  x[ 16] = +54749.0726
  x[ 17] = +58184.1209
  x[ 18] = +61620.1786
  x[ 19] = +64991.1395
  x[ 20] = +67898.3958
  x[ 21] = +70147.5264
  x[ 22] = +71503.3662
  x[ 23] = +71936.5209
```

## Iteration Trace

**Iter 0** | λ=4.388e-08 | RMSE=0.0993 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=67476.7190
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
