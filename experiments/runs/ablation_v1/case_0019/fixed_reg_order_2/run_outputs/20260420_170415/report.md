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
- Lambda: `2.6422e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.580318`
- Regularisation norm: `23686.488240`
- Objective value: `3.979817`

### Estimated Parameters

```
  x[  0] = -2500.8011
  x[  1] = +3146.7081
  x[  2] = +10562.0687
  x[  3] = +22193.7014
  x[  4] = +35975.2086
  x[  5] = +45815.5369
  x[  6] = +47048.9714
  x[  7] = +40998.3930
  x[  8] = +34069.9443
  x[  9] = +33036.6989
  x[ 10] = +39035.8707
  x[ 11] = +45950.6672
  x[ 12] = +46699.5145
  x[ 13] = +40679.4825
  x[ 14] = +34189.7989
  x[ 15] = +33327.5939
  x[ 16] = +39140.4862
  x[ 17] = +45724.4642
  x[ 18] = +46161.0012
  x[ 19] = +38388.4715
  x[ 20] = +25256.9141
  x[ 21] = +12745.9935
  x[ 22] = +3345.1301
  x[ 23] = -4570.4897
```

## Iteration Trace

**Iter 0** | λ=2.642e-09 | RMSE=0.1016 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.02, L1_rough=154161.6794
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
