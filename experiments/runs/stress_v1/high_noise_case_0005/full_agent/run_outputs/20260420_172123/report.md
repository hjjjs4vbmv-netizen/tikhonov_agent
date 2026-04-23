# IHCP Inversion Report

**Date:** 2026-04-20 17:21  
**Status:** `weak_pass`  
**Iterations:** 9  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 2.0

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `7.2642e-09`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `27.545017`
- Regularisation norm: `28832.904960`
- Objective value: `764.766928`

### Estimated Parameters

```
  x[  0] = +7993.8089
  x[  1] = +17152.7521
  x[  2] = +20914.9031
  x[  3] = +28341.7295
  x[  4] = +37902.2917
  x[  5] = +43782.5525
  x[  6] = +47729.3512
  x[  7] = +54926.8886
  x[  8] = +57438.3919
  x[  9] = +54196.1422
  x[ 10] = +53958.0895
  x[ 11] = +54205.3130
  x[ 12] = +48766.3679
  x[ 13] = +40007.0906
  x[ 14] = +37148.3970
  x[ 15] = +27490.9374
  x[ 16] = +18717.3258
  x[ 17] = +8778.7648
  x[ 18] = +2385.6248
  x[ 19] = +7993.6447
  x[ 20] = +5463.7677
  x[ 21] = +5477.7744
  x[ 22] = +7784.5664
  x[ 23] = +7239.9832
```

## Iteration Trace

**Iter 0** | λ=1.860e-06 | RMSE=1.9984 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=28967.4180
  - Fit marginal: rmse=1.9984, rel_err=0.0992

**Iter 1** | λ=9.298e-07 | RMSE=1.9162 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=43573.5433
  - Fit marginal: rmse=1.9162, rel_err=0.0951

**Iter 2** | λ=4.649e-07 | RMSE=1.8480 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=59847.1396
  - Fit marginal: rmse=1.8480, rel_err=0.0917

**Iter 3** | λ=2.325e-07 | RMSE=1.8061 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=73980.7191
  - Fit marginal: rmse=1.8061, rel_err=0.0896

**Iter 4** | λ=1.162e-07 | RMSE=1.7862 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=83893.3840
  - Fit marginal: rmse=1.7862, rel_err=0.0886

**Iter 5** | λ=5.811e-08 | RMSE=1.7781 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=90070.5505
  - Fit marginal: rmse=1.7781, rel_err=0.0882

**Iter 6** | λ=2.906e-08 | RMSE=1.7747 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=94425.8102
  - Fit marginal: rmse=1.7747, rel_err=0.0881

**Iter 7** | λ=1.453e-08 | RMSE=1.7727 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.01, L1_rough=102876.9826
  - Fit marginal: rmse=1.7727, rel_err=0.0880

**Iter 8** | λ=7.264e-09 | RMSE=1.7707 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.02, L1_rough=115995.0759
  - Fit marginal: rmse=1.7707, rel_err=0.0879

## Notes

- Completed in 9 iteration(s)
