# IHCP Inversion Report

**Date:** 2026-04-20 17:04  
**Status:** `pass`  
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
- Lambda: `1.5300e-07`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.466254`
- Regularisation norm: `19858.330912`
- Objective value: `299.539371`

### Estimated Parameters

```
  x[  0] = +20209.3998
  x[  1] = +21612.6695
  x[  2] = +24790.8590
  x[  3] = +29192.5654
  x[  4] = +34320.0539
  x[  5] = +39609.0827
  x[  6] = +44859.6402
  x[  7] = +49129.2974
  x[  8] = +52124.7702
  x[  9] = +53689.1225
  x[ 10] = +53673.0779
  x[ 11] = +52153.1675
  x[ 12] = +48891.3334
  x[ 13] = +43948.3826
  x[ 14] = +37683.2097
  x[ 15] = +30962.1879
  x[ 16] = +24539.8697
  x[ 17] = +18798.5695
  x[ 18] = +13788.2738
  x[ 19] = +9834.0266
  x[ 20] = +6817.3895
  x[ 21] = +4689.9431
  x[ 22] = +3680.0030
  x[ 23] = +3526.0158
```

## Iteration Trace

**Iter 0** | λ=1.530e-07 | RMSE=0.9942 | well_regularized | → stop_success
  - skip_verifier=True: verification bypassed (ablation)

## Notes

- Completed in 1 iteration(s)
