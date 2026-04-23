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
- Residual norm: `1.543939`
- Regularisation norm: `166448.603169`
- Objective value: `41.588716`

### Estimated Parameters

```
  x[  0] = +130.8677
  x[  1] = +5078.6619
  x[  2] = +9091.6710
  x[  3] = +20597.0571
  x[  4] = +35502.0381
  x[  5] = +46154.7987
  x[  6] = +46945.5258
  x[  7] = +41311.7269
  x[  8] = +33542.2354
  x[  9] = +31238.3539
  x[ 10] = +38677.3116
  x[ 11] = +47458.9224
  x[ 12] = +48239.1013
  x[ 13] = +39545.6091
  x[ 14] = +34177.3783
  x[ 15] = +31492.4248
  x[ 16] = +39301.0822
  x[ 17] = +46724.1835
  x[ 18] = +45035.1742
  x[ 19] = +39235.1308
  x[ 20] = +22870.4725
  x[ 21] = +11251.0615
  x[ 22] = +5046.7296
  x[ 23] = +946.3960
```

## Iteration Trace

**Iter 0** | λ=1.415e-09 | RMSE=0.0992 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.03, L1_rough=157278.8000
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
