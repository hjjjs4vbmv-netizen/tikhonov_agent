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
- Lambda: `1.5248e-07`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.439096`
- Regularisation norm: `5899.620444`
- Objective value: `243.672903`

### Estimated Parameters

```
  x[  0] = -715.6349
  x[  1] = +8432.0964
  x[  2] = +17414.4196
  x[  3] = +25643.9510
  x[  4] = +32364.0935
  x[  5] = +36941.1825
  x[  6] = +39281.1370
  x[  7] = +39710.4241
  x[  8] = +39249.9110
  x[  9] = +38989.8473
  x[ 10] = +39463.7706
  x[ 11] = +40516.8490
  x[ 12] = +41488.2666
  x[ 13] = +41938.9459
  x[ 14] = +41944.8769
  x[ 15] = +41874.7846
  x[ 16] = +41687.7643
  x[ 17] = +40661.3174
  x[ 18] = +37816.7250
  x[ 19] = +32675.3689
  x[ 20] = +25348.7965
  x[ 21] = +16554.9735
  x[ 22] = +7241.2641
  x[ 23] = -2088.2731
```

## Iteration Trace

**Iter 0** | λ=3.904e-07 | RMSE=1.0015 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=78480.4293
  - Fit marginal: rmse=1.0015, rel_err=0.0542

**Iter 1** | λ=1.952e-07 | RMSE=0.9946 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.14, L1_rough=85189.8286
  - Fit marginal: rmse=0.9946, rel_err=0.0539

**Iter 2** | λ=9.759e-08 | RMSE=0.9890 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.23, L1_rough=94200.3429
  - Fit marginal: rmse=0.9890, rel_err=0.0536

**Iter 3** | λ=4.879e-07 | RMSE=1.0040 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=76590.6323
  - Fit marginal: rmse=1.0040, rel_err=0.0544

**Iter 4** | λ=2.440e-07 | RMSE=0.9966 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=82698.2415
  - Fit marginal: rmse=0.9966, rel_err=0.0540

**Iter 5** | λ=1.220e-07 | RMSE=0.9907 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.14, L1_rough=90853.9628
  - Fit marginal: rmse=0.9907, rel_err=0.0537

**Iter 6** | λ=6.099e-08 | RMSE=0.9855 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.23, L1_rough=102497.8024
  - Fit marginal: rmse=0.9855, rel_err=0.0534

**Iter 7** | λ=3.050e-07 | RMSE=0.9988 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=80668.5983
  - Fit marginal: rmse=0.9988, rel_err=0.0541

**Iter 8** | λ=1.525e-07 | RMSE=0.9925 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.14, L1_rough=88134.8154
  - Fit marginal: rmse=0.9925, rel_err=0.0538

## Notes

- Completed in 9 iteration(s)
