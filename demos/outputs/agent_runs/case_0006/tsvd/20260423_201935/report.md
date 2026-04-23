# IHCP Inversion Report

**Date:** 2026-04-23 20:19  
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
- Residual norm: `14.514775`
- Regularisation norm: `366083.009255`
- Objective value: `210.678699`

### Estimated Parameters

```
  x[  0] = +25641.9070
  x[  1] = -39595.7970
  x[  2] = +43925.7953
  x[  3] = -41893.9398
  x[  4] = +71718.3700
  x[  5] = -93087.6273
  x[  6] = +68399.9437
  x[  7] = +14020.9313
  x[  8] = +43490.6430
  x[  9] = +71606.1204
  x[ 10] = +5387.0872
  x[ 11] = +80849.1308
  x[ 12] = +33425.3941
  x[ 13] = +85906.3915
  x[ 14] = +31520.9059
  x[ 15] = +55679.1312
  x[ 16] = +19805.0622
  x[ 17] = +97219.0113
  x[ 18] = +8105.7901
  x[ 19] = +65813.9190
  x[ 20] = +68256.2847
  x[ 21] = +34414.2243
  x[ 22] = +20172.4816
  x[ 23] = +98450.2617
```

## Iteration Trace

**Iter 0** | λ=1.000e-02 | RMSE=0.9330 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=5.92, L1_rough=1495491.9497
  - Fit marginal: rmse=0.9330, rel_err=0.0444

## Notes

- Completed in 1 iteration(s)
