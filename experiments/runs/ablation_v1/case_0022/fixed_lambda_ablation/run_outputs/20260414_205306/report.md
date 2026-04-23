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
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `3.9062e-03`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `16.608949`
- Regularisation norm: `5.649088`
- Objective value: `275.981832`

### Estimated Parameters

```
  x[  0] = +32844.5293
  x[  1] = +32844.9061
  x[  2] = +32845.7457
  x[  3] = +32846.9903
  x[  4] = +32848.5502
  x[  5] = +32850.3188
  x[  6] = +32852.2019
  x[  7] = +32854.1128
  x[  8] = +32855.9995
  x[  9] = +32857.8219
  x[ 10] = +32859.5343
  x[ 11] = +32861.0877
  x[ 12] = +32862.4310
  x[ 13] = +32863.5369
  x[ 14] = +32864.4050
  x[ 15] = +32865.0557
  x[ 16] = +32865.5065
  x[ 17] = +32865.7659
  x[ 18] = +32865.8468
  x[ 19] = +32865.7916
  x[ 20] = +32865.6589
  x[ 21] = +32865.5174
  x[ 22] = +32865.4261
  x[ 23] = +32865.3986
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.0681 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=16.6164 is above target=7.7782 (rel_dev=1.14)
  - Fit marginal: rmse=1.0681, rel_err=0.0645

**Iter 1** | λ=5.000e-01 | RMSE=1.0681 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=16.6164 is above target=7.7782 (rel_dev=1.14)
  - Fit marginal: rmse=1.0681, rel_err=0.0645

**Iter 2** | λ=2.500e-01 | RMSE=1.0681 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=16.6163 is above target=7.7782 (rel_dev=1.14)
  - Fit marginal: rmse=1.0681, rel_err=0.0645

**Iter 3** | λ=1.250e-01 | RMSE=1.0681 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=16.6162 is above target=7.7782 (rel_dev=1.14)
  - Fit marginal: rmse=1.0681, rel_err=0.0645

**Iter 4** | λ=6.250e-02 | RMSE=1.0681 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=16.6160 is above target=7.7782 (rel_dev=1.14)
  - Fit marginal: rmse=1.0681, rel_err=0.0645

**Iter 5** | λ=3.125e-02 | RMSE=1.0681 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=16.6155 is above target=7.7782 (rel_dev=1.14)
  - Fit marginal: rmse=1.0681, rel_err=0.0645

**Iter 6** | λ=1.562e-02 | RMSE=1.0680 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=16.6146 is above target=7.7782 (rel_dev=1.14)
  - Under-regularisation suspected: osc=0.05, L1_rough=5.4472
  - Fit marginal: rmse=1.0680, rel_err=0.0645

**Iter 7** | λ=7.812e-03 | RMSE=1.0679 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=16.6127 is above target=7.7782 (rel_dev=1.14)
  - Under-regularisation suspected: osc=0.05, L1_rough=10.8905
  - Fit marginal: rmse=1.0679, rel_err=0.0645

**Iter 8** | λ=3.906e-03 | RMSE=1.0677 | under_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=16.6089 is above target=7.7782 (rel_dev=1.14)
  - Under-regularisation suspected: osc=0.05, L1_rough=21.7657
  - Fit marginal: rmse=1.0677, rel_err=0.0644

## Notes

- Completed in 9 iteration(s)
