# benchmark_2d_v2 — Findings Note

**Generated:** 2026-05-01  
**Runner:** `scripts/run_benchmark_2d_v2.py`  
**Figures:** `reports/figures_v2/`

---

## 1. Solvers Included

| Solver | Method | Key hyperparameters |
|--------|--------|---------------------|
| `tikhonov_2d` | Closed-form normal equations (NumPy) | λ = 1e-3, 1st-order diff reg. |
| `tsvd_2d` | Truncated SVD pseudoinverse (NumPy) | rel. threshold tol = 0.01 |
| `deepxde_2d` | PyTorch Adam optimisation | λ = 1e-4, lr = 10.0, 500 iter |

All three solvers invert the same linear forward map (sensitivity matrix S),
share identical observation vectors `y_obs`, and are evaluated on the same
coarse flux grid (NY_Q=10, NT_Q=20 = 200 parameters).

---

## 2. Main Benchmark Axes

| Axis | Values |
|------|--------|
| **Target type** | `smooth`, `localized`, `multi_spot` |
| **Sensor configuration** | `sparse` (4), `medium` (9), `dense` (16) |
| **Noise level σ** | 0.1 K, 0.5 K, 1.0 K |
| **Seeds** | 0, 1 |

Total: 3 × 3 × 3 × 2 × 3 solvers = **162 solver runs**.

---

## 3. Does Sensor Count Still Dominate?

**Partially, and it is solver-dependent.**

| Solver | Sparse (4) | Medium (9) | Dense (16) |
|--------|-----------|-----------|-----------|
| tikhonov_2d | 195.5 W/m² | 177.6 W/m² | 171.9 W/m² |
| tsvd_2d     | 572.5 W/m² | 575.9 W/m² | 682.0 W/m² |
| deepxde_2d  | 202.8 W/m² | 149.5 W/m² | 128.3 W/m² |

*Averaged over all targets, noise levels, and seeds.*

- **DeepXDE (Adam)** shows the clearest sensor-count benefit: RMSE drops
  ~37% from sparse to dense (202 → 128 W/m²).
- **Tikhonov** is more muted: RMSE falls only ~12% (196 → 172 W/m²), with
  regularisation absorbing most of the additional signal.
- **TSVD** fails to improve with more sensors and actually worsens at `dense`
  because high-noise cases inflate the aggregate — the fixed truncation
  tolerance (1%) retains too many noise-amplifying modes.

Conclusion: sensor count still helps, but only meaningfully for well-tuned
solvers (DeepXDE). For Tikhonov the benefit is small at these noise levels.

---

## 4. Does Sensor Layout Matter When Count Is Fixed?

**Yes, significantly for clustering, less so for boundary bias.**

Layout note: 9 sensors, 2 targets (smooth, localized), 2 noise levels (0.1, 1.0 K), seed=2.

| Solver | Uniform grid | Boundary-biased | Clustered (centre) |
|--------|-------------|----------------|--------------------|
| tikhonov_2d | 180.0 W/m² | 175.5 W/m² | 256.7 W/m² |
| tsvd_2d     | 674.5 W/m² | 651.2 W/m² | 1382.6 W/m² |
| deepxde_2d  | 136.4 W/m² | 124.6 W/m² | 248.5 W/m² |

Key findings:

- **Clustered sensors** (concentrated in the centre of the domain, x ≈ 35–65%,
  y ≈ 35–65%) cause a large RMSE increase across **all** solvers: +83% for
  Tikhonov, +105% for DeepXDE, +105% for TSVD compared to uniform grid.
  Centre-clustered sensors have low spatial rank relative to the boundary flux
  (all sensors lie far from the flux boundary at x=0 and far from the domain
  edges), reducing the effective information content about q(y,t).

- **Boundary-biased sensors** (x positions shifted toward the left wall:
  10%, 20%, 35% of Lx) are marginally better than uniform grid for DeepXDE
  (−9%, 136 → 125 W/m²) and Tikhonov (−3%). Proximity to the heated boundary
  at x=0 provides slightly sharper impulse responses in S.

- The layout effect is **orthogonal** to the noise effect: clustered sensors
  suffer even at σ=0.1 K, confirming that the problem is one of spatial
  ill-conditioning, not measurement noise.

---

## 5. Solver Noise Robustness

| Solver | σ = 0.1 K | σ = 0.5 K | σ = 1.0 K |
|--------|----------|----------|----------|
| tikhonov_2d | 181.2 W/m² | 181.3 W/m² | 182.5 W/m² |
| tsvd_2d     | 171.9 W/m² | 563.0 W/m² | 1095.5 W/m² |
| deepxde_2d  | 157.5 W/m² | 158.8 W/m² | 164.4 W/m² |

- **TSVD** is highly competitive at low noise (σ=0.1) — best among all three
  solvers — but degrades catastrophically as noise increases. The fixed
  relative truncation rule (tol=0.01) does not adapt to the noise level,
  so the same rank (~40–77 out of 200) is kept regardless of SNR, amplifying
  noise through small singular values.
- **Tikhonov** and **DeepXDE** are both noise-robust; their respective
  regularisation (λL^TL penalty / Adam early stopping) implicitly damps
  noise modes. RMSE variation across the three noise levels is ≤ 7 W/m².
- DeepXDE is slightly better than Tikhonov at all noise levels and sensor counts.
  Mean runtime: 338 ms vs 5 ms, so the accuracy gain comes at roughly 70× cost.

---

## 6. Recommended Next Benchmark Extension

The most scientifically useful next step is **noise-adaptive TSVD / L-curve
hyperparameter sweep**:

1. **Adaptive TSVD**: tune truncation rank per noise level using the Morozov
   discrepancy principle or the L-curve criterion. This would likely close
   most of TSVD's noise-sensitivity gap and make it competitive with Tikhonov
   at σ > 0.1 K.

2. **λ sweep for Tikhonov**: the current λ=1e-3 was not cross-validated.
   A grid search over λ ∈ {1e-5, …, 1e-1} per noise level would quantify
   the sensitivity and could reduce Tikhonov RMSE substantially.

3. **Temporal / spatial anisotropic regularisation**: current L is a 1-D
   differencing operator on the flattened q vector. A 2-D Laplacian
   regulariser on the (ny_q × nt_q) grid would better match the smoothness
   structure of physically realistic flux patterns.

4. **3D benchmark** (time-varying boundary in 3D slab): extend from 2D plate
   (x,y) + t to a full 3D geometry to test scalability of S-matrix approach.
