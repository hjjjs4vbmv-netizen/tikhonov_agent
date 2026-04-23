# IHCP Inversion Report

**Date:** 2026-04-14 20:48  
**Status:** `weak_pass`  
**Iterations:** 4  

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
- Lambda: `3.5377e-08`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `2.174040`
- Regularisation norm: `9341.447838`
- Objective value: `7.813541`

### Estimated Parameters

```
  x[  0] = +775.6959
  x[  1] = -1005.7803
  x[  2] = -2470.6540
  x[  3] = -2665.0717
  x[  4] = -225.3045
  x[  5] = +6062.0345
  x[  6] = +16339.8482
  x[  7] = +28835.3935
  x[  8] = +40278.5656
  x[  9] = +48149.1017
  x[ 10] = +51958.3422
  x[ 11] = +52697.5320
  x[ 12] = +51840.3679
  x[ 13] = +50632.4214
  x[ 14] = +49766.2901
  x[ 15] = +49356.3037
  x[ 16] = +49303.5989
  x[ 17] = +49436.2111
  x[ 18] = +49652.3674
  x[ 19] = +49901.4329
  x[ 20] = +50081.7088
  x[ 21] = +50224.4194
  x[ 22] = +50355.0220
  x[ 23] = +50471.6188
```

## Iteration Trace

**Iter 0** | λ=1.934e-09 | RMSE=0.1002 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=0.41, L1_rough=62774.1877
  - Fit is good but regularisation balance is uncertain

**Iter 1** | λ=1.415e-09 | RMSE=0.1001 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.36, L1_rough=66339.4039
  - Fit is good but regularisation balance is uncertain

**Iter 2** | λ=7.075e-09 | RMSE=0.1141 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.23, L1_rough=63693.7515
  - Fit is good but regularisation balance is uncertain

**Iter 3** | λ=3.538e-08 | RMSE=0.1398 | under_regularized | → stop_success_weak_pass
  - Discrepancy principle: ||r||=2.1740 is above target=1.5556 (rel_dev=0.40)
  - Under-regularisation suspected: osc=0.14, L1_rough=63365.3243
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 4 iteration(s)
