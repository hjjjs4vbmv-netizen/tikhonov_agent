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
- Regularisation order: 2
- Lambda: `7.5787e-02`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.508554`
- Regularisation norm: `0.003312`
- Objective value: `2.275735`

### Estimated Parameters

```
  x[  0] = +1411.7240
  x[  1] = +4738.2147
  x[  2] = +8064.7055
  x[  3] = +11391.1965
  x[  4] = +14717.6880
  x[  5] = +18044.1801
  x[  6] = +21370.6732
  x[  7] = +24697.1676
  x[  8] = +28023.6633
  x[  9] = +31350.1604
  x[ 10] = +34676.6588
  x[ 11] = +38003.1584
  x[ 12] = +41329.6587
  x[ 13] = +44656.1595
  x[ 14] = +47982.6604
  x[ 15] = +51309.1614
  x[ 16] = +54635.6623
  x[ 17] = +57962.1632
  x[ 18] = +61288.6638
  x[ 19] = +64615.1644
  x[ 20] = +67941.6647
  x[ 21] = +71268.1649
  x[ 22] = +74594.6651
  x[ 23] = +77921.1654
```

## Iteration Trace

**Iter 0** | λ=7.579e-02 | RMSE=0.0970 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=76509.4413
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
