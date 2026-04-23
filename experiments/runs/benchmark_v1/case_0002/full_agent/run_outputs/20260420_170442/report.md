# IHCP Inversion Report

**Date:** 2026-04-20 17:04  
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
- Regularisation order: 1
- Lambda: `1.4151e-09`
- Lambda strategy: `discrepancy`
- Physical bounds: (-500000.0, 500000.0)

## Solver Results

- Status: `success`
- Residual norm: `1.565926`
- Regularisation norm: `30536.195798`
- Objective value: `3.771627`

### Estimated Parameters

```
  x[  0] = +360.0771
  x[  1] = -53.1010
  x[  2] = +523.4062
  x[  3] = +39.5578
  x[  4] = -1527.7460
  x[  5] = -2102.4646
  x[  6] = +9731.3318
  x[  7] = +32396.4248
  x[  8] = +48392.0740
  x[  9] = +51708.9038
  x[ 10] = +50060.1393
  x[ 11] = +50069.7692
  x[ 12] = +50627.6996
  x[ 13] = +50944.3561
  x[ 14] = +50003.0625
  x[ 15] = +49356.1039
  x[ 16] = +49637.7835
  x[ 17] = +50332.3493
  x[ 18] = +49779.8298
  x[ 19] = +50327.1306
  x[ 20] = +50437.3559
  x[ 21] = +49274.3196
  x[ 22] = +49285.5211
  x[ 23] = +50452.4919
```

## Iteration Trace

**Iter 0** | λ=1.415e-09 | RMSE=0.1007 | under_regularized | → stop_success_weak_pass
  - Under-regularisation suspected: osc=0.01, L1_rough=66075.6576
  - Fit is good but regularisation balance is uncertain

## Notes

- Completed in 1 iteration(s)
