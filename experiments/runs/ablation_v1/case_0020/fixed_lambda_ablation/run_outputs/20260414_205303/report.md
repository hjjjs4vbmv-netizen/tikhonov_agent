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
- Noise std: 0.1

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `3.9062e-03`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.114017`
- Regularisation norm: `5.819228`
- Objective value: `228.565776`

### Estimated Parameters

```
  x[  0] = +32784.1278
  x[  1] = +32784.5170
  x[  2] = +32785.3819
  x[  3] = +32786.6664
  x[  4] = +32788.2783
  x[  5] = +32790.1074
  x[  6] = +32792.0499
  x[  7] = +32794.0216
  x[  8] = +32795.9653
  x[  9] = +32797.8364
  x[ 10] = +32799.5887
  x[ 11] = +32801.1726
  x[ 12] = +32802.5451
  x[ 13] = +32803.6843
  x[ 14] = +32804.5920
  x[ 15] = +32805.2825
  x[ 16] = +32805.7682
  x[ 17] = +32806.0571
  x[ 18] = +32806.1649
  x[ 19] = +32806.1314
  x[ 20] = +32806.0174
  x[ 21] = +32805.8919
  x[ 22] = +32805.8082
  x[ 23] = +32805.7808
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=0.9721 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.1227 is above target=1.5556 (rel_dev=8.72)
  - Fit marginal: rmse=0.9721, rel_err=0.0640

**Iter 1** | λ=5.000e-01 | RMSE=0.9721 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.1227 is above target=1.5556 (rel_dev=8.72)
  - Fit marginal: rmse=0.9721, rel_err=0.0640

**Iter 2** | λ=2.500e-01 | RMSE=0.9721 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.1226 is above target=1.5556 (rel_dev=8.72)
  - Fit marginal: rmse=0.9721, rel_err=0.0640

**Iter 3** | λ=1.250e-01 | RMSE=0.9721 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.1225 is above target=1.5556 (rel_dev=8.72)
  - Fit marginal: rmse=0.9721, rel_err=0.0640

**Iter 4** | λ=6.250e-02 | RMSE=0.9721 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.1222 is above target=1.5556 (rel_dev=8.72)
  - Fit marginal: rmse=0.9721, rel_err=0.0640

**Iter 5** | λ=3.125e-02 | RMSE=0.9721 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.1217 is above target=1.5556 (rel_dev=8.72)
  - Fit marginal: rmse=0.9721, rel_err=0.0640

**Iter 6** | λ=1.562e-02 | RMSE=0.9720 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.1206 is above target=1.5556 (rel_dev=8.72)
  - Under-regularisation suspected: osc=0.05, L1_rough=5.6113
  - Fit marginal: rmse=0.9720, rel_err=0.0640

**Iter 7** | λ=7.812e-03 | RMSE=0.9718 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.1184 is above target=1.5556 (rel_dev=8.72)
  - Under-regularisation suspected: osc=0.05, L1_rough=11.2186
  - Fit marginal: rmse=0.9718, rel_err=0.0640

**Iter 8** | λ=3.906e-03 | RMSE=0.9716 | under_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=15.1140 is above target=1.5556 (rel_dev=8.72)
  - Under-regularisation suspected: osc=0.05, L1_rough=22.4212
  - Fit marginal: rmse=0.9716, rel_err=0.0640

## Notes

- Completed in 9 iteration(s)
