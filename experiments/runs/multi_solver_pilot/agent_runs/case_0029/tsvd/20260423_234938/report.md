# IHCP Inversion Report

**Date:** 2026-04-23 23:49  
**Status:** `weak_pass`  
**Iterations:** 3  

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
- Lambda: `5.0000e-02`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `13.805427`
- Regularisation norm: `31539.738552`
- Objective value: `190.589827`

### Estimated Parameters

```
  x[  0] = +38993.7841
  x[  1] = +56377.3035
  x[  2] = +63044.6578
  x[  3] = +61326.3121
  x[  4] = +54296.2286
  x[  5] = +47252.6776
  x[  6] = +38809.4697
  x[  7] = +27201.9074
  x[  8] = +17980.3235
  x[  9] = +17506.5829
  x[ 10] = +24096.3287
  x[ 11] = +32448.9212
  x[ 12] = +41731.3054
  x[ 13] = +52451.8134
  x[ 14] = +60234.2596
  x[ 15] = +60011.8523
  x[ 16] = +52815.5212
  x[ 17] = +42618.9794
  x[ 18] = +31236.6419
  x[ 19] = +22076.8419
  x[ 20] = +21851.4186
  x[ 21] = +29575.7538
  x[ 22] = +30369.9911
  x[ 23] = +13742.3846
```

## Iteration Trace

**Iter 0** | λ=1.000e-02 | RMSE=0.8518 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=5.91, L1_rough=1397557.2187
  - Fit marginal: rmse=0.8518, rel_err=0.0421

**Iter 1** | λ=1.000e-02 | RMSE=0.8518 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=5.91, L1_rough=1397557.2187
  - Fit marginal: rmse=0.8518, rel_err=0.0421

**Iter 2** | λ=5.000e-02 | RMSE=0.8874 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.02, L1_rough=175845.6453
  - Fit marginal: rmse=0.8874, rel_err=0.0438

## Notes

- Completed in 3 iteration(s)
