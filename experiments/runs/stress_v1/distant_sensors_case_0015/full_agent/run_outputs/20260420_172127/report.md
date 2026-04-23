# IHCP Inversion Report

**Date:** 2026-04-20 17:21  
**Status:** `fail`  
**Iterations:** 9  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.04, 0.045] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `1.8169e-01`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `8.110428`
- Regularisation norm: `0.006444`
- Objective value: `65.779056`

### Estimated Parameters

```
  x[  0] = +22893.4525
  x[  1] = +22893.4529
  x[  2] = +22893.4537
  x[  3] = +22893.4549
  x[  4] = +22893.4564
  x[  5] = +22893.4583
  x[  6] = +22893.4603
  x[  7] = +22893.4625
  x[  8] = +22893.4647
  x[  9] = +22893.4669
  x[ 10] = +22893.4689
  x[ 11] = +22893.4708
  x[ 12] = +22893.4724
  x[ 13] = +22893.4738
  x[ 14] = +22893.4750
  x[ 15] = +22893.4758
  x[ 16] = +22893.4764
  x[ 17] = +22893.4768
  x[ 18] = +22893.4771
  x[ 19] = +22893.4772
  x[ 20] = +22893.4772
  x[ 21] = +22893.4772
  x[ 22] = +22893.4773
  x[ 23] = +22893.4773
```

## Iteration Trace

**Iter 0** | λ=4.651e-07 | RMSE=0.5024 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=8295.1380
  - Fit failed: rmse=0.5024 > threshold 2.0

**Iter 1** | λ=2.326e-06 | RMSE=0.5169 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=1872.4693
  - Fit failed: rmse=0.5169 > threshold 2.0

**Iter 2** | λ=1.163e-05 | RMSE=0.5204 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=384.3788
  - Fit failed: rmse=0.5204 > threshold 2.0

**Iter 3** | λ=5.814e-05 | RMSE=0.5212 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=77.2837
  - Fit failed: rmse=0.5212 > threshold 2.0

**Iter 4** | λ=2.907e-04 | RMSE=0.5213 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=15.4732
  - Fit failed: rmse=0.5213 > threshold 2.0

**Iter 5** | λ=1.454e-03 | RMSE=0.5214 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=3.0953
  - Fit failed: rmse=0.5214 > threshold 2.0

**Iter 6** | λ=7.268e-03 | RMSE=0.5214 | well_regularized | → increase_lambda
  - Fit failed: rmse=0.5214 > threshold 2.0

**Iter 7** | λ=3.634e-02 | RMSE=0.5214 | well_regularized | → increase_lambda
  - Fit failed: rmse=0.5214 > threshold 2.0

**Iter 8** | λ=1.817e-01 | RMSE=0.5214 | well_regularized | → stop_with_failure
  - Fit failed: rmse=0.5214 > threshold 2.0

## Notes

- Completed in 9 iteration(s)
