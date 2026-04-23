# IHCP Inversion Report

**Date:** 2026-04-23 19:57  
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

- Solver: `tsvd`
- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `1.0000e-02`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `1.326920`
- Regularisation norm: `45412.875334`
- Objective value: `20623294.221412`

### Estimated Parameters

```
  x[  0] = +5035.3188
  x[  1] = +20447.7229
  x[  2] = +15355.5216
  x[  3] = +27185.5404
  x[  4] = +33600.7894
  x[  5] = +42440.1977
  x[  6] = +45552.3505
  x[  7] = +55329.9593
  x[  8] = +59687.7711
  x[  9] = +57696.5039
  x[ 10] = +59547.1443
  x[ 11] = +55432.1869
  x[ 12] = +53986.1356
  x[ 13] = +37303.5743
  x[ 14] = +42975.3813
  x[ 15] = +24549.4712
  x[ 16] = +23060.0616
  x[ 17] = +18703.7708
  x[ 18] = +2824.6955
  x[ 19] = +16030.5534
  x[ 20] = -144.6745
  x[ 21] = +3767.4226
  x[ 22] = +3393.8221
  x[ 23] = -363.3331
```

## Iteration Trace

**Iter 0** | λ=1.000e-02 | RMSE=0.0853 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.16, L1_rough=174168.7637
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
