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
- Noise std: 0.1

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 0
- Lambda: `7.5787e-10`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.785212`
- Regularisation norm: `217408.851465`
- Objective value: `39.008898`

### Estimated Parameters

```
  x[  0] = +2832.5876
  x[  1] = +3648.8632
  x[  2] = +8962.7772
  x[  3] = +11272.8017
  x[  4] = +16286.5441
  x[  5] = +15049.1872
  x[  6] = +23384.1010
  x[  7] = +24341.7911
  x[  8] = +27277.5124
  x[  9] = +31633.2866
  x[ 10] = +32924.3071
  x[ 11] = +38588.8570
  x[ 12] = +41728.9984
  x[ 13] = +46167.3558
  x[ 14] = +47693.0557
  x[ 15] = +50506.8974
  x[ 16] = +53868.0692
  x[ 17] = +59431.5220
  x[ 18] = +59883.3947
  x[ 19] = +65038.9137
  x[ 20] = +69062.7845
  x[ 21] = +70398.6519
  x[ 22] = +75437.0119
  x[ 23] = +52194.9441
```

## Iteration Trace

**Iter 0** | λ=7.579e-10 | RMSE=0.1148 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.14, L1_rough=98321.2059
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
