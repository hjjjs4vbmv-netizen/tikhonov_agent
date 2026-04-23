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
- Noise std: 0.1

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 0
- Lambda: `7.5787e-10`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.645249`
- Regularisation norm: `199917.319493`
- Objective value: `32.996560`

### Estimated Parameters

```
  x[  0] = +1027.7236
  x[  1] = -998.3122
  x[  2] = +995.1531
  x[  3] = -3.9273
  x[  4] = +1622.9379
  x[  5] = -3942.1972
  x[  6] = +6658.5318
  x[  7] = +34872.8892
  x[  8] = +50234.9490
  x[  9] = +50537.5721
  x[ 10] = +48166.9827
  x[ 11] = +50550.0677
  x[ 12] = +50372.2606
  x[ 13] = +51484.9507
  x[ 14] = +49685.2861
  x[ 15] = +49173.3505
  x[ 16] = +49208.6833
  x[ 17] = +51446.6368
  x[ 18] = +48572.8794
  x[ 19] = +50408.1819
  x[ 20] = +51141.0876
  x[ 21] = +48921.7192
  x[ 22] = +49989.3360
  x[ 23] = +34370.7420
```

## Iteration Trace

**Iter 0** | λ=7.579e-10 | RMSE=0.1058 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.04, L1_rough=101666.9541
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
