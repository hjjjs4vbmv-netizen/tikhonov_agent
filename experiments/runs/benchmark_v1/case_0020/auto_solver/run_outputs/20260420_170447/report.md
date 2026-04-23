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
- Noise std: 0.1

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `1.4151e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: None

## Solver Results

- Status: `success`
- Residual norm: `1.571522`
- Regularisation norm: `39277.005600`
- Objective value: `4.652701`

### Estimated Parameters

```
  x[  0] = +633.9091
  x[  1] = +2469.9640
  x[  2] = +9605.7252
  x[  3] = +21449.6048
  x[  4] = +35802.9868
  x[  5] = +45628.7985
  x[  6] = +48501.2844
  x[  7] = +41178.0507
  x[  8] = +32737.7956
  x[  9] = +31718.4623
  x[ 10] = +38346.4414
  x[ 11] = +47219.9094
  x[ 12] = +48802.6927
  x[ 13] = +41995.0372
  x[ 14] = +33083.6836
  x[ 15] = +31535.5421
  x[ 16] = +38877.3663
  x[ 17] = +47534.7704
  x[ 18] = +47422.8433
  x[ 19] = +38551.5793
  x[ 20] = +24220.9616
  x[ 21] = +10383.3425
  x[ 22] = +3132.0527
  x[ 23] = +2096.5822
```

## Iteration Trace

**Iter 0** | λ=1.415e-09 | RMSE=0.1010 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.03, L1_rough=160438.9950
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
