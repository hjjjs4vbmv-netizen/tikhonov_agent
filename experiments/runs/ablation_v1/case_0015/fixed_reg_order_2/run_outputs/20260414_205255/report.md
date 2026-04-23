# IHCP Inversion Report

**Date:** 2026-04-14 20:52  
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
- Regularisation order: 2
- Lambda: `2.5411e-06`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.796436`
- Regularisation norm: `3736.248535`
- Objective value: `96.256733`

### Estimated Parameters

```
  x[  0] = +10673.8822
  x[  1] = +17385.2096
  x[  2] = +24037.8080
  x[  3] = +30510.6143
  x[  4] = +36619.1100
  x[  5] = +42131.3633
  x[  6] = +46796.3601
  x[  7] = +50372.7762
  x[  8] = +52656.9020
  x[  9] = +53516.6984
  x[ 10] = +52912.2109
  x[ 11] = +50896.8392
  x[ 12] = +47614.0512
  x[ 13] = +43284.5051
  x[ 14] = +38176.6133
  x[ 15] = +32566.3687
  x[ 16] = +26712.8533
  x[ 17] = +20823.9793
  x[ 18] = +15038.9741
  x[ 19] = +9419.9779
  x[ 20] = +3956.8898
  x[ 21] = -1394.0987
  x[ 22] = -6688.7710
  x[ 23] = -11969.3264
```

## Iteration Trace

**Iter 0** | λ=2.541e-06 | RMSE=0.5012 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.05, L1_rough=108328.8410
  - Fit marginal: rmse=0.5012, rel_err=0.0316

## Notes

- Completed in 1 iteration(s)
