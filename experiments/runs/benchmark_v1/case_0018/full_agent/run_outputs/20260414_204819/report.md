# IHCP Inversion Report

**Date:** 2026-04-14 20:48  
**Status:** `weak_pass`  
**Iterations:** 9  

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
- Regularisation order: 2
- Lambda: `1.1953e-09`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `14.910780`
- Regularisation norm: `30221.393400`
- Objective value: `223.423036`

### Estimated Parameters

```
  x[  0] = +11773.9090
  x[  1] = +14160.5066
  x[  2] = +22832.4001
  x[  3] = +30272.2113
  x[  4] = +34265.1507
  x[  5] = +36475.5700
  x[  6] = +49622.8439
  x[  7] = +55589.7452
  x[  8] = +55473.0657
  x[  9] = +53754.9962
  x[ 10] = +51905.4633
  x[ 11] = +56611.9780
  x[ 12] = +59031.6490
  x[ 13] = +52952.2625
  x[ 14] = +36869.9787
  x[ 15] = +22949.8276
  x[ 16] = +17957.1556
  x[ 17] = +16957.5639
  x[ 18] = +11950.6320
  x[ 19] = +11016.9015
  x[ 20] = +6657.2033
  x[ 21] = -3846.3651
  x[ 22] = -4869.8558
  x[ 23] = +6502.5547
```

## Iteration Trace

**Iter 0** | λ=1.530e-07 | RMSE=0.9942 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=83642.8295
  - Fit marginal: rmse=0.9942, rel_err=0.0574

**Iter 1** | λ=7.650e-08 | RMSE=0.9748 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.05, L1_rough=91547.8131
  - Fit marginal: rmse=0.9748, rel_err=0.0563

**Iter 2** | λ=3.825e-08 | RMSE=0.9678 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.09, L1_rough=96166.3309
  - Fit marginal: rmse=0.9678, rel_err=0.0559

**Iter 3** | λ=1.912e-08 | RMSE=0.9648 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.09, L1_rough=98798.9555
  - Fit marginal: rmse=0.9648, rel_err=0.0557

**Iter 4** | λ=9.562e-09 | RMSE=0.9627 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.18, L1_rough=102779.2471
  - Fit marginal: rmse=0.9627, rel_err=0.0556

**Iter 5** | λ=4.781e-09 | RMSE=0.9608 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.18, L1_rough=108421.6310
  - Fit marginal: rmse=0.9608, rel_err=0.0555

**Iter 6** | λ=2.391e-09 | RMSE=0.9585 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.18, L1_rough=118365.8543
  - Fit marginal: rmse=0.9585, rel_err=0.0554

**Iter 7** | λ=1.195e-09 | RMSE=0.9557 | under_regularized | → switch_reg_order_to_2
  - Under-regularisation suspected: osc=0.59, L1_rough=158731.1485
  - Fit marginal: rmse=0.9557, rel_err=0.0552

**Iter 8** | λ=1.195e-09 | RMSE=0.9585 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.18, L1_rough=129900.2192
  - Fit marginal: rmse=0.9585, rel_err=0.0554

## Notes

- Completed in 9 iteration(s)
