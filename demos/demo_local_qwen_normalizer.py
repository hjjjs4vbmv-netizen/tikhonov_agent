#!/usr/bin/env python3
"""
demo_local_qwen_normalizer.py
=============================
Demonstrates the real local-Qwen-assisted PDE schema normalizer.

Runs four messy-input cases through LocalQwenPDESchemaFiller and prints:
  - raw LLM output
  - parsed candidate dict
  - validation result (errors / warnings)
  - ProblemSpec if validation passes

Usage
-----
    cd /root/claude-code/tikhonov_agent
    python demos/demo_local_qwen_normalizer.py

Optional env override for a non-default model path:
    QWEN_MODEL_PATH=/other/path python demos/demo_local_qwen_normalizer.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

# Ensure the tikhonov_agent src is on the path when run from the demos/ dir
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.qwen_pde_filler import LocalQwenPDESchemaFiller, _resolve_model_path
from src.pde_normalizer import normalize_with_llm, build_problem_spec_from_schema
from src.pde_schema import PDESchemaMapper

# ─────────────────────────────────────────────────────────────────────────────
# Test inputs
# ─────────────────────────────────────────────────────────────────────────────

CASES = {
    "A – semi-structured engineering prose": (
        "1D steel rod of length L = 0.05 m, rho = 7800 kg/m^3, cp = 500 J/(kg·K), "
        "k = 50 W/(m·K). Initial temperature T0 = 300 K. Left boundary heat flux "
        "is unknown (inversion target); right boundary fixed at T_right = 300 K. "
        "Two sensors at 0.01 m and 0.03 m. T_end = 60 s, n_steps = 121. "
        "noise_std = 0.3 K. Observations in data/demo_temperature.csv."
    ),
    "B – messy aliased mixed-format input": (
        "problem: inverse heat conduction; rod len=5e-2 m; rho=7800; c_p=500; "
        "kappa=50; right bc temp 300K; recover left flux; sensors=[0.01,0.03]; "
        "T_end=60s; n_steps=121; obs file data/demo_temperature.csv"
    ),
    "C – incomplete input (missing conductivity)": (
        "1D steel rod. Length 0.05 m. density=7800 kg/m3, specific_heat=500. "
        "Right side is 300 K (fixed). Left flux unknown. "
        "Sensors at x=0.01 and x=0.03 m. End time 60 s, 121 steps."
        # conductivity NOT mentioned
    ),
    "D – contradictory BC (two unknowns)": (
        "1D rod L=0.05m, rho=7800, cp=500, k=50. "
        "Both left and right boundaries have unknown heat flux. "
        "Sensors at 0.01 m and 0.03 m. T_end=60 s, n_steps=121."
    ),
}

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _sep(title: str) -> None:
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def _print_schema_summary(schema) -> None:
    print(f"  Schema:     {schema.summary()}")
    print(f"  parse_path: {schema.metadata.parse_path}")
    print(f"  confidence: {schema.metadata.confidence:.2f}")
    meta = schema.metadata.extra
    imeta = meta.get("inference_meta", {})
    if imeta:
        print(f"  backend:    {imeta.get('backend')}")
        print(f"  device:     {imeta.get('device')}")
        print(f"  tokens:     {imeta.get('prompt_tokens')} prompt + "
              f"{imeta.get('completion_tokens')} completion")
        print(f"  infer_time: {imeta.get('inference_time_s')} s")


def _print_validation(vr) -> None:
    status = "PASS ✓" if vr.valid else "FAIL ✗"
    print(f"  Validation: {status}  (errors={len(vr.errors)}, warnings={len(vr.warnings)})")
    for e in vr.errors:
        print(f"    ERR:  {e}")
    for w in vr.warnings:
        print(f"    WARN: {w}")


# ─────────────────────────────────────────────────────────────────────────────
# Main demo
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    model_path = _resolve_model_path(None)
    print(f"\nLocal Qwen PDE-Schema Normalizer — Demo")
    print(f"Model path: {model_path}")
    if not Path(model_path).exists():
        print(f"ERROR: model path does not exist: {model_path}")
        print("Set QWEN_MODEL_PATH env var or place model at the default location.")
        sys.exit(1)

    print("Loading model (this may take ~30-60 s on first call) …")
    t0 = time.time()
    filler = LocalQwenPDESchemaFiller(model_path=model_path)

    results: list[dict] = []

    for case_name, text in CASES.items():
        _sep(case_name)
        print(f"\nINPUT:\n  {text[:200]}{'...' if len(text)>200 else ''}")

        # Raw fill_schema call
        raw_result = filler.fill_schema(text)
        raw_output = raw_result.get("_raw_output", "(not recorded)")
        print(f"\nRAW LLM OUTPUT (first 400 chars):\n  {raw_output[:400]!r}")

        # Full pipeline
        schema, vr = normalize_with_llm(text, filler, strict=False)
        print()
        _print_schema_summary(schema)
        _print_validation(vr)

        # Try ProblemSpec
        spec = None
        if vr.valid:
            try:
                mapper = PDESchemaMapper()
                if schema.observation.observations_array is None and \
                   schema.observation.observations_file is not None:
                    # Provide a stub CSV loader for demo (no real CSV needed)
                    n_s = len(schema.observation.sensor_positions)
                    n_t = schema.time.n_steps or 121
                    def _stub_loader(path, ns, nt):
                        return [[300.0 + 0.1*i for i in range(nt)] for _ in range(ns)]
                    mapper = PDESchemaMapper(csv_loader=_stub_loader)
                spec = mapper.map(schema)
                print(f"  ProblemSpec: n_time={spec.n_time}, n_sensors={spec.n_sensors}, "
                      f"k={spec.material.conductivity}")
            except Exception as exc:
                print(f"  ProblemSpec: FAILED — {exc}")
        else:
            print("  ProblemSpec: NOT BUILT (schema invalid)")

        results.append({
            "case": case_name,
            "valid": vr.valid,
            "errors": vr.errors,
            "warnings": vr.warnings[:3],
            "length_extracted": schema.domain.length,
            "conductivity_extracted": schema.material.conductivity,
            "spec_built": spec is not None,
        })

    # ── Summary table ─────────────────────────────────────────────────────────
    _sep("SUMMARY")
    total_load = time.time() - t0
    print(f"\nTotal wall time (including model load): {total_load:.1f} s")
    print(f"Model: {filler.model_path}")
    print(f"Device: {filler._loaded_device}\n")

    col_w = 44
    print(f"  {'Case':<{col_w}} {'Valid':<6}  {'SpecBuilt':<10}  {'L(m)':<8}  {'k(W/mK)'}")
    print(f"  {'-'*col_w} {'-----':<6}  {'--------':<10}  {'-----':<8}  -------")
    for r in results:
        name = r["case"][:col_w]
        L = f"{r['length_extracted']:.4f}" if r['length_extracted'] else "None"
        k = f"{r['conductivity_extracted']:.1f}" if r['conductivity_extracted'] else "None"
        print(f"  {name:<{col_w}} {'Yes' if r['valid'] else 'No':<6}  "
              f"{'Yes' if r['spec_built'] else 'No':<10}  {L:<8}  {k}")

    filler.unload()
    print("\nDemo complete.")


if __name__ == "__main__":
    main()
