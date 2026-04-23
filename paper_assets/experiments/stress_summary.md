# Stress v1 — Key Results Summary

**Source:** `experiments/runs/stress_v1/`  
**Cases:** 32 cases across 6 stress scenarios  
**Variant:** full_agent only (the validated configuration)

---

## Stress scenarios and case counts

| Scenario | n_cases | Notes |
|----------|---------|-------|
| `high_noise` | 8 | σ = 2.0 K and 5.0 K (10× to 50× benchmark noise) |
| `few_sensors` | 6 | Only 1 sensor (vs 2 in benchmark) |
| `distant_sensors` | 4 | Sensors at 0.04 m and 0.045 m (far from heated face) |
| `low_time_resolution` | 6 | 31 time steps (vs 121 in benchmark) |
| `high_dimension` | 4 | 50 inversion parameters (vs ≈24 typical) |
| `wrong_noise_estimate` | 4 | noise_std underestimated by 10× |

---

## Aggregate results (full_agent, 32 cases)

| Metric | Value |
|--------|-------|
| Success rate | 75% (24/32) |
| Failure rate | 25% (8/32) |
| Flux RMSE mean [W/m²] | 11,638 ± 7,183 |
| Replay RMSE mean [K] | 1.25 ± 1.52 |
| Iterations mean | 5.06 ± 3.98 |
| Runtime mean [s] | 0.26 ± 0.22 |

*(Vs benchmark full_agent: 100% success, RMSE ≈ 5,491, 1.93 iters)*

---

## Main findings
1. **Full agent degrades gracefully under stress:** 75% success vs 100% on benchmark — not catastrophic failure.
2. **High noise is the hardest scenario:** σ=5.0 K cases mostly fail; σ=2.0 K mixed.
3. **Few sensors and distant sensors** reduce accuracy but the agent still converges in most cases.
4. **Wrong noise estimate** (factor 10×) misleads the discrepancy principle but recovery is partial.
5. **Agent iteration count increases substantially** under stress (5.06 mean vs 1.93) — the replanner engages more.

---

## Figure assets available
- `experiments/runs/stress_v1/figures/stress_success_barplot.png`
- `experiments/runs/stress_v1/figures/stress_flux_rmse_boxplot.png`
- `experiments/runs/stress_v1/figures/stress_oscillation_score_boxplot.png`
