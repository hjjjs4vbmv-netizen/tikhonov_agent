# IHCP Inversion Report

**Date:** 2026-04-20 17:04  
**Status:** `fail`  
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
- Regularisation order: 1
- Lambda: `1.0000e+00`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `36.191305`
- Regularisation norm: `0.084337`
- Objective value: `1309.817646`

### Estimated Parameters

```
  x[  0] = +30819.5524
  x[  1] = +30819.5558
  x[  2] = +30819.5635
  x[  3] = +30819.5755
  x[  4] = +30819.5915
  x[  5] = +30819.6111
  x[  6] = +30819.6339
  x[  7] = +30819.6589
  x[  8] = +30819.6853
  x[  9] = +30819.7122
  x[ 10] = +30819.7388
  x[ 11] = +30819.7645
  x[ 12] = +30819.7888
  x[ 13] = +30819.8111
  x[ 14] = +30819.8310
  x[ 15] = +30819.8485
  x[ 16] = +30819.8633
  x[ 17] = +30819.8754
  x[ 18] = +30819.8849
  x[ 19] = +30819.8918
  x[ 20] = +30819.8965
  x[ 21] = +30819.8992
  x[ 22] = +30819.9005
  x[ 23] = +30819.9008
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=2.3265 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=36.1913 is above target=7.7782 (rel_dev=3.65)
  - Fit failed: rmse=2.3265 > threshold 2.0

## Notes

- Completed in 1 iteration(s)
