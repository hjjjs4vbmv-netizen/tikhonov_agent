# IHCP Inversion Report

**Date:** 2026-04-20 17:04  
**Status:** `weak_pass`  
**Iterations:** 9  

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
- Regularisation order: 1
- Lambda: `3.9062e-03`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `22.229313`
- Regularisation norm: `7.012862`
- Objective value: `494.334472`

### Estimated Parameters

```
  x[  0] = +35480.8857
  x[  1] = +35481.0060
  x[  2] = +35481.2592
  x[  3] = +35481.5927
  x[  4] = +35481.9280
  x[  5] = +35482.1705
  x[  6] = +35482.2226
  x[  7] = +35481.9905
  x[  8] = +35481.4005
  x[  9] = +35480.4056
  x[ 10] = +35478.9920
  x[ 11] = +35477.1819
  x[ 12] = +35475.0312
  x[ 13] = +35472.6268
  x[ 14] = +35470.0795
  x[ 15] = +35467.5150
  x[ 16] = +35465.0604
  x[ 17] = +35462.8324
  x[ 18] = +35460.9271
  x[ 19] = +35459.4134
  x[ 20] = +35458.3224
  x[ 21] = +35457.6425
  x[ 22] = +35457.3151
  x[ 23] = +35457.2276
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.4295 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=22.2379 is above target=1.5556 (rel_dev=13.30)
  - Fit marginal: rmse=1.4295, rel_err=0.0959

**Iter 1** | λ=5.000e-01 | RMSE=1.4295 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=22.2379 is above target=1.5556 (rel_dev=13.30)
  - Fit marginal: rmse=1.4295, rel_err=0.0959

**Iter 2** | λ=2.500e-01 | RMSE=1.4295 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=22.2378 is above target=1.5556 (rel_dev=13.30)
  - Fit marginal: rmse=1.4295, rel_err=0.0959

**Iter 3** | λ=1.250e-01 | RMSE=1.4295 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=22.2377 is above target=1.5556 (rel_dev=13.29)
  - Fit marginal: rmse=1.4295, rel_err=0.0959

**Iter 4** | λ=6.250e-02 | RMSE=1.4295 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=22.2374 is above target=1.5556 (rel_dev=13.29)
  - Fit marginal: rmse=1.4295, rel_err=0.0959

**Iter 5** | λ=3.125e-02 | RMSE=1.4294 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=22.2369 is above target=1.5556 (rel_dev=13.29)
  - Under-regularisation suspected: osc=0.00, L1_rough=3.2942
  - Fit marginal: rmse=1.4294, rel_err=0.0959

**Iter 6** | λ=1.562e-02 | RMSE=1.4294 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=22.2358 is above target=1.5556 (rel_dev=13.29)
  - Under-regularisation suspected: osc=0.00, L1_rough=6.5876
  - Fit marginal: rmse=1.4294, rel_err=0.0959

**Iter 7** | λ=7.812e-03 | RMSE=1.4292 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=22.2336 is above target=1.5556 (rel_dev=13.29)
  - Under-regularisation suspected: osc=0.00, L1_rough=13.1721
  - Fit marginal: rmse=1.4292, rel_err=0.0959

**Iter 8** | λ=3.906e-03 | RMSE=1.4290 | under_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=22.2293 is above target=1.5556 (rel_dev=13.29)
  - Under-regularisation suspected: osc=0.00, L1_rough=26.3321
  - Fit marginal: rmse=1.4290, rel_err=0.0959

## Notes

- Completed in 9 iteration(s)
