# IHCP Inversion Report

**Date:** 2026-04-20 17:04  
**Status:** `weak_pass`  
**Iterations:** 1  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 0
- Lambda: `2.6422e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.836279`
- Regularisation norm: `209855.824376`
- Objective value: `177.768772`

### Estimated Parameters

```
  x[  0] = +4930.6899
  x[  1] = +3611.8836
  x[  2] = +10457.1171
  x[  3] = +12748.7582
  x[  4] = +17531.8454
  x[  5] = +11948.2323
  x[  6] = +25036.6347
  x[  7] = +24428.9949
  x[  8] = +25814.6745
  x[  9] = +30267.3919
  x[ 10] = +30034.6535
  x[ 11] = +38963.8481
  x[ 12] = +44049.8045
  x[ 13] = +49351.5205
  x[ 14] = +47628.3967
  x[ 15] = +48333.8114
  x[ 16] = +52555.5222
  x[ 17] = +60559.8559
  x[ 18] = +58560.2252
  x[ 19] = +65786.2182
  x[ 20] = +70711.8368
  x[ 21] = +67034.0721
  x[ 22] = +62944.2217
  x[ 23] = +37824.9630
```

## Iteration Trace

**Iter 0** | λ=2.642e-09 | RMSE=0.5037 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.04, L1_rough=121599.1251
  - Fit marginal: rmse=0.5037, rel_err=0.0228

## Notes

- Completed in 1 iteration(s)
