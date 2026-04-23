# IHCP Inversion Report

**Date:** 2026-04-14 20:52  
**Status:** `weak_pass`  
**Iterations:** 5  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 0.1

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 2
- Lambda: `1.8947e-08`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `2.014730`
- Regularisation norm: `10734.916540`
- Objective value: `6.242527`

### Estimated Parameters

```
  x[  0] = +1966.1242
  x[  1] = -145.9094
  x[  2] = -2032.2569
  x[  3] = -2983.3243
  x[  4] = -1453.4812
  x[  5] = +4404.2734
  x[  6] = +15316.6899
  x[  7] = +29096.5947
  x[  8] = +41465.0588
  x[  9] = +49326.7832
  x[ 10] = +52487.3141
  x[ 11] = +52632.4107
  x[ 12] = +51560.3094
  x[ 13] = +50419.8136
  x[ 14] = +49670.2959
  x[ 15] = +49425.2748
  x[ 16] = +49574.0734
  x[ 17] = +49871.9333
  x[ 18] = +50082.1942
  x[ 19] = +50156.7170
  x[ 20] = +50048.9582
  x[ 21] = +49818.8075
  x[ 22] = +49647.7043
  x[ 23] = +49572.7952
```

## Iteration Trace

**Iter 0** | λ=7.579e-10 | RMSE=0.1058 | under_regularized | → switch_reg_order_to_1
  - Under-regularisation suspected: osc=0.73, L1_rough=101666.9541
  - Fit is good but regularisation balance is uncertain

**Iter 1** | λ=1.415e-09 | RMSE=0.1007 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=0.50, L1_rough=66075.6576
  - Fit is good but regularisation balance is uncertain

**Iter 2** | λ=7.579e-10 | RMSE=0.0993 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.45, L1_rough=70997.9434
  - Fit is good but regularisation balance is uncertain

**Iter 3** | λ=3.789e-09 | RMSE=0.1100 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.23, L1_rough=63002.0859
  - Fit is good but regularisation balance is uncertain

**Iter 4** | λ=1.895e-08 | RMSE=0.1295 | under_regularized | → stop_success_weak_pass
  - Discrepancy principle: ||r||=2.0147 is above target=1.5556 (rel_dev=0.30)
  - Under-regularisation suspected: osc=0.18, L1_rough=65087.6835
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 5 iteration(s)
