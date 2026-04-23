# IHCP Inversion Report

**Date:** 2026-04-20 17:21  
**Status:** `weak_pass`  
**Iterations:** 1  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (31 steps, dt=2.0000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (6 parameters)
- Regularisation order: 1
- Lambda: `1.6912e-08`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `3.842926`
- Regularisation norm: `32470.409822`
- Objective value: `32.598514`

### Estimated Parameters

```
  x[  0] = -1331.8748
  x[  1] = +16848.2261
  x[  2] = +42409.2619
  x[  3] = +50508.2105
  x[  4] = +51723.2583
  x[  5] = +53560.5347
```

## Iteration Trace

**Iter 0** | λ=1.691e-08 | RMSE=0.4881 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.04, L1_rough=54892.4095
  - Fit marginal: rmse=0.4881, rel_err=0.0238

## Notes

- Completed in 1 iteration(s)
