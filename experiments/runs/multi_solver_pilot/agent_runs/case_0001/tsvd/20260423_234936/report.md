# IHCP Inversion Report

**Date:** 2026-04-23 23:49  
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

- Solver: `tsvd`
- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `1.0000e-02`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `1.332789`
- Regularisation norm: `64819.494936`
- Objective value: `1.776326`

### Estimated Parameters

```
  x[  0] = -4510.5443
  x[  1] = +6585.3449
  x[  2] = -4193.3672
  x[  3] = +1447.6066
  x[  4] = -456.2247
  x[  5] = +3248.0423
  x[  6] = -7342.5256
  x[  7] = +42962.9085
  x[  8] = +53994.0485
  x[  9] = +46634.0126
  x[ 10] = +50686.3219
  x[ 11] = +49253.9486
  x[ 12] = +53384.1288
  x[ 13] = +43388.1673
  x[ 14] = +56595.2301
  x[ 15] = +45654.5318
  x[ 16] = +51104.3908
  x[ 17] = +52725.7701
  x[ 18] = +41694.5415
  x[ 19] = +58607.6406
  x[ 20] = +45114.3075
  x[ 21] = +50872.8059
  x[ 22] = +51690.8209
  x[ 23] = +48707.2667
```

## Iteration Trace

**Iter 0** | λ=1.000e-02 | RMSE=0.0857 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.25, L1_rough=214238.4035
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
