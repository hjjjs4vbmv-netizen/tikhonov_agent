# IHCP Inversion Report

**Date:** 2026-04-14 20:52  
**Status:** `weak_pass`  
**Iterations:** 2  

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
- Lambda: `5.3340e-07`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.717968`
- Regularisation norm: `12744.053886`
- Objective value: `146.196804`

### Estimated Parameters

```
  x[  0] = +8789.3113
  x[  1] = +9367.8466
  x[  2] = +10586.2433
  x[  3] = +12401.5117
  x[  4] = +14709.2929
  x[  5] = +17386.8968
  x[  6] = +20349.4808
  x[  7] = +23540.5791
  x[  8] = +26874.2443
  x[  9] = +30302.5253
  x[ 10] = +33819.4516
  x[ 11] = +37378.7765
  x[ 12] = +40917.1342
  x[ 13] = +44398.2851
  x[ 14] = +47805.9059
  x[ 15] = +51043.4605
  x[ 16] = +54081.4861
  x[ 17] = +56853.4958
  x[ 18] = +59307.7058
  x[ 19] = +61394.5113
  x[ 20] = +62968.3749
  x[ 21] = +64021.1807
  x[ 22] = +64572.7258
  x[ 23] = +64727.2335
```

## Iteration Trace

**Iter 0** | λ=4.933e-09 | RMSE=0.5046 | under_regularized | → switch_reg_order_to_1
  - Under-regularisation suspected: osc=0.23, L1_rough=107465.4749
  - Fit marginal: rmse=0.5046, rel_err=0.0224

**Iter 1** | λ=5.334e-07 | RMSE=0.4961 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=55937.9222
  - Fit marginal: rmse=0.4961, rel_err=0.0220

## Notes

- Completed in 2 iteration(s)
