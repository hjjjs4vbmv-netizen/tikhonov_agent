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
- Residual norm: `7.763575`
- Regularisation norm: `163231.156146`
- Objective value: `191.722849`

### Estimated Parameters

```
  x[  0] = +4514.5522
  x[  1] = +5272.7618
  x[  2] = +13533.9791
  x[  3] = +23002.2147
  x[  4] = +35035.3036
  x[  5] = +38567.1229
  x[  6] = +46279.5946
  x[  7] = +40048.0245
  x[  8] = +33601.2130
  x[  9] = +33414.4131
  x[ 10] = +36120.3937
  x[ 11] = +45089.9875
  x[ 12] = +47446.4889
  x[ 13] = +44052.7351
  x[ 14] = +35423.1201
  x[ 15] = +32713.3721
  x[ 16] = +37707.8403
  x[ 17] = +45310.2082
  x[ 18] = +41781.3219
  x[ 19] = +36385.2255
  x[ 20] = +25501.0763
  x[ 21] = +10490.9428
  x[ 22] = +3143.1212
  x[ 23] = +2929.6966
```

## Iteration Trace

**Iter 0** | λ=4.933e-09 | RMSE=0.4991 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.03, L1_rough=138372.7642
  - Fit marginal: rmse=0.4991, rel_err=0.0301

## Notes

- Completed in 1 iteration(s)
