# IHCP Inversion Report

**Date:** 2026-04-20 17:03  
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
- Regularisation order: 0
- Lambda: `6.7414e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.913413`
- Regularisation norm: `187097.236479`
- Objective value: `298.605615`

### Estimated Parameters

```
  x[  0] = -1090.2262
  x[  1] = +2660.0977
  x[  2] = +216.2295
  x[  3] = +801.6052
  x[  4] = +2970.2190
  x[  5] = +5351.6333
  x[  6] = +12676.4087
  x[  7] = +30772.9082
  x[  8] = +43182.8274
  x[  9] = +45613.6314
  x[ 10] = +47626.0057
  x[ 11] = +49611.4676
  x[ 12] = +49385.9690
  x[ 13] = +47287.2466
  x[ 14] = +50671.6029
  x[ 15] = +48614.5650
  x[ 16] = +49147.3289
  x[ 17] = +48012.2141
  x[ 18] = +45842.6936
  x[ 19] = +51039.3423
  x[ 20] = +47904.8821
  x[ 21] = +45718.1515
  x[ 22] = +38427.1941
  x[ 23] = +16777.4097
```

## Iteration Trace

**Iter 0** | λ=6.741e-09 | RMSE=0.5087 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.02, L1_rough=106651.0259
  - Fit marginal: rmse=0.5087, rel_err=0.0257

## Notes

- Completed in 1 iteration(s)
