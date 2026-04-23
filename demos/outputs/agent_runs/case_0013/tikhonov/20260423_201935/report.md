# IHCP Inversion Report

**Date:** 2026-04-23 20:19  
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

- Solver: `tikhonov`
- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `2.3503e-08`
- Lambda strategy: `discrepancy`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `1.573725`
- Regularisation norm: `24229.870762`
- Objective value: `16.274796`

### Estimated Parameters

```
  x[  0] = +12657.3977
  x[  1] = +15002.5561
  x[  2] = +19654.8619
  x[  3] = +26058.7628
  x[  4] = +33412.3127
  x[  5] = +40863.7616
  x[  6] = +47721.8295
  x[  7] = +53405.6262
  x[  8] = +57229.5274
  x[  9] = +58787.8888
  x[ 10] = +58059.9231
  x[ 11] = +55098.4417
  x[ 12] = +50136.7760
  x[ 13] = +43733.3133
  x[ 14] = +36653.7939
  x[ 15] = +29322.9058
  x[ 16] = +22406.0014
  x[ 17] = +16287.2597
  x[ 18] = +11292.1344
  x[ 19] = +7635.3265
  x[ 20] = +4957.4652
  x[ 21] = +3310.1438
  x[ 22] = +2527.8324
  x[ 23] = +2287.3193
```

## Iteration Trace

**Iter 0** | λ=2.350e-08 | RMSE=0.1012 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=102631.0605
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
