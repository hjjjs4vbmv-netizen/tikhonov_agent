# Schema Table — Paper Snippet

> Copy-paste ready for the paper.  Adjust column widths / caption as needed.

## Compact field reference (paper table)

| Category | Symbol | Field (`NormalizedSchema`) | Unit | Required |
|---|---|---|---|---|
| PDE family | — | `problem_type = "1D_transient_IHCP"` | — | no |
| Geometry | L | `rod_length_m` | m | yes |
| Geometry | N_x | `n_cells` | — | no |
| Material | ρ | `density_kg_m3` | kg/m³ | yes |
| Material | c_p | `specific_heat_J_kgK` | J/(kg·K) | yes |
| Material | k | `conductivity_W_mK` | W/(m·K) | yes |
| Initial condition | T₀ | `initial_temperature_K` | K | no |
| Right BC | T_R / q_R | `bc_right_value` | K or W/m² | no |
| Inversion target | q(t) | `unknown_target = "boundary_heat_flux"` | W/m² | — |
| Time domain | t_end | `time_end_s` | s | yes |
| Time steps | N_t | `time_n_steps` | — | yes |
| Sensor positions | x_s | `sensor_positions_m` | m | yes |
| Observations | Y | `observations_file` | K (CSV) | yes |
| Noise estimate | σ | `noise_std_K` | K | no |
| Solver choice | — | `solver_preferences["solver_name"]` | — | no |

**Caption suggestion:**  
*Table X. Fields of the NormalizedSchema produced by the Input Normalizer.
Required fields must be set for a complete problem specification.
Optional fields use documented defaults.  The left boundary condition
(x=0) is the inversion target q(t) and is not stored in the schema.*
