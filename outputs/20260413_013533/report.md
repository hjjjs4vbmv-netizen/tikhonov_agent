# IHCP Inversion Report

**Date:** 2026-04-13 01:35  
**Status:** `weak_pass`  
**Iterations:** 1  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 60 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 0.3

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `7.8438e-08`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `4.659673`
- Regularisation norm: `15349.746519`
- Objective value: `40.193729`

### Estimated Parameters

```
  x[  0] = +49917.2504
  x[  1] = +50169.5009
  x[  2] = +50539.3072
  x[  3] = +50828.7850
  x[  4] = +50869.6455
  x[  5] = +50443.6186
  x[  6] = +49350.0584
  x[  7] = +47337.6559
  x[  8] = +44154.6278
  x[  9] = +39851.8269
  x[ 10] = +34580.7221
  x[ 11] = +28646.5321
  x[ 12] = +22520.5329
  x[ 13] = +16790.1319
  x[ 14] = +11561.2265
  x[ 15] = +7048.7657
  x[ 16] = +3548.8987
  x[ 17] = +1233.5141
  x[ 18] = -81.6629
  x[ 19] = -771.1233
  x[ 20] = -1203.4251
  x[ 21] = -1541.4977
  x[ 22] = -1790.7692
  x[ 23] = -1886.9758
```

## Iteration Trace

**Iter 0** | λ=7.844e-08 | RMSE=0.2995 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.05, L1_rough=53709.0165
  - Fit marginal: rmse=0.2995, rel_err=0.0226

## Notes

- Completed in 1 iteration(s)
