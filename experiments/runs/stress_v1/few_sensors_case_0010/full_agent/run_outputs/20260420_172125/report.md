# IHCP Inversion Report

**Date:** 2026-04-20 17:21  
**Status:** `weak_pass`  
**Iterations:** 9  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 1 at positions [0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `1.5535e-10`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `5.185040`
- Regularisation norm: `43528.087945`
- Objective value: `27.178981`

### Estimated Parameters

```
  x[  0] = +16419.5930
  x[  1] = +9752.9174
  x[  2] = -1425.1130
  x[  3] = -10382.0734
  x[  4] = -11126.4528
  x[  5] = -4117.7798
  x[  6] = +6420.2640
  x[  7] = +22633.3219
  x[  8] = +42358.1674
  x[  9] = +59968.9109
  x[ 10] = +68456.2364
  x[ 11] = +63596.4569
  x[ 12] = +50870.6305
  x[ 13] = +41337.4725
  x[ 14] = +42342.6645
  x[ 15] = +49255.9421
  x[ 16] = +53934.2933
  x[ 17] = +53117.2722
  x[ 18] = +48098.0467
  x[ 19] = +41062.9797
  x[ 20] = +37616.4234
  x[ 21] = +40450.2054
  x[ 22] = +43238.8239
  x[ 23] = +43501.2528
```

## Iteration Trace

**Iter 0** | λ=3.977e-08 | RMSE=0.5021 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=52305.9582
  - Fit marginal: rmse=0.5021, rel_err=0.0640

**Iter 1** | λ=1.989e-08 | RMSE=0.4915 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=55626.0801
  - Fit marginal: rmse=0.4915, rel_err=0.0627

**Iter 2** | λ=9.943e-09 | RMSE=0.4855 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=59370.5154
  - Fit marginal: rmse=0.4855, rel_err=0.0619

**Iter 3** | λ=4.971e-09 | RMSE=0.4815 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=63261.2721
  - Fit marginal: rmse=0.4815, rel_err=0.0614

**Iter 4** | λ=2.486e-09 | RMSE=0.4785 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=71068.6164
  - Fit marginal: rmse=0.4785, rel_err=0.0610

**Iter 5** | λ=1.243e-09 | RMSE=0.4760 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=84532.6230
  - Fit marginal: rmse=0.4760, rel_err=0.0607

**Iter 6** | λ=6.214e-10 | RMSE=0.4740 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.01, L1_rough=99726.5927
  - Fit marginal: rmse=0.4740, rel_err=0.0604

**Iter 7** | λ=3.107e-10 | RMSE=0.4725 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.01, L1_rough=129951.9399
  - Fit marginal: rmse=0.4725, rel_err=0.0602

**Iter 8** | λ=1.554e-10 | RMSE=0.4714 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.02, L1_rough=169047.0191
  - Fit marginal: rmse=0.4714, rel_err=0.0601

## Notes

- Completed in 9 iteration(s)
