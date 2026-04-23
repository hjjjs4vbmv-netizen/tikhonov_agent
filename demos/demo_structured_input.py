"""
demo_structured_input.py
========================
Demonstrates Part A of the packaging upgrade:

  Structured YAML / CSV  →  Input Normalizer  →  NormalizedSchema  →  ProblemSpec

Shows that the existing structured workflow produces a well-formed
NormalizedSchema and that the schema can be round-tripped back to a
ProblemSpec identical to what the legacy parser produces.

Run from the tikhonov_agent/ directory:
    python demos/demo_structured_input.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure tikhonov_agent/src is importable when run from any directory
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.input_normalizer import normalize_from_yaml
from src.parser import parse_problem


def main() -> None:
    config_path = REPO_ROOT / "configs" / "example_case.yaml"
    obs_path = REPO_ROOT / "data" / "demo_temperature.csv"

    print("=" * 60)
    print("Demo: Structured YAML → NormalizedSchema → ProblemSpec")
    print("=" * 60)

    # ----------------------------------------------------------------
    # Step 1: normalize_from_yaml produces a NormalizedSchema
    # ----------------------------------------------------------------
    print("\n[Step 1] normalize_from_yaml()")
    schema = normalize_from_yaml(config_path, obs_path)

    print(f"  pde_family         : {schema.pde_family}")
    print(f"  problem_type       : {schema.problem_type}")
    print(f"  dimension          : {schema.dimension}")
    print(f"  transient          : {schema.transient}")
    print(f"  unknown_target     : {schema.unknown_target}")
    print(f"  rod_length_m       : {schema.rod_length_m}")
    print(f"  n_cells            : {schema.n_cells}")
    print(f"  density_kg_m3      : {schema.density_kg_m3}")
    print(f"  specific_heat_J_kgK: {schema.specific_heat_J_kgK}")
    print(f"  conductivity_W_mK  : {schema.conductivity_W_mK}")
    print(f"  initial_temp_K     : {schema.initial_temperature_K}")
    print(f"  bc_right_type      : {schema.bc_right_type}")
    print(f"  bc_right_value     : {schema.bc_right_value}")
    print(f"  time_start_s       : {schema.time_start_s}")
    print(f"  time_end_s         : {schema.time_end_s}")
    print(f"  time_n_steps       : {schema.time_n_steps}")
    print(f"  sensor_positions_m : {schema.sensor_positions_m}")
    print(f"  observations_file  : {schema.observations_file}")
    print(f"  noise_std_K        : {schema.noise_std_K}")
    print(f"  solver_preferences : {schema.solver_preferences}")
    print(f"  is_complete()      : {schema.is_complete()}")

    # ----------------------------------------------------------------
    # Step 2: schema.to_problem_spec() produces a ProblemSpec
    # ----------------------------------------------------------------
    print("\n[Step 2] schema.to_problem_spec()")
    spec = schema.to_problem_spec()
    print(f"  problem_type  : {spec.problem_type}")
    print(f"  target_name   : {spec.target_name}")
    print(f"  n_time        : {spec.n_time}")
    print(f"  n_sensors     : {spec.n_sensors}")
    print(f"  dt            : {spec.dt:.4f} s")
    print(f"  total_time    : {spec.total_time:.1f} s")
    print(f"  geometry      : L={spec.geometry.length} m, n_cells={spec.geometry.n_cells}")
    print(f"  material      : k={spec.material.conductivity} W/(m·K), alpha={spec.material.diffusivity:.2e} m²/s")
    print(f"  noise_std     : {spec.noise_std}")

    # ----------------------------------------------------------------
    # Step 3: Compare with legacy parser output
    # ----------------------------------------------------------------
    print("\n[Step 3] Compare with legacy parse_problem()")
    legacy_spec = parse_problem(config_path, obs_path)

    checks = [
        ("n_time",    spec.n_time,               legacy_spec.n_time),
        ("n_sensors", spec.n_sensors,             legacy_spec.n_sensors),
        ("rod length",spec.geometry.length,       legacy_spec.geometry.length),
        ("density",   spec.material.density,      legacy_spec.material.density),
        ("noise_std", spec.noise_std,             legacy_spec.noise_std),
        ("T0",        spec.initial_condition,     legacy_spec.initial_condition),
        ("obs[0][0]", spec.observations[0][0],    legacy_spec.observations[0][0]),
    ]
    all_ok = True
    for name, v_new, v_old in checks:
        ok = abs(float(v_new) - float(v_old)) < 1e-9
        status = "OK" if ok else "MISMATCH"
        print(f"  {status:8s}  {name}: normalizer={v_new}, parser={v_old}")
        all_ok = all_ok and ok

    print()
    if all_ok:
        print("  ✓ NormalizedSchema produces identical ProblemSpec to legacy parser.")
    else:
        print("  ✗ Mismatch detected — check input_normalizer logic.")

    print("\nDemo complete.")


if __name__ == "__main__":
    main()
