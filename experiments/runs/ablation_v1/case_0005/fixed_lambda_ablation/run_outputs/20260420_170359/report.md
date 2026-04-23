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
- Noise std: 1.0

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `3.9062e+05`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `warning`
- Residual norm: `36.997628`
- Regularisation norm: `0.000000`
- Objective value: `1368.824507`

### Estimated Parameters

```
  x[  0] = +30357.6282
  x[  1] = +30357.6282
  x[  2] = +30357.6282
  x[  3] = +30357.6282
  x[  4] = +30357.6282
  x[  5] = +30357.6282
  x[  6] = +30357.6282
  x[  7] = +30357.6282
  x[  8] = +30357.6282
  x[  9] = +30357.6282
  x[ 10] = +30357.6282
  x[ 11] = +30357.6282
  x[ 12] = +30357.6282
  x[ 13] = +30357.6282
  x[ 14] = +30357.6282
  x[ 15] = +30357.6282
  x[ 16] = +30357.6282
  x[ 17] = +30357.6282
  x[ 18] = +30357.6282
  x[ 19] = +30357.6282
  x[ 20] = +30357.6282
  x[ 21] = +30357.6282
  x[ 22] = +30357.6282
  x[ 23] = +30357.6282
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=2.3783 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=36.9974 is above target=15.5563 (rel_dev=1.38)
  - Fit failed: rmse=2.3783 > threshold 2.0

**Iter 1** | λ=5.000e+00 | RMSE=2.3783 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=36.9976 is above target=15.5563 (rel_dev=1.38)
  - Fit failed: rmse=2.3783 > threshold 2.0

**Iter 2** | λ=2.500e+01 | RMSE=2.3783 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=36.9976 is above target=15.5563 (rel_dev=1.38)
  - Fit failed: rmse=2.3783 > threshold 2.0

**Iter 3** | λ=1.250e+02 | RMSE=2.3783 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=36.9976 is above target=15.5563 (rel_dev=1.38)
  - Fit failed: rmse=2.3783 > threshold 2.0

**Iter 4** | λ=6.250e+02 | RMSE=2.3783 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=36.9976 is above target=15.5563 (rel_dev=1.38)
  - Fit failed: rmse=2.3783 > threshold 2.0

**Iter 5** | λ=3.125e+03 | RMSE=2.3783 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=36.9976 is above target=15.5563 (rel_dev=1.38)
  - Fit failed: rmse=2.3783 > threshold 2.0

**Iter 6** | λ=1.562e+04 | RMSE=2.3783 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=36.9976 is above target=15.5563 (rel_dev=1.38)
  - Fit failed: rmse=2.3783 > threshold 2.0

**Iter 7** | λ=7.812e+04 | RMSE=2.3783 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=36.9976 is above target=15.5563 (rel_dev=1.38)
  - Fit failed: rmse=2.3783 > threshold 2.0

**Iter 8** | λ=3.906e+05 | RMSE=2.3783 | over_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=36.9976 is above target=15.5563 (rel_dev=1.38)
  - Over-regularisation suspected: solution is flat but rmse=2.3783
  - Fit failed: rmse=2.3783 > threshold 2.0

## Warnings

- Ill-conditioned system: cond ≈ 3.16e+12

## Notes

- Completed in 9 iteration(s)
