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
- Residual norm: `6.924501`
- Regularisation norm: `0.029819`
- Objective value: `47.948776`

### Estimated Parameters

```
  x[  0] = +1701.2465
  x[  1] = +4974.0917
  x[  2] = +8246.9369
  x[  3] = +11519.7824
  x[  4] = +14792.6287
  x[  5] = +18065.4768
  x[  6] = +21338.3279
  x[  7] = +24611.1834
  x[  8] = +27884.0448
  x[  9] = +31156.9135
  x[ 10] = +34429.7910
  x[ 11] = +37702.6781
  x[ 12] = +40975.5753
  x[ 13] = +44248.4826
  x[ 14] = +47521.4000
  x[ 15] = +50794.3266
  x[ 16] = +54067.2618
  x[ 17] = +57340.2045
  x[ 18] = +60613.1536
  x[ 19] = +63886.1075
  x[ 20] = +67159.0646
  x[ 21] = +70432.0236
  x[ 22] = +73704.9833
  x[ 23] = +76977.9432
```

## Iteration Trace

**Iter 0** | λ=7.579e-02 | RMSE=0.4451 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=75276.6967
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
