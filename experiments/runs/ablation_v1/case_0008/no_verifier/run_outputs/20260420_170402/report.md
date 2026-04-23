# IHCP Inversion Report

**Date:** 2026-04-20 17:04  
**Status:** `pass`  
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
- Regularisation order: 1
- Lambda: `2.3503e-08`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.563710`
- Regularisation norm: `14810.205657`
- Objective value: `7.600347`

### Estimated Parameters

```
  x[  0] = +4052.6394
  x[  1] = +5252.9659
  x[  2] = +7734.3150
  x[  3] = +10875.0854
  x[  4] = +14262.5537
  x[  5] = +17643.8105
  x[  6] = +21147.3112
  x[  7] = +24478.7081
  x[  8] = +27743.2442
  x[  9] = +31061.1123
  x[ 10] = +34466.3232
  x[ 11] = +38046.0036
  x[ 12] = +41584.9004
  x[ 13] = +44954.5121
  x[ 14] = +48117.7465
  x[ 15] = +51305.0880
  x[ 16] = +54676.7947
  x[ 17] = +58202.8562
  x[ 18] = +61689.7492
  x[ 19] = +65133.8756
  x[ 20] = +68203.1532
  x[ 21] = +70556.6249
  x[ 22] = +72082.1209
  x[ 23] = +72692.5702
```

## Iteration Trace

**Iter 0** | λ=2.350e-08 | RMSE=0.1005 | well_regularized | → stop_success
  - skip_verifier=True: verification bypassed (ablation)

## Notes

- Completed in 1 iteration(s)
