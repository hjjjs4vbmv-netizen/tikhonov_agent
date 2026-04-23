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
- Lambda: `4.9335e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.842742`
- Regularisation norm: `202177.736503`
- Objective value: `263.168864`

### Estimated Parameters

```
  x[  0] = +44146.1922
  x[  1] = +54481.4591
  x[  2] = +58632.7146
  x[  3] = +57814.5690
  x[  4] = +54111.0091
  x[  5] = +41547.9756
  x[  6] = +38508.6831
  x[  7] = +28589.2554
  x[  8] = +22387.0079
  x[  9] = +22273.9586
  x[ 10] = +24341.6725
  x[ 11] = +35406.7285
  x[ 12] = +45778.4498
  x[ 13] = +54599.3974
  x[ 14] = +55779.2069
  x[ 15] = +54123.9808
  x[ 16] = +50775.6954
  x[ 17] = +46410.7622
  x[ 18] = +34906.3941
  x[ 19] = +29473.3233
  x[ 20] = +25178.6119
  x[ 21] = +19130.4040
  x[ 22] = +17387.4548
  x[ 23] = +11892.5912
```

## Iteration Trace

**Iter 0** | λ=4.933e-09 | RMSE=0.5042 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.02, L1_rough=128237.1425
  - Fit marginal: rmse=0.5042, rel_err=0.0270

## Notes

- Completed in 1 iteration(s)
