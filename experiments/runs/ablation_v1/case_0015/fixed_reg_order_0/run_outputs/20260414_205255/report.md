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
- Regularisation order: 0
- Lambda: `1.2587e-08`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.879909`
- Regularisation norm: `166427.071901`
- Objective value: `410.736240`

### Estimated Parameters

```
  x[  0] = +12482.3102
  x[  1] = +19701.2233
  x[  2] = +22190.4434
  x[  3] = +27682.5026
  x[  4] = +34511.1711
  x[  5] = +40369.2187
  x[  6] = +45228.4053
  x[  7] = +50876.5041
  x[  8] = +54034.4478
  x[  9] = +53991.4169
  x[ 10] = +53611.9703
  x[ 11] = +51880.1866
  x[ 12] = +47325.9845
  x[ 13] = +40538.4603
  x[ 14] = +36087.9796
  x[ 15] = +28469.4874
  x[ 16] = +22495.4658
  x[ 17] = +16281.3768
  x[ 18] = +10546.5586
  x[ 19] = +9964.1980
  x[ 20] = +5926.7460
  x[ 21] = +4071.5655
  x[ 22] = +3131.6790
  x[ 23] = +920.9401
```

## Iteration Trace

**Iter 0** | λ=1.259e-08 | RMSE=0.5065 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.05, L1_rough=94665.6452
  - Fit marginal: rmse=0.5065, rel_err=0.0320

## Notes

- Completed in 1 iteration(s)
