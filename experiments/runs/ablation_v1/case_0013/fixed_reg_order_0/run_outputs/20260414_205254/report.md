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
- Lambda: `1.9336e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.515786`
- Regularisation norm: `173437.691883`
- Objective value: `60.462510`

### Estimated Parameters

```
  x[  0] = +9347.7764
  x[  1] = +16167.2096
  x[  2] = +19403.4060
  x[  3] = +26099.0244
  x[  4] = +33948.4603
  x[  5] = +41028.6060
  x[  6] = +47078.3303
  x[  7] = +53802.7698
  x[  8] = +57862.9157
  x[  9] = +58419.8174
  x[ 10] = +58016.8626
  x[ 11] = +55616.6358
  x[ 12] = +50330.0404
  x[ 13] = +42471.7721
  x[ 14] = +37188.7154
  x[ 15] = +28535.7242
  x[ 16] = +22336.5855
  x[ 17] = +16080.4184
  x[ 18] = +9839.5293
  x[ 19] = +9061.8462
  x[ 20] = +4590.7832
  x[ 21] = +2988.5401
  x[ 22] = +2444.5797
  x[ 23] = +663.6293
```

## Iteration Trace

**Iter 0** | λ=1.934e-09 | RMSE=0.0974 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.05, L1_rough=106828.2292
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
