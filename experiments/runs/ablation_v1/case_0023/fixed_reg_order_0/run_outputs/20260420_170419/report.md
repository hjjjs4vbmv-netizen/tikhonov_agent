# IHCP Inversion Report

**Date:** 2026-04-20 17:04  
**Status:** `weak_pass`  
**Iterations:** 3  

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
- Regularisation order: 0
- Lambda: `5.8757e-09`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `13.905336`
- Regularisation norm: `159552.544855`
- Objective value: `342.936210`

### Estimated Parameters

```
  x[  0] = -379.5513
  x[  1] = +11191.4329
  x[  2] = +11550.3656
  x[  3] = +22033.0872
  x[  4] = +36135.9900
  x[  5] = +43110.2733
  x[  6] = +41529.5341
  x[  7] = +41549.3720
  x[  8] = +36889.4646
  x[  9] = +31029.3134
  x[ 10] = +36457.5449
  x[ 11] = +44672.0213
  x[ 12] = +44429.5432
  x[ 13] = +35403.7259
  x[ 14] = +38363.0955
  x[ 15] = +33106.0814
  x[ 16] = +38463.8306
  x[ 17] = +40293.7079
  x[ 18] = +34669.9220
  x[ 19] = +39431.6475
  x[ 20] = +22808.7617
  x[ 21] = +13507.9095
  x[ 22] = +9313.3927
  x[ 23] = +2122.6656
```

## Iteration Trace

**Iter 0** | λ=2.350e-08 | RMSE=0.9818 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.01, L1_rough=77060.7952
  - Fit marginal: rmse=0.9818, rel_err=0.0536

**Iter 1** | λ=1.175e-08 | RMSE=0.9188 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.02, L1_rough=99730.4615
  - Fit marginal: rmse=0.9188, rel_err=0.0502

**Iter 2** | λ=5.876e-09 | RMSE=0.8939 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.07, L1_rough=141619.9672
  - Fit marginal: rmse=0.8939, rel_err=0.0488

## Notes

- Completed in 3 iteration(s)
