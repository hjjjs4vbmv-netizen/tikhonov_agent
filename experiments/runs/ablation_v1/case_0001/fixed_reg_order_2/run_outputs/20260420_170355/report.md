# IHCP Inversion Report

**Date:** 2026-04-20 17:03  
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
- Regularisation order: 2
- Lambda: `1.4151e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.557070`
- Regularisation norm: `20384.067395`
- Objective value: `3.012446`

### Estimated Parameters

```
  x[  0] = -685.0527
  x[  1] = +825.2752
  x[  2] = +783.1336
  x[  3] = -606.0186
  x[  4] = -2613.8248
  x[  5] = -1215.6972
  x[  6] = +10473.0852
  x[  7] = +31678.6399
  x[  8] = +48106.1035
  x[  9] = +52692.8048
  x[ 10] = +51295.6462
  x[ 11] = +49782.1509
  x[ 12] = +49334.7599
  x[ 13] = +49498.8498
  x[ 14] = +50177.9848
  x[ 15] = +50143.1118
  x[ 16] = +49892.4289
  x[ 17] = +49451.0216
  x[ 18] = +49367.3584
  x[ 19] = +50142.6657
  x[ 20] = +50110.8197
  x[ 21] = +50101.6215
  x[ 22] = +50328.8952
  x[ 23] = +50356.7202
```

## Iteration Trace

**Iter 0** | λ=1.415e-09 | RMSE=0.1001 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.01, L1_rough=66339.4039
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
