# IHCP Inversion Report

**Date:** 2026-04-14 20:48  
**Status:** `fail`  
**Iterations:** 1  

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
- Lambda: `2.6422e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `1.592322`
- Regularisation norm: `35603.181818`
- Objective value: `5.884718`

### Estimated Parameters

```
  x[  0] = -309.2568
  x[  1] = +3147.3567
  x[  2] = +9873.2411
  x[  3] = +21626.2698
  x[  4] = +35633.9270
  x[  5] = +45535.4435
  x[  6] = +46837.6979
  x[  7] = +41193.8379
  x[  8] = +34353.8981
  x[  9] = +33020.2705
  x[ 10] = +39004.0368
  x[ 11] = +46046.1758
  x[ 12] = +46706.1656
  x[ 13] = +40464.9292
  x[ 14] = +34387.1502
  x[ 15] = +33437.8013
  x[ 16] = +39407.3723
  x[ 17] = +45810.8008
  x[ 18] = +45734.8342
  x[ 19] = +38043.4578
  x[ 20] = +24198.1688
  x[ 21] = +11894.5941
  x[ 22] = +4895.5000
  x[ 23] = +2568.7310
```

## Iteration Trace

**Iter 0** | λ=2.642e-09 | RMSE=0.1024 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=0.23, L1_rough=143533.7107
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
