# IHCP Inversion Report

**Date:** 2026-04-14 20:53  
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
- Lambda: `6.7414e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.562597`
- Regularisation norm: `16735.192963`
- Objective value: `4.329739`

### Estimated Parameters

```
  x[  0] = +47345.2923
  x[  1] = +53501.8362
  x[  2] = +58134.6168
  x[  3] = +58880.6204
  x[  4] = +54619.2246
  x[  5] = +46172.9958
  x[  6] = +36032.8901
  x[  7] = +26712.2418
  x[  8] = +20817.3483
  x[  9] = +20107.0421
  x[ 10] = +24883.9109
  x[ 11] = +33968.0058
  x[ 12] = +44651.9433
  x[ 13] = +53836.2125
  x[ 14] = +59018.2510
  x[ 15] = +59108.2870
  x[ 16] = +54292.4745
  x[ 17] = +45825.1959
  x[ 18] = +35894.8974
  x[ 19] = +27361.7674
  x[ 20] = +22254.6798
  x[ 21] = +21221.2506
  x[ 22] = +23469.8225
  x[ 23] = +27089.9873
```

## Iteration Trace

**Iter 0** | λ=6.741e-09 | RMSE=0.1004 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.18, L1_rough=133065.9245
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
