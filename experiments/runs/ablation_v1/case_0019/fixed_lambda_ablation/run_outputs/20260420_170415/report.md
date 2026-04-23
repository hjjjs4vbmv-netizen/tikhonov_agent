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
- Noise std: 0.1

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `3.9062e-03`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `15.026531`
- Regularisation norm: `5.777126`
- Objective value: `225.927014`

### Estimated Parameters

```
  x[  0] = +32731.1111
  x[  1] = +32731.5007
  x[  2] = +32732.3640
  x[  3] = +32733.6461
  x[  4] = +32735.2544
  x[  5] = +32737.0774
  x[  6] = +32739.0098
  x[  7] = +32740.9696
  x[  8] = +32742.8987
  x[  9] = +32744.7525
  x[ 10] = +32746.4864
  x[ 11] = +32748.0514
  x[ 12] = +32749.4062
  x[ 13] = +32750.5313
  x[ 14] = +32751.4296
  x[ 15] = +32752.1133
  x[ 16] = +32752.5942
  x[ 17] = +32752.8803
  x[ 18] = +32752.9884
  x[ 19] = +32752.9579
  x[ 20] = +32752.8476
  x[ 21] = +32752.7261
  x[ 22] = +32752.6449
  x[ 23] = +32752.6177
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=0.9665 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.0352 is above target=1.5556 (rel_dev=8.66)
  - Fit marginal: rmse=0.9665, rel_err=0.0635

**Iter 1** | λ=5.000e-01 | RMSE=0.9665 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.0351 is above target=1.5556 (rel_dev=8.66)
  - Fit marginal: rmse=0.9665, rel_err=0.0635

**Iter 2** | λ=2.500e-01 | RMSE=0.9665 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.0351 is above target=1.5556 (rel_dev=8.66)
  - Fit marginal: rmse=0.9665, rel_err=0.0635

**Iter 3** | λ=1.250e-01 | RMSE=0.9665 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.0349 is above target=1.5556 (rel_dev=8.66)
  - Fit marginal: rmse=0.9665, rel_err=0.0635

**Iter 4** | λ=6.250e-02 | RMSE=0.9665 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.0347 is above target=1.5556 (rel_dev=8.66)
  - Fit marginal: rmse=0.9665, rel_err=0.0635

**Iter 5** | λ=3.125e-02 | RMSE=0.9664 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.0341 is above target=1.5556 (rel_dev=8.66)
  - Fit marginal: rmse=0.9664, rel_err=0.0635

**Iter 6** | λ=1.562e-02 | RMSE=0.9664 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.0330 is above target=1.5556 (rel_dev=8.66)
  - Under-regularisation suspected: osc=0.00, L1_rough=5.5679
  - Fit marginal: rmse=0.9664, rel_err=0.0635

**Iter 7** | λ=7.812e-03 | RMSE=0.9662 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=15.0309 is above target=1.5556 (rel_dev=8.66)
  - Under-regularisation suspected: osc=0.00, L1_rough=11.1319
  - Fit marginal: rmse=0.9662, rel_err=0.0634

**Iter 8** | λ=3.906e-03 | RMSE=0.9659 | under_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=15.0265 is above target=1.5556 (rel_dev=8.66)
  - Under-regularisation suspected: osc=0.00, L1_rough=22.2481
  - Fit marginal: rmse=0.9659, rel_err=0.0634

## Notes

- Completed in 9 iteration(s)
