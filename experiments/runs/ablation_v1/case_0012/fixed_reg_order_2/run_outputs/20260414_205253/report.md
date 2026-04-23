# IHCP Inversion Report

**Date:** 2026-04-14 20:52  
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
- Lambda: `7.5787e-02`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.094368`
- Regularisation norm: `0.032632`
- Objective value: `227.840027`

### Estimated Parameters

```
  x[  0] = +2122.3985
  x[  1] = +5386.4859
  x[  2] = +8650.5740
  x[  3] = +11914.6642
  x[  4] = +15178.7587
  x[  5] = +18442.8602
  x[  6] = +21706.9716
  x[  7] = +24971.0948
  x[  8] = +28235.2316
  x[  9] = +31499.3823
  x[ 10] = +34763.5460
  x[ 11] = +38027.7207
  x[ 12] = +41291.9028
  x[ 13] = +44556.0890
  x[ 14] = +47820.2766
  x[ 15] = +51084.4643
  x[ 16] = +54348.6515
  x[ 17] = +57612.8374
  x[ 18] = +60877.0216
  x[ 19] = +64141.2038
  x[ 20] = +67405.3843
  x[ 21] = +70669.5636
  x[ 22] = +73933.7426
  x[ 23] = +77197.9216
```

## Iteration Trace

**Iter 0** | λ=7.579e-02 | RMSE=0.9703 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=75075.5231
  - Fit marginal: rmse=0.9703, rel_err=0.0414

## Notes

- Completed in 1 iteration(s)
