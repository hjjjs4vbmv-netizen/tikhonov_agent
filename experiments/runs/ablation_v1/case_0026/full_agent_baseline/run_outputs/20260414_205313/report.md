# IHCP Inversion Report

**Date:** 2026-04-14 20:53  
**Status:** `weak_pass`  
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
- Regularisation order: 1
- Lambda: `2.6422e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.568523`
- Regularisation norm: `31588.050190`
- Objective value: `5.096674`

### Estimated Parameters

```
  x[  0] = +48484.9780
  x[  1] = +52524.6985
  x[  2] = +57926.2444
  x[  3] = +59133.9313
  x[  4] = +54743.3889
  x[  5] = +45628.9441
  x[  6] = +36167.5555
  x[  7] = +26909.9025
  x[  8] = +20998.1701
  x[  9] = +20307.2540
  x[ 10] = +24760.2738
  x[ 11] = +34023.8513
  x[ 12] = +44763.5169
  x[ 13] = +53936.3563
  x[ 14] = +58719.4862
  x[ 15] = +58706.7784
  x[ 16] = +54236.4674
  x[ 17] = +46167.5924
  x[ 18] = +35801.9799
  x[ 19] = +27249.0567
  x[ 20] = +22177.5345
  x[ 21] = +21234.7932
  x[ 22] = +24231.7644
  x[ 23] = +27159.1385
```

## Iteration Trace

**Iter 0** | λ=2.642e-09 | RMSE=0.1008 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.18, L1_rough=131296.9012
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
