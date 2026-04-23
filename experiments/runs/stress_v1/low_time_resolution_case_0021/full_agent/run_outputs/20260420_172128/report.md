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
- Lambda: `1.2376e-08`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `3.806990`
- Regularisation norm: `37605.419245`
- Objective value: `31.995424`

### Estimated Parameters

```
  x[  0] = +21117.1590
  x[  1] = +42206.0603
  x[  2] = +55029.9770
  x[  3] = +41026.3281
  x[  4] = +18375.0531
  x[  5] = +8587.7901
```

## Iteration Trace

**Iter 0** | λ=1.238e-08 | RMSE=0.4835 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.14, L1_rough=80355.0049
  - Fit marginal: rmse=0.4835, rel_err=0.0317

## Notes

- Completed in 1 iteration(s)
