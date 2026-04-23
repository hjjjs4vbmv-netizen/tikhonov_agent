"""
demo_semistructured_input.py
============================
Demonstrates Part A of the packaging upgrade:

  Semi-structured text / partial dict  →  Input Normalizer  →  NormalizedSchema

Shows that the normalizer can extract key physical parameters from a
brief text description and from a Python dict with partial data, and
produce the same unified NormalizedSchema as the structured YAML path.

Run from the tikhonov_agent/ directory:
    python demos/demo_semistructured_input.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.input_normalizer import normalize_from_dict, normalize_from_text


# ---------------------------------------------------------------------------
# Semi-structured text example
# ---------------------------------------------------------------------------

SAMPLE_TEXT = """
Inverse heat conduction experiment — steel rod benchmark

Geometry: L = 0.05 m, n_cells = 60
Material: rho = 7800.0 kg/m³, cp = 500.0 J/(kg·K), k = 50.0 W/(m·K)
Initial condition: T0 = 300.0 K
Right boundary: T_right = 300.0 K (Dirichlet)
Sensors at 0.01 m and 0.03 m
Time: T_end = 60.0 s, n_steps = 121
Noise: noise_std = 0.3 K
Observations = data/demo_temperature.csv
"""

# ---------------------------------------------------------------------------
# Partial dict example (as might come from a form, API, or preprocessed input)
# ---------------------------------------------------------------------------

PARTIAL_DICT = {
    "problem_type": "1D_transient_IHCP",
    "geometry": {
        "length": 0.05,
        "n_cells": 60,
    },
    "material": {
        "density": 7800.0,
        "specific_heat": 500.0,
        "conductivity": 50.0,
    },
    "initial_condition": 300.0,
    "boundary_conditions": {
        "right_type": "dirichlet",
        "right_value": 300.0,
    },
    "time": {
        "start": 0.0,
        "end": 60.0,
        "n_steps": 121,
    },
    "sensor_positions": [0.01, 0.03],
    "noise_std": 0.3,
    "observations_file": "data/demo_temperature.csv",
    "metadata": {"source": "form_input", "experimenter": "demo"},
}


def main() -> None:
    print("=" * 60)
    print("Demo: Semi-Structured Input → NormalizedSchema")
    print("=" * 60)

    # ----------------------------------------------------------------
    # Path 1: text extraction
    # ----------------------------------------------------------------
    print("\n[Path 1] normalize_from_text()")
    print("  Input text (truncated):", SAMPLE_TEXT[:80].strip(), "...")
    schema_text = normalize_from_text(SAMPLE_TEXT)

    print("\n  Extracted fields:")
    print(f"    rod_length_m       = {schema_text.rod_length_m}")
    print(f"    n_cells            = {schema_text.n_cells}")
    print(f"    density_kg_m3      = {schema_text.density_kg_m3}")
    print(f"    specific_heat_J_kgK= {schema_text.specific_heat_J_kgK}")
    print(f"    conductivity_W_mK  = {schema_text.conductivity_W_mK}")
    print(f"    initial_temp_K     = {schema_text.initial_temperature_K}")
    print(f"    bc_right_value     = {schema_text.bc_right_value}")
    print(f"    time_end_s         = {schema_text.time_end_s}")
    print(f"    time_n_steps       = {schema_text.time_n_steps}")
    print(f"    sensor_positions_m = {schema_text.sensor_positions_m}")
    print(f"    noise_std_K        = {schema_text.noise_std_K}")
    print(f"    observations_file  = {schema_text.observations_file}")
    print(f"    is_complete()      = {schema_text.is_complete()}")
    if schema_text.missing_fields():
        print(f"    missing_fields()   = {schema_text.missing_fields()}")

    # ----------------------------------------------------------------
    # Path 2: partial dict
    # ----------------------------------------------------------------
    print("\n[Path 2] normalize_from_dict()")
    schema_dict = normalize_from_dict(PARTIAL_DICT)

    print("\n  Schema fields:")
    print(f"    rod_length_m       = {schema_dict.rod_length_m}")
    print(f"    n_cells            = {schema_dict.n_cells}")
    print(f"    density_kg_m3      = {schema_dict.density_kg_m3}")
    print(f"    specific_heat_J_kgK= {schema_dict.specific_heat_J_kgK}")
    print(f"    conductivity_W_mK  = {schema_dict.conductivity_W_mK}")
    print(f"    initial_temp_K     = {schema_dict.initial_temperature_K}")
    print(f"    bc_right_type      = {schema_dict.bc_right_type}")
    print(f"    bc_right_value     = {schema_dict.bc_right_value}")
    print(f"    time_end_s         = {schema_dict.time_end_s}")
    print(f"    time_n_steps       = {schema_dict.time_n_steps}")
    print(f"    sensor_positions_m = {schema_dict.sensor_positions_m}")
    print(f"    noise_std_K        = {schema_dict.noise_std_K}")
    print(f"    observations_file  = {schema_dict.observations_file}")
    print(f"    solver_preferences = {schema_dict.solver_preferences}")
    print(f"    is_complete()      = {schema_dict.is_complete()}")
    if schema_dict.missing_fields():
        print(f"    missing_fields()   = {schema_dict.missing_fields()}")

    # ----------------------------------------------------------------
    # Cross-check: both paths produce consistent schemas
    # ----------------------------------------------------------------
    print("\n[Cross-check] Text vs Dict schema consistency:")
    fields_to_check = [
        ("rod_length_m",        schema_text.rod_length_m,        schema_dict.rod_length_m),
        ("density_kg_m3",       schema_text.density_kg_m3,       schema_dict.density_kg_m3),
        ("specific_heat_J_kgK", schema_text.specific_heat_J_kgK, schema_dict.specific_heat_J_kgK),
        ("conductivity_W_mK",   schema_text.conductivity_W_mK,   schema_dict.conductivity_W_mK),
        ("initial_temp_K",      schema_text.initial_temperature_K, schema_dict.initial_temperature_K),
        ("time_end_s",          schema_text.time_end_s,          schema_dict.time_end_s),
        ("time_n_steps",        schema_text.time_n_steps,        schema_dict.time_n_steps),
        ("noise_std_K",         schema_text.noise_std_K,         schema_dict.noise_std_K),
    ]
    all_ok = True
    for name, v_text, v_dict in fields_to_check:
        if v_text is None or v_dict is None:
            ok = v_text == v_dict
        else:
            ok = abs(float(v_text) - float(v_dict)) < 1e-9
        status = "MATCH" if ok else "DIFF"
        print(f"  {status:6s}  {name}: text={v_text}, dict={v_dict}")
        all_ok = all_ok and ok

    print()
    if all_ok:
        print("  ✓ Both input paths produce identical physical parameters.")
    else:
        print("  ✗ Some fields differ — check text extraction patterns.")

    # ----------------------------------------------------------------
    # Convert dict schema to ProblemSpec (text schema is also convertible,
    # but its observations_file path is relative; dict schema works as-is
    # if run from tikhonov_agent/)
    # ----------------------------------------------------------------
    print("\n[ProblemSpec conversion] from dict schema:")
    try:
        spec = schema_dict.to_problem_spec()
        print(f"  OK — n_time={spec.n_time}, n_sensors={spec.n_sensors}, "
              f"material.k={spec.material.conductivity}")
    except Exception as exc:
        print(f"  Note: {exc}")
        print("  (Expected if observations_file path is relative and not found from this cwd.)")
        print("  Run from tikhonov_agent/ directory or supply absolute path.")

    print("\nDemo complete.")


if __name__ == "__main__":
    main()
