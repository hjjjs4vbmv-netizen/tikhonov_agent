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
- Noise std: 1.0

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `3.9062e-03`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `19.496171`
- Regularisation norm: `5.018418`
- Objective value: `380.199053`

### Estimated Parameters

```
  x[  0] = +32389.8627
  x[  1] = +32390.2279
  x[  2] = +32391.0201
  x[  3] = +32392.1915
  x[  4] = +32393.6493
  x[  5] = +32395.2810
  x[  6] = +32396.9893
  x[  7] = +32398.7056
  x[  8] = +32400.3751
  x[  9] = +32401.9628
  x[ 10] = +32403.4416
  x[ 11] = +32404.7675
  x[ 12] = +32405.8986
  x[ 13] = +32406.8204
  x[ 14] = +32407.5460
  x[ 15] = +32408.0785
  x[ 16] = +32408.4380
  x[ 17] = +32408.6325
  x[ 18] = +32408.6828
  x[ 19] = +32408.6308
  x[ 20] = +32408.5102
  x[ 21] = +32408.3900
  x[ 22] = +32408.3140
  x[ 23] = +32408.2880
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.2536 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=19.5012 is above target=15.5563 (rel_dev=0.25)
  - Fit marginal: rmse=1.2536, rel_err=0.0685

**Iter 1** | λ=5.000e-01 | RMSE=1.2536 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=19.5012 is above target=15.5563 (rel_dev=0.25)
  - Fit marginal: rmse=1.2536, rel_err=0.0685

**Iter 2** | λ=2.500e-01 | RMSE=1.2536 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=19.5011 is above target=15.5563 (rel_dev=0.25)
  - Fit marginal: rmse=1.2536, rel_err=0.0685

**Iter 3** | λ=1.250e-01 | RMSE=1.2536 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=19.5011 is above target=15.5563 (rel_dev=0.25)
  - Fit marginal: rmse=1.2536, rel_err=0.0685

**Iter 4** | λ=6.250e-02 | RMSE=1.2536 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=19.5009 is above target=15.5563 (rel_dev=0.25)
  - Fit marginal: rmse=1.2536, rel_err=0.0685

**Iter 5** | λ=3.125e-02 | RMSE=1.2535 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=19.5006 is above target=15.5563 (rel_dev=0.25)
  - Fit marginal: rmse=1.2535, rel_err=0.0685

**Iter 6** | λ=1.562e-02 | RMSE=1.2535 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=19.5000 is above target=15.5563 (rel_dev=0.25)
  - Under-regularisation suspected: osc=0.00, L1_rough=4.8088
  - Fit marginal: rmse=1.2535, rel_err=0.0685

**Iter 7** | λ=7.812e-03 | RMSE=1.2534 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=19.4987 is above target=15.5563 (rel_dev=0.25)
  - Under-regularisation suspected: osc=0.00, L1_rough=9.6142
  - Fit marginal: rmse=1.2534, rel_err=0.0685

**Iter 8** | λ=3.906e-03 | RMSE=1.2533 | under_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=19.4962 is above target=15.5563 (rel_dev=0.25)
  - Under-regularisation suspected: osc=0.00, L1_rough=19.2149
  - Fit marginal: rmse=1.2533, rel_err=0.0684

## Notes

- Completed in 9 iteration(s)
