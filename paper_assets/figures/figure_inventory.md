# Figure Inventory and Paper Placement

## Available figures

### benchmark_v1/figures/ (8 PNGs)

| File | Content | Paper placement |
|------|---------|-----------------|
| `success_failure_barplot.png` | Acceptance rate by variant (fixed/auto/verifier/full_agent) | **Main paper** — core result figure |
| `flux_error_by_variant_boxplot.png` | Flux RMSE distribution by variant | **Main paper** — quantitative comparison |
| `qualitative_flux_reconstruction_examples.png` | Side-by-side q(t) reconstruction examples | **Main paper** — illustrative |
| `replay_error_by_noise_lineplot.png` | Replay RMSE vs noise level by variant | **Main paper** or appendix — shows noise sensitivity |
| `replanning_action_histogram.png` | Histogram of replanning actions taken | Appendix — operational detail |
| `lambda_vs_error_scatter.png` | Lambda vs flux error scatter | Appendix — regularization analysis |
| `qualitative_temperature_replay_examples.png` | Temperature fit examples | Appendix — supplementary |
| `ablation_comparison_barplot.png` | Duplicate from ablation (same file name) | Do not use from benchmark dir |

### ablation_v1/figures/ (8 PNGs)

| File | Content | Paper placement |
|------|---------|-----------------|
| `ablation_comparison_barplot.png` | Success/failure by ablation variant | **Main paper** — ablation result |
| `flux_error_by_variant_boxplot.png` | Flux RMSE by ablation variant | **Main paper** — ablation RMSE |
| `success_failure_barplot.png` | Acceptance rate by ablation variant | Appendix (if ablation_comparison_barplot covers it) |
| `qualitative_flux_reconstruction_examples.png` | q(t) examples from ablation | Appendix |
| `replanning_action_histogram.png` | Replanning distribution under ablation | Appendix |
| `replay_error_by_noise_lineplot.png` | Replay RMSE vs noise for ablation variants | Appendix |
| `lambda_vs_error_scatter.png` | Lambda behavior in ablation | Appendix |
| `qualitative_temperature_replay_examples.png` | Temperature fit examples | Appendix |

### stress_v1/figures/ (3 PNGs)

| File | Content | Paper placement |
|------|---------|-----------------|
| `stress_success_barplot.png` | Success rate by stress scenario | **Main paper** — stress result |
| `stress_flux_rmse_boxplot.png` | Flux RMSE by stress scenario | Main paper or appendix |
| `stress_oscillation_score_boxplot.png` | Oscillation score under stress | Appendix |

---

## Recommended main-paper figure set (4–6 figures)

1. **Architecture diagram** (from `architecture_diagram.md` or Mermaid render) — system overview
2. **benchmark success_failure_barplot** — core result: full_agent achieves 100% vs 86.7%/10%
3. **benchmark flux_error_by_variant_boxplot** — RMSE comparison across variants
4. **ablation_comparison_barplot** — ablation: which components matter
5. **stress_success_barplot** — stress: graceful degradation
6. **qualitative_flux_reconstruction_examples** (benchmark) — one illustrative example

## Appendix figures

- All remaining benchmark and ablation figures
- stress_flux_rmse_boxplot

### multi_solver_pilot/figures/ (3 PNGs) — generated from pilot data

| File | Content | Paper placement |
|------|---------|-----------------|
| `multi_solver_flux_rmse_grouped.png` | Grouped bars: Flux RMSE by family × noise level, Tikhonov vs TSVD | **Main paper** — multi-solver result (Extensibility section) |
| `multi_solver_rmse_vs_noise.png` | Line plot: RMSE vs noise level per family, both solvers | Main paper or appendix — noise sensitivity |
| `multi_solver_scatter.png` | Per-case scatter: Tikhonov RMSE vs TSVD RMSE, diagonal = equal | Appendix — per-case comparison |

*(Copies also in `paper_assets/figures/`.)*

---

## Missing figures to generate (future work)

- Input normalization round-trip diagram
- Per-case flux profile gallery for the paper supplement
