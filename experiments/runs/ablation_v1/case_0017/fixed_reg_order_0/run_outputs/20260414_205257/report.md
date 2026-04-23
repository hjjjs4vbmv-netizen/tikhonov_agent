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
- Regularisation order: 2
- Lambda: `3.6723e-09`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `13.772073`
- Regularisation norm: `10916.995001`
- Objective value: `190.107667`

### Estimated Parameters

```
  x[  0] = +5541.9305
  x[  1] = +15747.0738
  x[  2] = +21719.8948
  x[  3] = +27929.3884
  x[  4] = +35446.0655
  x[  5] = +42096.8736
  x[  6] = +48150.2347
  x[  7] = +54601.0775
  x[  8] = +57817.5909
  x[  9] = +57267.4232
  x[ 10] = +56580.5897
  x[ 11] = +54938.5123
  x[ 12] = +49688.3629
  x[ 13] = +42486.0706
  x[ 14] = +36799.6728
  x[ 15] = +28735.9095
  x[ 16] = +20073.1755
  x[ 17] = +11613.4418
  x[ 18] = +6587.9057
  x[ 19] = +7035.2585
  x[ 20] = +5559.0592
  x[ 21] = +4616.5250
  x[ 22] = +4800.3334
  x[ 23] = +4291.0840
```

## Iteration Trace

**Iter 0** | λ=2.350e-08 | RMSE=0.9799 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=86593.3649
  - Fit marginal: rmse=0.9799, rel_err=0.0569

**Iter 1** | λ=1.175e-08 | RMSE=0.9139 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.14, L1_rough=102533.4868
  - Fit marginal: rmse=0.9139, rel_err=0.0531

**Iter 2** | λ=5.876e-09 | RMSE=0.8904 | under_regularized | → switch_reg_order_to_1
  - Under-regularisation suspected: osc=0.50, L1_rough=132069.9229
  - Fit marginal: rmse=0.8904, rel_err=0.0517

**Iter 3** | λ=5.876e-09 | RMSE=0.8851 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=0.23, L1_rough=107332.3597
  - Fit marginal: rmse=0.8851, rel_err=0.0514

**Iter 4** | λ=5.876e-09 | RMSE=0.8858 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.14, L1_rough=104808.8952
  - Fit marginal: rmse=0.8858, rel_err=0.0514

**Iter 5** | λ=2.938e-09 | RMSE=0.8850 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.23, L1_rough=109201.5380
  - Fit marginal: rmse=0.8850, rel_err=0.0514

**Iter 6** | λ=1.469e-08 | RMSE=0.8864 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.14, L1_rough=104705.9293
  - Fit marginal: rmse=0.8864, rel_err=0.0515

**Iter 7** | λ=7.345e-09 | RMSE=0.8860 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.14, L1_rough=104738.7079
  - Fit marginal: rmse=0.8860, rel_err=0.0515

**Iter 8** | λ=3.672e-09 | RMSE=0.8853 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.23, L1_rough=107064.4897
  - Fit marginal: rmse=0.8853, rel_err=0.0514

## Notes

- Completed in 9 iteration(s)
