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
- Noise std: 0.1

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 2
- Lambda: `1.0356e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.542562`
- Regularisation norm: `29992.394780`
- Objective value: `3.311056`

### Estimated Parameters

```
  x[  0] = -317.9183
  x[  1] = +2793.0986
  x[  2] = +9480.5484
  x[  3] = +21334.2459
  x[  4] = +35897.8706
  x[  5] = +46547.4947
  x[  6] = +48689.7543
  x[  7] = +41166.7797
  x[  8] = +32304.0152
  x[  9] = +31042.7383
  x[ 10] = +38382.1793
  x[ 11] = +47621.8969
  x[ 12] = +49384.0936
  x[ 13] = +42011.2063
  x[ 14] = +32676.1753
  x[ 15] = +31006.2708
  x[ 16] = +38668.2759
  x[ 17] = +47654.1368
  x[ 18] = +48221.4522
  x[ 19] = +38938.3361
  x[ 20] = +24184.9969
  x[ 21] = +10630.3308
  x[ 22] = +2633.1356
  x[ 23] = -1690.6868
```

## Iteration Trace

**Iter 0** | λ=1.036e-09 | RMSE=0.0992 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.03, L1_rough=170501.1871
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
