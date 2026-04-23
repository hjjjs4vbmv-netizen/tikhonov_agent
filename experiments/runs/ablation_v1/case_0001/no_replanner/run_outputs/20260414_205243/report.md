# IHCP Inversion Report

**Date:** 2026-04-14 20:52  
**Status:** `fail`  
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
- Lambda: `1.9336e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.559188`
- Regularisation norm: `29501.016974`
- Objective value: `4.113928`

### Estimated Parameters

```
  x[  0] = -445.8214
  x[  1] = +620.0352
  x[  2] = +61.5472
  x[  3] = -677.7658
  x[  4] = -1601.8049
  x[  5] = -480.2391
  x[  6] = +10010.8123
  x[  7] = +31976.9403
  x[  8] = +47989.6782
  x[  9] = +51592.2989
  x[ 10] = +50866.9725
  x[ 11] = +50273.7046
  x[ 12] = +49829.0056
  x[ 13] = +49422.4514
  x[ 14] = +50247.3543
  x[ 15] = +49956.9006
  x[ 16] = +49947.7018
  x[ 17] = +49529.4481
  x[ 18] = +49164.7595
  x[ 19] = +50422.9408
  x[ 20] = +50000.0411
  x[ 21] = +50020.8881
  x[ 22] = +50412.0067
  x[ 23] = +50290.0113
```

## Iteration Trace

**Iter 0** | λ=1.934e-09 | RMSE=0.1002 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=0.41, L1_rough=62774.1877
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
