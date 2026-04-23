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
- Lambda: `3.5499e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `3.910151`
- Regularisation norm: `38463.554230`
- Objective value: `20.541212`

### Estimated Parameters

```
  x[  0] = +59038.3663
  x[  1] = +38959.1944
  x[  2] = +28498.5044
  x[  3] = +48722.6438
  x[  4] = +47323.6294
  x[  5] = +23746.6752
```

## Iteration Trace

**Iter 0** | λ=3.550e-09 | RMSE=0.4966 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.18, L1_rough=75739.9699
  - Fit marginal: rmse=0.4966, rel_err=0.0268

## Notes

- Completed in 1 iteration(s)
