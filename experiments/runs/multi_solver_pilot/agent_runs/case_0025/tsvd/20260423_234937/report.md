# IHCP Inversion Report

**Date:** 2026-04-23 23:49  
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
- Residual norm: `1.320677`
- Regularisation norm: `51825.505619`
- Objective value: `1.744188`

### Estimated Parameters

```
  x[  0] = +39645.5771
  x[  1] = +60138.5015
  x[  2] = +55125.5679
  x[  3] = +60951.3860
  x[  4] = +55267.7263
  x[  5] = +47757.2893
  x[  6] = +33256.7482
  x[  7] = +27707.8678
  x[  8] = +22207.4325
  x[  9] = +17865.2866
  x[ 10] = +25247.4120
  x[ 11] = +33173.7508
  x[ 12] = +47519.2685
  x[ 13] = +46946.8057
  x[ 14] = +65814.6951
  x[ 15] = +55438.6138
  x[ 16] = +56128.5586
  x[ 17] = +48977.3861
  x[ 18] = +27484.5800
  x[ 19] = +35090.6963
  x[ 20] = +15850.4871
  x[ 21] = +21173.4676
  x[ 22] = +26466.7723
  x[ 23] = +33018.5353
```

## Iteration Trace

**Iter 0** | λ=1.000e-02 | RMSE=0.0849 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.12, L1_rough=207236.4879
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
