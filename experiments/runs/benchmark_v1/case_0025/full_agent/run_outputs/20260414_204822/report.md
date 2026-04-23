# IHCP Inversion Report

**Date:** 2026-04-14 20:48  
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
- Regularisation order: 1
- Lambda: `4.9335e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.555818`
- Regularisation norm: `30061.708228`
- Objective value: `6.878989`

### Estimated Parameters

```
  x[  0] = +49268.0218
  x[  1] = +53086.7015
  x[  2] = +57058.0647
  x[  3] = +57996.6591
  x[  4] = +54198.9187
  x[  5] = +46058.1835
  x[  6] = +36025.4329
  x[  7] = +27309.6171
  x[  8] = +21818.5153
  x[  9] = +20960.1962
  x[ 10] = +25502.2190
  x[ 11] = +34044.1696
  x[ 12] = +43899.7211
  x[ 13] = +52554.0049
  x[ 14] = +58268.7660
  x[ 15] = +58627.6796
  x[ 16] = +54014.0906
  x[ 17] = +45454.5548
  x[ 18] = +35559.7569
  x[ 19] = +27714.7393
  x[ 20] = +22765.6854
  x[ 21] = +22218.7439
  x[ 22] = +24423.0601
  x[ 23] = +25907.0610
```

## Iteration Trace

**Iter 0** | λ=4.933e-09 | RMSE=0.1000 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.18, L1_rough=123529.8365
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
