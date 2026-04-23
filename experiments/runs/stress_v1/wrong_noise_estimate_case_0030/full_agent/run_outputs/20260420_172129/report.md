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
- Residual norm: `7.392354`
- Regularisation norm: `40527.218761`
- Objective value: `55.891671`

### Estimated Parameters

```
  x[  0] = +2559.3250
  x[  1] = -1888.2689
  x[  2] = +2431.1066
  x[  3] = +2541.2876
  x[  4] = +1160.0662
  x[  5] = -8844.1471
  x[  6] = +11142.2479
  x[  7] = +33994.5596
  x[  8] = +48181.7301
  x[  9] = +50256.3924
  x[ 10] = +44923.3910
  x[ 11] = +50532.9388
  x[ 12] = +53971.7250
  x[ 13] = +55907.7551
  x[ 14] = +49612.2311
  x[ 15] = +45914.3736
  x[ 16] = +48025.6172
  x[ 17] = +53063.5582
  x[ 18] = +47480.9263
  x[ 19] = +51901.2720
  x[ 20] = +53610.9333
  x[ 21] = +45119.1807
  x[ 22] = +45412.6597
  x[ 23] = +54915.1578
```

## Iteration Trace

**Iter 0** | λ=7.579e-10 | RMSE=0.4752 | under_regularized | → stop_success_weak_pass
  - Discrepancy principle: ||r||=7.3924 is above target=0.7778 (rel_dev=8.50)
  - Under-regularisation suspected: osc=0.05, L1_rough=142823.4246
  - Fit marginal: rmse=0.4752, rel_err=0.0243

## Notes

- Completed in 1 iteration(s)
