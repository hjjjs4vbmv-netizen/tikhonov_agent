# tikhonov_agent

**A scientific workflow / agent prototype for thermal inverse PDE problems —
validated on 1D transient boundary heat flux reconstruction (IHCP).**

*Version 1.1 — packaging upgrade: Input Normalizer + Solver Registry*

---

## What This Is

`tikhonov_agent` is a research prototype of a **scientific agent system for
inverse heat conduction problems (IHCP)**.

It implements a deterministic, rule-based agent that orchestrates:

```
Input → Input Normalizer → Parser → Planner → Solver Registry
      ↓
      Solver (Tikhonov | TSVD | …)
      ↓
      Verifier → Replanner → Reporter
```

The system is an *agent* in the precise sense: it autonomously plans, acts,
evaluates its own output, and revises its strategy — without requiring a human
in every iteration and without requiring an LLM.

### Current validated use case

**1D transient IHCP — boundary heat flux reconstruction**

Given temperature time-series measured at one or more internal sensors in a
1D rod, recover the unknown time-varying heat flux applied at the left boundary.

This is the only use case that has been fully validated with the included
benchmark / ablation / stress experiments.  The rest of this document discusses
extensibility, but the validated scientific scope remains 1D transient IHCP.

---

## Architecture

```
tikhonov_agent/
├── main.py                      CLI entry point
├── src/
│   ├── types.py                 All dataclasses (ProblemSpec, InversionConfig, …)
│   │
│   ├── input_normalizer.py  ★   Input normalization layer (v1.1 new)
│   │                            YAML / dict / text → NormalizedSchema → ProblemSpec
│   ├── parser.py                YAML + CSV input → ProblemSpec (existing)
│   │
│   ├── forward_model.py         1D FD heat conduction forward solver
│   ├── sensitivity.py           Response matrix G construction (unit-pulse method)
│   ├── regularization.py        L matrix construction (orders 0, 1, 2)
│   ├── lambda_selector.py       L-curve, GCV, discrepancy, fixed, grid strategies
│   │
│   ├── solver_registry.py   ★   Solver registry & dispatch layer (v1.1 new)
│   ├── tikhonov_solver.py       Tikhonov normal-equation solver (existing)
│   ├── tsvd_solver.py       ★   Truncated SVD solver (v1.1 new)
│   │
│   ├── planner.py               Rule-based initial plan generator
│   ├── verifier.py              Multi-criteria physical + statistical verification
│   ├── replanner.py             Rule-based plan revision from verification result
│   ├── agent.py                 Main orchestration loop (IHCPAgent)
│   ├── reporter.py              JSON + Markdown report writer
│   ├── llm_hooks.py             Optional LLM adapter protocols + Qwen placeholder
│   ├── logging_utils.py         Structured logging
│   └── utils.py                 Serialisation, timing, array helpers
│
├── configs/
│   ├── default.yaml             Default problem configuration
│   └── example_case.yaml        Demo case (step heat flux on steel rod)
├── data/
│   └── demo_temperature.csv     Synthetic temperature observations
├── demos/                   ★   (v1.1 new)
│   ├── demo_structured_input.py     YAML → NormalizedSchema → ProblemSpec demo
│   ├── demo_semistructured_input.py Text / dict → NormalizedSchema demo
│   ├── validate_input_normalizer.py Input normalizer validation script
│   └── validate_multi_solver.py     Tikhonov vs TSVD comparison script
└── tests/
    ├── test_regularization.py
    ├── test_lambda_selector.py
    ├── test_solver.py
    ├── test_verifier.py
    ├── test_replanner.py
    └── test_agent_loop.py
```

★ = new in v1.1

### Data flow (v1.1)

```
[Structured YAML/CSV]     ──┐
[Python dict]             ──┤  Input Normalizer  →  NormalizedSchema
[Semi-structured text]    ──┘        │
                                      ↓
                               ProblemSpec
                                      │
                               Planner  (reads solver_name from config)
                                      │
                               InversionConfig  (includes solver_name)
                                      │
                               Solver Registry
                              ┌───────┴──────────┐
                       tikhonov_solver      tsvd_solver
                              └───────┬──────────┘
                               SolverResult
                                      │
                          Verifier → Replanner (loop)
                                      │
                               Reporter  (includes solver_name in output)
```

---

## v1.1 Packaging Upgrade: What's New

### Part A — Input Normalizer

`src/input_normalizer.py` adds a normalization layer in front of the parser.

**`NormalizedSchema`** is a unified internal schema with explicit fields:

| Field | Description |
|-------|-------------|
| `pde_family` | "parabolic" (heat equation) |
| `problem_type` | "1D_transient_IHCP" |
| `unknown_target` | "boundary_heat_flux" |
| `rod_length_m`, `n_cells` | 1D geometry |
| `density_kg_m3`, `specific_heat_J_kgK`, `conductivity_W_mK` | Material |
| `initial_temperature_K` | Uniform T(x,0) |
| `bc_right_type`, `bc_right_value` | Right boundary condition |
| `time_start_s`, `time_end_s`, `time_n_steps` | Time discretisation |
| `sensor_positions_m` | Sensor x-positions |
| `observations_file` / `observations_array` | Measurement data |
| `noise_std_K` | Measurement noise (for discrepancy principle) |
| `solver_preferences` | Optional planner overrides |

Three entry points accept different input formats:

```python
from src.input_normalizer import (
    normalize_from_yaml,   # existing YAML config (primary path)
    normalize_from_dict,   # Python dict (API / partial data)
    normalize_from_text,   # semi-structured text (lightweight extraction)
)
schema = normalize_from_yaml("configs/example_case.yaml")
spec   = schema.to_problem_spec()   # → ProblemSpec for the agent
```

Validation: both YAML and text extraction paths produce identical `ProblemSpec`
objects (confirmed by `demos/validate_input_normalizer.py`).

### Part B — Solver Registry + TSVD

**`src/solver_registry.py`** provides a lightweight registry abstraction:

```python
from src.solver_registry import get_registry
registry = get_registry()
print(registry.available())  # ['tikhonov', 'tsvd']
result = registry.solve_single("tsvd", G, y, config, lam)
```

**`src/tsvd_solver.py`** implements Truncated SVD inversion:

- Decomposes G = U S V^T via full SVD
- Keeps only singular values ≥ `lam × s_max` (truncation threshold)
- `lam → 0`: keep all (less regularization); `lam → 1`: keep few (more)
- Same `(G, y, config, lam) → SolverResult` interface as Tikhonov

**To select a solver**, add `solver_name` to the YAML planner section:

```yaml
planner:
  solver_name: tsvd          # or "tikhonov" (default)
  lambda_strategy: fixed
  lambda_value: 0.01         # TSVD truncation threshold
```

**Multi-solver comparison** (from `demos/outputs/multi_solver_comparison.csv`):

| Case | Label | Solver | Decision | Flux RMSE | Replay RMSE | Runtime |
|------|-------|--------|----------|-----------|-------------|---------|
| case_0001 | step, low-noise | tikhonov | weak_pass | 4886 | 0.100 | 0.07s |
| case_0001 | step, low-noise | tsvd | weak_pass | 6044 | 0.086 | 0.05s |
| case_0007 | step, med-noise | tikhonov | weak_pass | 1977 | 0.099 | 0.06s |
| case_0007 | step, med-noise | tsvd | weak_pass | 4166 | 0.085 | 0.05s |
| case_0013 | step, high-noise | tikhonov | weak_pass | 1697 | 0.101 | 0.06s |
| case_0013 | step, high-noise | tsvd | weak_pass | 4308 | 0.085 | 0.05s |

Notes: single-iteration comparison; TSVD uses fixed threshold 0.01.
Tikhonov outperforms TSVD on flux RMSE in all cases at default settings.
TSVD requires threshold tuning and/or multi-iteration agent loop for best results.
Both solvers produce `weak_pass` decisions and participate fully in the agent workflow.

---

## Quick Start

### Install

```bash
pip install -e .
# or for development:
pip install -e ".[dev]"
```

Requires Python ≥ 3.11, numpy, scipy, pyyaml.

### Run the demo

```bash
cd tikhonov_agent/
python main.py --config configs/example_case.yaml
```

### Run with TSVD solver

Add to your YAML config's `planner:` section:

```yaml
planner:
  solver_name: tsvd
  lambda_strategy: fixed
  lambda_value: 0.005
```

Or pass as CLI override via `--planner-overrides` (if supported by your main.py).

### Run demos

```bash
cd tikhonov_agent/

# Part A demos
python demos/demo_structured_input.py
python demos/demo_semistructured_input.py
python demos/validate_input_normalizer.py

# Part B demo
python demos/validate_multi_solver.py
```

### Run tests

```bash
pytest tests/ -q
```

---

## Scope and Limitations

### Current validated scope

| Aspect | Status |
|--------|--------|
| Problem type | **1D transient IHCP** (heat flux at left boundary) |
| Forward model | 1D finite-difference implicit scheme |
| Primary solver | Tikhonov regularization (fully validated) |
| Secondary solver | TSVD (new; functional, not yet benchmarked at full scale) |
| Benchmarked cases | 30 synthetic cases (step/ramp/pulse flux × 3 noise levels × 2 seeds) |
| Ablation study | 7 variants completed |
| Stress tests | 6 scenarios (high noise, few sensors, low time resolution, etc.) |

### What this system is NOT (yet)

| Out of scope (current version) | Planned? |
|--------------------------------|----------|
| 2D / 3D geometries | Future |
| Temperature-dependent material properties | Future |
| Multiple coupled unknowns | Future |
| Bayesian / MCMC / ABC inference | Planned (see below) |
| Ensemble Kalman Smoothing (EnKS) | Planned |
| Physics-Informed Neural Networks (PINN) | Future research |
| Reinforcement learning orchestration | Future research |
| LLM-driven planning | Optional stub only |
| Arbitrary natural-language input | Requires LLM hook |

---

## Future Solver Extensions (Roadmap)

The solver registry is designed for extension. The following solver families
are **planned for future work** but are **not implemented** in this version:

| Solver family | Approach | Notes |
|---------------|----------|-------|
| Bayesian inference | MCMC or variational posterior | Quantifies uncertainty; requires prior specification |
| ABC (Approximate Bayesian Computation) | Likelihood-free inference | Suitable for non-Gaussian noise |
| Ensemble Kalman Smoothing (EnKS) | Sequential data assimilation | Real-time / streaming data |
| PINN / DeepONet | Neural surrogate | Requires training data |

To add a new solver, implement the interface:

```python
# src/my_solver.py
def solve_single(G, y, config, lam) -> SolverResult: ...
def solve_grid(G, y, config, lambda_grid) -> list[SolverResult]: ...

# Register it:
from src.solver_registry import get_registry
get_registry().register("my_solver", my_solver_module)
```

---

## Experiment Pipeline (Benchmarking)

> **Note:** The existing benchmark/ablation/stress results are not affected by
> the v1.1 changes. All prior outputs remain valid.

```bash
# Generate synthetic cases
python experiments/generate_cases.py \
    --config experiments/configs/benchmark_v1.yaml

# Run all four variants
python experiments/run_benchmark.py \
    --config experiments/configs/benchmark_v1.yaml \
    --variant all

# Aggregate summary tables
python experiments/analyze_results.py \
    --input experiments/runs/benchmark_v1/results_raw.csv
```

---

## Configuration

```yaml
time:
  start: 0.0
  end:   60.0
  n_steps: 121

geometry:
  length:  0.05     # [m]
  n_cells: 60

material:
  density:       7800.0
  specific_heat:  500.0
  conductivity:    50.0

noise_std: 0.3      # enables discrepancy principle

planner:
  solver_name: tikhonov    # "tikhonov" or "tsvd"
  reg_order: 1
  max_retries: 8
  physical_bounds: [-5.0e5, 5.0e5]
```

---

## Optional Qwen-2.5-3B LLM Hook

The system runs fully without any LLM.  An optional Qwen adapter is provided
for parsing free-form descriptions, explaining verification results, and
drafting narrative report sections.

**The LLM never makes scientific decisions.**

```bash
pip install -e ".[llm]"
python main.py --config configs/example_case.yaml --use-qwen --qwen-device cuda
```

---

## Why Is This Called a "Scientific Agent"?

The term *agent* refers to the **agentic workflow pattern**, not an LLM chatbot:

1. **Autonomy:** the system decides whether to accept a result or retry.
2. **Planning:** the Planner generates an inspectable inversion configuration.
3. **Tool use:** the Solver Registry is a "toolbox" dispatched by the orchestrator.
4. **Self-evaluation:** the Verifier applies physical + statistical checks.
5. **Failure recovery:** the Replanner modifies the plan and re-invokes the Solver.
6. **Decision trace:** every iteration is recorded for reproducibility.

This is the same *plan → act → observe → revise* loop found in LLM agents, but
implemented deterministically with domain-specific rules.

---

## License

MIT
