# IHCP Inversion Report

**Date:** 2026-04-23 20:19  
**Status:** `weak_pass`  
**Iterations:** 1  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 1.0

## Final Inversion Configuration

- Solver: `tikhonov`
- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `2.0906e-07`
- Lambda strategy: `discrepancy`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `15.507798`
- Regularisation norm: `16396.371086`
- Objective value: `296.695872`

### Estimated Parameters

```
  x[  0] = -453.4174
  x[  1] = +117.8883
  x[  2] = +1623.6972
  x[  3] = +4105.9033
  x[  4] = +7768.7975
  x[  5] = +12734.3502
  x[  6] = +19159.9660
  x[  7] = +26210.1277
  x[  8] = +33065.4017
  x[  9] = +39089.6971
  x[ 10] = +43978.1175
  x[ 11] = +47772.2741
  x[ 12] = +50322.5492
  x[ 13] = +51658.8138
  x[ 14] = +51965.9180
  x[ 15] = +51747.2919
  x[ 16] = +51398.1026
  x[ 17] = +51044.4940
  x[ 18] = +50598.5589
  x[ 19] = +50220.7082
  x[ 20] = +49803.6959
  x[ 21] = +49353.9236
  x[ 22] = +49148.1112
  x[ 23] = +49179.6590
```

## Iteration Trace

**Iter 0** | λ=2.091e-07 | RMSE=0.9969 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=55268.6901
  - Fit marginal: rmse=0.9969, rel_err=0.0474

## Notes

- Completed in 1 iteration(s)
