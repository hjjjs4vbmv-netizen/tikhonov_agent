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
- Noise std: 2.0

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `3.8904e-01`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `45.570092`
- Regularisation norm: `0.210249`
- Objective value: `2076.650527`

### Estimated Parameters

```
  x[  0] = +31044.4044
  x[  1] = +31044.4126
  x[  2] = +31044.4315
  x[  3] = +31044.4608
  x[  4] = +31044.4999
  x[  5] = +31044.5481
  x[  6] = +31044.6043
  x[  7] = +31044.6663
  x[  8] = +31044.7320
  x[  9] = +31044.7993
  x[ 10] = +31044.8663
  x[ 11] = +31044.9313
  x[ 12] = +31044.9925
  x[ 13] = +31045.0485
  x[ 14] = +31045.0983
  x[ 15] = +31045.1417
  x[ 16] = +31045.1784
  x[ 17] = +31045.2085
  x[ 18] = +31045.2318
  x[ 19] = +31045.2489
  x[ 20] = +31045.2601
  x[ 21] = +31045.2665
  x[ 22] = +31045.2695
  x[ 23] = +31045.2703
```

## Iteration Trace

**Iter 0** | λ=9.960e-07 | RMSE=2.0011 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=45031.2608
  - Fit failed: rmse=2.0011 > threshold 2.0

**Iter 1** | λ=4.980e-06 | RMSE=2.2296 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=29596.5226
  - Fit failed: rmse=2.2296 > threshold 2.0

**Iter 2** | λ=2.490e-05 | RMSE=2.6419 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=41.0980 is above target=31.1127 (rel_dev=0.32)
  - Under-regularisation suspected: osc=0.00, L1_rough=10780.7221
  - Fit failed: rmse=2.6419 > threshold 2.0

**Iter 3** | λ=1.245e-04 | RMSE=2.8580 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=44.4602 is above target=31.1127 (rel_dev=0.43)
  - Under-regularisation suspected: osc=0.00, L1_rough=2574.9412
  - Fit failed: rmse=2.8580 > threshold 2.0

**Iter 4** | λ=6.225e-04 | RMSE=2.9144 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=45.3375 is above target=31.1127 (rel_dev=0.46)
  - Under-regularisation suspected: osc=0.00, L1_rough=535.7555
  - Fit failed: rmse=2.9144 > threshold 2.0

**Iter 5** | λ=3.112e-03 | RMSE=2.9264 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=45.5234 is above target=31.1127 (rel_dev=0.46)
  - Under-regularisation suspected: osc=0.00, L1_rough=108.0219
  - Fit failed: rmse=2.9264 > threshold 2.0

**Iter 6** | λ=1.556e-02 | RMSE=2.9288 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=45.5610 is above target=31.1127 (rel_dev=0.46)
  - Under-regularisation suspected: osc=0.00, L1_rough=21.6396
  - Fit failed: rmse=2.9288 > threshold 2.0

**Iter 7** | λ=7.781e-02 | RMSE=2.9293 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=45.5686 is above target=31.1127 (rel_dev=0.46)
  - Under-regularisation suspected: osc=0.00, L1_rough=4.3293
  - Fit failed: rmse=2.9293 > threshold 2.0

**Iter 8** | λ=3.890e-01 | RMSE=2.9294 | well_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=45.5701 is above target=31.1127 (rel_dev=0.46)
  - Fit failed: rmse=2.9294 > threshold 2.0

## Notes

- Completed in 9 iteration(s)
