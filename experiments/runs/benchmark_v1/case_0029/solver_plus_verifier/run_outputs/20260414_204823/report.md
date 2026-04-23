# IHCP Inversion Report

**Date:** 2026-04-14 20:48  
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
- Regularisation order: 1
- Lambda: `2.8567e-07`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.524796`
- Regularisation norm: `9645.258367`
- Objective value: `267.595529`

### Estimated Parameters

```
  x[  0] = +52967.2702
  x[  1] = +52605.8886
  x[  2] = +51424.7784
  x[  3] = +49400.8703
  x[  4] = +46552.1806
  x[  5] = +43090.4945
  x[  6] = +39548.4081
  x[  7] = +36603.1216
  x[  8] = +34696.8816
  x[  9] = +34146.7600
  x[ 10] = +35078.8829
  x[ 11] = +37126.3680
  x[ 12] = +39607.7325
  x[ 13] = +41849.1313
  x[ 14] = +43340.2419
  x[ 15] = +43521.3896
  x[ 16] = +42429.7851
  x[ 17] = +40315.5114
  x[ 18] = +37743.0516
  x[ 19] = +35374.6456
  x[ 20] = +33391.3995
  x[ 21] = +32153.4159
  x[ 22] = +31622.5945
  x[ 23] = +31485.4539
```

## Iteration Trace

**Iter 0** | λ=2.857e-07 | RMSE=0.9980 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.09, L1_rough=40231.0757
  - Fit marginal: rmse=0.9980, rel_err=0.0493

## Notes

- Completed in 1 iteration(s)
