# IHCP Inversion Report

**Date:** 2026-04-14 20:52  
**Status:** `weak_pass`  
**Iterations:** 1  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 1.0

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 0
- Lambda: `1.2587e-08`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.681526`
- Regularisation norm: `189984.682496`
- Objective value: `700.239335`

### Estimated Parameters

```
  x[  0] = +3093.9981
  x[  1] = +9692.6212
  x[  2] = +9305.4709
  x[  3] = +12514.1805
  x[  4] = +17021.4453
  x[  5] = +19310.4409
  x[  6] = +20482.4639
  x[  7] = +25274.4773
  x[  8] = +28160.2556
  x[  9] = +28463.4132
  x[ 10] = +32243.5095
  x[ 11] = +37324.8572
  x[ 12] = +40176.8584
  x[ 13] = +41049.2029
  x[ 14] = +47977.2463
  x[ 15] = +48841.7569
  x[ 16] = +52297.7203
  x[ 17] = +53822.3624
  x[ 18] = +54297.9515
  x[ 19] = +62554.4206
  x[ 20] = +60513.6928
  x[ 21] = +57456.4205
  x[ 22] = +46575.3020
  x[ 23] = +19451.9306
```

## Iteration Trace

**Iter 0** | λ=1.259e-08 | RMSE=1.0080 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.14, L1_rough=103337.2130
  - Fit marginal: rmse=1.0080, rel_err=0.0413

## Notes

- Completed in 1 iteration(s)
