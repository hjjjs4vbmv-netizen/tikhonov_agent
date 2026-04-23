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
- Residual norm: `6.819976`
- Regularisation norm: `35433.511258`
- Objective value: `47.463606`

### Estimated Parameters

```
  x[  0] = +5296.8126
  x[  1] = +19000.3929
  x[  2] = +18457.8391
  x[  3] = +25310.7684
  x[  4] = +36347.1743
  x[  5] = +42168.7234
  x[  6] = +45280.7340
  x[  7] = +55804.9992
  x[  8] = +60253.8432
  x[  9] = +56067.0478
  x[ 10] = +56821.4286
  x[ 11] = +57940.4594
  x[ 12] = +51083.5522
  x[ 13] = +39037.8576
  x[ 14] = +39597.1543
  x[ 15] = +27878.9532
  x[ 16] = +22532.1716
  x[ 17] = +13784.9207
  x[ 18] = +4078.8741
  x[ 19] = +12874.1050
  x[ 20] = +3791.6412
  x[ 21] = +2057.6324
  x[ 22] = +4753.2155
  x[ 23] = +2296.9230
```

## Iteration Trace

**Iter 0** | λ=7.579e-10 | RMSE=0.4384 | under_regularized | → stop_success_weak_pass
  - Discrepancy principle: ||r||=6.8200 is above target=0.7778 (rel_dev=7.77)
  - Under-regularisation suspected: osc=0.06, L1_rough=141846.1027
  - Fit marginal: rmse=0.4384, rel_err=0.0277

## Notes

- Completed in 1 iteration(s)
