# IHCP Inversion Report

**Date:** 2026-04-23 23:49  
**Status:** `weak_pass`  
**Iterations:** 3  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 0.5

## Final Inversion Configuration

- Solver: `tsvd`
- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 2
- Lambda: `5.0000e-02`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `6.925038`
- Regularisation norm: `31872.847363`
- Objective value: `47.956148`

### Estimated Parameters

```
  x[  0] = +40197.6214
  x[  1] = +56293.0556
  x[  2] = +61379.8127
  x[  3] = +60014.8839
  x[  4] = +54242.0959
  x[  5] = +47206.6856
  x[  6] = +37798.9163
  x[  7] = +26384.3325
  x[  8] = +18827.8146
  x[  9] = +19350.0067
  x[ 10] = +25138.8844
  x[ 11] = +32554.9071
  x[ 12] = +42294.4562
  x[ 13] = +53632.6283
  x[ 14] = +60505.1786
  x[ 15] = +59106.4565
  x[ 16] = +53003.3770
  x[ 17] = +45473.0071
  x[ 18] = +34676.9389
  x[ 19] = +22759.7877
  x[ 20] = +19699.9674
  x[ 21] = +27620.6273
  x[ 22] = +30302.0694
  x[ 23] = +14195.8549
```

## Iteration Trace

**Iter 0** | λ=1.000e-02 | RMSE=0.4257 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=2.30, L1_rough=712773.2191
  - Fit marginal: rmse=0.4257, rel_err=0.0229

**Iter 1** | λ=1.000e-02 | RMSE=0.4257 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=2.30, L1_rough=712773.2191
  - Fit marginal: rmse=0.4257, rel_err=0.0229

**Iter 2** | λ=5.000e-02 | RMSE=0.4452 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.02, L1_rough=172925.0811
  - Fit marginal: rmse=0.4452, rel_err=0.0239

## Notes

- Completed in 3 iteration(s)
