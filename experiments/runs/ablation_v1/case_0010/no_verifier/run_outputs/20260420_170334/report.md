# IHCP Inversion Report

**Date:** 2026-04-20 17:03  
**Status:** `pass`  
**Iterations:** 1  

## Problem Summary

- Type: `1D_transient_IHCP`
- Inversion target: `boundary_heat_flux`
- Time horizon: 60.00 s (121 steps, dt=0.5000 s)
- Sensors: 2 at positions [0.01, 0.03] m
- Geometry: L=0.05 m, 50 cells
- Material: k=50.0 W/(m·K), rho=7800.0 kg/m³
- Noise std: 0.5

## Final Inversion Configuration

- Parameterisation: `piecewise_constant` (24 parameters)
- Regularisation order: 1
- Lambda: `2.8567e-07`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `7.777607`
- Regularisation norm: `13360.266538`
- Objective value: `111.482444`

### Estimated Parameters

```
  x[  0] = +7924.7286
  x[  1] = +8522.4159
  x[  2] = +9866.0734
  x[  3] = +11800.8304
  x[  4] = +14203.2574
  x[  5] = +16957.5051
  x[  6] = +20068.0046
  x[  7] = +23351.8562
  x[  8] = +26795.3906
  x[  9] = +30399.3666
  x[ 10] = +34129.6270
  x[ 11] = +37966.8480
  x[ 12] = +41761.1936
  x[ 13] = +45403.4620
  x[ 14] = +48836.1472
  x[ 15] = +52121.3907
  x[ 16] = +55285.2059
  x[ 17] = +58255.9642
  x[ 18] = +60882.9507
  x[ 19] = +63108.6918
  x[ 20] = +64791.2909
  x[ 21] = +65866.5368
  x[ 22] = +66442.0091
  x[ 23] = +66643.9564
```

## Iteration Trace

**Iter 0** | λ=2.857e-07 | RMSE=0.5000 | well_regularized | → stop_success
  - skip_verifier=True: verification bypassed (ablation)

## Notes

- Completed in 1 iteration(s)
