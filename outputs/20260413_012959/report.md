# IHCP Inversion Report

**Date:** 2026-04-13 01:29  
**Status:** `fail`  
**Iterations:** 9  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 60 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 0.3

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 2
- Lambda: `5.6679e-05`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1256.538721`
- Regularisation norm: `13260.965681`
- Objective value: `1588856.663981`

### Estimated Parameters

```
  x[  0] = +500000.0000
  x[  1] = +500000.0000
  x[  2] = +500000.0000
  x[  3] = +500000.0000
  x[  4] = +495624.5060
  x[  5] = +478789.4011
  x[  6] = +462266.9503
  x[  7] = +445999.8980
  x[  8] = +429890.6968
  x[  9] = +413816.1346
  x[ 10] = +397643.1943
  x[ 11] = +381244.3817
  x[ 12] = +364510.9320
  x[ 13] = +347362.7951
  x[ 14] = +329754.7510
  x[ 15] = +311679.0624
  x[ 16] = +293163.7062
  x[ 17] = +274266.3691
  x[ 18] = +255064.9881
  x[ 19] = +235646.0929
  x[ 20] = +216092.2242
  x[ 21] = +196470.3975
  x[ 22] = +176824.3655
  x[ 23] = +157174.0728
```

## Iteration Trace

**Iter 0** | λ=7.255e-10 | RMSE=81.3684 | under_regularized | → switch_reg_order_to_2
  - Discrepancy principle: ||r||=1265.7950 is above target=4.6669 (rel_dev=270.23)
  - Under-regularisation suspected: osc=0.18, L1_rough=955796.8695
  - Fit failed: rmse=81.3684 > threshold 2.0

**Iter 1** | λ=7.255e-10 | RMSE=81.4818 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=1267.5592 is above target=4.6669 (rel_dev=270.61)
  - Under-regularisation suspected: osc=0.27, L1_rough=1077943.9831
  - Fit failed: rmse=81.4818 > threshold 2.0

**Iter 2** | λ=3.627e-09 | RMSE=81.3308 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=1265.2098 is above target=4.6669 (rel_dev=270.10)
  - Under-regularisation suspected: osc=0.18, L1_rough=830196.4529
  - Fit failed: rmse=81.3308 > threshold 2.0

**Iter 3** | λ=1.814e-08 | RMSE=81.1004 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=1261.6258 is above target=4.6669 (rel_dev=269.33)
  - Under-regularisation suspected: osc=0.14, L1_rough=695889.6035
  - Fit failed: rmse=81.1004 > threshold 2.0

**Iter 4** | λ=9.069e-08 | RMSE=80.9329 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=1259.0208 is above target=4.6669 (rel_dev=268.78)
  - Under-regularisation suspected: osc=0.14, L1_rough=604628.8614
  - Fit failed: rmse=80.9329 > threshold 2.0

**Iter 5** | λ=4.534e-07 | RMSE=80.8278 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=1257.3856 is above target=4.6669 (rel_dev=268.43)
  - Under-regularisation suspected: osc=0.14, L1_rough=500223.7695
  - Fit failed: rmse=80.8278 > threshold 2.0

**Iter 6** | λ=2.267e-06 | RMSE=80.7709 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=1256.5002 is above target=4.6669 (rel_dev=268.24)
  - Under-regularisation suspected: osc=0.05, L1_rough=420821.5001
  - Fit failed: rmse=80.7709 > threshold 2.0

**Iter 7** | λ=1.134e-05 | RMSE=80.7656 | under_regularized | → increase_lambda
  - Discrepancy principle: ||r||=1256.4185 is above target=4.6669 (rel_dev=268.22)
  - Under-regularisation suspected: osc=0.05, L1_rough=371209.5423
  - Fit failed: rmse=80.7656 > threshold 2.0

**Iter 8** | λ=5.668e-05 | RMSE=80.7734 | under_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=1256.5387 is above target=4.6669 (rel_dev=268.24)
  - Under-regularisation suspected: osc=0.05, L1_rough=342825.9272
  - Fit failed: rmse=80.7734 > threshold 2.0

## Warnings

- Solution clamped to physical bounds [-500000.0, 500000.0]; 3 parameters affected
- Solution clamped to physical bounds [-500000.0, 500000.0]; 2 parameters affected
- Solution clamped to physical bounds [-500000.0, 500000.0]; 4 parameters affected

## Notes

- Completed in 9 iteration(s)
