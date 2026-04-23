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
- Lambda: `2.0425e-02`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `8.739500`
- Regularisation norm: `0.058193`
- Objective value: `76.378923`

### Estimated Parameters

```
  x[  0] = +24614.7897
  x[  1] = +24614.7932
  x[  2] = +24614.8008
  x[  3] = +24614.8121
  x[  4] = +24614.8267
  x[  5] = +24614.8440
  x[  6] = +24614.8630
  x[  7] = +24614.8831
  x[  8] = +24614.9033
  x[  9] = +24614.9230
  x[ 10] = +24614.9413
  x[ 11] = +24614.9577
  x[ 12] = +24614.9719
  x[ 13] = +24614.9837
  x[ 14] = +24614.9929
  x[ 15] = +24614.9999
  x[ 16] = +24615.0047
  x[ 17] = +24615.0078
  x[ 18] = +24615.0096
  x[ 19] = +24615.0106
  x[ 20] = +24615.0109
  x[ 21] = +24615.0110
  x[ 22] = +24615.0111
  x[ 23] = +24615.0111
```

## Iteration Trace

**Iter 0** | λ=5.229e-08 | RMSE=0.5018 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=34377.0042
  - Fit failed: rmse=0.5018 > threshold 2.0

**Iter 1** | λ=2.614e-07 | RMSE=0.5339 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=13310.2712
  - Fit failed: rmse=0.5339 > threshold 2.0

**Iter 2** | λ=1.307e-06 | RMSE=0.5544 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=3263.3542
  - Fit failed: rmse=0.5544 > threshold 2.0

**Iter 3** | λ=6.536e-06 | RMSE=0.5602 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=683.4442
  - Fit failed: rmse=0.5602 > threshold 2.0

**Iter 4** | λ=3.268e-05 | RMSE=0.5615 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=137.9892
  - Fit failed: rmse=0.5615 > threshold 2.0

**Iter 5** | λ=1.634e-04 | RMSE=0.5617 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=27.6504
  - Fit failed: rmse=0.5617 > threshold 2.0

**Iter 6** | λ=8.170e-04 | RMSE=0.5618 | under_regularized | → increase_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=5.5322
  - Fit failed: rmse=0.5618 > threshold 2.0

**Iter 7** | λ=4.085e-03 | RMSE=0.5618 | well_regularized | → increase_lambda
  - Fit failed: rmse=0.5618 > threshold 2.0

**Iter 8** | λ=2.043e-02 | RMSE=0.5618 | well_regularized | → stop_with_failure
  - Fit failed: rmse=0.5618 > threshold 2.0

## Notes

- Completed in 9 iteration(s)
