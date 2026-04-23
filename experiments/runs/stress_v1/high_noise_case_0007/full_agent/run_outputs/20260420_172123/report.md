# IHCP Inversion Report

**Date:** 2026-04-20 17:21  
**Status:** `fail`  
**Iterations:** 9  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 5.0

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `2.9604e+04`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `72.813125`
- Regularisation norm: `0.000001`
- Objective value: `5301.751229`

### Estimated Parameters

```
  x[  0] = +33557.1057
  x[  1] = +33557.1057
  x[  2] = +33557.1057
  x[  3] = +33557.1057
  x[  4] = +33557.1057
  x[  5] = +33557.1057
  x[  6] = +33557.1057
  x[  7] = +33557.1057
  x[  8] = +33557.1057
  x[  9] = +33557.1057
  x[ 10] = +33557.1057
  x[ 11] = +33557.1057
  x[ 12] = +33557.1057
  x[ 13] = +33557.1057
  x[ 14] = +33557.1057
  x[ 15] = +33557.1057
  x[ 16] = +33557.1057
  x[ 17] = +33557.1057
  x[ 18] = +33557.1057
  x[ 19] = +33557.1057
  x[ 20] = +33557.1057
  x[ 21] = +33557.1057
  x[ 22] = +33557.1057
  x[ 23] = +33557.1057
```

## Iteration Trace

**Iter 0** | λ=7.579e-02 | RMSE=4.6806 | well_regularized | → increase_lambda
  - Fit failed: rmse=4.6806 > threshold 2.0

**Iter 1** | λ=3.789e-01 | RMSE=4.6806 | well_regularized | → increase_lambda
  - Fit failed: rmse=4.6806 > threshold 2.0

**Iter 2** | λ=1.895e+00 | RMSE=4.6806 | well_regularized | → increase_lambda
  - Fit failed: rmse=4.6806 > threshold 2.0

**Iter 3** | λ=9.473e+00 | RMSE=4.6806 | well_regularized | → increase_lambda
  - Fit failed: rmse=4.6806 > threshold 2.0

**Iter 4** | λ=4.737e+01 | RMSE=4.6806 | well_regularized | → increase_lambda
  - Fit failed: rmse=4.6806 > threshold 2.0

**Iter 5** | λ=2.368e+02 | RMSE=4.6806 | well_regularized | → increase_lambda
  - Fit failed: rmse=4.6806 > threshold 2.0

**Iter 6** | λ=1.184e+03 | RMSE=4.6806 | well_regularized | → increase_lambda
  - Fit failed: rmse=4.6806 > threshold 2.0

**Iter 7** | λ=5.921e+03 | RMSE=4.6806 | well_regularized | → increase_lambda
  - Fit failed: rmse=4.6806 > threshold 2.0

**Iter 8** | λ=2.960e+04 | RMSE=4.6806 | well_regularized | → stop_with_failure
  - Fit failed: rmse=4.6806 > threshold 2.0

## Notes

- Completed in 9 iteration(s)
