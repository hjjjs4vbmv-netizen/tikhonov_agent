# IHCP Inversion Report

**Date:** 2026-04-13 11:20  
**Status:** `fail`  
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
- Regularisation order: 1
- Lambda: `1.0000e+00`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `35.690449`
- Regularisation norm: `0.084845`
- Objective value: `1273.815384`

### Estimated Parameters

```
  x[  0] = +30706.4368
  x[  1] = +30706.4402
  x[  2] = +30706.4480
  x[  3] = +30706.4602
  x[  4] = +30706.4764
  x[  5] = +30706.4962
  x[  6] = +30706.5191
  x[  7] = +30706.5443
  x[  8] = +30706.5709
  x[  9] = +30706.5979
  x[ 10] = +30706.6246
  x[ 11] = +30706.6504
  x[ 12] = +30706.6747
  x[ 13] = +30706.6970
  x[ 14] = +30706.7171
  x[ 15] = +30706.7347
  x[ 16] = +30706.7496
  x[ 17] = +30706.7619
  x[ 18] = +30706.7714
  x[ 19] = +30706.7785
  x[ 20] = +30706.7833
  x[ 21] = +30706.7861
  x[ 22] = +30706.7873
  x[ 23] = +30706.7877
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=2.2943 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.6904 is above target=1.5556 (rel_dev=21.94)
  - Fit failed: rmse=2.2943 > threshold 2.0

## Notes

- Completed in 1 iteration(s)
