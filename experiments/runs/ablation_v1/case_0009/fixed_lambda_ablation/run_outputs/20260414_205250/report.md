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
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `3.9062e+05`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `warning`
- Residual norm: `35.117694`
- Regularisation norm: `0.000000`
- Objective value: `1233.252412`

### Estimated Parameters

```
  x[  0] = +31901.1032
  x[  1] = +31901.1032
  x[  2] = +31901.1032
  x[  3] = +31901.1032
  x[  4] = +31901.1032
  x[  5] = +31901.1032
  x[  6] = +31901.1032
  x[  7] = +31901.1032
  x[  8] = +31901.1032
  x[  9] = +31901.1032
  x[ 10] = +31901.1032
  x[ 11] = +31901.1032
  x[ 12] = +31901.1032
  x[ 13] = +31901.1032
  x[ 14] = +31901.1032
  x[ 15] = +31901.1032
  x[ 16] = +31901.1032
  x[ 17] = +31901.1032
  x[ 18] = +31901.1032
  x[ 19] = +31901.1032
  x[ 20] = +31901.1032
  x[ 21] = +31901.1032
  x[ 22] = +31901.1032
  x[ 23] = +31901.1032
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=2.2574 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.1175 is above target=7.7782 (rel_dev=3.51)
  - Fit failed: rmse=2.2574 > threshold 2.0

**Iter 1** | λ=5.000e+00 | RMSE=2.2574 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.1176 is above target=7.7782 (rel_dev=3.51)
  - Fit failed: rmse=2.2574 > threshold 2.0

**Iter 2** | λ=2.500e+01 | RMSE=2.2574 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.1177 is above target=7.7782 (rel_dev=3.51)
  - Fit failed: rmse=2.2574 > threshold 2.0

**Iter 3** | λ=1.250e+02 | RMSE=2.2575 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.1177 is above target=7.7782 (rel_dev=3.51)
  - Fit failed: rmse=2.2575 > threshold 2.0

**Iter 4** | λ=6.250e+02 | RMSE=2.2575 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.1177 is above target=7.7782 (rel_dev=3.51)
  - Fit failed: rmse=2.2575 > threshold 2.0

**Iter 5** | λ=3.125e+03 | RMSE=2.2575 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.1177 is above target=7.7782 (rel_dev=3.51)
  - Fit failed: rmse=2.2575 > threshold 2.0

**Iter 6** | λ=1.562e+04 | RMSE=2.2575 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.1177 is above target=7.7782 (rel_dev=3.51)
  - Fit failed: rmse=2.2575 > threshold 2.0

**Iter 7** | λ=7.812e+04 | RMSE=2.2575 | well_regularized | → increase_lambda
  - Discrepancy principle: ||r||=35.1177 is above target=7.7782 (rel_dev=3.51)
  - Fit failed: rmse=2.2575 > threshold 2.0

**Iter 8** | λ=3.906e+05 | RMSE=2.2575 | over_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=35.1177 is above target=7.7782 (rel_dev=3.51)
  - Over-regularisation suspected: solution is flat but rmse=2.2575
  - Fit failed: rmse=2.2575 > threshold 2.0

## Warnings

- Ill-conditioned system: cond ≈ 3.16e+12

## Notes

- Completed in 9 iteration(s)
