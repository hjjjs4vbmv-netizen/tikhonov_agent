# IHCP Inversion Report

**Date:** 2026-04-20 17:04  
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
- Lambda: `1.5248e-09`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `14.934942`
- Regularisation norm: `42305.429753`
- Objective value: `225.781542`

### Estimated Parameters

```
  x[  0] = +1204.6130
  x[  1] = +3354.0136
  x[  2] = +12733.6755
  x[  3] = +25140.3634
  x[  4] = +36664.9361
  x[  5] = +42982.3224
  x[  6] = +49195.4348
  x[  7] = +42059.8182
  x[  8] = +30261.9647
  x[  9] = +26063.1491
  x[ 10] = +32421.1538
  x[ 11] = +47700.0215
  x[ 12] = +55868.1430
  x[ 13] = +49537.9200
  x[ 14] = +33872.2058
  x[ 15] = +26822.9467
  x[ 16] = +35153.1427
  x[ 17] = +47626.3357
  x[ 18] = +48748.7997
  x[ 19] = +41886.9155
  x[ 20] = +25842.3310
  x[ 21] = +5692.9677
  x[ 22] = -2827.5370
  x[ 23] = +770.7663
```

## Iteration Trace

**Iter 0** | λ=3.904e-07 | RMSE=1.0015 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=78480.4293
  - Fit marginal: rmse=1.0015, rel_err=0.0542

**Iter 1** | λ=1.952e-07 | RMSE=0.9946 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=85189.8286
  - Fit marginal: rmse=0.9946, rel_err=0.0539

**Iter 2** | λ=9.759e-08 | RMSE=0.9890 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=94200.3429
  - Fit marginal: rmse=0.9890, rel_err=0.0536

**Iter 3** | λ=4.879e-08 | RMSE=0.9839 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=107496.2495
  - Fit marginal: rmse=0.9839, rel_err=0.0533

**Iter 4** | λ=2.440e-08 | RMSE=0.9785 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.01, L1_rough=124645.6456
  - Fit marginal: rmse=0.9785, rel_err=0.0530

**Iter 5** | λ=1.220e-08 | RMSE=0.9729 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.01, L1_rough=145398.5777
  - Fit marginal: rmse=0.9729, rel_err=0.0527

**Iter 6** | λ=6.099e-09 | RMSE=0.9677 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.02, L1_rough=167243.6271
  - Fit marginal: rmse=0.9677, rel_err=0.0524

**Iter 7** | λ=3.050e-09 | RMSE=0.9633 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.04, L1_rough=186434.5511
  - Fit marginal: rmse=0.9633, rel_err=0.0522

**Iter 8** | λ=1.525e-09 | RMSE=0.9601 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.06, L1_rough=207073.7909
  - Fit marginal: rmse=0.9601, rel_err=0.0520

## Notes

- Completed in 9 iteration(s)
