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
- Regularisation order: 0
- Lambda: `1.0356e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.579033`
- Regularisation norm: `167501.351196`
- Objective value: `31.548568`

### Estimated Parameters

```
  x[  0] = +1938.0555
  x[  1] = +2488.8453
  x[  2] = +10095.8283
  x[  3] = +20642.0429
  x[  4] = +36287.5200
  x[  5] = +43970.0824
  x[  6] = +49876.5525
  x[  7] = +40772.4621
  x[  8] = +31977.2833
  x[  9] = +31790.5721
  x[ 10] = +37606.5431
  x[ 11] = +47980.4964
  x[ 12] = +48987.0562
  x[ 13] = +42391.6673
  x[ 14] = +32415.5731
  x[ 15] = +30889.1797
  x[ 16] = +38434.7280
  x[ 17] = +48546.7756
  x[ 18] = +46522.1123
  x[ 19] = +38213.7032
  x[ 20] = +24410.6351
  x[ 21] = +9941.3572
  x[ 22] = +2960.6604
  x[ 23] = +2272.8838
```

## Iteration Trace

**Iter 0** | λ=1.036e-09 | RMSE=0.1015 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.04, L1_rough=165250.3258
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
