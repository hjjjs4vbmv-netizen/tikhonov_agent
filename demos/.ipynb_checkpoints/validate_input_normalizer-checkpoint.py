"""
validate_input_normalizer.py
============================
Validation script for Part A: Input Normalizer.

Demonstrates and verifies that both structured YAML and semi-structured
text inputs produce consistent NormalizedSchema objects.

Run from the tikhonov_agent/ directory:
    python demos/validate_input_normalizer.py

Outputs:
    demos/outputs/normalizer_validation.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.input_normalizer import normalize_from_dict, normalize_from_text, normalize_from_yaml

OUTPUT_DIR = REPO_ROOT / "demos" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SEMI_TEXT = """
Steel rod inverse heat conduction
L = 0.05 m, n_cells = 60
Material: rho = 7800.0 kg/m³, cp = 500.0 J/(kg·K), k = 50.0 W/(m·K)
Initial: T0 = 300.0 K
Right boundary: T_right = 300.0 K
Sensors at 0.01 m and 0.03 m
T_end = 60.0 s, n_steps = 121
noise_std = 0.3 K
observations = data/demo_temperature.csv
"""


def schema_summary(schema) -> dict:
    return {
        "problem_type": schema.problem_type,
        "rod_length_m": schema.rod_length_m,
        "n_cells": schema.n_cells,
        "density_kg_m3": schema.density_kg_m3,
        "specific_heat_J_kgK": schema.specific_heat_J_kgK,
        "conductivity_W_mK": schema.conductivity_W_mK,
        "initial_temperature_K": schema.initial_temperature_K,
        "bc_right_type": schema.bc_right_type,
        "bc_right_value": schema.bc_right_value,
        "time_start_s": schema.time_start_s,
        "time_end_s": schema.time_end_s,
        "time_n_steps": schema.time_n_steps,
        "sensor_positions_m": schema.sensor_positions_m,
        "noise_std_K": schema.noise_std_K,
        "observations_file": schema.observations_file,
        "is_complete": schema.is_complete(),
        "missing_fields": schema.missing_fields(),
    }


def main() -> None:
    print("=" * 60)
    print("Input Normalizer Validation")
    print("=" * 60)

    config_path = REPO_ROOT / "configs" / "example_case.yaml"
    obs_path = REPO_ROOT / "data" / "demo_temperature.csv"

    # --- Path 1: Structured YAML ---
    print("\n[1] normalize_from_yaml")
    schema_yaml = normalize_from_yaml(config_path, obs_path)
    s1 = schema_summary(schema_yaml)
    print(f"  is_complete: {s1['is_complete']}")
    print(f"  rod_length_m: {s1['rod_length_m']}")
    print(f"  conductivity_W_mK: {s1['conductivity_W_mK']}")
    print(f"  sensor_positions_m: {s1['sensor_positions_m']}")
    print(f"  noise_std_K: {s1['noise_std_K']}")

    # --- Path 2: Semi-structured text ---
    print("\n[2] normalize_from_text")
    schema_text = normalize_from_text(SEMI_TEXT)
    # Override observation file to absolute path for conversion test
    schema_text.observations_file = str(obs_path)
    s2 = schema_summary(schema_text)
    print(f"  is_complete: {s2['is_complete']}")
    print(f"  rod_length_m: {s2['rod_length_m']}")
    print(f"  conductivity_W_mK: {s2['conductivity_W_mK']}")
    print(f"  sensor_positions_m: {s2['sensor_positions_m']}")
    print(f"  noise_std_K: {s2['noise_std_K']}")

    # --- Consistency check ---
    print("\n[Consistency check] YAML vs Text extraction:")
    fields = [
        "rod_length_m", "density_kg_m3", "specific_heat_J_kgK",
        "conductivity_W_mK", "initial_temperature_K", "bc_right_value",
        "time_end_s", "time_n_steps", "noise_std_K",
    ]
    all_ok = True
    results = []
    for f in fields:
        v1 = s1[f]
        v2 = s2[f]
        if v1 is None or v2 is None:
            ok = (v1 == v2)
        else:
            ok = abs(float(v1) - float(v2)) < 1e-9
        status = "MATCH" if ok else "DIFF"
        print(f"  {status:6s}  {f}: yaml={v1}, text={v2}")
        results.append({"field": f, "yaml": v1, "text": v2, "match": ok})
        all_ok = all_ok and ok

    # Sensor positions
    sp_ok = s1["sensor_positions_m"] == s2["sensor_positions_m"]
    print(f"  {'MATCH' if sp_ok else 'DIFF':6s}  sensor_positions_m: yaml={s1['sensor_positions_m']}, text={s2['sensor_positions_m']}")
    all_ok = all_ok and sp_ok

    # --- ProblemSpec conversion from both paths ---
    print("\n[ProblemSpec conversion]")
    for label, schema in [("yaml", schema_yaml), ("text", schema_text)]:
        try:
            spec = schema.to_problem_spec()
            print(f"  {label}: OK — n_time={spec.n_time}, n_sensors={spec.n_sensors}")
        except Exception as exc:
            print(f"  {label}: FAILED — {exc}")

    # --- Save validation record ---
    validation_record = {
        "overall_pass": all_ok,
        "yaml_schema": s1,
        "text_schema": s2,
        "field_comparison": results,
        "sensor_positions_match": sp_ok,
    }
    output_path = OUTPUT_DIR / "normalizer_validation.json"
    with output_path.open("w") as fh:
        json.dump(validation_record, fh, indent=2)

    print(f"\nValidation record saved: {output_path}")
    print()
    if all_ok and sp_ok:
        print("RESULT: PASS — both input paths produce identical physical parameters.")
    else:
        print("RESULT: PARTIAL — some fields differ (see above).")


if __name__ == "__main__":
    main()
