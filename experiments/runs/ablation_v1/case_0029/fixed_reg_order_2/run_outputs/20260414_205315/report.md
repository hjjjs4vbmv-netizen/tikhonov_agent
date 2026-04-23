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
- Noise std: 1.0

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 2
- Lambda: `2.5411e-06`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.562034`
- Regularisation norm: `2771.126708`
- Objective value: `261.690193`

### Estimated Parameters

```
  x[  0] = +59298.3777
  x[  1] = +55514.3508
  x[  2] = +51724.8876
  x[  3] = +47966.4388
  x[  4] = +44334.8283
  x[  5] = +40999.4843
  x[  6] = +38192.6429
  x[  7] = +36157.1441
  x[  8] = +35072.8360
  x[  9] = +35006.0097
  x[ 10] = +35871.8368
  x[ 11] = +37419.2581
  x[ 12] = +39273.4344
  x[ 13] = +41015.5892
  x[ 14] = +42262.8685
  x[ 15] = +42729.1630
  x[ 16] = +42289.5667
  x[ 17] = +40975.3405
  x[ 18] = +38943.2243
  x[ 19] = +36409.2936
  x[ 20] = +33573.6034
  x[ 21] = +30601.8601
  x[ 22] = +27589.4266
  x[ 23] = +24570.0104
```

## Iteration Trace

**Iter 0** | λ=2.541e-06 | RMSE=1.0004 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.09, L1_rough=50174.6740
  - Fit marginal: rmse=1.0004, rel_err=0.0494

## Notes

- Completed in 1 iteration(s)
