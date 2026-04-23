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
- Noise std: 0.1

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `3.9062e-03`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `22.234421`
- Regularisation norm: `7.041921`
- Objective value: `494.563164`

### Estimated Parameters

```
  x[  0] = +35427.8691
  x[  1] = +35427.9898
  x[  2] = +35428.2415
  x[  3] = +35428.5726
  x[  4] = +35428.9041
  x[  5] = +35429.1406
  x[  6] = +35429.1826
  x[  7] = +35428.9387
  x[  8] = +35428.3340
  x[  9] = +35427.3218
  x[ 10] = +35425.8898
  x[ 11] = +35424.0608
  x[ 12] = +35421.8925
  x[ 13] = +35419.4738
  x[ 14] = +35416.9173
  x[ 15] = +35414.3459
  x[ 16] = +35411.8865
  x[ 17] = +35409.6557
  x[ 18] = +35407.7507
  x[ 19] = +35406.2401
  x[ 20] = +35405.1526
  x[ 21] = +35404.4768
  x[ 22] = +35404.1519
  x[ 23] = +35404.0646
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.4298 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=22.2431 is above target=1.5556 (rel_dev=13.30)
  - Fit marginal: rmse=1.4298, rel_err=0.0965

**Iter 1** | λ=5.000e-01 | RMSE=1.4298 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=22.2431 is above target=1.5556 (rel_dev=13.30)
  - Fit marginal: rmse=1.4298, rel_err=0.0965

**Iter 2** | λ=2.500e-01 | RMSE=1.4298 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=22.2430 is above target=1.5556 (rel_dev=13.30)
  - Fit marginal: rmse=1.4298, rel_err=0.0965

**Iter 3** | λ=1.250e-01 | RMSE=1.4298 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=22.2429 is above target=1.5556 (rel_dev=13.30)
  - Fit marginal: rmse=1.4298, rel_err=0.0965

**Iter 4** | λ=6.250e-02 | RMSE=1.4298 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=22.2426 is above target=1.5556 (rel_dev=13.30)
  - Fit marginal: rmse=1.4298, rel_err=0.0965

**Iter 5** | λ=3.125e-02 | RMSE=1.4298 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=22.2420 is above target=1.5556 (rel_dev=13.30)
  - Under-regularisation suspected: osc=0.05, L1_rough=3.3066
  - Fit marginal: rmse=1.4298, rel_err=0.0965

**Iter 6** | λ=1.562e-02 | RMSE=1.4297 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=22.2410 is above target=1.5556 (rel_dev=13.30)
  - Under-regularisation suspected: osc=0.05, L1_rough=6.6125
  - Fit marginal: rmse=1.4297, rel_err=0.0965

**Iter 7** | λ=7.812e-03 | RMSE=1.4296 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=22.2388 is above target=1.5556 (rel_dev=13.30)
  - Under-regularisation suspected: osc=0.05, L1_rough=13.2219
  - Fit marginal: rmse=1.4296, rel_err=0.0965

**Iter 8** | λ=3.906e-03 | RMSE=1.4293 | under_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=22.2344 is above target=1.5556 (rel_dev=13.29)
  - Under-regularisation suspected: osc=0.05, L1_rough=26.4316
  - Fit marginal: rmse=1.4293, rel_err=0.0965

## Notes

- Completed in 9 iteration(s)
