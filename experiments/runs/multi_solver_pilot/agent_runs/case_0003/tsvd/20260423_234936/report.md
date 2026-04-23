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
- Residual norm: `7.037893`
- Regularisation norm: `43019.129129`
- Objective value: `49.531935`

### Estimated Parameters

```
  x[  0] = -2632.2712
  x[  1] = +104.6748
  x[  2] = +3778.4906
  x[  3] = +2174.1005
  x[  4] = -3130.4919
  x[  5] = -2945.9723
  x[  6] = +10035.5163
  x[  7] = +31930.2328
  x[  8] = +49734.7769
  x[  9] = +54124.0360
  x[ 10] = +48985.9675
  x[ 11] = +45726.0942
  x[ 12] = +48961.9915
  x[ 13] = +52481.7932
  x[ 14] = +50599.7594
  x[ 15] = +47252.2280
  x[ 16] = +48493.5866
  x[ 17] = +51215.7456
  x[ 18] = +48532.1508
  x[ 19] = +44159.9437
  x[ 20] = +49044.2936
  x[ 21] = +60179.4384
  x[ 22] = +55583.5922
  x[ 23] = +23734.6059
```

## Iteration Trace

**Iter 0** | λ=1.000e-02 | RMSE=0.4263 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=2.55, L1_rough=775482.3344
  - Fit marginal: rmse=0.4263, rel_err=0.0216

**Iter 1** | λ=1.000e-02 | RMSE=0.4263 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=2.55, L1_rough=775482.3344
  - Fit marginal: rmse=0.4263, rel_err=0.0216

**Iter 2** | λ=5.000e-02 | RMSE=0.4524 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.05, L1_rough=154441.1247
  - Fit marginal: rmse=0.4524, rel_err=0.0229

## Notes

- Completed in 3 iteration(s)
