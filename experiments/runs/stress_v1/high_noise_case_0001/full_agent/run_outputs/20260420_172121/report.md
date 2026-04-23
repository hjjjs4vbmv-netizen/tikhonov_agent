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
- Lambda: `1.3563e-08`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `27.647087`
- Regularisation norm: `22664.057325`
- Objective value: `771.328452`

### Estimated Parameters

```
  x[  0] = -2111.1369
  x[  1] = +1380.6485
  x[  2] = +458.5995
  x[  3] = +908.7453
  x[  4] = +3540.3471
  x[  5] = +7476.3133
  x[  6] = +15623.5005
  x[  7] = +29787.1076
  x[  8] = +40566.8599
  x[  9] = +44461.5707
  x[ 10] = +47246.9895
  x[ 11] = +49490.1321
  x[ 12] = +49020.7325
  x[ 13] = +47449.1265
  x[ 14] = +49476.8655
  x[ 15] = +47750.0888
  x[ 16] = +46116.7102
  x[ 17] = +43641.2570
  x[ 18] = +43174.4340
  x[ 19] = +49227.4616
  x[ 20] = +50552.8065
  x[ 21] = +52543.8721
  x[ 22] = +54928.7721
  x[ 23] = +55000.9230
```

## Iteration Trace

**Iter 0** | λ=3.472e-06 | RMSE=1.9982 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=33291.3171
  - Fit marginal: rmse=1.9982, rel_err=0.0788

**Iter 1** | λ=1.736e-06 | RMSE=1.8970 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=40478.4866
  - Fit marginal: rmse=1.8970, rel_err=0.0748

**Iter 2** | λ=8.681e-07 | RMSE=1.8407 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=45483.4153
  - Fit marginal: rmse=1.8407, rel_err=0.0726

**Iter 3** | λ=4.340e-07 | RMSE=1.8107 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=48803.1209
  - Fit marginal: rmse=1.8107, rel_err=0.0714

**Iter 4** | λ=2.170e-07 | RMSE=1.7953 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=51977.3969
  - Fit marginal: rmse=1.7953, rel_err=0.0708

**Iter 5** | λ=1.085e-07 | RMSE=1.7874 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=56316.8278
  - Fit marginal: rmse=1.7874, rel_err=0.0705

**Iter 6** | λ=5.425e-08 | RMSE=1.7829 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=60862.3186
  - Fit marginal: rmse=1.7829, rel_err=0.0703

**Iter 7** | λ=2.713e-08 | RMSE=1.7798 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=65861.6013
  - Fit marginal: rmse=1.7798, rel_err=0.0702

**Iter 8** | λ=1.356e-08 | RMSE=1.7772 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.01, L1_rough=75643.0320
  - Fit marginal: rmse=1.7772, rel_err=0.0701

## Notes

- Completed in 9 iteration(s)
