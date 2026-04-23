# IHCP Inversion Report

**Date:** 2026-04-23 19:57  
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

- Solver: `tsvd`
- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 2
- Lambda: `1.0000e-02`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `14.524965`
- Regularisation norm: `380767.936498`
- Objective value: `1449842425.625219`

### Estimated Parameters

```
  x[  0] = +26975.5146
  x[  1] = -34955.5551
  x[  2] = +52034.1183
  x[  3] = -30843.9068
  x[  4] = +87085.5699
  x[  5] = -76828.2282
  x[  6] = +94537.4297
  x[  7] = -3037.1800
  x[  8] = +18935.4183
  x[  9] = +53949.7449
  x[ 10] = -10358.0210
  x[ 11] = +69017.5470
  x[ 12] = +24689.7409
  x[ 13] = +80601.3076
  x[ 14] = +29509.2826
  x[ 15] = +57017.3024
  x[ 16] = +24469.4983
  x[ 17] = +105220.5005
  x[ 18] = +19437.0831
  x[ 19] = +80484.9051
  x[ 20] = +86246.0209
  x[ 21] = +55772.5648
  x[ 22] = +44777.2618
  x[ 23] = +126626.8830
```

## Iteration Trace

**Iter 0** | λ=1.000e-02 | RMSE=0.9337 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=5.53, L1_rough=1551301.5288
  - Fit marginal: rmse=0.9337, rel_err=0.0399

## Notes

- Completed in 1 iteration(s)
