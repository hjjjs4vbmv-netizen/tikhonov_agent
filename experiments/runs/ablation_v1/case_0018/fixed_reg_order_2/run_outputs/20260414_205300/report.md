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
- Lambda: `1.8534e-08`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `14.998880`
- Regularisation norm: `7424.812044`
- Objective value: `225.988137`

### Estimated Parameters

```
  x[  0] = +10212.9532
  x[  1] = +16049.7871
  x[  2] = +22360.9522
  x[  3] = +28675.9507
  x[  4] = +34844.1862
  x[  5] = +40899.9383
  x[  6] = +47237.7020
  x[  7] = +51950.7713
  x[  8] = +54752.4645
  x[  9] = +56249.2192
  x[ 10] = +56911.7989
  x[ 11] = +56776.8084
  x[ 12] = +54100.7070
  x[ 13] = +47674.4267
  x[ 14] = +38118.6738
  x[ 15] = +28289.7667
  x[ 16] = +20591.0160
  x[ 17] = +15332.8045
  x[ 18] = +11358.8433
  x[ 19] = +8181.6774
  x[ 20] = +4718.5764
  x[ 21] = +887.3001
  x[ 22] = -1976.1933
  x[ 23] = -3771.9357
```

## Iteration Trace

**Iter 0** | λ=4.745e-06 | RMSE=1.0049 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=101701.9298
  - Fit marginal: rmse=1.0049, rel_err=0.0580

**Iter 1** | λ=2.372e-06 | RMSE=0.9866 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=108846.7032
  - Fit marginal: rmse=0.9866, rel_err=0.0570

**Iter 2** | λ=1.186e-06 | RMSE=0.9772 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=112096.3610
  - Fit marginal: rmse=0.9772, rel_err=0.0564

**Iter 3** | λ=5.931e-07 | RMSE=0.9719 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=112686.1255
  - Fit marginal: rmse=0.9719, rel_err=0.0561

**Iter 4** | λ=2.965e-07 | RMSE=0.9688 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=111747.9733
  - Fit marginal: rmse=0.9688, rel_err=0.0559

**Iter 5** | λ=1.483e-07 | RMSE=0.9670 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=110502.7057
  - Fit marginal: rmse=0.9670, rel_err=0.0558

**Iter 6** | λ=7.414e-08 | RMSE=0.9659 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=109625.2413
  - Fit marginal: rmse=0.9659, rel_err=0.0558

**Iter 7** | λ=3.707e-08 | RMSE=0.9651 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=108776.7594
  - Fit marginal: rmse=0.9651, rel_err=0.0557

**Iter 8** | λ=1.853e-08 | RMSE=0.9642 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.05, L1_rough=107382.5804
  - Fit marginal: rmse=0.9642, rel_err=0.0557

## Notes

- Completed in 9 iteration(s)
