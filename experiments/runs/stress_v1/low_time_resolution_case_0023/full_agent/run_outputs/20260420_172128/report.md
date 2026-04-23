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
- Lambda: `9.0573e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `3.969333`
- Regularisation norm: `22501.833677`
- Objective value: `20.341620`

### Estimated Parameters

```
  x[  0] = +52718.7745
  x[  1] = +43053.2165
  x[  2] = +32022.4048
  x[  3] = +45344.4543
  x[  4] = +42820.8847
  x[  5] = +32458.1970
```

## Iteration Trace

**Iter 0** | λ=9.057e-09 | RMSE=0.5041 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.09, L1_rough=46904.6764
  - Fit marginal: rmse=0.5041, rel_err=0.0271

## Notes

- Completed in 1 iteration(s)
