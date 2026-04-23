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
- Regularisation order: 2
- Lambda: `2.0906e-07`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.846364`
- Regularisation norm: `7830.012703`
- Objective value: `74.382749`

### Estimated Parameters

```
  x[  0] = +59357.4559
  x[  1] = +57405.1928
  x[  2] = +55029.7318
  x[  3] = +51695.5160
  x[  4] = +47079.9450
  x[  5] = +41380.0082
  x[  6] = +35409.0820
  x[  7] = +30366.6087
  x[  8] = +27411.0888
  x[  9] = +27326.1580
  x[ 10] = +30238.5010
  x[ 11] = +35458.8511
  x[ 12] = +41666.5641
  x[ 13] = +47317.8050
  x[ 14] = +51050.8403
  x[ 15] = +51973.3423
  x[ 16] = +49972.4793
  x[ 17] = +45610.8267
  x[ 18] = +39887.7212
  x[ 19] = +33825.3561
  x[ 20] = +28060.1771
  x[ 21] = +22856.0354
  x[ 22] = +18074.9669
  x[ 23] = +13428.5695
```

## Iteration Trace

**Iter 0** | λ=2.091e-07 | RMSE=0.5044 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=95223.2549
  - Fit marginal: rmse=0.5044, rel_err=0.0271

## Notes

- Completed in 1 iteration(s)
