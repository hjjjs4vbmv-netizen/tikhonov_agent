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
- Noise std: 1.0

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 0
- Lambda: `6.7414e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.654069`
- Regularisation norm: `200635.456318`
- Objective value: `516.420137`

### Estimated Parameters

```
  x[  0] = +6449.1498
  x[  1] = +5739.7866
  x[  2] = +11694.2893
  x[  3] = +14014.4767
  x[  4] = +17462.7989
  x[  5] = +12609.7714
  x[  6] = +24184.4957
  x[  7] = +24092.4255
  x[  8] = +24866.1976
  x[  9] = +28495.5335
  x[ 10] = +29252.6147
  x[ 11] = +38850.1115
  x[ 12] = +45381.6775
  x[ 13] = +50420.8481
  x[ 14] = +47995.7944
  x[ 15] = +47666.9998
  x[ 16] = +51771.1393
  x[ 17] = +59471.1756
  x[ 18] = +58505.0680
  x[ 19] = +64946.0589
  x[ 20] = +67836.5051
  x[ 21] = +60088.8654
  x[ 22] = +49632.9343
  x[ 23] = +26663.3303
```

## Iteration Trace

**Iter 0** | λ=6.741e-09 | RMSE=1.0063 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.03, L1_rough=121309.3636
  - Fit marginal: rmse=1.0063, rel_err=0.0430

## Notes

- Completed in 1 iteration(s)
