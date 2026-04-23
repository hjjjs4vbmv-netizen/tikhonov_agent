# IHCP Inversion Report

**Date:** 2026-04-14 20:53  
**Status:** `weak_pass`  
**Iterations:** 9  

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
- Regularisation order: 1
- Lambda: `3.9062e-03`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `20.926474`
- Regularisation norm: `5.437508`
- Objective value: `438.032803`

### Estimated Parameters

```
  x[  0] = +32920.0311
  x[  1] = +32920.3925
  x[  2] = +32921.2004
  x[  3] = +32922.3951
  x[  4] = +32923.8900
  x[  5] = +32925.5829
  x[  6] = +32927.3919
  x[  7] = +32929.2267
  x[  8] = +32931.0422
  x[  9] = +32932.8036
  x[ 10] = +32934.4662
  x[ 11] = +32935.9815
  x[ 12] = +32937.2884
  x[ 13] = +32938.3525
  x[ 14] = +32939.1711
  x[ 15] = +32939.7721
  x[ 16] = +32940.1793
  x[ 17] = +32940.4019
  x[ 18] = +32940.4490
  x[ 19] = +32940.3667
  x[ 20] = +32940.2105
  x[ 21] = +32940.0491
  x[ 22] = +32939.9485
  x[ 23] = +32939.9207
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.3456 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=20.9320 is above target=15.5563 (rel_dev=0.35)
  - Fit marginal: rmse=1.3456, rel_err=0.0729

**Iter 1** | λ=5.000e-01 | RMSE=1.3456 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=20.9320 is above target=15.5563 (rel_dev=0.35)
  - Fit marginal: rmse=1.3456, rel_err=0.0729

**Iter 2** | λ=2.500e-01 | RMSE=1.3456 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=20.9319 is above target=15.5563 (rel_dev=0.35)
  - Fit marginal: rmse=1.3456, rel_err=0.0729

**Iter 3** | λ=1.250e-01 | RMSE=1.3455 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=20.9318 is above target=15.5563 (rel_dev=0.35)
  - Fit marginal: rmse=1.3455, rel_err=0.0729

**Iter 4** | λ=6.250e-02 | RMSE=1.3455 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=20.9317 is above target=15.5563 (rel_dev=0.35)
  - Fit marginal: rmse=1.3455, rel_err=0.0729

**Iter 5** | λ=3.125e-02 | RMSE=1.3455 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=20.9313 is above target=15.5563 (rel_dev=0.35)
  - Fit marginal: rmse=1.3455, rel_err=0.0729

**Iter 6** | λ=1.562e-02 | RMSE=1.3455 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=20.9306 is above target=15.5563 (rel_dev=0.35)
  - Under-regularisation suspected: osc=0.05, L1_rough=5.2421
  - Fit marginal: rmse=1.3455, rel_err=0.0729

**Iter 7** | λ=7.812e-03 | RMSE=1.3454 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=20.9292 is above target=15.5563 (rel_dev=0.35)
  - Under-regularisation suspected: osc=0.05, L1_rough=10.4805
  - Fit marginal: rmse=1.3454, rel_err=0.0729

**Iter 8** | λ=3.906e-03 | RMSE=1.3452 | under_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=20.9265 is above target=15.5563 (rel_dev=0.35)
  - Under-regularisation suspected: osc=0.05, L1_rough=20.9463
  - Fit marginal: rmse=1.3452, rel_err=0.0729

## Notes

- Completed in 9 iteration(s)
