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
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `4.3884e-08`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.805600`
- Regularisation norm: `19783.676746`
- Objective value: `78.103319`

### Estimated Parameters

```
  x[  0] = -1091.9864
  x[  1] = -1136.6684
  x[  2] = -707.9805
  x[  3] = +462.5461
  x[  4] = +3248.3286
  x[  5] = +8520.8045
  x[  6] = +17235.5230
  x[  7] = +27552.1109
  x[  8] = +37053.4694
  x[  9] = +44126.7470
  x[ 10] = +48611.3892
  x[ 11] = +51348.2515
  x[ 12] = +52541.4466
  x[ 13] = +52490.8671
  x[ 14] = +51535.1314
  x[ 15] = +50543.9015
  x[ 16] = +50048.7389
  x[ 17] = +49981.2771
  x[ 18] = +49855.9642
  x[ 19] = +49867.1457
  x[ 20] = +49637.4660
  x[ 21] = +49104.9026
  x[ 22] = +48900.5950
  x[ 23] = +49057.5940
```

## Iteration Trace

**Iter 0** | λ=4.388e-08 | RMSE=0.5018 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=57543.0104
  - Fit marginal: rmse=0.5018, rel_err=0.0257

## Notes

- Completed in 1 iteration(s)
