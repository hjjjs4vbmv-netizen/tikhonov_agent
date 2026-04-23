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
- Lambda: `4.8508e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `3.947738`
- Regularisation norm: `39020.217548`
- Objective value: `22.970357`

### Estimated Parameters

```
  x[  0] = -865.1425
  x[  1] = +11595.4032
  x[  2] = +48109.6143
  x[  3] = +50772.1726
  x[  4] = +53242.0728
  x[  5] = +48677.5424
```

## Iteration Trace

**Iter 0** | λ=4.851e-09 | RMSE=0.5014 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.17, L1_rough=58671.7458
  - Fit marginal: rmse=0.5014, rel_err=0.0259

## Notes

- Completed in 1 iteration(s)
