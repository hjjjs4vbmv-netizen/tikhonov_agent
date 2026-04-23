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
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `3.9062e-03`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `23.205919`
- Regularisation norm: `7.273215`
- Objective value: `538.721330`

### Estimated Parameters

```
  x[  0] = +35276.2029
  x[  1] = +35276.3127
  x[  2] = +35276.5328
  x[  3] = +35276.8147
  x[  4] = +35277.0794
  x[  5] = +35277.2308
  x[  6] = +35277.1733
  x[  7] = +35276.8211
  x[  8] = +35276.1010
  x[  9] = +35274.9705
  x[ 10] = +35273.4251
  x[ 11] = +35271.4899
  x[ 12] = +35269.2221
  x[ 13] = +35266.7132
  x[ 14] = +35264.0798
  x[ 15] = +35261.4412
  x[ 16] = +35258.9279
  x[ 17] = +35256.6564
  x[ 18] = +35254.7257
  x[ 19] = +35253.2055
  x[ 20] = +35252.1135
  x[ 21] = +35251.4383
  x[ 22] = +35251.1157
  x[ 23] = +35251.0288
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.4923 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=23.2148 is above target=7.7782 (rel_dev=1.98)
  - Fit marginal: rmse=1.4923, rel_err=0.0942

**Iter 1** | λ=5.000e-01 | RMSE=1.4923 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=23.2148 is above target=7.7782 (rel_dev=1.98)
  - Fit marginal: rmse=1.4923, rel_err=0.0942

**Iter 2** | λ=2.500e-01 | RMSE=1.4923 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=23.2147 is above target=7.7782 (rel_dev=1.98)
  - Fit marginal: rmse=1.4923, rel_err=0.0942

**Iter 3** | λ=1.250e-01 | RMSE=1.4923 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=23.2145 is above target=7.7782 (rel_dev=1.98)
  - Fit marginal: rmse=1.4923, rel_err=0.0942

**Iter 4** | λ=6.250e-02 | RMSE=1.4923 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=23.2143 is above target=7.7782 (rel_dev=1.98)
  - Fit marginal: rmse=1.4923, rel_err=0.0942

**Iter 5** | λ=3.125e-02 | RMSE=1.4922 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=23.2137 is above target=7.7782 (rel_dev=1.98)
  - Under-regularisation suspected: osc=0.00, L1_rough=3.4070
  - Fit marginal: rmse=1.4922, rel_err=0.0942

**Iter 6** | λ=1.562e-02 | RMSE=1.4922 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=23.2126 is above target=7.7782 (rel_dev=1.98)
  - Under-regularisation suspected: osc=0.00, L1_rough=6.8130
  - Fit marginal: rmse=1.4922, rel_err=0.0942

**Iter 7** | λ=7.812e-03 | RMSE=1.4920 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=23.2104 is above target=7.7782 (rel_dev=1.98)
  - Under-regularisation suspected: osc=0.00, L1_rough=13.6224
  - Fit marginal: rmse=1.4920, rel_err=0.0942

**Iter 8** | λ=3.906e-03 | RMSE=1.4917 | under_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=23.2059 is above target=7.7782 (rel_dev=1.98)
  - Under-regularisation suspected: osc=0.00, L1_rough=27.2299
  - Fit marginal: rmse=1.4917, rel_err=0.0942

## Notes

- Completed in 9 iteration(s)
