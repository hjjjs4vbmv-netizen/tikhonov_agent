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
- Lambda: `1.8362e-10`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `13.456168`
- Regularisation norm: `133177.203183`
- Objective value: `184.325107`

### Estimated Parameters

```
  x[  0] = -11939.3037
  x[  1] = +41507.8175
  x[  2] = +9287.1458
  x[  3] = +22374.2417
  x[  4] = +43397.5182
  x[  5] = +45837.2056
  x[  6] = +34979.1769
  x[  7] = +60905.7694
  x[  8] = +67303.6241
  x[  9] = +46453.4264
  x[ 10] = +53145.1074
  x[ 11] = +63433.9449
  x[ 12] = +56007.6227
  x[ 13] = +20812.3431
  x[ 14] = +56989.8081
  x[ 15] = +17193.7036
  x[ 16] = +27037.8176
  x[ 17] = +17521.2081
  x[ 18] = -20887.7300
  x[ 19] = +38020.5927
  x[ 20] = -6361.1306
  x[ 21] = -942.2444
  x[ 22] = +14135.3959
  x[ 23] = -1991.2405
```

## Iteration Trace

**Iter 0** | λ=2.350e-08 | RMSE=0.9799 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.01, L1_rough=86593.3649
  - Fit marginal: rmse=0.9799, rel_err=0.0569

**Iter 1** | λ=1.175e-08 | RMSE=0.9139 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.02, L1_rough=102533.4868
  - Fit marginal: rmse=0.9139, rel_err=0.0531

**Iter 2** | λ=5.876e-09 | RMSE=0.8904 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=132069.9229
  - Fit marginal: rmse=0.8904, rel_err=0.0517

**Iter 3** | λ=2.938e-09 | RMSE=0.8805 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.18, L1_rough=194036.2069
  - Fit marginal: rmse=0.8805, rel_err=0.0511

**Iter 4** | λ=1.469e-09 | RMSE=0.8735 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.52, L1_rough=303339.3366
  - Fit marginal: rmse=0.8735, rel_err=0.0507

**Iter 5** | λ=7.345e-10 | RMSE=0.8668 | under_regularized | → switch_reg_order_to_1
  - Under-regularisation suspected: osc=1.29, L1_rough=468246.2372
  - Fit marginal: rmse=0.8668, rel_err=0.0503

**Iter 6** | λ=7.345e-10 | RMSE=0.8764 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.24, L1_rough=229071.2970
  - Fit marginal: rmse=0.8764, rel_err=0.0509

**Iter 7** | λ=3.672e-10 | RMSE=0.8710 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.65, L1_rough=347185.8974
  - Fit marginal: rmse=0.8710, rel_err=0.0506

**Iter 8** | λ=1.836e-10 | RMSE=0.8650 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=1.49, L1_rough=519509.0865
  - Fit marginal: rmse=0.8650, rel_err=0.0502

## Notes

- Completed in 9 iteration(s)
