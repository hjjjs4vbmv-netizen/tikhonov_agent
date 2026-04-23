# IHCP Inversion Report

**Date:** 2026-04-20 17:03  
**Status:** `fail`  
**Iterations:** 9  

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
- Lambda: `3.9062e+05`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `warning`
- Residual norm: `35.740074`
- Regularisation norm: `0.000000`
- Objective value: `1277.352909`

### Estimated Parameters

```
  x[  0] = +30548.0106
  x[  1] = +30548.0106
  x[  2] = +30548.0106
  x[  3] = +30548.0106
  x[  4] = +30548.0106
  x[  5] = +30548.0106
  x[  6] = +30548.0106
  x[  7] = +30548.0106
  x[  8] = +30548.0106
  x[  9] = +30548.0106
  x[ 10] = +30548.0106
  x[ 11] = +30548.0106
  x[ 12] = +30548.0106
  x[ 13] = +30548.0106
  x[ 14] = +30548.0106
  x[ 15] = +30548.0106
  x[ 16] = +30548.0106
  x[ 17] = +30548.0106
  x[ 18] = +30548.0106
  x[ 19] = +30548.0106
  x[ 20] = +30548.0106
  x[ 21] = +30548.0106
  x[ 22] = +30548.0106
  x[ 23] = +30548.0106
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=2.2974 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.7399 is above target=7.7782 (rel_dev=3.59)
  - Fit failed: rmse=2.2974 > threshold 2.0

**Iter 1** | λ=5.000e+00 | RMSE=2.2975 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.7400 is above target=7.7782 (rel_dev=3.59)
  - Fit failed: rmse=2.2975 > threshold 2.0

**Iter 2** | λ=2.500e+01 | RMSE=2.2975 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.7401 is above target=7.7782 (rel_dev=3.59)
  - Fit failed: rmse=2.2975 > threshold 2.0

**Iter 3** | λ=1.250e+02 | RMSE=2.2975 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.7401 is above target=7.7782 (rel_dev=3.59)
  - Fit failed: rmse=2.2975 > threshold 2.0

**Iter 4** | λ=6.250e+02 | RMSE=2.2975 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.7401 is above target=7.7782 (rel_dev=3.59)
  - Fit failed: rmse=2.2975 > threshold 2.0

**Iter 5** | λ=3.125e+03 | RMSE=2.2975 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.7401 is above target=7.7782 (rel_dev=3.59)
  - Fit failed: rmse=2.2975 > threshold 2.0

**Iter 6** | λ=1.562e+04 | RMSE=2.2975 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.7401 is above target=7.7782 (rel_dev=3.59)
  - Fit failed: rmse=2.2975 > threshold 2.0

**Iter 7** | λ=7.812e+04 | RMSE=2.2975 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.7401 is above target=7.7782 (rel_dev=3.59)
  - Fit failed: rmse=2.2975 > threshold 2.0

**Iter 8** | λ=3.906e+05 | RMSE=2.2975 | over_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=35.7401 is above target=7.7782 (rel_dev=3.59)
  - Over-regularisation suspected: solution is flat but rmse=2.2975
  - Fit failed: rmse=2.2975 > threshold 2.0

## Warnings

- Ill-conditioned system: cond ≈ 3.16e+12

## Notes

- Completed in 9 iteration(s)
