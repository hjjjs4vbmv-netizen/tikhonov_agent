# IHCP Inversion Report

**Date:** 2026-04-20 17:03  
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
- Regularisation order: 2
- Lambda: `3.0886e-05`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.682119`
- Regularisation norm: `977.542867`
- Objective value: `275.443372`

### Estimated Parameters

```
  x[  0] = -5925.1095
  x[  1] = -1163.7193
  x[  2] = +3591.1668
  x[  3] = +8325.6358
  x[  4] = +13015.4308
  x[  5] = +17624.6813
  x[  6] = +22106.5727
  x[  7] = +26405.5741
  x[  8] = +30462.7874
  x[  9] = +34225.8628
  x[ 10] = +37656.6559
  x[ 11] = +40734.0619
  x[ 12] = +43455.2869
  x[ 13] = +45835.4830
  x[ 14] = +47904.8306
  x[ 15] = +49703.8082
  x[ 16] = +51280.5077
  x[ 17] = +52685.2625
  x[ 18] = +53966.5316
  x[ 19] = +55166.6447
  x[ 20] = +56318.3252
  x[ 21] = +57446.0069
  x[ 22] = +58564.7179
  x[ 23] = +59681.4190
```

## Iteration Trace

**Iter 0** | λ=3.089e-05 | RMSE=1.0081 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=65606.5285
  - Fit marginal: rmse=1.0081, rel_err=0.0466

## Notes

- Completed in 1 iteration(s)
