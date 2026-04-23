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
- Lambda: `5.4188e-05`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.090170`
- Regularisation norm: `4.478857`
- Objective value: `50.271603`

### Estimated Parameters

```
  x[  0] = +36486.0790
  x[  1] = +36486.4894
  x[  2] = +36487.3545
  x[  3] = +36488.5908
  x[  4] = +36490.1011
  x[  5] = +36491.7788
  x[  6] = +36493.5135
  x[  7] = +36495.2012
  x[  8] = +36496.7520
  x[  9] = +36498.0968
  x[ 10] = +36499.1958
  x[ 11] = +36500.0368
  x[ 12] = +36500.6282
  x[ 13] = +36500.9968
  x[ 14] = +36501.1851
  x[ 15] = +36501.2429
  x[ 16] = +36501.2209
  x[ 17] = +36501.1645
  x[ 18] = +36501.1073
  x[ 19] = +36501.0690
  x[ 20] = +36501.0516
  x[ 21] = +36501.0462
  x[ 22] = +36501.0451
  x[ 23] = +36501.0450
```

## Iteration Trace

**Iter 0** | λ=1.387e-02 | RMSE=0.4558 | well_regularized | → decrease_lambda
  - Fit marginal: rmse=0.4558, rel_err=0.0914

**Iter 1** | λ=6.936e-03 | RMSE=0.4558 | well_regularized | → decrease_lambda
  - Fit marginal: rmse=0.4558, rel_err=0.0914

**Iter 2** | λ=3.468e-03 | RMSE=0.4558 | well_regularized | → decrease_lambda
  - Fit marginal: rmse=0.4558, rel_err=0.0914

**Iter 3** | λ=1.734e-03 | RMSE=0.4558 | well_regularized | → decrease_lambda
  - Fit marginal: rmse=0.4558, rel_err=0.0914

**Iter 4** | λ=8.670e-04 | RMSE=0.4558 | well_regularized | → decrease_lambda
  - Fit marginal: rmse=0.4558, rel_err=0.0914

**Iter 5** | λ=4.335e-04 | RMSE=0.4558 | well_regularized | → decrease_lambda
  - Fit marginal: rmse=0.4558, rel_err=0.0914

**Iter 6** | λ=2.168e-04 | RMSE=0.4558 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=3.8442
  - Fit marginal: rmse=0.4558, rel_err=0.0914

**Iter 7** | λ=1.084e-04 | RMSE=0.4558 | under_regularized | → decrease_lambda
  - Under-regularisation suspected: osc=0.00, L1_rough=7.6859
  - Fit marginal: rmse=0.4558, rel_err=0.0914

**Iter 8** | λ=5.419e-05 | RMSE=0.4558 | under_regularized | → stop_with_failure
  - Under-regularisation suspected: osc=0.00, L1_rough=15.3618
  - Fit marginal: rmse=0.4558, rel_err=0.0914

## Notes

- Completed in 9 iteration(s)
