# IHCP Inversion Report

**Date:** 2026-04-20 17:21  
**Status:** `weak_pass`  
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
- Lambda: `2.0425e-10`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.519815`
- Regularisation norm: `36576.362366`
- Objective value: `56.820874`

### Estimated Parameters

```
  x[  0] = +28535.5518
  x[  1] = +22796.4648
  x[  2] = +17279.5178
  x[  3] = +16774.4295
  x[  4] = +22082.2025
  x[  5] = +31407.2242
  x[  6] = +43187.9929
  x[  7] = +55760.8881
  x[  8] = +66447.7059
  x[  9] = +72326.3309
  x[ 10] = +71324.1934
  x[ 11] = +63869.0354
  x[ 12] = +52662.2709
  x[ 13] = +40396.0499
  x[ 14] = +28402.3014
  x[ 15] = +17601.1480
  x[ 16] = +9012.6905
  x[ 17] = +3183.3504
  x[ 18] = +189.1650
  x[ 19] = -112.8904
  x[ 20] = +1245.5644
  x[ 21] = +2483.6774
  x[ 22] = +2821.6831
  x[ 23] = +2837.8278
```

## Iteration Trace

**Iter 0** | λ=5.229e-08 | RMSE=0.5000 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=11477.4654
  - Fit marginal: rmse=0.5000, rel_err=0.0957

**Iter 1** | λ=2.614e-08 | RMSE=0.4976 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=19859.3167
  - Fit marginal: rmse=0.4976, rel_err=0.0953

**Iter 2** | λ=1.307e-08 | RMSE=0.4943 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=32891.1928
  - Fit marginal: rmse=0.4943, rel_err=0.0946

**Iter 3** | λ=6.536e-09 | RMSE=0.4907 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=51259.2181
  - Fit marginal: rmse=0.4907, rel_err=0.0939

**Iter 4** | λ=3.268e-09 | RMSE=0.4876 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=71770.3663
  - Fit marginal: rmse=0.4876, rel_err=0.0934

**Iter 5** | λ=1.634e-09 | RMSE=0.4855 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=90172.1317
  - Fit marginal: rmse=0.4855, rel_err=0.0930

**Iter 6** | λ=8.170e-10 | RMSE=0.4844 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=104895.6907
  - Fit marginal: rmse=0.4844, rel_err=0.0928

**Iter 7** | λ=4.085e-10 | RMSE=0.4838 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=121456.4683
  - Fit marginal: rmse=0.4838, rel_err=0.0926

**Iter 8** | λ=2.043e-10 | RMSE=0.4834 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.01, L1_rough=142702.9632
  - Fit marginal: rmse=0.4834, rel_err=0.0926

## Notes

- Completed in 9 iteration(s)
