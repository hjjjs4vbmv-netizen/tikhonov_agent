# IHCP Inversion Report

**Date:** 2026-04-14 20:48  
**Status:** `fail`  
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
- Lambda: `3.9035e-07`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.626679`
- Regularisation norm: `15605.372170`
- Objective value: `339.255124`

### Estimated Parameters

```
  x[  0] = +24434.4648
  x[  1] = +25598.9289
  x[  2] = +27972.5361
  x[  3] = +31381.9041
  x[  4] = +35430.3252
  x[  5] = +39614.7833
  x[  6] = +43497.1467
  x[  7] = +46709.9684
  x[  8] = +48837.6563
  x[  9] = +49640.2553
  x[ 10] = +49096.6317
  x[ 11] = +47199.1788
  x[ 12] = +44020.6573
  x[ 13] = +39822.9288
  x[ 14] = +35012.4615
  x[ 15] = +29833.8940
  x[ 16] = +24736.4044
  x[ 17] = +20053.1407
  x[ 18] = +16107.1947
  x[ 19] = +13140.2015
  x[ 20] = +10999.9459
  x[ 21] = +9719.8917
  x[ 22] = +9142.0783
  x[ 23] = +8979.7930
```

## Iteration Trace

**Iter 0** | λ=3.904e-07 | RMSE=1.0045 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=65866.2527
  - Fit marginal: rmse=1.0045, rel_err=0.0583

## Notes

- Completed in 1 iteration(s)
