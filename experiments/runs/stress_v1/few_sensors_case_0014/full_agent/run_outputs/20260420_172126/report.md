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
- Lambda: `2.9007e-10`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `5.193597`
- Regularisation norm: `28310.891233`
- Objective value: `27.205945`

### Estimated Parameters

```
  x[  0] = +65754.0111
  x[  1] = +63052.4290
  x[  2] = +57134.9415
  x[  3] = +49646.8199
  x[  4] = +42518.1442
  x[  5] = +35476.4487
  x[  6] = +27848.3054
  x[  7] = +23769.1690
  x[  8] = +25369.8096
  x[  9] = +31695.4760
  x[ 10] = +38973.1368
  x[ 11] = +43181.6313
  x[ 12] = +44707.1401
  x[ 13] = +46964.2287
  x[ 14] = +51893.5255
  x[ 15] = +55820.7814
  x[ 16] = +54248.2313
  x[ 17] = +46484.7342
  x[ 18] = +35226.5913
  x[ 19] = +23878.9750
  x[ 20] = +16968.3071
  x[ 21] = +16125.9451
  x[ 22] = +16997.4006
  x[ 23] = +17085.9916
```

## Iteration Trace

**Iter 0** | λ=7.426e-08 | RMSE=0.5007 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=10685.8944
  - Fit marginal: rmse=0.5007, rel_err=0.0561

**Iter 1** | λ=3.713e-08 | RMSE=0.4951 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=16907.7871
  - Fit marginal: rmse=0.4951, rel_err=0.0555

**Iter 2** | λ=1.856e-08 | RMSE=0.4893 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=25776.7762
  - Fit marginal: rmse=0.4893, rel_err=0.0549

**Iter 3** | λ=9.282e-09 | RMSE=0.4839 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=38147.6512
  - Fit marginal: rmse=0.4839, rel_err=0.0543

**Iter 4** | λ=4.641e-09 | RMSE=0.4793 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=53234.4699
  - Fit marginal: rmse=0.4793, rel_err=0.0537

**Iter 5** | λ=2.321e-09 | RMSE=0.4760 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=70062.9823
  - Fit marginal: rmse=0.4760, rel_err=0.0534

**Iter 6** | λ=1.160e-09 | RMSE=0.4740 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=86103.7536
  - Fit marginal: rmse=0.4740, rel_err=0.0531

**Iter 7** | λ=5.801e-10 | RMSE=0.4729 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=100672.4628
  - Fit marginal: rmse=0.4729, rel_err=0.0530

**Iter 8** | λ=2.901e-10 | RMSE=0.4721 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.01, L1_rough=114691.3374
  - Fit marginal: rmse=0.4721, rel_err=0.0529

## Notes

- Completed in 9 iteration(s)
