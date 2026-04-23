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
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 0
- Lambda: `9.2117e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.888173`
- Regularisation norm: `196945.357360`
- Objective value: `419.522120`

### Estimated Parameters

```
  x[  0] = +40825.9949
  x[  1] = +55881.1661
  x[  2] = +55442.0218
  x[  3] = +54994.6689
  x[  4] = +52159.5137
  x[  5] = +45177.2325
  x[  6] = +36318.6593
  x[  7] = +30717.2377
  x[  8] = +26449.6958
  x[  9] = +24136.2636
  x[ 10] = +27896.3812
  x[ 11] = +35360.8883
  x[ 12] = +42547.8142
  x[ 13] = +47595.1118
  x[ 14] = +54147.3930
  x[ 15] = +52956.5124
  x[ 16] = +49820.0093
  x[ 17] = +42551.9048
  x[ 18] = +33395.9392
  x[ 19] = +30493.7846
  x[ 20] = +23771.5470
  x[ 21] = +21082.5205
  x[ 22] = +18354.5763
  x[ 23] = +8281.7911
```

## Iteration Trace

**Iter 0** | λ=9.212e-09 | RMSE=0.5071 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.14, L1_rough=122676.8049
  - Fit marginal: rmse=0.5071, rel_err=0.0273

## Notes

- Completed in 1 iteration(s)
