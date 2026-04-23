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
- Lambda: `6.0993e-08`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.331422`
- Regularisation norm: `8374.082248`
- Objective value: `239.329623`

### Estimated Parameters

```
  x[  0] = -3063.3335
  x[  1] = +7086.9961
  x[  2] = +17217.9452
  x[  3] = +26603.9540
  x[  4] = +34159.6797
  x[  5] = +38859.5233
  x[  6] = +40562.8892
  x[  7] = +39677.1333
  x[  8] = +37991.3814
  x[  9] = +37383.4226
  x[ 10] = +38519.9719
  x[ 11] = +40676.5433
  x[ 12] = +42192.8828
  x[ 13] = +42200.8794
  x[ 14] = +41270.5751
  x[ 15] = +40819.1185
  x[ 16] = +41335.8541
  x[ 17] = +41624.2449
  x[ 18] = +39699.5626
  x[ 19] = +34490.3412
  x[ 20] = +25968.3483
  x[ 21] = +15273.8541
  x[ 22] = +4025.7078
  x[ 23] = -7063.5238
```

## Iteration Trace

**Iter 0** | λ=1.259e-08 | RMSE=1.0030 | under_regularized | → switch_reg_order_to_1
  - Under-regularisation suspected: osc=0.23, L1_rough=109800.9775
  - Fit marginal: rmse=1.0030, rel_err=0.0543

**Iter 1** | λ=4.388e-08 | RMSE=0.9991 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=0.23, L1_rough=69294.8938
  - Fit marginal: rmse=0.9991, rel_err=0.0541

**Iter 2** | λ=3.904e-07 | RMSE=1.0015 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=78480.4293
  - Fit marginal: rmse=1.0015, rel_err=0.0542

**Iter 3** | λ=1.952e-07 | RMSE=0.9946 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.14, L1_rough=85189.8286
  - Fit marginal: rmse=0.9946, rel_err=0.0539

**Iter 4** | λ=9.759e-08 | RMSE=0.9890 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.23, L1_rough=94200.3429
  - Fit marginal: rmse=0.9890, rel_err=0.0536

**Iter 5** | λ=4.879e-07 | RMSE=1.0040 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=76590.6323
  - Fit marginal: rmse=1.0040, rel_err=0.0544

**Iter 6** | λ=2.440e-07 | RMSE=0.9966 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=82698.2415
  - Fit marginal: rmse=0.9966, rel_err=0.0540

**Iter 7** | λ=1.220e-07 | RMSE=0.9907 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.14, L1_rough=90853.9628
  - Fit marginal: rmse=0.9907, rel_err=0.0537

**Iter 8** | λ=6.099e-08 | RMSE=0.9855 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.23, L1_rough=102497.8024
  - Fit marginal: rmse=0.9855, rel_err=0.0534

## Notes

- Completed in 9 iteration(s)
