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
- Regularisation order: 2
- Lambda: `7.5787e-02`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `13.849851`
- Regularisation norm: `0.059544`
- Objective value: `191.818637`

### Estimated Parameters

```
  x[  0] = +2069.7326
  x[  1] = +5281.9986
  x[  2] = +8494.2645
  x[  3] = +11706.5311
  x[  4] = +14918.7994
  x[  5] = +18131.0712
  x[  6] = +21343.3489
  x[  7] = +24555.6355
  x[  8] = +27767.9338
  x[  9] = +30980.2468
  x[ 10] = +34192.5773
  x[ 11] = +37404.9270
  x[ 12] = +40617.2967
  x[ 13] = +43829.6868
  x[ 14] = +47042.0969
  x[ 15] = +50254.5255
  x[ 16] = +53466.9712
  x[ 17] = +56679.4319
  x[ 18] = +59891.9053
  x[ 19] = +63104.3885
  x[ 20] = +66316.8780
  x[ 21] = +69529.3711
  x[ 22] = +72741.8657
  x[ 23] = +75954.3607
```

## Iteration Trace

**Iter 0** | λ=7.579e-02 | RMSE=0.8903 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=73884.6281
  - Fit marginal: rmse=0.8903, rel_err=0.0364

## Notes

- Completed in 1 iteration(s)
