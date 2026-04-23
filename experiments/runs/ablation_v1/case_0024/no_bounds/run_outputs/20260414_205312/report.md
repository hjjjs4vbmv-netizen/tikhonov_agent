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
- Noise std: 1.0

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 2
- Lambda: `3.0496e-07`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `15.537922`
- Regularisation norm: `4530.953808`
- Objective value: `247.687806`

### Estimated Parameters

```
  x[  0] = +1638.0047
  x[  1] = +9670.6307
  x[  2] = +17539.2743
  x[  3] = +24795.3239
  x[  4] = +30886.5119
  x[  5] = +35361.8866
  x[  6] = +38122.7788
  x[  7] = +39376.6491
  x[  8] = +39755.8735
  x[  9] = +39964.2522
  x[ 10] = +40416.1666
  x[ 11] = +41132.3800
  x[ 12] = +41811.7268
  x[ 13] = +42194.6229
  x[ 14] = +42222.9649
  x[ 15] = +41950.3503
  x[ 16] = +41218.2998
  x[ 17] = +39552.6086
  x[ 18] = +36408.3115
  x[ 19] = +31569.4781
  x[ 20] = +25193.4747
  x[ 21] = +17790.7101
  x[ 22] = +9987.2202
  x[ 23] = +2139.3268
```

## Iteration Trace

**Iter 0** | λ=4.388e-08 | RMSE=0.9991 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=0.23, L1_rough=69294.8938
  - Fit marginal: rmse=0.9991, rel_err=0.0541

**Iter 1** | λ=3.904e-07 | RMSE=1.0015 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=78480.4293
  - Fit marginal: rmse=1.0015, rel_err=0.0542

**Iter 2** | λ=1.952e-07 | RMSE=0.9946 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.14, L1_rough=85189.8286
  - Fit marginal: rmse=0.9946, rel_err=0.0539

**Iter 3** | λ=9.759e-08 | RMSE=0.9890 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.23, L1_rough=94200.3429
  - Fit marginal: rmse=0.9890, rel_err=0.0536

**Iter 4** | λ=4.879e-07 | RMSE=1.0040 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=76590.6323
  - Fit marginal: rmse=1.0040, rel_err=0.0544

**Iter 5** | λ=2.440e-07 | RMSE=0.9966 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=82698.2415
  - Fit marginal: rmse=0.9966, rel_err=0.0540

**Iter 6** | λ=1.220e-07 | RMSE=0.9907 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.14, L1_rough=90853.9628
  - Fit marginal: rmse=0.9907, rel_err=0.0537

**Iter 7** | λ=6.099e-08 | RMSE=0.9855 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.23, L1_rough=102497.8024
  - Fit marginal: rmse=0.9855, rel_err=0.0534

**Iter 8** | λ=3.050e-07 | RMSE=0.9988 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.05, L1_rough=80668.5983
  - Fit marginal: rmse=0.9988, rel_err=0.0541

## Notes

- Completed in 9 iteration(s)
