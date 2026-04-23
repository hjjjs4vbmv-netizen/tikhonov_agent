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
- Regularisation order: 0
- Lambda: `1.4151e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.558017`
- Regularisation norm: `173986.604873`
- Objective value: `45.263763`

### Estimated Parameters

```
  x[  0] = +10745.3671
  x[  1] = +14113.4411
  x[  2] = +20300.1435
  x[  3] = +26350.3034
  x[  4] = +34348.7328
  x[  5] = +38852.4358
  x[  6] = +49062.3075
  x[  7] = +53507.4910
  x[  8] = +57108.1326
  x[  9] = +59399.2915
  x[ 10] = +57386.0024
  x[ 11] = +55837.2345
  x[ 12] = +50843.6322
  x[ 13] = +44905.2445
  x[ 14] = +36203.1485
  x[ 15] = +28266.1866
  x[ 16] = +21620.1975
  x[ 17] = +17170.3135
  x[ 18] = +10511.7498
  x[ 19] = +8027.6103
  x[ 20] = +5838.1181
  x[ 21] = +2021.5309
  x[ 22] = +816.6471
  x[ 23] = +1717.0899
```

## Iteration Trace

**Iter 0** | λ=1.415e-09 | RMSE=0.1002 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.01, L1_rough=108137.0116
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
