# IHCP Inversion Report

**Date:** 2026-04-14 20:53  
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
- Regularisation order: 1
- Lambda: `3.9062e-03`
- Lambda strategy: `fixed`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `18.792281`
- Regularisation norm: `4.426006`
- Objective value: `353.226343`

### Estimated Parameters

```
  x[  0] = +41593.5294
  x[  1] = +41593.2994
  x[  2] = +41592.7548
  x[  3] = +41591.9091
  x[  4] = +41590.7939
  x[  5] = +41589.4668
  x[  6] = +41588.0161
  x[  7] = +41586.5426
  x[  8] = +41585.1264
  x[  9] = +41583.8306
  x[ 10] = +41582.6933
  x[ 11] = +41581.7056
  x[ 12] = +41580.8256
  x[ 13] = +41580.0058
  x[ 14] = +41579.2086
  x[ 15] = +41578.3940
  x[ 16] = +41577.5699
  x[ 17] = +41576.7636
  x[ 18] = +41576.0282
  x[ 19] = +41575.4228
  x[ 20] = +41574.9663
  x[ 21] = +41574.6814
  x[ 22] = +41574.5486
  x[ 23] = +41574.5133
```

## Iteration Trace

**Iter 0** | λ=1.000e+00 | RMSE=1.2083 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=18.7963 is above target=15.5563 (rel_dev=0.21)
  - Fit marginal: rmse=1.2083, rel_err=0.0597

**Iter 1** | λ=5.000e-01 | RMSE=1.2083 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=18.7963 is above target=15.5563 (rel_dev=0.21)
  - Fit marginal: rmse=1.2083, rel_err=0.0597

**Iter 2** | λ=2.500e-01 | RMSE=1.2083 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=18.7963 is above target=15.5563 (rel_dev=0.21)
  - Fit marginal: rmse=1.2083, rel_err=0.0597

**Iter 3** | λ=1.250e-01 | RMSE=1.2083 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=18.7962 is above target=15.5563 (rel_dev=0.21)
  - Fit marginal: rmse=1.2083, rel_err=0.0597

**Iter 4** | λ=6.250e-02 | RMSE=1.2083 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=18.7961 is above target=15.5563 (rel_dev=0.21)
  - Fit marginal: rmse=1.2083, rel_err=0.0597

**Iter 5** | λ=3.125e-02 | RMSE=1.2082 | well_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=18.7958 is above target=15.5563 (rel_dev=0.21)
  - Fit marginal: rmse=1.2082, rel_err=0.0597

**Iter 6** | λ=1.562e-02 | RMSE=1.2082 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=18.7953 is above target=15.5563 (rel_dev=0.21)
  - Under-regularisation suspected: osc=0.00, L1_rough=4.7594
  - Fit marginal: rmse=1.2082, rel_err=0.0597

**Iter 7** | λ=7.812e-03 | RMSE=1.2081 | under_regularized | → decrease_lambda
  - Discrepancy principle: ||r||=18.7943 is above target=15.5563 (rel_dev=0.21)
  - Under-regularisation suspected: osc=0.00, L1_rough=9.5152
  - Fit marginal: rmse=1.2081, rel_err=0.0597

**Iter 8** | λ=3.906e-03 | RMSE=1.2080 | under_regularized | → stop_with_failure
  - Discrepancy principle: ||r||=18.7923 is above target=15.5563 (rel_dev=0.21)
  - Under-regularisation suspected: osc=0.00, L1_rough=19.0161
  - Fit marginal: rmse=1.2080, rel_err=0.0597

## Notes

- Completed in 9 iteration(s)
