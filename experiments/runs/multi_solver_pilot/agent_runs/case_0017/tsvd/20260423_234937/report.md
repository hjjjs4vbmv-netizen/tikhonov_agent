# IHCP Inversion Report

**Date:** 2026-04-23 23:49  
**Status:** `weak_pass`  
**Iterations:** 7  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 1.0

## Final Inversion Configuration

- Solver: `tsvd`
- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 2
- Lambda: `3.1250e-02`
- Lambda strategy: `fixed`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `13.622395`
- Regularisation norm: `190033.285331`
- Objective value: `185.569647`

### Estimated Parameters

```
  x[  0] = -11917.7036
  x[  1] = +36909.4844
  x[  2] = +23655.5866
  x[  3] = +3566.9039
  x[  4] = +53438.1219
  x[  5] = +51455.6694
  x[  6] = +21975.0279
  x[  7] = +65743.0172
  x[  8] = +76184.9241
  x[  9] = +34563.6996
  x[ 10] = +54468.8362
  x[ 11] = +74389.5956
  x[ 12] = +40561.2671
  x[ 13] = +35433.1851
  x[ 14] = +43588.9631
  x[ 15] = +27440.1783
  x[ 16] = +24317.0463
  x[ 17] = +11240.7493
  x[ 18] = -6787.2111
  x[ 19] = +16779.8997
  x[ 20] = +17092.7756
  x[ 21] = -14355.6669
  x[ 22] = +7161.7157
  x[ 23] = +22173.9242
```

## Iteration Trace

**Iter 0** | λ=1.000e-02 | RMSE=0.8522 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=6.94, L1_rough=1402581.9250
  - Fit marginal: rmse=0.8522, rel_err=0.0495

**Iter 1** | λ=1.000e-02 | RMSE=0.8522 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=6.94, L1_rough=1402581.9250
  - Fit marginal: rmse=0.8522, rel_err=0.0495

**Iter 2** | λ=5.000e-02 | RMSE=0.8863 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.01, L1_rough=117458.6669
  - Fit marginal: rmse=0.8863, rel_err=0.0515

**Iter 3** | λ=2.500e-02 | RMSE=0.8634 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=3.87, L1_rough=1047801.2544
  - Fit marginal: rmse=0.8634, rel_err=0.0501

**Iter 4** | λ=1.250e-01 | RMSE=0.8871 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=104029.3230
  - Fit marginal: rmse=0.8871, rel_err=0.0515

**Iter 5** | λ=6.250e-02 | RMSE=0.8863 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.01, L1_rough=117137.3202
  - Fit marginal: rmse=0.8863, rel_err=0.0515

**Iter 6** | λ=3.125e-02 | RMSE=0.8757 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=1.02, L1_rough=488507.4805
  - Fit marginal: rmse=0.8757, rel_err=0.0509

## Notes

- Completed in 7 iteration(s)
