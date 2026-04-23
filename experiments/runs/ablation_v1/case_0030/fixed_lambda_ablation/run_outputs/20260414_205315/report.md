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
- Residual norm: `20.189456`
- Regularisation norm: `4.048829`
- Objective value: `407.678161`

### Estimated Parameters

```
  x[  0] = +42123.6980
  x[  1] = +42123.4642
  x[  2] = +42122.9354
  x[  3] = +42122.1129
  x[  4] = +42121.0348
  x[  5] = +42119.7690
  x[  6] = +42118.4190
  x[  7] = +42117.0640
  x[  8] = +42115.7938
  x[  9] = +42114.6716
  x[ 10] = +42113.7182
  x[ 11] = +42112.9198
  x[ 12] = +42112.2155
  x[ 13] = +42111.5382
  x[ 14] = +42110.8339
  x[ 15] = +42110.0879
  x[ 16] = +42109.3115
  x[ 17] = +42108.5333
  x[ 18] = +42107.7947
  x[ 19] = +42107.1590
  x[ 20] = +42106.6670
  x[ 21] = +42106.3409
  x[ 22] = +42106.1834
  x[ 23] = +42106.1463
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.2980 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=20.1926 is above target=15.5563 (rel_dev=0.30)
  - Fit marginal: rmse=1.2980, rel_err=0.0639

**Iter 1** | λ=5.000e-01 | RMSE=1.2980 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=20.1926 is above target=15.5563 (rel_dev=0.30)
  - Fit marginal: rmse=1.2980, rel_err=0.0639

**Iter 2** | λ=2.500e-01 | RMSE=1.2980 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=20.1926 is above target=15.5563 (rel_dev=0.30)
  - Fit marginal: rmse=1.2980, rel_err=0.0639

**Iter 3** | λ=1.250e-01 | RMSE=1.2980 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=20.1925 is above target=15.5563 (rel_dev=0.30)
  - Fit marginal: rmse=1.2980, rel_err=0.0639

**Iter 4** | λ=6.250e-02 | RMSE=1.2980 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=20.1924 is above target=15.5563 (rel_dev=0.30)
  - Fit marginal: rmse=1.2980, rel_err=0.0639

**Iter 5** | λ=3.125e-02 | RMSE=1.2980 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=20.1922 is above target=15.5563 (rel_dev=0.30)
  - Fit marginal: rmse=1.2980, rel_err=0.0639

**Iter 6** | λ=1.562e-02 | RMSE=1.2980 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=20.1918 is above target=15.5563 (rel_dev=0.30)
  - Under-regularisation suspected: osc=0.00, L1_rough=4.3927
  - Fit marginal: rmse=1.2980, rel_err=0.0639

**Iter 7** | λ=7.812e-03 | RMSE=1.2979 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=20.1910 is above target=15.5563 (rel_dev=0.30)
  - Under-regularisation suspected: osc=0.00, L1_rough=8.7822
  - Fit marginal: rmse=1.2979, rel_err=0.0639

**Iter 8** | λ=3.906e-03 | RMSE=1.2978 | under_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=20.1895 is above target=15.5563 (rel_dev=0.30)
  - Under-regularisation suspected: osc=0.00, L1_rough=17.5517
  - Fit marginal: rmse=1.2978, rel_err=0.0639

## Notes

- Completed in 9 iteration(s)
