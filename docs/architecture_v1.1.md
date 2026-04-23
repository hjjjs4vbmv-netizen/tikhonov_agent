# Architecture Notes — v1.1 Packaging Upgrade

## Overview

Version 1.1 adds two extensibility layers on top of the existing validated
Tikhonov agent, without changing the core scientific workflow.

---

## Part A: Input Normalization Layer

### Motivation

The v1.0 parser accepted only one input format: YAML config + CSV observations.
The v1.1 input normalizer adds a thin conversion layer that can accept
multiple input representations and funnel them into one unified schema.

### Design

```
[YAML file]         ──┐
[Python dict]       ──┤  normalize_from_*(...)  →  NormalizedSchema
[Text description]  ──┘           │
                           to_problem_spec()
                                   │
                            ProblemSpec
                         (unchanged downstream)
```

The `NormalizedSchema` dataclass (`src/input_normalizer.py`) makes every
scientific assumption explicit in its field names. This serves as a
human-readable contract between input parsing and the scientific core.

The legacy `parser.py` is still the authoritative path for structured YAML
inputs; `normalize_from_yaml()` delegates to the same logic internally. The
`NormalizedSchema` is a convenience wrapper for the normalization step, not a
replacement for `ProblemSpec`.

### Limitations (intentional)

- Text extraction uses regex patterns, not LLM inference.
- Only patterns listed in `_TEXT_PATTERNS` are recognized.
- For robust natural-language input, plug in a `ProblemParserLLM` adapter
  (the `llm_hooks.py` protocol is unchanged).

---

## Part B: Solver Registry + TSVD

### Motivation

v1.0 had a single hardcoded `solve_single` call in `agent.py`. Adding a second
solver required either modifying the agent loop or duplicating the entire
orchestration.

v1.1 introduces a lightweight registry that:
1. Decouples solver identity from the agent loop.
2. Makes adding a new solver a one-file change (implement the interface,
   call `registry.register()`).
3. Preserves all existing Tikhonov behaviour with zero changes to the
   core solver code.

### Design

```
InversionConfig.solver_name  ──►  SolverRegistry.solve_single(name, …)
                                          │
                              ┌───────────┴───────────┐
                       tikhonov_solver          tsvd_solver
                       (existing, unchanged)    (new)
                              │
                        SolverResult
                       (unchanged structure)
```

The agent loop change is minimal: one line replaces the direct import:

```python
# Before
from src.tikhonov_solver import solve_single
result = solve_single(G, y, config, lam)

# After
from src.solver_registry import get_registry
result = get_registry().solve_single(config.solver_name, G, y, config, lam)
```

### TSVD solver

`tsvd_solver.py` implements truncated SVD inversion:
- Decomposes G = U S V^T
- Keeps singular values ≥ `lam × s_max` (threshold = lambda parameter)
- Same `(G, y, config, lam) → SolverResult` interface as Tikhonov

The `lam` parameter reinterpretation (Tikhonov: regularization weight;
TSVD: truncation fraction) is explicit in the docstring and is the only
semantic change. The verifier, replanner, and reporter are fully reused.

### Verified compatibility

- Existing benchmark/ablation/stress results: **not affected** (solver_name
  defaults to "tikhonov"; all existing YAML configs continue to work).
- TSVD participates fully in the agent loop: verifier checks, replanning
  actions, and reporter output all work with TSVD results.

---

## Files Modified

| File | Change |
|------|--------|
| `src/types.py` | Added `solver_name: str = "tikhonov"` to `InversionConfig` |
| `src/agent.py` | Replaced `tikhonov_solver` direct import with `solver_registry` dispatch |
| `src/planner.py` | Reads `solver_name` from overrides; logs it; passes to config |
| `src/reporter.py` | Includes `solver_name` in JSON summary and Markdown report |

## Files Added

| File | Description |
|------|-------------|
| `src/input_normalizer.py` | Input normalization layer + NormalizedSchema |
| `src/tsvd_solver.py` | Truncated SVD inversion solver |
| `src/solver_registry.py` | Solver registry and dispatch |
| `demos/demo_structured_input.py` | Structured YAML input demo |
| `demos/demo_semistructured_input.py` | Semi-structured text/dict input demo |
| `demos/validate_input_normalizer.py` | Input normalizer validation script |
| `demos/validate_multi_solver.py` | Multi-solver comparison script |

---

## Validation Results

### Input normalizer (validate_input_normalizer.py)

Both `normalize_from_yaml()` and `normalize_from_text()` produce identical
`NormalizedSchema` values for all 9 checked physical fields and both sensor
positions. Both convert to a valid `ProblemSpec`.

### Multi-solver (validate_multi_solver.py, 5 benchmark cases)

| Case | Solver | Decision | Flux RMSE | Notes |
|------|--------|----------|-----------|-------|
| step, low-noise | tikhonov | weak_pass | 4886 | auto lambda |
| step, low-noise | tsvd | weak_pass | 6044 | threshold=0.01 |
| step, med-noise | tikhonov | weak_pass | 1977 | auto lambda |
| step, med-noise | tsvd | weak_pass | 4166 | threshold=0.01 |
| step, high-noise | tikhonov | weak_pass | 1697 | auto lambda |
| step, high-noise | tsvd | weak_pass | 4308 | threshold=0.01 |

Single-iteration comparison; TSVD at default threshold is less accurate than
Tikhonov on flux RMSE, which is expected at `lam=0.01` without threshold tuning.
Both solvers are functional and pass the agent verifier.

---

## Future Work

- TSVD threshold selection: adapt L-curve or GCV for truncation rank selection
- Add Bayesian posterior sampler (MCMC or variational)
- Add Ensemble Kalman Smoother for sequential / streaming data
- Extend normalizer with Excel input and robust LLM parsing
