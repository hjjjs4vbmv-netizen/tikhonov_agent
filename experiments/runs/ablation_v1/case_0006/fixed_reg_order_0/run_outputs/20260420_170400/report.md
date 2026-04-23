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
- Noise std: 1.0

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 0
- Lambda: `9.2117e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.654156`
- Regularisation norm: `184740.726372`
- Objective value: `559.440194`

### Estimated Parameters

```
  x[  0] = +3054.9531
  x[  1] = +956.8058
  x[  2] = +3568.9552
  x[  3] = +3403.4772
  x[  4] = +4589.4733
  x[  5] = +1889.4215
  x[  6] = +16697.7080
  x[  7] = +28913.6205
  x[  8] = +38448.5221
  x[  9] = +43768.6613
  x[ 10] = +44006.1406
  x[ 11] = +49832.3487
  x[ 12] = +52946.9241
  x[ 13] = +54397.8686
  x[ 14] = +49869.4256
  x[ 15] = +46845.6098
  x[ 16] = +47384.8985
  x[ 17] = +50709.8959
  x[ 18] = +47540.6238
  x[ 19] = +49672.8343
  x[ 20] = +48812.0066
  x[ 21] = +39904.6915
  x[ 22] = +30399.8776
  x[ 23] = +15933.8168
```

## Iteration Trace

**Iter 0** | λ=9.212e-09 | RMSE=1.0063 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.02, L1_rough=111727.3146
  - Fit marginal: rmse=1.0063, rel_err=0.0478

## Notes

- Completed in 1 iteration(s)
