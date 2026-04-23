# Problem Schema v1 — Normalized Problem Representation

**tikhonov_agent: NormalizedSchema field reference**

> This document describes the unified internal schema produced by the Input
> Normalizer (`src/input_normalizer.py`) from any supported raw input format.
> The schema serves as the contract between input parsing and the scientific
> core.  All downstream modules consume `ProblemSpec` (produced by
> `NormalizedSchema.to_problem_spec()`), never the raw input directly.

---

## 1. Field Reference Table

| Field | Meaning | Type | Req? | Example Value |
|-------|---------|------|------|---------------|
| **Problem taxonomy** | | | | |
| `pde_family` | PDE family | `str` | no | `"parabolic"` |
| `problem_type` | Specific problem identifier | `str` | no | `"1D_transient_IHCP"` |
| `dimension` | Spatial dimension | `int` | no | `1` |
| `transient` | Time-dependent? | `bool` | no | `True` |
| `unknown_target` | What is being reconstructed | `str` | no | `"boundary_heat_flux"` |
| **Geometry** | | | | |
| `rod_length_m` | Total rod length [m] | `float` | **yes** | `0.05` |
| `n_cells` | Number of FD spatial cells | `int` | no | `50` (default) |
| **Material properties** | | | | |
| `density_kg_m3` | Material density ρ [kg/m³] | `float` | **yes** | `7800.0` |
| `specific_heat_J_kgK` | Specific heat capacity cₚ [J/(kg·K)] | `float` | **yes** | `500.0` |
| `conductivity_W_mK` | Thermal conductivity k [W/(m·K)] | `float` | **yes** | `50.0` |
| **Initial condition** | | | | |
| `initial_temperature_K` | Uniform initial temperature T(x,0) [K] | `float` | no | `300.0` (default) |
| **Boundary conditions** | | | | |
| `bc_right_type` | Right BC type (`"dirichlet"` or `"neumann"`) | `str` | no | `"dirichlet"` (default) |
| `bc_right_value` | Right BC value [K or W/m²] | `float` | no | `300.0` (default) |
| *Left BC (x=0)* | *The unknown q(t); not stored — it is the inversion target* | — | — | — |
| **Time discretisation** | | | | |
| `time_start_s` | Simulation start time [s] | `float` | no | `0.0` (default) |
| `time_end_s` | Simulation end time [s] | `float` | **yes** | `60.0` |
| `time_n_steps` | Number of time steps | `int` | **yes** | `121` |
| **Observations** | | | | |
| `sensor_positions_m` | x-coordinates of sensors [m] (list) | `list[float]` | **yes** | `[0.01, 0.03]` |
| `observations_file` | Path to CSV temperature observations | `str` | **yes*** | `"data/demo_temperature.csv"` |
| `observations_array` | In-memory observation array (n_sensors × n_t) | `list[list[float]]` | **yes*** | (array) |
| **Noise** | | | | |
| `noise_std_K` | Estimated measurement noise std [K]; enables Morozov discrepancy | `float \| None` | no | `0.3` |
| **Solver preferences** | | | | |
| `solver_preferences` | Dict of planner overrides (e.g. `solver_name`, `reg_order`, bounds) | `dict` | no | `{"solver_name": "tsvd", "reg_order": 1}` |
| **Metadata** | | | | |
| `metadata` | Free-form dict (case name, source, etc.) | `dict` | no | `{"case_name": "steel_rod_step"}` |

*One of `observations_file` or `observations_array` must be provided.

**Completeness check:** `NormalizedSchema.is_complete()` verifies all required
fields are set.  `missing_fields()` returns a list of unfilled required fields
by name.

---

## 2. Derived quantities (computed from schema, not stored)

| Quantity | Formula | Notes |
|----------|---------|-------|
| Thermal diffusivity α | k / (ρ cₚ) | Used internally by forward model |
| Time step dt | (time_end_s − time_start_s) / (time_n_steps − 1) | Uniform grid |
| Number of time steps N_t | `time_n_steps` | |
| Number of sensors N_s | `len(sensor_positions_m)` | |
| Observation count M | N_s × N_t | Size of flattened y vector |

---

## 3. Compact schema table (paper-ready excerpt)

> This subsection is formatted for direct reuse in a paper table.

| Category | Symbol | Field | Unit | Required |
|----------|--------|-------|------|----------|
| PDE family | — | `problem_type` | — | no |
| Geometry | L | `rod_length_m` | m | yes |
| Geometry | N_x | `n_cells` | — | no |
| Material | ρ | `density_kg_m3` | kg/m³ | yes |
| Material | cₚ | `specific_heat_J_kgK` | J/(kg·K) | yes |
| Material | k | `conductivity_W_mK` | W/(m·K) | yes |
| Initial condition | T₀ | `initial_temperature_K` | K | no |
| Boundary condition (right) | T_R / q_R | `bc_right_value` | K or W/m² | no |
| Inversion target (left BC) | q(t) | `unknown_target` | W/m² | no |
| Time | t_end | `time_end_s` | s | yes |
| Time | N_t | `time_n_steps` | — | yes |
| Observations | y | `observations_file` | K (CSV) | yes |
| Sensor positions | x_s | `sensor_positions_m` | m | yes |
| Noise estimate | σ | `noise_std_K` | K | no |
| Solver choice | — | `solver_preferences.solver_name` | — | no |

---

## 4. Structured input example (YAML/CSV)

This is the canonical structured input format.  The `normalize_from_yaml()`
path reads this directly.

```yaml
# configs/example_case.yaml
problem_type: "1D_transient_IHCP"
dimension: 1
transient: true
target_name: "boundary_heat_flux"

description: >
  A steel rod (L=5 cm) is heated at the left face by an unknown heat flux.
  Two thermocouples at 1 cm and 3 cm. Reconstruct q(t).

time:
  start: 0.0
  end:   60.0       # [s]
  n_steps: 121      # dt = 0.5 s

geometry:
  length:  0.05     # [m]
  n_cells: 60

material:
  density:       7800.0   # [kg/m³]
  specific_heat:  500.0   # [J/(kg·K)]
  conductivity:    50.0   # [W/(m·K)]

boundary_conditions:
  right_type:  "dirichlet"
  right_value: 300.0      # [K]

sensor_positions:
  - 0.01
  - 0.03

initial_condition: 300.0  # [K]

noise_std: 0.3            # [K]  enables discrepancy principle

observations_file: data/demo_temperature.csv

planner:
  solver_name: tikhonov
  reg_order: 1
  max_retries: 8
  physical_bounds: [-5.0e5, 5.0e5]

metadata:
  case_name: "example_step_flux"
```

**Resulting NormalizedSchema (key fields):**

| Field | Value |
|-------|-------|
| `pde_family` | `"parabolic"` |
| `problem_type` | `"1D_transient_IHCP"` |
| `unknown_target` | `"boundary_heat_flux"` |
| `rod_length_m` | `0.05` |
| `n_cells` | `60` |
| `density_kg_m3` | `7800.0` |
| `specific_heat_J_kgK` | `500.0` |
| `conductivity_W_mK` | `50.0` |
| `initial_temperature_K` | `300.0` |
| `bc_right_type` | `"dirichlet"` |
| `bc_right_value` | `300.0` |
| `time_start_s` | `0.0` |
| `time_end_s` | `60.0` |
| `time_n_steps` | `121` |
| `sensor_positions_m` | `[0.01, 0.03]` |
| `observations_file` | `"data/demo_temperature.csv"` |
| `noise_std_K` | `0.3` |
| `solver_preferences` | `{"solver_name": "tikhonov", "reg_order": 1, ...}` |
| `is_complete()` | `True` |

---

## 5. Semi-structured input example

This illustrates `normalize_from_text()` — lightweight regex extraction from
a prose or table-like description.

**Raw input text:**

```
Steel rod inverse heat conduction experiment

Geometry: L = 0.05 m, n_cells = 60
Material: rho = 7800.0 kg/m³, cp = 500.0 J/(kg·K), k = 50.0 W/(m·K)
Initial condition: T0 = 300.0 K
Right boundary: T_right = 300.0 K
Sensors at 0.01 m and 0.03 m
T_end = 60.0 s, n_steps = 121
Measurement noise: noise_std = 0.3 K
Observations file: data/demo_temperature.csv
```

**Mapping to NormalizedSchema fields:**

| Extracted text fragment | Regex trigger | NormalizedSchema field | Value |
|------------------------|---------------|----------------------|-------|
| `L = 0.05 m` | `L\s*=\s*([\d.]+)\s*m` | `rod_length_m` | `0.05` |
| `n_cells = 60` | `n_cells\s*=\s*(\d+)` | `n_cells` | `60` |
| `rho = 7800.0 kg` | `rho\s*=\s*([\d.]+)\s*kg` | `density_kg_m3` | `7800.0` |
| `cp = 500.0 J` | `cp\s*=\s*([\d.]+)\s*J` | `specific_heat_J_kgK` | `500.0` |
| `k = 50.0 W` | `k\s*=\s*([\d.]+)\s*W` | `conductivity_W_mK` | `50.0` |
| `T0 = 300.0 K` | `T0\s*=\s*([\d.]+)\s*K` | `initial_temperature_K` | `300.0` |
| `T_right = 300.0 K` | `T_right\s*=\s*([\d.]+)\s*K` | `bc_right_value` | `300.0` |
| `T_end = 60.0 s` | `T_end\s*=\s*([\d.]+)\s*s` | `time_end_s` | `60.0` |
| `n_steps = 121` | `n_steps\s*=\s*(\d+)` | `time_n_steps` | `121` |
| `noise_std = 0.3 K` | `noise_std\s*=\s*([\d.]+)\s*K` | `noise_std_K` | `0.3` |
| `sensors at 0.01 m and 0.03 m` | `sensors?\s+at\s+(...)` | `sensor_positions_m` | `[0.01, 0.03]` |
| `observations = ...csv` | `observations\s*=\s*([^\s]+\.csv)` | `observations_file` | `"data/..."` |

**Limitations of text extraction:**
- Only the patterns listed above are recognized.
- `bc_right_type` is not extractable and defaults to `"dirichlet"`.
- `solver_preferences` must be supplied separately.
- For free-form natural language input, a `ProblemParserLLM` adapter is required.

---

## 6. How NormalizedSchema relates to ProblemSpec

`NormalizedSchema` is the *input-format-agnostic intermediate representation*.
`ProblemSpec` (in `src/types.py`) is the *internal scientific representation*
consumed by all downstream modules.

```
NormalizedSchema
  .to_problem_spec()
         │
         ▼
ProblemSpec
  ├── geometry: Geometry(length, n_cells)
  ├── material: Material(density, specific_heat, conductivity)
  ├── boundary_conditions: BoundaryConditions(right_type, right_value)
  ├── time_grid: list[float]  (linspace from start to end)
  ├── sensor_positions: list[float]
  ├── observations: list[list[float]]  (shape n_sensors × n_time)
  ├── initial_condition: float
  ├── noise_std: float | None
  └── metadata: dict
```

`NormalizedSchema` fields that do not map to `ProblemSpec`:
- `pde_family`, `solver_preferences`, `observations_array` (direct array input path)

`solver_preferences` is passed separately to the Planner as `planner_overrides`.
