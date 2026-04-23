# IHCP Inversion Report

**Date:** 2026-04-20 17:04  
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
- Residual norm: `38.095120`
- Regularisation norm: `0.000000`
- Objective value: `1451.238182`

### Estimated Parameters

```
  x[  0] = +30888.4226
  x[  1] = +30888.4226
  x[  2] = +30888.4226
  x[  3] = +30888.4226
  x[  4] = +30888.4226
  x[  5] = +30888.4226
  x[  6] = +30888.4226
  x[  7] = +30888.4226
  x[  8] = +30888.4226
  x[  9] = +30888.4226
  x[ 10] = +30888.4226
  x[ 11] = +30888.4226
  x[ 12] = +30888.4226
  x[ 13] = +30888.4226
  x[ 14] = +30888.4226
  x[ 15] = +30888.4226
  x[ 16] = +30888.4226
  x[ 17] = +30888.4226
  x[ 18] = +30888.4226
  x[ 19] = +30888.4226
  x[ 20] = +30888.4226
  x[ 21] = +30888.4226
  x[ 22] = +30888.4226
  x[ 23] = +30888.4226
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=2.4488 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=38.0949 is above target=15.5563 (rel_dev=1.45)
  - Fit failed: rmse=2.4488 > threshold 2.0

**Iter 1** | λ=5.000e+00 | RMSE=2.4488 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=38.0951 is above target=15.5563 (rel_dev=1.45)
  - Fit failed: rmse=2.4488 > threshold 2.0

**Iter 2** | λ=2.500e+01 | RMSE=2.4488 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=38.0951 is above target=15.5563 (rel_dev=1.45)
  - Fit failed: rmse=2.4488 > threshold 2.0

**Iter 3** | λ=1.250e+02 | RMSE=2.4488 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=38.0951 is above target=15.5563 (rel_dev=1.45)
  - Fit failed: rmse=2.4488 > threshold 2.0

**Iter 4** | λ=6.250e+02 | RMSE=2.4488 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=38.0951 is above target=15.5563 (rel_dev=1.45)
  - Fit failed: rmse=2.4488 > threshold 2.0

**Iter 5** | λ=3.125e+03 | RMSE=2.4488 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=38.0951 is above target=15.5563 (rel_dev=1.45)
  - Fit failed: rmse=2.4488 > threshold 2.0

**Iter 6** | λ=1.562e+04 | RMSE=2.4488 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=38.0951 is above target=15.5563 (rel_dev=1.45)
  - Fit failed: rmse=2.4488 > threshold 2.0

**Iter 7** | λ=7.812e+04 | RMSE=2.4488 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=38.0951 is above target=15.5563 (rel_dev=1.45)
  - Fit failed: rmse=2.4488 > threshold 2.0

**Iter 8** | λ=3.906e+05 | RMSE=2.4488 | over_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=38.0951 is above target=15.5563 (rel_dev=1.45)
  - Over-regularisation suspected: solution is flat but rmse=2.4488
  - Fit failed: rmse=2.4488 > threshold 2.0

## Warnings

- Ill-conditioned system: cond ≈ 3.16e+12

## Notes

- Completed in 9 iteration(s)
