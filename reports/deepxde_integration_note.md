# DeepXDE Solver Integration Note

**Date:** 2026-05-01
**Stage:** v1.2 integration complete

---

## 1. What was integrated

`src/deepxde_solver.py` and an updated `src/solver_registry.py` were added by the
advisor and wired into the agent pipeline in this session.

Changes made:

| File | Change |
|------|--------|
| `README.md` | Added `deepxde_solver.py` to arch tree; updated solver flow diagram; added v1.2 section describing solver, config snippet, scope note |
| `configs/default.yaml` | Added commented `solver_name: deepxde` example with all optional DeepXDE fields |
| `tests/test_deepxde_solver.py` | New smoke test (10 tests covering registry, solve_single, diagnostics, lbfgs path, missing-dependency path) |
| `reports/deepxde_integration_note.md` | This file |

No changes to `planner.py`, `parser.py`, `agent.py`, or `types.py` were required:
the planner already passes `solver_name` through to the registry without restriction.

---

## 2. Current meaning of the DeepXDE solver

`deepxde_solver.py` solves the **same regularised linear inverse objective** as the
Tikhonov solver:

```
min_x  ||G x - y||²  +  λ ||L x||²
```

The difference is the backend: instead of forming normal equations analytically
(NumPy linalg), it treats `x` as a `torch.nn.Parameter` and minimises the loss
with PyTorch (Adam, L-BFGS, or Adam→L-BFGS warm start).

Lambda semantics are identical to Tikhonov — all existing lambda selection
strategies (L-curve, discrepancy, fixed, grid search) apply unchanged.

**This is not a PINN.** There are no PDE residual terms, no collocation points,
no IC/BC residual components in the loss. The solver is a differentiable
inversion baseline that uses DeepXDE's PyTorch backend for its optimisation.

---

## 3. Config selection status

`solver_name: deepxde` is now fully usable from YAML configs:

```yaml
planner:
  solver_name: deepxde
  # optional:
  # deepxde_iterations: 5000
  # deepxde_lr: 0.01
  # deepxde_optimizer: adam   # or lbfgs
  # deepxde_device: cpu
```

The planner, registry, and agent loop all pass the solver name through correctly.
No validation rejections. Existing `tikhonov` and `tsvd` behaviour is unchanged.

**Dependency requirement:** `pip install deepxde torch` + `export DDE_BACKEND=pytorch`

---

## 4. Smoke test results

```
tests/test_deepxde_solver.py  10 passed  (with deepxde installed, DDE_BACKEND=pytorch)
```

Tests verified:
- Registry contains `"deepxde"` and all three solvers (`tikhonov`, `tsvd`, `deepxde`)
- `registry.solve_single("deepxde", G, y, config, lam)` returns a valid `SolverResult`
- All required fields present (`estimated_x`, `status`, `residual_norm`, `diagnostics`)
- `diagnostics.solve_method` contains `"deepxde"` for traceability
- `solve_grid` returns one result per lambda
- L-BFGS optimizer path runs cleanly
- Missing-dependency path raises `ImportError` with a clear message

Without `deepxde` installed: 4 pass, 6 skip (registry and dependency-path tests still run).

---

## 5. Current limitations

1. **Not a PINN.** The DeepXDE solver does not yet add physical value beyond
   differentiability — it solves the same objective as Tikhonov with more
   overhead.  The extension path (adding PDE residual terms) is the next step.

2. **Slower on small problems.** PyTorch initialisation overhead means deepxde
   is slower than Tikhonov on the 20–50 parameter problems in the current
   benchmark.  This is expected and acceptable for the current integration stage.

3. **Not benchmarked at scale.** No systematic comparison against Tikhonov/TSVD
   across the 30-case benchmark suite has been run yet.

4. **Requires extra dependencies.** `deepxde` + `torch` are not in the base
   `requirements.txt`.  The solver fails gracefully (ImportError) if absent.

5. **L-BFGS with many parameters may need tuning.** The default LBFGS `max_iter`
   is derived from `deepxde_iterations - deepxde_adam_iterations`.  For
   ill-conditioned problems, this may need manual adjustment.

---

## 6. Recommended immediate next step

**Run a 3-solver comparison before the holiday deadline.**

Proposed action:

1. Extend `demos/validate_multi_solver.py` (or create a new script) to run all
   three solvers on the same 3–5 benchmark cases.
2. Compare: flux RMSE, replay RMSE, wall-clock time, verifier decision.
3. Include `deepxde_iterations=500` for a fast first pass.

This will answer: *Does DeepXDE at current settings match or underperform Tikhonov,
and is there any case type where it already shows advantage?*

Expected outcome: Tikhonov likely wins on these small problems; the value is
establishing the baseline for when PDE residuals are added.
