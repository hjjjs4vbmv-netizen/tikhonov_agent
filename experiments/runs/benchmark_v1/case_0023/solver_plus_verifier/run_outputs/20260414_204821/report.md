# IHCP Inversion Report

**Date:** 2026-04-14 20:48  
**Status:** `fail`  
**Iterations:** 1  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 1.0

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `5.3340e-07`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.527235`
- Regularisation norm: `7701.341436`
- Objective value: `272.731259`

### Estimated Parameters

```
  x[  0] = +18627.8735
  x[  1] = +19603.5236
  x[  2] = +21587.0790
  x[  3] = +24361.1021
  x[  4] = +27499.5492
  x[  5] = +30519.9269
  x[  6] = +33105.1365
  x[  7] = +35164.8412
  x[  8] = +36700.6814
  x[  9] = +37828.9736
  x[ 10] = +38674.0216
  x[ 11] = +39181.3611
  x[ 12] = +39243.6007
  x[ 13] = +38885.2693
  x[ 14] = +38265.1120
  x[ 15] = +37400.6754
  x[ 16] = +36378.8898
  x[ 17] = +35147.9007
  x[ 18] = +33713.2436
  x[ 19] = +32210.7480
  x[ 20] = +30708.7008
  x[ 21] = +29542.3518
  x[ 22] = +28887.9821
  x[ 23] = +28679.2992
```

## Iteration Trace

**Iter 0** | λ=5.334e-07 | RMSE=0.9981 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=31180.0288
  - Fit marginal: rmse=0.9981, rel_err=0.0545

## Notes

- Completed in 1 iteration(s)
