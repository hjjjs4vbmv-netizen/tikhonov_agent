# PDE-Schema Normalizer: Design Note

## Summary

This document describes the upgraded PDE-schema normalizer introduced in the
`tikhonov_agent` repository.  The key improvement over the previous
`input_normalizer.py` is a **clean three-layer architecture** that separates
(1) syntax-level normalisation, (2) PDE-level semantic validation, and
(3) downstream `ProblemSpec` construction.

---

## 1. Diagnosis of the Old Design

The old `input_normalizer.py` had four structural problems:

| Problem | Detail |
|---------|--------|
| Flat IHCP schema | `NormalizedSchema` was a flat dataclass with fields like `rod_length_m`, `bc_right_type`.  No concept of PDE family, equation class, domain type, coordinate system, coefficient variability, BC status, or observation layout. |
| Ad-hoc dict parser | `_dict_to_schema()` was ~100 lines of `if "X" in raw` guards with no alias table, no enum validation, no precedence logic. |
| Weak text extraction | 13 hardcoded regex patterns, no material-name recognition, no LLM path, no confidence tracking. |
| Incomplete validation | `is_complete()` / `missing_fields()` only checked field presence.  No PDE semantic checks (sensor-in-domain, Fourier number, BC consistency, inversion-target designation). |

---

## 2. New Architecture

```
Raw input
  ├─ Path A (clean structured)
  │    StructuredInputParser
  │         ↓
  │    PDESchema (with full PDE taxonomy)
  │
  └─ Path B (messy / semi-structured)
       LLMPDESchemaFiller.fill_schema(text)
            ↓ candidate dict
       StructuredInputParser   ← same parser as Path A
            ↓
       PDESchema
              ↓
       PDESchemaValidator  ← always deterministic
              ↓
       PDESchemaMapper
              ↓
       ProblemSpec ──► existing solver/verifier/replanner pipeline
```

The key design principles are:

* **The LLM never owns the final schema.**  It only produces a candidate dict.
  That dict is fed through the deterministic `StructuredInputParser` and then
  through `PDESchemaValidator` before anything downstream sees it.
* **Both paths produce the same type.**  `normalize_structured()` and
  `normalize_with_llm()` both return `(PDESchema, ValidationResult)`.
* **Backward compatibility is preserved.**  `NormalizedSchema` now wraps a
  `PDESchema` internally and exposes the old flat field names as properties.
  Existing tests and demos continue to work without modification.

---

## 3. File Map

| File | Role |
|------|------|
| `src/pde_schema.py` | `PDESchema` sub-dataclasses, `PDESchemaValidator`, `PDESchemaMapper` |
| `src/pde_normalizer.py` | `StructuredInputParser` (Path A), `MockPDESchemaFiller` (Path B), public API |
| `src/input_normalizer.py` | Backward-compatible `NormalizedSchema` adapter; delegates to `pde_normalizer.py` |
| `tests/test_pde_schema.py` | Unit tests for schema dataclasses, validator, mapper |
| `tests/test_pde_normalizer.py` | Unit tests for both parsing paths, alias table, failure cases |
| `tests/fixtures/clean_ihcp.yaml` | Canonical nested YAML fixture (Path A) |
| `tests/fixtures/legacy_ihcp.yaml` | Legacy flat YAML fixture (backward compat) |

---

## 4. PDESchema Field Reference

### 4.1 Top-level taxonomy

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `pde_family` | `"parabolic"\|"elliptic"\|"hyperbolic"\|"mixed"` | `"parabolic"` | PDE classification |
| `equation_class` | `"heat_equation"\|"wave_equation"\|"poisson"\|"other"` | `"heat_equation"` | Specific equation |
| `problem_kind` | `"inverse"\|"forward"` | `"inverse"` | IHCP vs forward problem |
| `dimension` | `int` | `1` | Spatial dimension (1–3) |
| `transient` | `bool` | `True` | Time-dependent vs steady-state |
| `unknown_target` | enum | `"boundary_heat_flux"` | What the inversion recovers |

### 4.2 `domain: DomainSpec`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `domain_type` | enum | `"interval"` | 1D interval, rectangle, etc. |
| `coord_system` | enum | `"cartesian"` | Coordinate system |
| `length` | `float\|None` | `None` | Domain length [m] (**required**) |
| `n_cells_x` | `int` | `50` | Spatial discretisation cells |
| `width`, `height` | `float\|None` | `None` | For 2-D/3-D (future) |

### 4.3 `material: MaterialSpec`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `density` | `float\|None` | `None` | ρ [kg/m³] (**required**) |
| `specific_heat` | `float\|None` | `None` | c_p [J/(kg·K)] (**required**) |
| `conductivity` | `float\|None` | `None` | k [W/(m·K)] (**required**) |
| `*_kind` | enum | `"constant"` | `"constant"`, `"variable"`, `"temperature_dependent"` |
| `source_term` | `float\|None` | `None` | Q [W/m³] volumetric source |

### 4.4 `initial_condition: InitialConditionSpec`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `ic_type` | `"uniform"\|"expression"\|"file"` | `"uniform"` | IC type |
| `value` | `float` | `300.0` | Uniform temperature [K] |
| `expression` | `str\|None` | `None` | Symbolic expression (future) |
| `file` | `str\|None` | `None` | CSV path (future) |

### 4.5 `boundary_conditions: BoundaryConditionsSpec`

Contains a list of `BoundaryConditionSpec`:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `location` | `str` | `"left"` | `"left"`, `"right"`, `"top"`, etc. |
| `bc_type` | enum | `"neumann"` | `"dirichlet"`, `"neumann"`, `"robin"`, `"unknown"` |
| `status` | enum | `"given"` | `"given"`, `"inversion_target"`, `"unknown"` |
| `value` | `float\|None` | `None` | BC value [K or W/m²] |

**IHCP convention:** the heated (left) surface BC has `status="inversion_target"`.

### 4.6 `observation: ObservationSpec`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `sensor_positions` | `list[float]` | `[]` | Sensor x-coordinates [m] (**required**) |
| `observed_variable` | enum | `"temperature"` | What sensors measure |
| `observations_file` | `str\|None` | `None` | CSV path (rows=time, cols=sensors) |
| `observations_array` | `list[list[float]]\|None` | `None` | In-memory (n_sensors × n_time) |
| `noise_std` | `float\|None` | `None` | Measurement noise σ [K] |
| `noise_model` | enum | `"gaussian"` | Noise distribution |

### 4.7 `time: TimeSpec`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `start` | `float` | `0.0` | t_start [s] |
| `end` | `float\|None` | `None` | t_end [s] (**required for transient**) |
| `n_steps` | `int\|None` | `None` | Number of time steps (**required for transient**) |

### 4.8 `solver_prefs: SolverPrefsSpec`

Passed through to the planner.  All fields are optional.

| Field | Type | Description |
|-------|------|-------------|
| `preferred_solver` | enum | `"tikhonov"`, `"tsvd"`, … |
| `reg_order` | `int\|None` | Regularisation order (0, 1, 2) |
| `lambda_strategy` | `str\|None` | `"fixed"`, `"lcurve"`, `"gcv"`, `"discrepancy"` |
| `lambda_value` | `float\|None` | Fixed λ value |
| `max_retries` | `int\|None` | Max replanning iterations |
| `iteration_budget` | `int\|None` | Hard cap on agent loop |
| `physical_bounds` | `tuple[float,float]\|None` | (q_min, q_max) [W/m²] |

### 4.9 `metadata: SchemaMetadata`

| Field | Type | Description |
|-------|------|-------------|
| `source` | `str` | File path, `"llm_assisted"`, `"text_extraction"`, … |
| `parse_path` | enum | `"structured"` or `"llm_assisted"` |
| `confidence` | `float` | 0.0–1.0; LLM path may reduce this |
| `warnings` | `list[str]` | Non-fatal notes from normalisation |
| `raw_input_preview` | `str` | First 300 chars of raw input (Path B) |

---

## 5. Field Alias Table (selected entries)

The full alias table is in `pde_normalizer._FIELD_ALIASES`.  Common aliases:

| Alias | Canonical |
|-------|-----------|
| `rho`, `mass_density` | `material.density` |
| `cp`, `c_p`, `heat_capacity` | `material.specific_heat` |
| `k`, `thermal_conductivity`, `lambda` | `material.conductivity` |
| `T0`, `T_initial`, `initial_temperature_K` | `initial_condition.value` |
| `T_right`, `right_temperature` | right BC value |
| `T_end`, `t_end`, `final_time` | `time.end` |
| `n_steps`, `nt`, `num_steps` | `time.n_steps` |
| `rod_length_m`, `L` | `domain.length` |
| `sensor_positions_m`, `sensors` | `observation.sensor_positions` |
| `noise_std_K`, `sigma` | `observation.noise_std` |

---

## 6. When Is Each Path Used?

| Condition | Path | Adapter |
|-----------|------|---------|
| Clean YAML file | A | `normalize_from_yaml()` |
| Clean Python dict | A | `normalize_structured()` |
| Legacy flat YAML (existing repo format) | A | Same; alias table handles names |
| Semi-structured text with known patterns | B | `normalize_from_text()` (mock) |
| Free-form engineering prose | B | `normalize_with_llm(text, real_adapter)` |
| Existing `normalize_from_dict()` callers | A (via compat layer) | `input_normalizer.normalize_from_dict()` |

**Decision rule:** if the input is a dict or YAML file, always use Path A.
Use Path B only when the input is raw text that cannot be parsed as YAML.

---

## 7. Semantic Validation Checks

`PDESchemaValidator.validate()` runs the following groups of checks:

| Group | Checks |
|-------|--------|
| Taxonomy | Valid enum values for `pde_family`, `equation_class`, `problem_kind`, `unknown_target`; dimension in 1–3 |
| Domain | `length > 0`; `n_cells_x > 0`; coord_system valid; dimension-width consistency |
| Material | `density`, `specific_heat`, `conductivity` all present and `> 0`; coefficient kind enums valid |
| Initial condition | IC type enum valid; `uniform` has a value; `expression` not empty if type is expression |
| Boundary conditions | At least one BC defined; enum checks for `bc_type` and `status`; no duplicate locations; given BCs have values |
| Observations | At least one sensor; sensor positions are numeric; data source present; array shape matches sensor count; `noise_std >= 0` |
| Time | `end > start`; `n_steps >= 2` for transient; warns if time settings given for steady state |
| IHCP-specific | Exactly one `inversion_target` BC; `unknown_target` consistent with BC type; sensors strictly interior to domain; Fourier number sanity check |

Errors are hard failures; warnings are non-fatal notes.  A schema is
considered valid only if the error list is empty.

---

## 8. Limitations (Honest Accounting)

* The `MockPDESchemaFiller` (Path B mock) recognises ~20 specific text patterns
  and 6 material names.  It is not a general NLP system.
* Variable/temperature-dependent material coefficients are declared in the
  schema but ignored by the current 1-D FD solver (constant properties only).
* 2-D/3-D geometry fields (`width`, `height`, `n_cells_y`, `n_cells_z`) are
  stored but not used by any current solver.
* `ic_type="expression"` and `ic_type="file"` are defined in the schema but
  not yet implemented in the mapper (raises `ValueError` if used).
* The LLM path requires a real adapter implementing `LLMPDESchemaFiller` to be
  useful in production; the mock is for testing only.
* `ValidationResult.valid=True` means the schema passes all *declared* checks;
  it does not guarantee physical realism or numerical stability of the solution.

---

## 9. Local Qwen Integration (Path B — Real LLM Backend)

### 9.1 Overview

The `LocalQwenPDESchemaFiller` class (in `src/qwen_pde_filler.py`) replaces the
mock regex filler with a real local Qwen2.5-3B-Instruct model loaded via
Hugging Face Transformers.  It implements the same `LLMPDESchemaFiller` protocol
so it slots directly into `normalize_with_llm()` without any other changes.

```
messy text
  └─ LocalQwenPDESchemaFiller.fill_schema(text)
       │  • loads local model (lazy, first call only)
       │  • builds system+user prompt
       │  • runs local inference via Transformers
       │  • parses JSON from output
       ↓
     candidate dict (translated to StructuredInputParser format)
       ↓
     StructuredInputParser  (alias resolution, type coercion)
       ↓
     PDESchemaValidator     (deterministic semantic checks — always)
       ↓
     PDESchemaMapper → ProblemSpec
```

**The LLM still cannot bypass deterministic validation.**

### 9.2 Model Path Configuration

Priority (highest to lowest):

| Priority | Source | Example |
|----------|--------|---------|
| 1 | Explicit constructor argument | `LocalQwenPDESchemaFiller(model_path="/my/path")` |
| 2 | Environment variable `QWEN_MODEL_PATH` | `export QWEN_MODEL_PATH=/my/path` |
| 3 | Compiled-in default | `/root/models/Qwen/Qwen2___5-3B-Instruct` |

### 9.3 When Each Path Is Used

| Input type | Path | Entry point |
|------------|------|-------------|
| Clean YAML file | A — deterministic | `normalize_from_yaml()` |
| Clean Python dict | A — deterministic | `normalize_structured()` |
| Legacy flat YAML | A — deterministic (alias table) | same |
| Semi-structured text | B — local Qwen | `normalize_with_local_qwen()` |
| Semi-structured text (no model) | B — mock regex | `normalize_from_text()` |
| Custom LLM backend | B — any adapter | `normalize_with_llm(text, adapter)` |

**Decision rule:** if the input is a dict or YAML file, use Path A.
Use Path B only when the input is raw text that cannot be parsed as YAML.

### 9.4 Prompt Design

The system message instructs the model to:
- output **only valid JSON** (no markdown, no prose)
- follow the exact `PDESchema` field names
- use SI units throughout
- map common aliases (`rho`→`density`, `cp`→`specific_heat`, `k/kappa`→`conductivity`, …)
- set **missing fields to `null`**, never invent values
- record `_confidence` (0–1) and `_llm_warnings` in the output

A single few-shot example is embedded in the system prompt to anchor the
output format.

### 9.5 How to Run the Demo

```bash
cd /root/claude-code/tikhonov_agent

# Default model path
python demos/demo_local_qwen_normalizer.py

# Custom model path
QWEN_MODEL_PATH=/your/path python demos/demo_local_qwen_normalizer.py
```

Expected output (abbreviated):

```
Model path: /root/models/Qwen/Qwen2___5-3B-Instruct
...
Case A – semi-structured:
  backend: local_qwen_transformers   device: cuda:0
  Validation: PASS ✓   ProblemSpec: n_time=121, n_sensors=2, k=50.0

Case C – missing conductivity:
  Validation: FAIL ✗
    ERR: material.conductivity is required but missing
  ProblemSpec: NOT BUILT (schema invalid)
```

### 9.6 Demonstrated Behaviours

The real-model demo (observed on `Qwen2.5-3B-Instruct`, `cuda:0`) showed:

| Case | Result | Key observation |
|------|--------|-----------------|
| A: semi-structured prose | PASS, ProblemSpec built | All 5 core fields extracted correctly |
| B: messy aliased format | PASS, ProblemSpec built | `kappa`→conductivity, `5e-2`→0.05 m resolved |
| C: missing conductivity | FAIL (validator caught it) | Model correctly returned `"conductivity": null`, did not hallucinate |
| D: contradictory BCs | FAIL (validator caught it) | Model flagged `right_type: "unknown"`, validator raised error |

### 9.7 Inference Metadata

Every schema produced by `LocalQwenPDESchemaFiller` has the following fields in
`schema.metadata.extra["inference_meta"]`:

| Key | Example value |
|-----|---------------|
| `backend` | `"local_qwen_transformers"` |
| `device` | `"cuda:0"` |
| `model_path` | `"/root/models/Qwen/Qwen2___5-3B-Instruct"` |
| `prompt_tokens` | `976` |
| `completion_tokens` | `219` |
| `inference_time_s` | `3.65` |

### 9.8 Remaining Limitations of the LLM Path

* A 3B model is not a universal NLP system; unusual phrasings or non-SI
  units embedded in prose may be mishandled.
* Unit conversion is handled by the prompt's alias table; the model itself
  may occasionally miss exotic unit spellings.
* The model can hallucinate values for ambiguous inputs — the validator is the
  last line of defence, not the model's self-reported confidence.
* First inference call loads ~6 GB of model weights; subsequent calls reuse
  the in-memory model.
* The validated scientific use case remains the **1D transient IHCP**.
  The schema and validator support richer PDE descriptions structurally,
  but only the 1D case is exercised end-to-end.

