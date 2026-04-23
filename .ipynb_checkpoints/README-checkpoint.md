# tikhonov_agent

**A rule-based scientific agent for 1D transient inverse heat conduction problems (IHCP) — Version 1 prototype.**

---

## What This Is

`tikhonov_agent` is the first executable prototype in a research programme on
**scientific agent systems for inverse heat conduction problems**.

It implements a deterministic, rule-based agent that orchestrates:

```
Input → Parser → Planner → Solver → Verifier → Replanner → Reporter
```

using **Tikhonov regularisation** as the core inversion method.

The system is an *agent* in the precise sense: it autonomously plans, acts,
evaluates its own output, and revises its strategy — without requiring a human
in every iteration and without requiring an LLM.

---

## What Problem It Solves

**Problem:** Given temperature time-series measured at one or more internal
sensors in a 1D rod, reconstruct the unknown time-varying heat flux applied at
the left boundary.

This is a classical **1D transient inverse heat conduction problem (IHCP)** — an
ill-posed problem requiring regularisation.

---

## What It Does NOT Solve (Intentional Scope Limits)

| Out of scope (Version 1) | Status |
|--------------------------|--------|
| 2D / 3D geometries | not implemented |
| Temperature-dependent material properties | not implemented |
| Multiple coupled unknowns | not implemented |
| Bayesian / MCMC / ABC inference | not implemented |
| Physics-Informed Neural Networks (PINN) | not implemented |
| Neural operators / DeepONet | not implemented |
| Reinforcement learning orchestration | not implemented |
| Multi-agent collaboration | not implemented |
| LLM-driven planning | not implemented (optional only) |

These are planned extensions in the research roadmap, not missing features.

---

## Why Is This Called an "Agent" Without an LLM?

The term *agent* here refers to the **agentic workflow pattern**, not to an LLM
chatbot:

1. **Autonomy:** the system decides whether to accept a result or retry.
2. **Planning:** the Planner generates an explicit, inspectable inversion
   configuration from problem features.
3. **Tool use:** the Solver is a "tool" called by the orchestrator.
4. **Self-evaluation:** the Verifier applies multiple physical and statistical
   checks emulating expert review.
5. **Failure recovery:** the Replanner modifies the plan and re-invokes the
   Solver without human intervention.
6. **Decision trace:** every iteration is recorded in the AgentTrace for
   reproducibility and audit.

This is the same *plan → act → observe → revise* loop found in LLM agents, but
implemented deterministically with domain-specific rules.

---

## Architecture

```
tikhonov_agent/
├── main.py                  CLI entry point
├── src/
│   ├── types.py             All dataclasses (ProblemSpec, InversionConfig, …)
│   ├── parser.py            YAML + CSV input → ProblemSpec
│   ├── forward_model.py     1D FD heat conduction forward solver
│   ├── sensitivity.py       Response matrix G construction (unit-pulse method)
│   ├── regularization.py    L matrix construction (orders 0, 1, 2)
│   ├── lambda_selector.py   L-curve, GCV, discrepancy, fixed, grid strategies
│   ├── tikhonov_solver.py   Tikhonov normal-equation solver
│   ├── planner.py           Rule-based initial plan generator
│   ├── verifier.py          Multi-criteria physical + statistical verification
│   ├── replanner.py         Rule-based plan revision from verification result
│   ├── agent.py             Main orchestration loop (IHCPAgent)
│   ├── reporter.py          JSON + Markdown report writer
│   ├── llm_hooks.py         Optional LLM adapter protocols + Qwen placeholder
│   ├── logging_utils.py     Structured logging
│   └── utils.py             Serialisation, timing, array helpers
├── configs/
│   ├── default.yaml         Default problem configuration
│   └── example_case.yaml    Demo case (step heat flux on steel rod)
├── data/
│   └── demo_temperature.csv Synthetic temperature observations
└── tests/
    ├── test_regularization.py
    ├── test_lambda_selector.py
    ├── test_solver.py
    ├── test_verifier.py
    ├── test_replanner.py
    └── test_agent_loop.py
```

### Data flow

```
configs/example_case.yaml ──► Parser ──► ProblemSpec
data/demo_temperature.csv ──►

ProblemSpec ──► Planner ──► InversionConfig

InversionConfig ──► forward_model + sensitivity ──► G matrix
                ──► lambda_selector              ──► λ
(G, λ) ──► tikhonov_solver ──► SolverResult

SolverResult ──► Verifier ──► VerificationResult
VerificationResult ──► Replanner ──► (new InversionConfig | stop)

SolverResult + traces ──► Reporter ──► summary.json + report.md + trace.json
```

---

## Quick Start

### Install

```bash
pip install -e .
# or for development:
pip install -e ".[dev]"
```

Requires Python ≥ 3.11, numpy, scipy, pyyaml, pandas.

### Run the demo

```bash
python main.py --config configs/example_case.yaml
```

This will:
1. Load the synthetic steel-rod IHCP from `configs/example_case.yaml`
2. Read noisy temperature observations from `data/demo_temperature.csv`
3. Run the Tikhonov agent loop (typically 2–6 iterations)
4. Write outputs to `outputs/<timestamp>/`

### Output files

| File | Contents |
|------|----------|
| `summary.json` | Machine-readable run summary (final status, lambda, residual, …) |
| `report.md` | Human-readable Markdown report with iteration trace |
| `trace.json` | Per-iteration JSON: lambda, RMSE, tradeoff label, replanning action |

### Run tests

```bash
pip install -e ".[dev]"
pytest
```

---

## Configuration

The YAML config supports:

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
  reg_order: 1
  max_retries: 8
  physical_bounds: [-5.0e5, 5.0e5]
```

---

## Optional Qwen-2.5-3B LLM Hook

The system runs fully without any LLM.  An optional Qwen adapter is provided
for:

- Parsing free-form natural language problem descriptions into the schema
- Explaining verification results in natural language
- Drafting narrative sections of the Markdown report

**The LLM never makes scientific decisions** (lambda selection, acceptance of
results, etc.).  All such decisions remain in the rule-based core.

To enable (after filling in the placeholder inference code in `src/llm_hooks.py`):

```bash
pip install -e ".[llm]"
python main.py --config configs/example_case.yaml --use-qwen --qwen-device cuda
```

The `QwenLocalAdapter` in `src/llm_hooks.py` contains clearly marked
`# PLACEHOLDER` sections where you insert the actual `transformers` inference
calls.

---

## Extension Roadmap

This prototype is designed for clean extension:

| Extension | Where to add |
|-----------|--------------|
| Alternative forward solver (e.g. FEniCS) | Replace `HeatConductionFD` in `forward_model.py` |
| Non-linear forward model (adjoint) | Extend `sensitivity.py` with iterative update |
| Bayesian / MCMC posterior | Add `src/bayesian_solver.py`; register in `agent.py` |
| PINN / DeepONet surrogate | Add `src/pinn_solver.py`; conditionally select in Planner |
| RL-based orchestration | Replace `planner.py` + `replanner.py` with a policy |
| 2D problem | Replace `forward_model.py`; types.py Geometry already extensible |
| Multi-sensor + multi-unknown | Extend `ProblemSpec` and `sensitivity.py` |

The scientific core (types, forward model, regularisation, verification) is
intentionally stable; the orchestration (planner, replanner, agent loop) is
the primary extension surface.

---

## Citation / Reference

If you use this prototype in your research, please cite it as:

```
tikhonov_agent v0.1.0 – Rule-based scientific agent for 1D transient IHCP.
https://github.com/your-org/tikhonov-agent
```

---

## License

MIT
