# IHCP Inversion Report

**Date:** 2026-04-20 17:21  
**Status:** `weak_pass`  
**Iterations:** 4  

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
- Lambda: `2.3683e-08`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `4.352199`
- Regularisation norm: `14933.910695`
- Objective value: `24.223423`

### Estimated Parameters

```
  x[  0] = -478.4487
  x[  1] = +311.5070
  x[  2] = +2130.5167
  x[  3] = +4972.3619
  x[  4] = +8785.2910
  x[  5] = +13453.3535
  x[  6] = +18749.4192
  x[  7] = +24362.7029
  x[  8] = +29962.3537
  x[  9] = +35217.5349
  x[ 10] = +39842.2064
  x[ 11] = +43684.3090
  x[ 12] = +46725.7161
  x[ 13] = +49020.6900
  x[ 14] = +50682.6597
  x[ 15] = +51873.1746
  x[ 16] = +52724.2910
  x[ 17] = +53330.0459
  x[ 18] = +53724.6361
  x[ 19] = +53940.9620
  x[ 20] = +54050.0450
  x[ 21] = +54090.5229
  x[ 22] = +54093.6574
  x[ 23] = +54091.6333
```

## Iteration Trace

**Iter 0** | λ=1.895e-07 | RMSE=0.4930 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=39701.6953
  - Fit marginal: rmse=0.4930, rel_err=0.0614

**Iter 1** | λ=9.473e-08 | RMSE=0.4340 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=47503.9803
  - Fit marginal: rmse=0.4340, rel_err=0.0540

**Iter 2** | λ=4.737e-08 | RMSE=0.4067 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=52322.6669
  - Fit marginal: rmse=0.4067, rel_err=0.0506

**Iter 3** | λ=2.368e-08 | RMSE=0.3957 | under_regularized | → stop_success_weak_pass
  - Discrepancy principle: ||r||=4.3522 is below target=5.5000 (rel_dev=0.21)
  - Under-regularisation suspected: osc=0.00, L1_rough=54574.1303
  - Fit marginal: rmse=0.3957, rel_err=0.0492

## Notes

- Completed in 4 iteration(s)
