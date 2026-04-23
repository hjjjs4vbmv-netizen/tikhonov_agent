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
- Lambda: `1.4151e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.600142`
- Regularisation norm: `204780.579268`
- Objective value: `61.901930`

### Estimated Parameters

```
  x[  0] = +41839.5629
  x[  1] = +56627.9162
  x[  2] = +57557.1186
  x[  3] = +58424.8447
  x[  4] = +54808.4026
  x[  5] = +46215.4765
  x[  6] = +35281.6473
  x[  7] = +27656.1268
  x[  8] = +22374.0164
  x[  9] = +20444.4557
  x[ 10] = +25360.0960
  x[ 11] = +34483.2156
  x[ 12] = +44201.0739
  x[ 13] = +51316.9913
  x[ 14] = +59222.7931
  x[ 15] = +57958.1071
  x[ 16] = +54316.3817
  x[ 17] = +45693.5601
  x[ 18] = +33966.8230
  x[ 19] = +28859.4762
  x[ 20] = +21225.0688
  x[ 21] = +21534.0569
  x[ 22] = +25894.2772
  x[ 23] = +16972.8381
```

## Iteration Trace

**Iter 0** | λ=1.415e-09 | RMSE=0.1029 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.02, L1_rough=144932.3800
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
