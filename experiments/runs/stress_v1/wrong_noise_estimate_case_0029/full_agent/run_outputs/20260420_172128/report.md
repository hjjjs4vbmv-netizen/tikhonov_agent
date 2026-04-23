# IHCP Inversion Report

**Date:** 2026-04-20 17:21  
**Status:** `weak_pass`  
**Iterations:** 1  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 0.05

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `7.5787e-10`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `6.855849`
- Regularisation norm: `42618.803583`
- Objective value: `48.379228`

### Estimated Parameters

```
  x[  0] = -4879.4376
  x[  1] = +5454.4042
  x[  2] = -706.9932
  x[  3] = -700.8996
  x[  4] = +1716.0505
  x[  5] = -916.2720
  x[  6] = +4572.6218
  x[  7] = +35093.7935
  x[  8] = +52449.8023
  x[  9] = +48047.1138
  x[ 10] = +47875.5022
  x[ 11] = +51761.6376
  x[ 12] = +50356.7689
  x[ 13] = +45162.1547
  x[ 14] = +53202.3468
  x[ 15] = +48966.9357
  x[ 16] = +50549.2595
  x[ 17] = +47786.3480
  x[ 18] = +42932.2334
  x[ 19] = +55438.7646
  x[ 20] = +49052.4787
  x[ 21] = +49192.7278
  x[ 22] = +53072.7809
  x[ 23] = +51095.1443
```

## Iteration Trace

**Iter 0** | λ=7.579e-10 | RMSE=0.4407 | under_regularized | → stop_success_weak_pass
  - Discrepancy principle: ||r||=6.8558 is above target=0.7778 (rel_dev=7.81)
  - Under-regularisation suspected: osc=0.07, L1_rough=136342.3072
  - Fit marginal: rmse=0.4407, rel_err=0.0223

## Notes

- Completed in 1 iteration(s)
