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
- Lambda: `7.2886e-07`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.603372`
- Regularisation norm: `13164.637617`
- Objective value: `369.782576`

### Estimated Parameters

```
  x[  0] = +3192.9601
  x[  1] = +3924.1015
  x[  2] = +5514.1896
  x[  3] = +8020.7335
  x[  4] = +11412.7952
  x[  5] = +15580.2302
  x[  6] = +20361.9425
  x[  7] = +25483.5941
  x[  8] = +30493.6039
  x[  9] = +35045.1620
  x[ 10] = +38996.4042
  x[ 11] = +42264.8676
  x[ 12] = +44825.5767
  x[ 13] = +46747.7665
  x[ 14] = +48164.3666
  x[ 15] = +49111.7180
  x[ 16] = +49735.4529
  x[ 17] = +50130.0926
  x[ 18] = +50405.9843
  x[ 19] = +50659.0138
  x[ 20] = +50809.3404
  x[ 21] = +50916.9916
  x[ 22] = +50985.2449
  x[ 23] = +50999.2040
```

## Iteration Trace

**Iter 0** | λ=7.289e-07 | RMSE=1.0030 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=47806.2438
  - Fit marginal: rmse=1.0030, rel_err=0.0464

## Notes

- Completed in 1 iteration(s)
