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
- Residual norm: `15.990136`
- Regularisation norm: `5.438956`
- Objective value: `255.800013`

### Estimated Parameters

```
  x[  0] = +32579.4452
  x[  1] = +32579.8240
  x[  2] = +32580.6557
  x[  3] = +32581.8886
  x[  4] = +32583.4300
  x[  5] = +32585.1680
  x[  6] = +32587.0008
  x[  7] = +32588.8524
  x[  8] = +32590.6661
  x[  9] = +32592.4016
  x[ 10] = +32594.0221
  x[ 11] = +32595.4809
  x[ 12] = +32596.7363
  x[ 13] = +32597.7710
  x[ 14] = +32598.5926
  x[ 15] = +32599.2090
  x[ 16] = +32599.6360
  x[ 17] = +32599.8813
  x[ 18] = +32599.9638
  x[ 19] = +32599.9237
  x[ 20] = +32599.8088
  x[ 21] = +32599.6879
  x[ 22] = +32599.6090
  x[ 23] = +32599.5824
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.0283 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.9973 is above target=7.7782 (rel_dev=1.06)
  - Fit marginal: rmse=1.0283, rel_err=0.0620

**Iter 1** | λ=5.000e-01 | RMSE=1.0283 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.9973 is above target=7.7782 (rel_dev=1.06)
  - Fit marginal: rmse=1.0283, rel_err=0.0620

**Iter 2** | λ=2.500e-01 | RMSE=1.0283 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.9973 is above target=7.7782 (rel_dev=1.06)
  - Fit marginal: rmse=1.0283, rel_err=0.0620

**Iter 3** | λ=1.250e-01 | RMSE=1.0283 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.9971 is above target=7.7782 (rel_dev=1.06)
  - Fit marginal: rmse=1.0283, rel_err=0.0620

**Iter 4** | λ=6.250e-02 | RMSE=1.0283 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.9969 is above target=7.7782 (rel_dev=1.06)
  - Fit marginal: rmse=1.0283, rel_err=0.0620

**Iter 5** | λ=3.125e-02 | RMSE=1.0283 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.9965 is above target=7.7782 (rel_dev=1.06)
  - Fit marginal: rmse=1.0283, rel_err=0.0620

**Iter 6** | λ=1.562e-02 | RMSE=1.0282 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.9956 is above target=7.7782 (rel_dev=1.06)
  - Under-regularisation suspected: osc=0.05, L1_rough=5.2305
  - Fit marginal: rmse=1.0282, rel_err=0.0620

**Iter 7** | λ=7.812e-03 | RMSE=1.0281 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.9937 is above target=7.7782 (rel_dev=1.06)
  - Under-regularisation suspected: osc=0.05, L1_rough=10.4574
  - Fit marginal: rmse=1.0281, rel_err=0.0620

**Iter 8** | λ=3.906e-03 | RMSE=1.0279 | under_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=15.9901 is above target=7.7782 (rel_dev=1.06)
  - Under-regularisation suspected: osc=0.05, L1_rough=20.9000
  - Fit marginal: rmse=1.0279, rel_err=0.0619

## Notes

- Completed in 9 iteration(s)
