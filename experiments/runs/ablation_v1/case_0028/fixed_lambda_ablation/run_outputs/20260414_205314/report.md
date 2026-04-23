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
- Residual norm: `14.821073`
- Regularisation norm: `3.822337`
- Objective value: `219.721263`

### Estimated Parameters

```
  x[  0] = +42048.1959
  x[  1] = +42047.9777
  x[  2] = +42047.4804
  x[  3] = +42046.7079
  x[  4] = +42045.6948
  x[  5] = +42044.5046
  x[  6] = +42043.2288
  x[  7] = +42041.9498
  x[  8] = +42040.7509
  x[  9] = +42039.6896
  x[ 10] = +42038.7860
  x[ 11] = +42038.0258
  x[ 12] = +42037.3580
  x[ 13] = +42036.7223
  x[ 14] = +42036.0675
  x[ 15] = +42035.3713
  x[ 16] = +42034.6384
  x[ 17] = +42033.8971
  x[ 18] = +42033.1922
  x[ 19] = +42032.5836
  x[ 20] = +42032.1151
  x[ 21] = +42031.8089
  x[ 22] = +42031.6608
  x[ 23] = +42031.6239
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=0.9530 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=14.8249 is above target=7.7782 (rel_dev=0.91)
  - Fit marginal: rmse=0.9530, rel_err=0.0510

**Iter 1** | λ=5.000e-01 | RMSE=0.9530 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=14.8249 is above target=7.7782 (rel_dev=0.91)
  - Fit marginal: rmse=0.9530, rel_err=0.0510

**Iter 2** | λ=2.500e-01 | RMSE=0.9530 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=14.8249 is above target=7.7782 (rel_dev=0.91)
  - Fit marginal: rmse=0.9530, rel_err=0.0510

**Iter 3** | λ=1.250e-01 | RMSE=0.9530 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=14.8248 is above target=7.7782 (rel_dev=0.91)
  - Fit marginal: rmse=0.9530, rel_err=0.0510

**Iter 4** | λ=6.250e-02 | RMSE=0.9530 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=14.8247 is above target=7.7782 (rel_dev=0.91)
  - Fit marginal: rmse=0.9530, rel_err=0.0510

**Iter 5** | λ=3.125e-02 | RMSE=0.9530 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=14.8244 is above target=7.7782 (rel_dev=0.91)
  - Fit marginal: rmse=0.9530, rel_err=0.0510

**Iter 6** | λ=1.562e-02 | RMSE=0.9529 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=14.8240 is above target=7.7782 (rel_dev=0.91)
  - Under-regularisation suspected: osc=0.00, L1_rough=4.1475
  - Fit marginal: rmse=0.9529, rel_err=0.0510

**Iter 7** | λ=7.812e-03 | RMSE=0.9529 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=14.8230 is above target=7.7782 (rel_dev=0.91)
  - Under-regularisation suspected: osc=0.00, L1_rough=8.2921
  - Fit marginal: rmse=0.9529, rel_err=0.0510

**Iter 8** | λ=3.906e-03 | RMSE=0.9527 | under_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=14.8211 is above target=7.7782 (rel_dev=0.91)
  - Under-regularisation suspected: osc=0.00, L1_rough=16.5720
  - Fit marginal: rmse=0.9527, rel_err=0.0510

## Notes

- Completed in 9 iteration(s)
