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
- Residual norm: `1.555654`
- Regularisation norm: `199956.504000`
- Objective value: `32.721649`

### Estimated Parameters

```
  x[  0] = -1673.8758
  x[  1] = +2367.6289
  x[  2] = -900.8569
  x[  3] = -118.4080
  x[  4] = +814.9194
  x[  5] = -535.1328
  x[  6] = +3508.9927
  x[  7] = +35773.7908
  x[  8] = +51685.1440
  x[  9] = +49049.4388
  x[ 10] = +49391.9548
  x[ 11] = +50459.3859
  x[ 12] = +50489.6062
  x[ 13] = +47863.7270
  x[ 14] = +51824.5791
  x[ 15] = +48850.9127
  x[ 16] = +50352.0365
  x[ 17] = +50117.9759
  x[ 18] = +47042.0774
  x[ 19] = +52640.6588
  x[ 20] = +48804.7818
  x[ 21] = +50026.4929
  x[ 22] = +52296.5929
  x[ 23] = +32472.5363
```

## Iteration Trace

**Iter 0** | λ=7.579e-10 | RMSE=0.1000 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.06, L1_rough=113793.7751
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
