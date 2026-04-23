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
- Lambda: `7.5787e-02`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.546664`
- Regularisation norm: `0.016343`
- Objective value: `56.952160`

### Estimated Parameters

```
  x[  0] = +1727.5794
  x[  1] = +5026.3353
  x[  2] = +8325.0915
  x[  3] = +11623.8488
  x[  4] = +14922.6083
  x[  5] = +18221.3712
  x[  6] = +21520.1391
  x[  7] = +24818.9130
  x[  8] = +28117.6936
  x[  9] = +31416.4812
  x[ 10] = +34715.2753
  x[ 11] = +38014.0749
  x[ 12] = +41312.8783
  x[ 13] = +44611.6836
  x[ 14] = +47910.4898
  x[ 15] = +51209.2960
  x[ 16] = +54508.1019
  x[ 17] = +57806.9072
  x[ 18] = +61105.7116
  x[ 19] = +64404.5151
  x[ 20] = +67703.3178
  x[ 21] = +71002.1198
  x[ 22] = +74300.9217
  x[ 23] = +77599.7236
```

## Iteration Trace

**Iter 0** | λ=7.579e-02 | RMSE=0.4851 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=75872.1442
  - Fit marginal: rmse=0.4851, rel_err=0.0220

## Notes

- Completed in 1 iteration(s)
