# IHCP Inversion Report

**Date:** 2026-04-20 17:21  
**Status:** `weak_pass`  
**Iterations:** 1  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 0.05

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `7.5787e-10`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.415240`
- Regularisation norm: `34970.116375`
- Objective value: `55.912583`

### Estimated Parameters

```
  x[  0] = +12735.5771
  x[  1] = +11657.7215
  x[  2] = +21595.9326
  x[  3] = +28552.9537
  x[  4] = +35791.2026
  x[  5] = +34240.8430
  x[  6] = +51850.3534
  x[  7] = +54705.7660
  x[  8] = +55985.7731
  x[  9] = +58276.3368
  x[ 10] = +53869.3177
  x[ 11] = +56711.7542
  x[ 12] = +54698.4945
  x[ 13] = +49783.4587
  x[ 14] = +36007.0461
  x[ 15] = +24826.3946
  x[ 16] = +20008.5327
  x[ 17] = +19062.1321
  x[ 18] = +8627.5670
  x[ 19] = +9336.6063
  x[ 20] = +8350.0942
  x[ 21] = -2015.9140
  x[ 22] = -2906.8983
  x[ 23] = +6116.9466
```

## Iteration Trace

**Iter 0** | λ=7.579e-10 | RMSE=0.4767 | under_regularized | → stop_success_weak_pass
  - Discrepancy principle: ||r||=7.4152 is above target=0.7778 (rel_dev=8.53)
  - Under-regularisation suspected: osc=0.05, L1_rough=128107.2220
  - Fit marginal: rmse=0.4767, rel_err=0.0299

## Notes

- Completed in 1 iteration(s)
