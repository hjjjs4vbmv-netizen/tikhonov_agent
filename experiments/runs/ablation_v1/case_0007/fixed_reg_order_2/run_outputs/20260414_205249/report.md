# IHCP Inversion Report

**Date:** 2026-04-14 20:52  
**Status:** `weak_pass`  
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
- Regularisation order: 2
- Lambda: `7.5787e-02`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.384277`
- Regularisation norm: `0.006039`
- Objective value: `1.916224`

### Estimated Parameters

```
  x[  0] = +1406.4571
  x[  1] = +4727.7657
  x[  2] = +8049.0743
  x[  3] = +11370.3830
  x[  4] = +14691.6918
  x[  5] = +18013.0010
  x[  6] = +21334.3109
  x[  7] = +24655.6216
  x[  8] = +27976.9335
  x[  9] = +31298.2468
  x[ 10] = +34619.5620
  x[ 11] = +37940.8791
  x[ 12] = +41262.1982
  x[ 13] = +44583.5194
  x[ 14] = +47904.8426
  x[ 15] = +51226.1677
  x[ 16] = +54547.4946
  x[ 17] = +57868.8229
  x[ 18] = +61190.1526
  x[ 19] = +64511.4832
  x[ 20] = +67832.8145
  x[ 21] = +71154.1462
  x[ 22] = +74475.4780
  x[ 23] = +77796.8098
```

## Iteration Trace

**Iter 0** | λ=7.579e-02 | RMSE=0.0890 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.00, L1_rough=76390.3527
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
