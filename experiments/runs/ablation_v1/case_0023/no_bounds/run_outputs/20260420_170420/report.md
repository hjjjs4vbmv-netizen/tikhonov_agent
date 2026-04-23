# IHCP Inversion Report

**Date:** 2026-04-20 17:04  
**Status:** `weak_pass`  
**Iterations:** 5  

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
- Lambda: `3.3337e-08`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `14.107444`
- Regularisation norm: `19591.684029`
- Objective value: `211.816025`

### Estimated Parameters

```
  x[  0] = +4047.8124
  x[  1] = +7912.3969
  x[  2] = +14381.0196
  x[  3] = +23237.2729
  x[  4] = +32270.8994
  x[  5] = +38587.7663
  x[  6] = +41110.1411
  x[  7] = +40958.7300
  x[  8] = +39279.0885
  x[  9] = +38019.6599
  x[ 10] = +38799.2853
  x[ 11] = +40333.7523
  x[ 12] = +40523.7134
  x[ 13] = +39298.8660
  x[ 14] = +38617.8112
  x[ 15] = +38129.0249
  x[ 16] = +38546.0067
  x[ 17] = +38191.1120
  x[ 18] = +35899.7170
  x[ 19] = +32045.3463
  x[ 20] = +25525.3219
  x[ 21] = +19642.6180
  x[ 22] = +16177.0662
  x[ 23] = +14917.7229
```

## Iteration Trace

**Iter 0** | λ=5.334e-07 | RMSE=0.9981 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=31180.0288
  - Fit marginal: rmse=0.9981, rel_err=0.0545

**Iter 1** | λ=2.667e-07 | RMSE=0.9643 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=39922.8229
  - Fit marginal: rmse=0.9643, rel_err=0.0527

**Iter 2** | λ=1.333e-07 | RMSE=0.9397 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=47603.1736
  - Fit marginal: rmse=0.9397, rel_err=0.0513

**Iter 3** | λ=6.667e-08 | RMSE=0.9209 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=56017.6279
  - Fit marginal: rmse=0.9209, rel_err=0.0503

**Iter 4** | λ=3.334e-08 | RMSE=0.9069 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=69096.8175
  - Fit marginal: rmse=0.9069, rel_err=0.0495

## Notes

- Completed in 5 iteration(s)
