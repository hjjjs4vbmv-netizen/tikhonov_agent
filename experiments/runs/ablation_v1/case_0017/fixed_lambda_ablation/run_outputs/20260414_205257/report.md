# IHCP Inversion Report

**Date:** 2026-04-14 20:52  
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
- Residual norm: `26.091238`
- Regularisation norm: `7.575081`
- Objective value: `680.976827`

### Estimated Parameters

```
  x[  0] = +35086.6204
  x[  1] = +35086.7167
  x[  2] = +35086.8973
  x[  3] = +35087.1177
  x[  4] = +35087.2988
  x[  5] = +35087.3439
  x[  6] = +35087.1619
  x[  7] = +35086.6744
  x[  8] = +35085.8100
  x[  9] = +35084.5318
  x[ 10] = +35082.8447
  x[ 11] = +35080.7767
  x[ 12] = +35078.3846
  x[ 13] = +35075.7627
  x[ 14] = +35073.0334
  x[ 15] = +35070.3108
  x[ 16] = +35067.7299
  x[ 17] = +35065.4076
  x[ 18] = +35063.4448
  x[ 19] = +35061.9127
  x[ 20] = +35060.8149
  x[ 21] = +35060.1404
  x[ 22] = +35059.8208
  x[ 23] = +35059.7345
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.6778 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=26.0998 is above target=15.5563 (rel_dev=0.68)
  - Fit marginal: rmse=1.6778, rel_err=0.0974

**Iter 1** | λ=5.000e-01 | RMSE=1.6778 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=26.0998 is above target=15.5563 (rel_dev=0.68)
  - Fit marginal: rmse=1.6778, rel_err=0.0974

**Iter 2** | λ=2.500e-01 | RMSE=1.6778 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=26.0997 is above target=15.5563 (rel_dev=0.68)
  - Fit marginal: rmse=1.6778, rel_err=0.0974

**Iter 3** | λ=1.250e-01 | RMSE=1.6777 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=26.0996 is above target=15.5563 (rel_dev=0.68)
  - Fit marginal: rmse=1.6777, rel_err=0.0974

**Iter 4** | λ=6.250e-02 | RMSE=1.6777 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=26.0993 is above target=15.5563 (rel_dev=0.68)
  - Fit marginal: rmse=1.6777, rel_err=0.0974

**Iter 5** | λ=3.125e-02 | RMSE=1.6777 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=26.0988 is above target=15.5563 (rel_dev=0.68)
  - Under-regularisation suspected: osc=0.05, L1_rough=3.5451
  - Fit marginal: rmse=1.6777, rel_err=0.0974

**Iter 6** | λ=1.562e-02 | RMSE=1.6776 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=26.0977 is above target=15.5563 (rel_dev=0.68)
  - Under-regularisation suspected: osc=0.05, L1_rough=7.0892
  - Fit marginal: rmse=1.6776, rel_err=0.0974

**Iter 7** | λ=7.812e-03 | RMSE=1.6775 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=26.0955 is above target=15.5563 (rel_dev=0.68)
  - Under-regularisation suspected: osc=0.05, L1_rough=14.1744
  - Fit marginal: rmse=1.6775, rel_err=0.0974

**Iter 8** | λ=3.906e-03 | RMSE=1.6772 | under_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=26.0912 is above target=15.5563 (rel_dev=0.68)
  - Under-regularisation suspected: osc=0.05, L1_rough=28.3329
  - Fit marginal: rmse=1.6772, rel_err=0.0974

## Notes

- Completed in 9 iteration(s)
