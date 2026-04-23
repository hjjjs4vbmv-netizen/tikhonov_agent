# IHCP Inversion Report

**Date:** 2026-04-20 17:03  
**Status:** `pass`  
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
- Regularisation order: 1
- Lambda: `5.9965e-08`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.822791`
- Regularisation norm: `19232.126676`
- Objective value: `83.375679`

### Estimated Parameters

```
  x[  0] = +54761.3699
  x[  1] = +55084.7585
  x[  2] = +54604.0357
  x[  3] = +52684.5758
  x[  4] = +48821.5611
  x[  5] = +43152.2812
  x[  6] = +36783.3351
  x[  7] = +31326.8784
  x[  8] = +27926.5439
  x[  9] = +27450.0000
  x[ 10] = +30288.3093
  x[ 11] = +35622.0933
  x[ 12] = +41848.5393
  x[ 13] = +47362.4118
  x[ 14] = +50952.3964
  x[ 15] = +51318.1907
  x[ 16] = +48618.6874
  x[ 17] = +43552.6053
  x[ 18] = +37576.6451
  x[ 19] = +32345.4090
  x[ 20] = +28273.6645
  x[ 21] = +26065.5925
  x[ 22] = +25378.4904
  x[ 23] = +25280.4243
```

## Iteration Trace

**Iter 0** | λ=5.997e-08 | RMSE=0.5029 | well_regularized | → stop_success
  - skip_verifier=True: verification bypassed (ablation)

## Notes

- Completed in 1 iteration(s)
