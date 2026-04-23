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
- Noise std: 0.1

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `3.9062e+05`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `warning`
- Residual norm: `34.965062`
- Regularisation norm: `0.000000`
- Objective value: `1222.555531`

### Estimated Parameters

```
  x[  0] = +32053.4090
  x[  1] = +32053.4090
  x[  2] = +32053.4090
  x[  3] = +32053.4090
  x[  4] = +32053.4090
  x[  5] = +32053.4090
  x[  6] = +32053.4090
  x[  7] = +32053.4090
  x[  8] = +32053.4090
  x[  9] = +32053.4090
  x[ 10] = +32053.4090
  x[ 11] = +32053.4090
  x[ 12] = +32053.4090
  x[ 13] = +32053.4090
  x[ 14] = +32053.4090
  x[ 15] = +32053.4090
  x[ 16] = +32053.4090
  x[ 17] = +32053.4090
  x[ 18] = +32053.4090
  x[ 19] = +32053.4090
  x[ 20] = +32053.4090
  x[ 21] = +32053.4090
  x[ 22] = +32053.4090
  x[ 23] = +32053.4090
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=2.2476 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=34.9648 is above target=1.5556 (rel_dev=21.48)
  - Fit failed: rmse=2.2476 > threshold 2.0

**Iter 1** | λ=5.000e+00 | RMSE=2.2476 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=34.9650 is above target=1.5556 (rel_dev=21.48)
  - Fit failed: rmse=2.2476 > threshold 2.0

**Iter 2** | λ=2.500e+01 | RMSE=2.2476 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=34.9650 is above target=1.5556 (rel_dev=21.48)
  - Fit failed: rmse=2.2476 > threshold 2.0

**Iter 3** | λ=1.250e+02 | RMSE=2.2476 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=34.9651 is above target=1.5556 (rel_dev=21.48)
  - Fit failed: rmse=2.2476 > threshold 2.0

**Iter 4** | λ=6.250e+02 | RMSE=2.2476 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=34.9651 is above target=1.5556 (rel_dev=21.48)
  - Fit failed: rmse=2.2476 > threshold 2.0

**Iter 5** | λ=3.125e+03 | RMSE=2.2476 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=34.9651 is above target=1.5556 (rel_dev=21.48)
  - Fit failed: rmse=2.2476 > threshold 2.0

**Iter 6** | λ=1.562e+04 | RMSE=2.2476 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=34.9651 is above target=1.5556 (rel_dev=21.48)
  - Fit failed: rmse=2.2476 > threshold 2.0

**Iter 7** | λ=7.812e+04 | RMSE=2.2476 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=34.9651 is above target=1.5556 (rel_dev=21.48)
  - Fit failed: rmse=2.2476 > threshold 2.0

**Iter 8** | λ=3.906e+05 | RMSE=2.2476 | over_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=34.9651 is above target=1.5556 (rel_dev=21.48)
  - Over-regularisation suspected: solution is flat but rmse=2.2476
  - Fit failed: rmse=2.2476 > threshold 2.0

## Warnings

- Ill-conditioned system: cond ≈ 3.16e+12

## Notes

- Completed in 9 iteration(s)
