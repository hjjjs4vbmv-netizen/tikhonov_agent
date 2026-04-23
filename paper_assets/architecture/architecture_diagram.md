# Architecture Diagram (ASCII standalone)

Use this as a figure in the paper if Mermaid is not supported by the target venue.
The Mermaid source is in `architecture_v1.2.md`.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         INPUT LAYER (v1.2)                              │
│                                                                         │
│  YAML/CSV ──┐                                                           │
│  dict      ─┼─► Input Normalizer ──► NormalizedSchema ──► ProblemSpec  │
│  text      ─┘   (src/input_normalizer.py)                               │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   │ ProblemSpec
                                   ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        PLANNING                                          │
│                                                                          │
│              Planner ──────────────────────► InversionConfig            │
│           (src/planner.py)                   (incl. solver_name)        │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   │ InversionConfig
                                   ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        SOLVER LAYER (v1.2)                               │
│                                                                          │
│              Solver Registry                                             │
│             (src/solver_registry.py)                                     │
│             ┌──────────┴──────────┐                                      │
│        Tikhonov              TSVD                                        │
│      (validated)           (v1.2 new)                                    │
│             └──────────┬──────────┘                                      │
│                        │ SolverResult                                    │
└───────────────────────-┼────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                    VERIFICATION & REPLANNING                             │
│                                                                          │
│    ┌──────────────────────────────────────────────────────────────┐     │
│    │                       AGENT LOOP                             │     │
│    │                                                              │     │
│    │   SolverResult ──► Verifier ──► VerificationResult          │     │
│    │                                       │                      │     │
│    │                                       ▼                      │     │
│    │                                  Replanner                   │     │
│    │                                  /       \                   │     │
│    │                         terminal?         not terminal       │     │
│    │                              │                  │            │     │
│    │                              │            update config      │     │
│    │                              │            rerun solver ──────┘     │
│    └──────────────────────────────┼────────────────────────────────┘   │
│                                   │ pass / weak_pass / fail / manual    │
└───────────────────────────────────┼─────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                           REPORTER                                       │
│                                                                          │
│         summary.json  ·  trace.json  ·  report.md                       │
└──────────────────────────────────────────────────────────────────────────┘

Shared physical components (used by all solvers):
  Forward Model (1D FD) ──► Sensitivity Matrix G ──► Regularization L
  Lambda Selector ──────────────────────────────────────────────────►
```
