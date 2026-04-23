# IHCP Inversion Report

**Date:** 2026-04-14 20:52  
**Status:** `fail`  
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
- Lambda: `3.9062e+05`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `warning`
- Residual norm: `37.507667`
- Regularisation norm: `0.000000`
- Objective value: `1406.825111`

### Estimated Parameters

```
  x[  0] = +32241.5153
  x[  1] = +32241.5153
  x[  2] = +32241.5153
  x[  3] = +32241.5153
  x[  4] = +32241.5153
  x[  5] = +32241.5153
  x[  6] = +32241.5153
  x[  7] = +32241.5153
  x[  8] = +32241.5153
  x[  9] = +32241.5153
  x[ 10] = +32241.5153
  x[ 11] = +32241.5153
  x[ 12] = +32241.5153
  x[ 13] = +32241.5153
  x[ 14] = +32241.5153
  x[ 15] = +32241.5153
  x[ 16] = +32241.5153
  x[ 17] = +32241.5153
  x[ 18] = +32241.5153
  x[ 19] = +32241.5153
  x[ 20] = +32241.5153
  x[ 21] = +32241.5153
  x[ 22] = +32241.5153
  x[ 23] = +32241.5153
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=2.4111 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=37.5075 is above target=15.5563 (rel_dev=1.41)
  - Fit failed: rmse=2.4111 > threshold 2.0

**Iter 1** | λ=5.000e+00 | RMSE=2.4111 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=37.5076 is above target=15.5563 (rel_dev=1.41)
  - Fit failed: rmse=2.4111 > threshold 2.0

**Iter 2** | λ=2.500e+01 | RMSE=2.4111 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=37.5077 is above target=15.5563 (rel_dev=1.41)
  - Fit failed: rmse=2.4111 > threshold 2.0

**Iter 3** | λ=1.250e+02 | RMSE=2.4111 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=37.5077 is above target=15.5563 (rel_dev=1.41)
  - Fit failed: rmse=2.4111 > threshold 2.0

**Iter 4** | λ=6.250e+02 | RMSE=2.4111 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=37.5077 is above target=15.5563 (rel_dev=1.41)
  - Fit failed: rmse=2.4111 > threshold 2.0

**Iter 5** | λ=3.125e+03 | RMSE=2.4111 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=37.5077 is above target=15.5563 (rel_dev=1.41)
  - Fit failed: rmse=2.4111 > threshold 2.0

**Iter 6** | λ=1.562e+04 | RMSE=2.4111 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=37.5077 is above target=15.5563 (rel_dev=1.41)
  - Fit failed: rmse=2.4111 > threshold 2.0

**Iter 7** | λ=7.812e+04 | RMSE=2.4111 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=37.5077 is above target=15.5563 (rel_dev=1.41)
  - Fit failed: rmse=2.4111 > threshold 2.0

**Iter 8** | λ=3.906e+05 | RMSE=2.4111 | over_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=37.5077 is above target=15.5563 (rel_dev=1.41)
  - Over-regularisation suspected: solution is flat but rmse=2.4111
  - Fit failed: rmse=2.4111 > threshold 2.0

## Warnings

- Ill-conditioned system: cond ≈ 3.16e+12

## Notes

- Completed in 9 iteration(s)
