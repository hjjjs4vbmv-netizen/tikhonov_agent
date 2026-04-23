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
- Lambda: `9.2117e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.620413`
- Regularisation norm: `158334.213374`
- Objective value: `289.005639`

### Estimated Parameters

```
  x[  0] = +3493.0709
  x[  1] = +9584.7636
  x[  2] = +13347.9291
  x[  3] = +22362.6495
  x[  4] = +33229.9626
  x[  5] = +40208.9633
  x[  6] = +41252.4113
  x[  7] = +40037.0724
  x[  8] = +36644.5657
  x[  9] = +34478.0903
  x[ 10] = +38086.6785
  x[ 11] = +42899.3929
  x[ 12] = +43047.0816
  x[ 13] = +38261.7173
  x[ 14] = +37143.4363
  x[ 15] = +35073.4221
  x[ 16] = +38264.3780
  x[ 17] = +40220.4640
  x[ 18] = +37428.3944
  x[ 19] = +34874.9397
  x[ 20] = +23346.2528
  x[ 21] = +14166.5767
  x[ 22] = +7938.0589
  x[ 23] = +2150.8670
```

## Iteration Trace

**Iter 0** | λ=9.212e-09 | RMSE=0.4899 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.01, L1_rough=104292.9514
  - Fit marginal: rmse=0.4899, rel_err=0.0295

## Notes

- Completed in 1 iteration(s)
