# IHCP Inversion Report

**Date:** 2026-04-20 17:03  
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
- Regularisation order: 0
- Lambda: `1.7200e-08`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.860769`
- Regularisation norm: `174271.683158`
- Objective value: `773.936396`

### Estimated Parameters

```
  x[  0] = +224.3087
  x[  1] = +3747.7252
  x[  2] = +2204.0634
  x[  3] = +3450.8884
  x[  4] = +6515.7801
  x[  5] = +9888.0042
  x[  6] = +16146.6232
  x[  7] = +28905.6877
  x[  8] = +38243.7285
  x[  9] = +41326.8097
  x[ 10] = +44356.5865
  x[ 11] = +47044.2300
  x[ 12] = +47405.3839
  x[ 13] = +45979.1255
  x[ 14] = +48849.4390
  x[ 15] = +47121.1356
  x[ 16] = +47177.2228
  x[ 17] = +45750.3609
  x[ 18] = +43570.0434
  x[ 19] = +47116.6092
  x[ 20] = +43043.3006
  x[ 21] = +38504.6987
  x[ 22] = +29576.2735
  x[ 23] = +11700.4391
```

## Iteration Trace

**Iter 0** | λ=1.720e-08 | RMSE=1.0196 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.01, L1_rough=98919.2767
  - Fit marginal: rmse=1.0196, rel_err=0.0471

## Notes

- Completed in 1 iteration(s)
