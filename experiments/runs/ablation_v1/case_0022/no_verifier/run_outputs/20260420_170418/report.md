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
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `9.2117e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.738561`
- Regularisation norm: `29735.927532`
- Objective value: `68.030550`

### Estimated Parameters

```
  x[  0] = +1693.9193
  x[  1] = +4671.6565
  x[  2] = +12773.9225
  x[  3] = +23609.1882
  x[  4] = +34481.9582
  x[  5] = +41291.0091
  x[  6] = +44228.2528
  x[  7] = +40689.3064
  x[  8] = +35834.4074
  x[  9] = +34711.2452
  x[ 10] = +37953.1118
  x[ 11] = +43601.7159
  x[ 12] = +45804.6653
  x[ 13] = +42954.3427
  x[ 14] = +37699.3018
  x[ 15] = +35950.2445
  x[ 16] = +39369.8524
  x[ 17] = +43783.3174
  x[ 18] = +42799.3984
  x[ 19] = +36246.2596
  x[ 20] = +24991.5138
  x[ 21] = +12941.1645
  x[ 22] = +6057.5466
  x[ 23] = +4904.9641
```

## Iteration Trace

**Iter 0** | λ=9.212e-09 | RMSE=0.4975 | well_regularized | → stop_success
  - skip_verifier=True: verification bypassed (ablation)

## Notes

- Completed in 1 iteration(s)
