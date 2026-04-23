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
- Noise std: 1.0

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 2
- Lambda: `1.8596e-06`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.580957`
- Regularisation norm: `2394.981773`
- Objective value: `253.432913`

### Estimated Parameters

```
  x[  0] = -10355.5096
  x[  1] = -5449.9369
  x[  2] = -478.8743
  x[  3] = +4666.4514
  x[  4] = +10100.6331
  x[  5] = +15880.3488
  x[  6] = +21951.4622
  x[  7] = +28099.9473
  x[  8] = +34024.7543
  x[  9] = +39418.1618
  x[ 10] = +44031.7849
  x[ 11] = +47708.3663
  x[ 12] = +50375.2884
  x[ 13] = +52059.0539
  x[ 14] = +52878.7180
  x[ 15] = +53021.5117
  x[ 16] = +52683.5253
  x[ 17] = +52025.0857
  x[ 18] = +51160.1096
  x[ 19] = +50173.4312
  x[ 20] = +49113.3022
  x[ 21] = +48015.5864
  x[ 22] = +46914.7751
  x[ 23] = +45821.8983
```

## Iteration Trace

**Iter 0** | λ=1.860e-06 | RMSE=1.0016 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.05, L1_rough=70576.6347
  - Fit marginal: rmse=1.0016, rel_err=0.0476

## Notes

- Completed in 1 iteration(s)
