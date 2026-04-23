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
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `3.9062e-03`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `23.331688`
- Regularisation norm: `7.123649`
- Objective value: `544.565905`

### Estimated Parameters

```
  x[  0] = +35541.2872
  x[  1] = +35541.3952
  x[  2] = +35541.6232
  x[  3] = +35541.9167
  x[  4] = +35542.1999
  x[  5] = +35542.3820
  x[  6] = +35542.3748
  x[  7] = +35542.0818
  x[  8] = +35541.4347
  x[  9] = +35540.3911
  x[ 10] = +35538.9376
  x[ 11] = +35537.0971
  x[ 12] = +35534.9172
  x[ 13] = +35532.4794
  x[ 14] = +35529.8926
  x[ 15] = +35527.2882
  x[ 16] = +35524.7987
  x[ 17] = +35522.5413
  x[ 18] = +35520.6090
  x[ 19] = +35519.0737
  x[ 20] = +35517.9639
  x[ 21] = +35517.2681
  x[ 22] = +35516.9332
  x[ 23] = +35516.8454
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.5004 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=23.3402 is above target=7.7782 (rel_dev=2.00)
  - Fit marginal: rmse=1.5004, rel_err=0.0941

**Iter 1** | λ=5.000e-01 | RMSE=1.5004 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=23.3401 is above target=7.7782 (rel_dev=2.00)
  - Fit marginal: rmse=1.5004, rel_err=0.0941

**Iter 2** | λ=2.500e-01 | RMSE=1.5004 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=23.3401 is above target=7.7782 (rel_dev=2.00)
  - Fit marginal: rmse=1.5004, rel_err=0.0940

**Iter 3** | λ=1.250e-01 | RMSE=1.5003 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=23.3399 is above target=7.7782 (rel_dev=2.00)
  - Fit marginal: rmse=1.5003, rel_err=0.0940

**Iter 4** | λ=6.250e-02 | RMSE=1.5003 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=23.3397 is above target=7.7782 (rel_dev=2.00)
  - Fit marginal: rmse=1.5003, rel_err=0.0940

**Iter 5** | λ=3.125e-02 | RMSE=1.5003 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=23.3391 is above target=7.7782 (rel_dev=2.00)
  - Under-regularisation suspected: osc=0.05, L1_rough=3.3320
  - Fit marginal: rmse=1.5003, rel_err=0.0940

**Iter 6** | λ=1.562e-02 | RMSE=1.5002 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=23.3381 is above target=7.7782 (rel_dev=2.00)
  - Under-regularisation suspected: osc=0.05, L1_rough=6.6632
  - Fit marginal: rmse=1.5002, rel_err=0.0940

**Iter 7** | λ=7.812e-03 | RMSE=1.5001 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=23.3359 is above target=7.7782 (rel_dev=2.00)
  - Under-regularisation suspected: osc=0.05, L1_rough=13.3228
  - Fit marginal: rmse=1.5001, rel_err=0.0940

**Iter 8** | λ=3.906e-03 | RMSE=1.4998 | under_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=23.3317 is above target=7.7782 (rel_dev=2.00)
  - Under-regularisation suspected: osc=0.05, L1_rough=26.6313
  - Fit marginal: rmse=1.4998, rel_err=0.0940

## Notes

- Completed in 9 iteration(s)
