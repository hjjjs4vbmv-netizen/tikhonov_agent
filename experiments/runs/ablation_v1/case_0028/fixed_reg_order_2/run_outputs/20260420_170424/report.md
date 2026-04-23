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
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 2
- Lambda: `5.9965e-08`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.783736`
- Regularisation norm: `12286.778347`
- Objective value: `69.639190`

### Estimated Parameters

```
  x[  0] = +55117.5818
  x[  1] = +56459.4637
  x[  2] = +57022.0273
  x[  3] = +55443.7094
  x[  4] = +50891.8671
  x[  5] = +43662.4409
  x[  6] = +35275.2612
  x[  7] = +27624.3837
  x[  8] = +22860.6291
  x[  9] = +22541.2871
  x[ 10] = +26965.3897
  x[ 11] = +35020.1604
  x[ 12] = +44299.8091
  x[ 13] = +52111.2384
  x[ 14] = +56415.1487
  x[ 15] = +56471.1304
  x[ 16] = +52670.6301
  x[ 17] = +46148.9589
  x[ 18] = +38429.8631
  x[ 19] = +31134.4922
  x[ 20] = +25206.8348
  x[ 21] = +20856.7167
  x[ 22] = +17761.2020
  x[ 23] = +15197.2895
```

## Iteration Trace

**Iter 0** | λ=5.997e-08 | RMSE=0.5004 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=111588.8698
  - Fit marginal: rmse=0.5004, rel_err=0.0268

## Notes

- Completed in 1 iteration(s)
