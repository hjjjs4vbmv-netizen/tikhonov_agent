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
- Lambda: `8.1939e-08`
- Lambda strategy: `discrepancy`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `7.834626`
- Regularisation norm: `21949.525005`
- Objective value: `100.858249`

### Estimated Parameters

```
  x[  0] = +16779.6614
  x[  1] = +18497.3339
  x[  2] = +22318.3073
  x[  3] = +27598.0108
  x[  4] = +33718.4364
  x[  5] = +39998.2806
  x[  6] = +46106.0421
  x[  7] = +51036.0293
  x[  8] = +54417.2553
  x[  9] = +56048.4064
  x[ 10] = +55790.6412
  x[ 11] = +53774.6211
  x[ 12] = +49884.2955
  x[ 13] = +44303.7371
  x[ 14] = +37487.2802
  x[ 15] = +30334.7414
  x[ 16] = +23606.7341
  x[ 17] = +17683.8617
  x[ 18] = +12609.0042
  x[ 19] = +8661.3318
  x[ 20] = +5695.4095
  x[ 21] = +3630.5512
  x[ 22] = +2652.0734
  x[ 23] = +2498.0228
```

## Iteration Trace

**Iter 0** | λ=8.194e-08 | RMSE=0.5036 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=92819.1285
  - Fit marginal: rmse=0.5036, rel_err=0.0316

## Notes

- Completed in 1 iteration(s)
