"""
pde_normalizer.py
=================
Two-path PDE-schema normalizer.

Architecture
------------

  Raw input
    ├─ Path A: StructuredInputParser   (deterministic, for clean YAML/dict)
    └─ Path B: LLMSchemaNormalizer     (LLM-assisted, for messy/semi-structured)
         ↓               ↓
       PDESchema      PDESchema  (same type from both paths)
              ↓
       PDESchemaValidator  (always deterministic)
              ↓
       PDESchemaMapper
              ↓
       ProblemSpec  ──► existing solver/verifier/replanner pipeline

Design principles
-----------------
* Path A is purely deterministic; it never calls an LLM.
* Path B uses an LLM adapter (or mock) to produce a *candidate* PDESchema
  dict, then applies the same deterministic validator as Path A.
  The LLM cannot bypass validation.
* Both paths share the same field-alias table, so alias normalization
  (e.g. ``rho`` → ``density``) is consistent regardless of path.
* This module has no side effects and no global state; all stateful objects
  (schemas, validation results) are returned to the caller.

Public API
----------
::

    from src.pde_normalizer import (
        normalize_structured,
        normalize_from_yaml,
        normalize_with_llm,
        normalize_from_text,
    )

    schema, vr = normalize_structured(raw_dict)       # Path A
    schema, vr = normalize_from_yaml("config.yaml")   # Path A via file
    schema, vr = normalize_with_llm(text, adapter)    # Path B
    schema, vr = normalize_from_text(text)             # Path B, mock adapter

The returned tuple is always ``(PDESchema, ValidationResult)``.
If validation fails and ``strict=True`` (default), a ValueError is raised.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

import yaml

from src.logging_utils import get_logger
from src.pde_schema import (
    BoundaryConditionSpec,
    BoundaryConditionsSpec,
    DomainSpec,
    InitialConditionSpec,
    MaterialSpec,
    ObservationSpec,
    PDESchema,
    PDESchemaMapper,
    PDESchemaValidator,
    SchemaMetadata,
    SolverPrefsSpec,
    TimeSpec,
    ValidationResult,
)

log = get_logger("pde_normalizer")


# ---------------------------------------------------------------------------
# Field-alias table
# ---------------------------------------------------------------------------
# Canonical path notation: "section.field"
# Each alias maps to one canonical path.  Applied by both parsing paths.

_FIELD_ALIASES: dict[str, str] = {
    # -- Geometry / domain --
    "L": "domain.length",
    "rod_length": "domain.length",
    "rod_length_m": "domain.length",
    "length": "domain.length",
    "domain_length": "domain.length",
    "ncells": "domain.n_cells_x",
    "n_cells": "domain.n_cells_x",
    "nx": "domain.n_cells_x",
    "num_cells": "domain.n_cells_x",

    # -- Material --
    "rho": "material.density",
    "density": "material.density",
    "density_kg_m3": "material.density",
    "mass_density": "material.density",
    "cp": "material.specific_heat",
    "specific_heat": "material.specific_heat",
    "specific_heat_J_kgK": "material.specific_heat",
    "heat_capacity": "material.specific_heat",
    "c_p": "material.specific_heat",
    "k": "material.conductivity",
    "conductivity": "material.conductivity",
    "conductivity_W_mK": "material.conductivity",
    "thermal_conductivity": "material.conductivity",
    "lambda": "material.conductivity",   # German notation

    # -- Initial condition --
    "T0": "initial_condition.value",
    "T_0": "initial_condition.value",
    "initial_temperature": "initial_condition.value",
    "initial_temperature_K": "initial_condition.value",
    "T_initial": "initial_condition.value",

    # -- Right boundary --
    "T_right": "bc_right_value",
    "right_temperature": "bc_right_value",
    "T_R": "bc_right_value",
    "right_bc_value": "bc_right_value",
    "bc_right_value": "bc_right_value",
    "right_boundary_temperature": "bc_right_value",

    # -- Time --
    "T_end": "time.end",
    "t_end": "time.end",
    "time_end": "time.end",
    "time_end_s": "time.end",
    "t_final": "time.end",
    "final_time": "time.end",
    "T_start": "time.start",
    "time_start": "time.start",
    "time_start_s": "time.start",
    "n_steps": "time.n_steps",
    "num_steps": "time.n_steps",
    "nt": "time.n_steps",
    "time_n_steps": "time.n_steps",

    # -- Observations --
    "sensors": "observation.sensor_positions",
    "sensor_positions": "observation.sensor_positions",
    "sensor_positions_m": "observation.sensor_positions",
    "sensor_x": "observation.sensor_positions",
    "observations_file": "observation.observations_file",
    "obs_file": "observation.observations_file",
    "observations_file_path": "observation.observations_file",
    "noise_std": "observation.noise_std",
    "noise_std_K": "observation.noise_std",
    "sigma": "observation.noise_std",
    "measurement_noise": "observation.noise_std",
}


# ---------------------------------------------------------------------------
# Path A: Deterministic structured parser
# ---------------------------------------------------------------------------


class StructuredInputParser:
    """Parse a clean dict (YAML-parsed or Python) into a PDESchema.

    Supports:
    * Nested YAML format (sections: ``problem``, ``geometry``, ``material``,
      ``initial_condition``, ``boundary_conditions``, ``observation``,
      ``sensors``, ``time``, ``planner``).
    * Legacy flat format (same top-level keys as the existing YAML files).
    * Field aliases via ``_FIELD_ALIASES``.
    * The ``example_case.yaml`` / ``default.yaml`` format used by the repo.
    """

    def parse(self, raw: dict[str, Any]) -> PDESchema:
        schema = PDESchema()
        schema.metadata = SchemaMetadata(source="structured_dict", parse_path="structured")
        self._parse_taxonomy(raw, schema)
        self._parse_domain(raw, schema)
        self._parse_material(raw, schema)
        self._parse_initial_condition(raw, schema)
        self._parse_boundary_conditions(raw, schema)
        self._parse_time(raw, schema)
        self._parse_observations(raw, schema)
        self._parse_solver_prefs(raw, schema)
        self._apply_aliases(raw, schema)
        self._apply_metadata(raw, schema)
        log.debug("StructuredInputParser: produced %s", schema.summary())
        return schema

    # ------------------------------------------------------------------
    # Section parsers
    # ------------------------------------------------------------------

    def _parse_taxonomy(self, raw: dict[str, Any], s: PDESchema) -> None:
        # Support nested 'problem' section OR flat top-level keys
        prob = raw.get("problem", {}) or {}

        def _get(*keys: str, default=None):
            for k in keys:
                if k in prob:
                    return prob[k]
                if k in raw:
                    return raw[k]
            return default

        pde_fam = _get("pde_family")
        if pde_fam:
            s.pde_family = str(pde_fam)

        eq_cls = _get("equation_class")
        if eq_cls:
            s.equation_class = str(eq_cls)

        pk = _get("problem_kind", "problem_type")
        if pk:
            # Translate legacy problem_type string
            pk_str = str(pk)
            if "IHCP" in pk_str or "inverse" in pk_str.lower():
                s.problem_kind = "inverse"
            elif "forward" in pk_str.lower():
                s.problem_kind = "forward"
            else:
                s.problem_kind = str(pk)  # type: ignore[assignment]

        dim = _get("dimension")
        if dim is not None:
            s.dimension = int(dim)

        tr = _get("transient")
        if tr is not None:
            s.transient = bool(tr)

        target = _get("unknown_target", "target_name", "target")
        if target:
            s.unknown_target = str(target)  # type: ignore[assignment]

    def _parse_domain(self, raw: dict[str, Any], s: PDESchema) -> None:
        geo = raw.get("geometry", raw.get("domain", {})) or {}
        d = s.domain

        length = geo.get("length", raw.get("rod_length_m", raw.get("rod_length")))
        if length is not None:
            d.length = float(length)

        n_cells = geo.get("n_cells", raw.get("n_cells"))
        if n_cells is not None:
            d.n_cells_x = int(n_cells)

        dt = geo.get("domain_type", raw.get("domain_type"))
        if dt:
            d.domain_type = str(dt)  # type: ignore[assignment]

        cs = geo.get("coord_system", raw.get("coord_system"))
        if cs:
            d.coord_system = str(cs)  # type: ignore[assignment]

        width = geo.get("width", raw.get("width"))
        if width is not None:
            d.width = float(width)

        height = geo.get("height", raw.get("height"))
        if height is not None:
            d.height = float(height)

    def _parse_material(self, raw: dict[str, Any], s: PDESchema) -> None:
        mat = raw.get("material", {}) or {}
        m = s.material

        # density
        rho = mat.get("density", mat.get("rho",
              raw.get("density_kg_m3", raw.get("density", raw.get("rho")))))
        if rho is not None:
            m.density = float(rho)

        # specific heat
        cp = mat.get("specific_heat", mat.get("cp",
             raw.get("specific_heat_J_kgK", raw.get("specific_heat", raw.get("cp")))))
        if cp is not None:
            m.specific_heat = float(cp)

        # conductivity
        k = mat.get("conductivity", mat.get("k",
            raw.get("conductivity_W_mK", raw.get("conductivity", raw.get("k")))))
        if k is not None:
            m.conductivity = float(k)

        # coefficient kinds (optional)
        for attr, keys in [
            ("density_kind", ["density_kind"]),
            ("specific_heat_kind", ["specific_heat_kind"]),
            ("conductivity_kind", ["conductivity_kind"]),
        ]:
            for key in keys:
                val = mat.get(key, raw.get(key))
                if val is not None:
                    setattr(m, attr, str(val))
                    break

        # source term
        src = mat.get("source_term", raw.get("source_term"))
        if src is not None:
            m.source_term = float(src)

    def _parse_initial_condition(self, raw: dict[str, Any], s: PDESchema) -> None:
        ic_raw = raw.get("initial_condition")

        if ic_raw is None:
            # Check flat aliases
            for key in ("T0", "T_0", "initial_temperature_K", "initial_temperature"):
                if key in raw:
                    s.initial_condition = InitialConditionSpec(
                        ic_type="uniform", value=float(raw[key])
                    )
                    return
            return

        if isinstance(ic_raw, (int, float)):
            s.initial_condition = InitialConditionSpec(
                ic_type="uniform", value=float(ic_raw)
            )
        elif isinstance(ic_raw, dict):
            ic = s.initial_condition
            ic.ic_type = str(ic_raw.get("type", ic.ic_type))  # type: ignore[assignment]
            if "value" in ic_raw:
                ic.value = float(ic_raw["value"])
            if "expression" in ic_raw:
                ic.expression = str(ic_raw["expression"])
            if "file" in ic_raw:
                ic.file = str(ic_raw["file"])
        else:
            log.warning("Unexpected initial_condition format: %r", ic_raw)

    def _parse_boundary_conditions(self, raw: dict[str, Any], s: PDESchema) -> None:
        bcs_raw = raw.get("boundary_conditions", {}) or {}
        conditions: list[BoundaryConditionSpec] = []

        # --- Nested rich format: boundary_conditions.left / .right / .conditions ---
        if "conditions" in bcs_raw:
            for item in bcs_raw["conditions"]:
                conditions.append(self._parse_one_bc(item))
        else:
            # Try individual location keys in the nested section
            for loc in ("left", "right", "top", "bottom", "inner", "outer"):
                if loc in bcs_raw:
                    bc_item = bcs_raw[loc]
                    if isinstance(bc_item, dict):
                        bc_item["location"] = loc
                        conditions.append(self._parse_one_bc(bc_item))

            # Legacy flat format: right_type / right_value at top level of BCs section
            if not conditions:
                right_type = bcs_raw.get("right_type", raw.get("bc_right_type", "dirichlet"))
                right_val = bcs_raw.get("right_value", raw.get("bc_right_value"))
                right_bc = BoundaryConditionSpec(
                    location="right",
                    bc_type=str(right_type),  # type: ignore[arg-type]
                    status="given",
                    value=float(right_val) if right_val is not None else None,
                )
                conditions.append(right_bc)
                # Left BC: always the inversion target in IHCP
                left_bc = BoundaryConditionSpec(
                    location="left",
                    bc_type="neumann",
                    status="inversion_target",
                    value=None,
                )
                conditions.append(left_bc)
            elif not any(c.location == "left" for c in conditions):
                # Add implied left inversion target if missing
                conditions.append(
                    BoundaryConditionSpec(
                        location="left",
                        bc_type="neumann",
                        status="inversion_target",
                        value=None,
                    )
                )

        # Override with flat top-level BC keys if present (legacy compat)
        if "bc_right_type" in raw or "bc_right_value" in raw:
            for c in conditions:
                if c.location == "right":
                    if "bc_right_type" in raw:
                        c.bc_type = str(raw["bc_right_type"])  # type: ignore[assignment]
                    if "bc_right_value" in raw:
                        c.value = float(raw["bc_right_value"])

        s.boundary_conditions = BoundaryConditionsSpec(conditions=conditions)

    def _parse_one_bc(self, item: dict[str, Any]) -> BoundaryConditionSpec:
        return BoundaryConditionSpec(
            location=str(item.get("location", "unknown")),
            bc_type=str(item.get("type", item.get("bc_type", "unknown"))),  # type: ignore[arg-type]
            status=str(item.get("status", "given")),  # type: ignore[arg-type]
            value=float(item["value"]) if item.get("value") is not None else None,
            expression=item.get("expression"),
        )

    def _parse_time(self, raw: dict[str, Any], s: PDESchema) -> None:
        t_raw = raw.get("time", {}) or {}
        t = s.time

        end = t_raw.get("end", raw.get("time_end_s", raw.get("time_end",
              raw.get("T_end", raw.get("t_end")))))
        if end is not None:
            t.end = float(end)

        start = t_raw.get("start", raw.get("time_start_s", raw.get("time_start", 0.0)))
        if start is not None:
            t.start = float(start)

        n_steps = t_raw.get("n_steps", raw.get("time_n_steps", raw.get("n_steps")))
        if n_steps is not None:
            t.n_steps = int(n_steps)

    def _parse_observations(self, raw: dict[str, Any], s: PDESchema) -> None:
        obs_raw = raw.get("observation", raw.get("observations", {})) or {}
        obs = s.observation

        # Sensor positions
        sensors = (
            obs_raw.get("sensor_positions")
            or raw.get("sensor_positions")
            or raw.get("sensor_positions_m")
            or raw.get("sensors")
        )
        if sensors is not None:
            obs.sensor_positions = [float(p) for p in sensors]

        # Observation data
        obs_file = (
            obs_raw.get("file")
            or obs_raw.get("observations_file")
            or raw.get("observations_file")
            or raw.get("observations_file_path")
        )
        if obs_file:
            obs.observations_file = str(obs_file)

        obs_arr = obs_raw.get("array", obs_raw.get("observations_array",
                  raw.get("observations_array")))
        if obs_arr is not None:
            obs.observations_array = obs_arr

        # Noise
        noise = (
            obs_raw.get("noise_std")
            or raw.get("noise_std")
            or raw.get("noise_std_K")
        )
        if noise is not None:
            obs.noise_std = float(noise)

        # Observed variable
        ov = obs_raw.get("observed_variable", raw.get("observed_variable"))
        if ov:
            obs.observed_variable = str(ov)  # type: ignore[assignment]

        # Noise model
        nm = obs_raw.get("noise_model", raw.get("noise_model"))
        if nm:
            obs.noise_model = str(nm)  # type: ignore[assignment]

    def _parse_solver_prefs(self, raw: dict[str, Any], s: PDESchema) -> None:
        planner = raw.get("planner", raw.get("solver_preferences", {})) or {}
        sp = s.solver_prefs

        for src_key, attr in [
            ("reg_order", "reg_order"),
            ("lambda_strategy", "lambda_strategy"),
            ("lambda_value", "lambda_value"),
            ("max_retries", "max_retries"),
            ("iteration_budget", "iteration_budget"),
            ("solver_name", "preferred_solver"),
            ("preferred_solver", "preferred_solver"),
        ]:
            val = planner.get(src_key, raw.get(src_key))
            if val is not None:
                if attr in ("reg_order", "max_retries", "iteration_budget"):
                    setattr(sp, attr, int(val))
                elif attr == "lambda_value":
                    setattr(sp, attr, float(val))
                else:
                    setattr(sp, attr, val)

        bounds = planner.get("physical_bounds", raw.get("physical_bounds"))
        if bounds is not None:
            if isinstance(bounds, (list, tuple)) and len(bounds) == 2:
                sp.physical_bounds = (float(bounds[0]), float(bounds[1]))

    def _apply_aliases(self, raw: dict[str, Any], s: PDESchema) -> None:
        """Apply top-level alias keys that weren't caught by section parsers."""
        for alias, canonical in _FIELD_ALIASES.items():
            if alias not in raw:
                continue
            val = raw[alias]
            if canonical == "domain.length" and s.domain.length is None:
                s.domain.length = float(val)
            elif canonical == "domain.n_cells_x" and s.domain.n_cells_x == 50:
                s.domain.n_cells_x = int(val)
            elif canonical == "material.density" and s.material.density is None:
                s.material.density = float(val)
            elif canonical == "material.specific_heat" and s.material.specific_heat is None:
                s.material.specific_heat = float(val)
            elif canonical == "material.conductivity" and s.material.conductivity is None:
                s.material.conductivity = float(val)
            elif canonical == "initial_condition.value":
                if s.initial_condition.value == 300.0 and alias not in ("T0", "T_0"):
                    s.initial_condition.value = float(val)
                elif alias in ("T0", "T_0"):
                    s.initial_condition.value = float(val)
            elif canonical == "bc_right_value":
                right_bc = s.boundary_conditions.get("right")
                if right_bc is not None and right_bc.value is None:
                    right_bc.value = float(val)
            elif canonical == "time.end" and s.time.end is None:
                s.time.end = float(val)
            elif canonical == "time.start":
                pass  # already set
            elif canonical == "time.n_steps" and s.time.n_steps is None:
                s.time.n_steps = int(val)
            elif canonical == "observation.sensor_positions" and not s.observation.sensor_positions:
                s.observation.sensor_positions = [float(p) for p in val]
            elif canonical == "observation.observations_file" and s.observation.observations_file is None:
                s.observation.observations_file = str(val)
            elif canonical == "observation.noise_std" and s.observation.noise_std is None:
                s.observation.noise_std = float(val)

    def _apply_metadata(self, raw: dict[str, Any], s: PDESchema) -> None:
        meta_raw = raw.get("metadata", {}) or {}
        if isinstance(meta_raw, dict):
            s.metadata.extra.update(meta_raw)
        # Store case_name if available
        if "case_name" in meta_raw:
            s.metadata.extra["case_name"] = meta_raw["case_name"]
        if "description" in raw:
            s.metadata.extra["description"] = str(raw["description"])[:500]


# ---------------------------------------------------------------------------
# Path B: LLM-assisted schema filling
# ---------------------------------------------------------------------------


@runtime_checkable
class LLMPDESchemaFiller(Protocol):
    """Protocol for an LLM backend that fills in a PDESchema from messy text.

    The LLM should return a dict that mirrors the structured YAML format
    (section keys: ``geometry``, ``material``, ``time``, etc.).  The returned
    dict is then fed to ``StructuredInputParser`` for alias resolution and
    proper type coercion, and finally to ``PDESchemaValidator``.

    The LLM never sees or modifies the final PDESchema directly; it only
    produces an intermediate candidate dict.

    Implementors
    ------------
    * ``MockPDESchemaFiller``    – regex/keyword mock (no external calls)
    * ``QwenPDESchemaFiller``    – wraps the existing QwenLocalAdapter (TODO)
    * (future) OpenAI / Anthropic structured-output adapters
    """

    def fill_schema(self, text: str) -> dict[str, Any]:
        """Extract PDE problem fields from *text*.

        Returns a partial or complete dict in the canonical YAML format.
        Fields that cannot be extracted should be omitted (not None'd out).
        Returns ``{}`` on total failure rather than raising.
        """
        ...


@dataclass
class LLMFillResult:
    """Result of an LLM-assisted schema fill attempt."""

    raw_output: dict[str, Any]
    confidence: float
    warnings: list[str] = field(default_factory=list)


class MockPDESchemaFiller:
    """Mock LLM schema filler using deterministic regex / keyword extraction.

    This class implements the ``LLMPDESchemaFiller`` protocol without any
    external API calls.  It is designed for:
    * Unit testing the LLM-assisted path
    * Demonstrating the two-path architecture when no real LLM is available
    * Providing a reference implementation for real adapters to follow

    Limitations (by design – this is a mock, not a real NLP system):
    * Recognises ~20 specific textual patterns; will miss creative phrasings.
    * No unit conversion; assumes SI units in the text.
    * No coreference resolution.
    """

    # Patterns: (field_path, regex)
    _PATTERNS: list[tuple[str, re.Pattern]] = [
        # Geometry
        ("geometry.length",
         re.compile(r"(?:rod\s+length|length|L)\s*[=:]\s*([\d.eE+\-]+)\s*m", re.I)),
        ("geometry.n_cells",
         re.compile(r"n_cells\s*[=:]\s*(\d+)", re.I)),
        # Material
        ("material.density",
         re.compile(r"(?:rho|density|ρ)\s*[=:]\s*([\d.eE+\-]+)\s*kg", re.I)),
        ("material.specific_heat",
         re.compile(r"(?:cp|c_p|specific\s+heat|heat\s+capacity)\s*[=:]\s*([\d.eE+\-]+)\s*J", re.I)),
        ("material.conductivity",
         re.compile(r"(?:k|conductivity|thermal\s+conductivity)\s*[=:]\s*([\d.eE+\-]+)\s*W", re.I)),
        # Initial / boundary temperatures
        ("initial_condition",
         re.compile(r"(?:T0|T_0|initial\s+temp(?:erature)?)\s*[=:]\s*([\d.eE+\-]+)\s*K", re.I)),
        ("bc_right_value",
         re.compile(
             r"(?:T_right|right\s+(?:boundary\s+)?temp(?:erature)?|right\s+BC\s+(?:value|temp))"
             r"\s*[=:]\s*([\d.eE+\-]+)\s*K", re.I
         )),
        # Time
        ("time.end",
         re.compile(r"(?:T_end|t_end|time\s+end|total\s+time|end\s+time)\s*[=:]\s*([\d.eE+\-]+)\s*s", re.I)),
        ("time.n_steps",
         re.compile(r"(?:n_steps|num_steps|time\s+steps|nt)\s*[=:]\s*(\d+)", re.I)),
        # Noise
        ("noise_std",
         re.compile(r"(?:noise_std|noise|sigma|σ)\s*[=:]\s*([\d.eE+\-]+)\s*K", re.I)),
        # Observations file
        ("observations_file",
         re.compile(r"(?:observations?|data)\s*[=:]\s*[\"']?([^\s\"']+\.csv)[\"']?", re.I)),
    ]

    # Known material names → properties (rho, cp, k)
    _KNOWN_MATERIALS: dict[str, dict[str, float]] = {
        "steel": {"density": 7800.0, "specific_heat": 500.0, "conductivity": 50.0},
        "aluminum": {"density": 2700.0, "specific_heat": 900.0, "conductivity": 205.0},
        "aluminium": {"density": 2700.0, "specific_heat": 900.0, "conductivity": 205.0},
        "copper": {"density": 8960.0, "specific_heat": 385.0, "conductivity": 401.0},
        "iron": {"density": 7874.0, "specific_heat": 449.0, "conductivity": 80.0},
        "concrete": {"density": 2300.0, "specific_heat": 880.0, "conductivity": 1.7},
    }

    def fill_schema(self, text: str) -> dict[str, Any]:
        """Extract fields from *text* using regex patterns."""
        out: dict[str, Any] = {}
        warnings: list[str] = []

        # Apply scalar patterns
        for field_path, pattern in self._PATTERNS:
            m = pattern.search(text)
            if not m:
                continue
            raw_val = m.group(1)
            try:
                if "n_steps" in field_path or "n_cells" in field_path:
                    val: Any = int(raw_val)
                elif field_path in ("observations_file",):
                    val = raw_val
                else:
                    val = float(raw_val)
                # Nest into dict
                parts = field_path.split(".")
                node = out
                for p in parts[:-1]:
                    node = node.setdefault(p, {})
                node[parts[-1]] = val
            except ValueError:
                warnings.append(f"Could not parse '{raw_val}' for {field_path}")

        # Sensor positions: "sensors at X m and Y m" or "sensor_positions: [X, Y]"
        sensor_pats = [
            re.compile(
                r"sensor[s]?\s+(?:at|located\s+at|position[s]?)\s+([\d.,\s]+(?:m\s+and\s+[\d.,\s]+)?)\s*m",
                re.I,
            ),
            re.compile(r"sensor_positions\s*[=:]\s*\[([\d.,\s]+)\]", re.I),
            re.compile(r"(?:at|positions?)\s+([\d.]+)\s*m\s+and\s+([\d.]+)\s*m", re.I),
        ]
        for sp in sensor_pats:
            sm = sp.search(text)
            if sm:
                groups = sm.groups()
                if len(groups) == 2 and groups[1]:
                    # Two-group pattern: "at X m and Y m"
                    try:
                        positions = [float(groups[0].strip()), float(groups[1].strip())]
                        out.setdefault("sensor_positions", positions)
                        break
                    except ValueError:
                        pass
                else:
                    vals_str = groups[0]
                    cleaned = re.sub(r"\band\b", " ", vals_str, flags=re.I)
                    try:
                        positions = [
                            float(v.strip())
                            for v in re.split(r"[,\s]+", cleaned)
                            if re.match(r"[\d.eE+\-]+", v.strip())
                        ]
                        if positions:
                            out.setdefault("sensor_positions", positions)
                            break
                    except ValueError:
                        pass

        # Material name recognition
        for mat_name, props in self._KNOWN_MATERIALS.items():
            if re.search(rf"\b{mat_name}\b", text, re.I):
                mat_node = out.setdefault("material", {})
                for prop_key, prop_val in props.items():
                    mat_node.setdefault(prop_key, prop_val)
                break  # Use first matched material

        # Dimension hint
        if re.search(r"\b1[- ]?D\b|\bone[- ]?dimensional\b", text, re.I):
            out.setdefault("dimension", 1)

        # Transient hint
        if re.search(r"\btransient\b|\btime-?dependent\b|\bunsteady\b", text, re.I):
            out.setdefault("transient", True)

        # Inverse hint
        if re.search(r"\binverse\b|\brecover\b|\breconstruct\b|\bestimate\b", text, re.I):
            out.setdefault("problem_kind", "inverse")

        # Left boundary is unknown flux
        if re.search(
            r"left\s+(?:boundary\s+)?(?:heat\s+flux|BC|boundary)\s+(?:is\s+)?unknown"
            r"|unknown\s+(?:heat\s+)?flux\s+at\s+(?:the\s+)?left",
            text, re.I,
        ):
            out.setdefault("_left_bc_is_target", True)

        # Metadata
        out["_mock_warnings"] = warnings
        return out


# ---------------------------------------------------------------------------
# Public normalizer functions
# ---------------------------------------------------------------------------


def normalize_structured(
    raw: dict[str, Any],
    *,
    strict: bool = True,
) -> tuple[PDESchema, ValidationResult]:
    """Path A: deterministic normalisation for clean structured input.

    Parameters
    ----------
    raw    : dict in YAML or flat format
    strict : if True (default), raise ValueError on validation failure

    Returns
    -------
    (PDESchema, ValidationResult)
    """
    parser = StructuredInputParser()
    schema = parser.parse(raw)
    vr = PDESchemaValidator().validate(schema)
    if schema.metadata.warnings:
        vr.warnings.extend(schema.metadata.warnings)
    if strict and not vr.valid:
        raise ValueError(
            "PDESchema validation failed (Path A):\n"
            + "\n".join(f"  - {e}" for e in vr.errors)
        )
    log.info(
        "normalize_structured: valid=%s, errors=%d, warnings=%d",
        vr.valid, len(vr.errors), len(vr.warnings),
    )
    return schema, vr


def normalize_from_yaml(
    config_path: str | Path,
    observations_path: str | Path | None = None,
    *,
    strict: bool = True,
) -> tuple[PDESchema, ValidationResult]:
    """Path A: load YAML file and normalise deterministically.

    Parameters
    ----------
    config_path       : path to YAML config
    observations_path : optional observations CSV path override
    strict            : raise on validation failure

    Returns
    -------
    (PDESchema, ValidationResult)
    """
    config_path = Path(config_path)
    log.info("normalize_from_yaml: %s", config_path)
    with config_path.open("r", encoding="utf-8") as fh:
        raw: dict[str, Any] = yaml.safe_load(fh)

    if observations_path is not None:
        raw["observations_file"] = str(observations_path)

    schema, vr = normalize_structured(raw, strict=strict)
    schema.metadata.source = str(config_path)
    return schema, vr


def normalize_with_llm(
    text: str,
    adapter: LLMPDESchemaFiller,
    *,
    strict: bool = True,
    confidence_threshold: float = 0.0,
) -> tuple[PDESchema, ValidationResult]:
    """Path B: LLM-assisted normalisation for messy / semi-structured input.

    The LLM adapter produces a candidate dict; deterministic validation is
    always applied afterward.  The LLM never owns the final schema decision.

    Parameters
    ----------
    text                : raw input text
    adapter             : object implementing ``LLMPDESchemaFiller.fill_schema``
    strict              : raise on validation failure
    confidence_threshold: minimum confidence to accept the LLM result
                          (adapter.fill_schema result is inspected for a
                          ``_confidence`` key if present)

    Returns
    -------
    (PDESchema, ValidationResult)
    """
    log.info("normalize_with_llm: len=%d chars, adapter=%s", len(text), type(adapter).__name__)

    candidate: dict[str, Any] = {}
    try:
        candidate = adapter.fill_schema(text)
    except Exception as exc:  # noqa: BLE001
        log.warning("LLM adapter raised: %s; falling back to empty candidate", exc)
        candidate = {}

    # Extract adapter-internal metadata before passing to parser.
    # Accept both _llm_warnings (real adapters) and _mock_warnings (mock).
    confidence = float(candidate.pop("_confidence", 1.0))
    llm_warnings: list[str] = (
        candidate.pop("_llm_warnings", None)
        or candidate.pop("_mock_warnings", [])
    )
    left_bc_target: bool = bool(candidate.pop("_left_bc_is_target", False))
    # Strip extra metadata keys produced by real adapters
    inference_meta: dict[str, Any] = candidate.pop("_inference_meta", {})
    candidate.pop("_raw_output", None)

    if confidence < confidence_threshold:
        raise ValueError(
            f"LLM adapter confidence {confidence:.2f} is below threshold "
            f"{confidence_threshold:.2f}"
        )

    # If the LLM flagged that the left BC is the inversion target, ensure the
    # structured parser sees it in a form it understands.
    if left_bc_target and "boundary_conditions" not in candidate:
        candidate.setdefault("boundary_conditions", {})
        # The structured parser will add left inversion target by default

    # Run through the deterministic structured parser for alias resolution
    parser = StructuredInputParser()
    schema = parser.parse(candidate)

    # Stamp LLM-specific metadata
    schema.metadata.source = "llm_assisted"
    schema.metadata.parse_path = "llm_assisted"
    schema.metadata.confidence = confidence
    schema.metadata.raw_input_preview = text[:300]
    if llm_warnings:
        schema.metadata.warnings.extend(llm_warnings)
    if inference_meta:
        schema.metadata.extra["inference_meta"] = inference_meta

    # Deterministic validation (always, regardless of LLM confidence)
    vr = PDESchemaValidator().validate(schema)
    vr.warnings.extend(schema.metadata.warnings)

    if strict and not vr.valid:
        raise ValueError(
            "PDESchema validation failed (Path B / LLM-assisted):\n"
            + "\n".join(f"  - {e}" for e in vr.errors)
        )
    log.info(
        "normalize_with_llm: valid=%s, errors=%d, warnings=%d, confidence=%.2f",
        vr.valid, len(vr.errors), len(vr.warnings), confidence,
    )
    return schema, vr


def normalize_from_text(
    text: str,
    *,
    strict: bool = False,
) -> tuple[PDESchema, ValidationResult]:
    """Path B with the built-in mock filler (no real LLM).

    Convenience wrapper that uses ``MockPDESchemaFiller``.  Useful for
    semi-structured text where a real LLM is not available.
    ``strict=False`` by default because text extraction is often incomplete.
    """
    mock = MockPDESchemaFiller()
    return normalize_with_llm(text, mock, strict=strict)


def build_problem_spec_from_schema(
    schema: PDESchema,
    vr: ValidationResult,
    *,
    csv_loader=None,
) -> Any:
    """Convert a validated PDESchema to a ProblemSpec.

    Parameters
    ----------
    schema     : validated PDESchema
    vr         : ValidationResult from the validator (used for logging)
    csv_loader : optional custom CSV loader (injected in tests)

    Returns
    -------
    ProblemSpec
    """
    if not vr.valid:
        raise ValueError(
            "Cannot build ProblemSpec from invalid PDESchema; "
            f"errors: {vr.errors}"
        )
    mapper = PDESchemaMapper(csv_loader=csv_loader)
    return mapper.map(schema)


def normalize_with_local_qwen(
    text: str,
    model_path: str | None = None,
    *,
    strict: bool = False,
    **filler_kwargs: Any,
) -> tuple[PDESchema, ValidationResult]:
    """Path B convenience wrapper: normalise *text* using a local Qwen model.

    This is the main entry point for the real LLM-assisted normalisation path.
    It instantiates a ``LocalQwenPDESchemaFiller`` (loading the model lazily
    on first call), calls ``normalize_with_llm``, and returns the result.

    The model path is resolved in priority order:
    1. ``model_path`` argument
    2. ``QWEN_MODEL_PATH`` environment variable
    3. Compiled-in default: ``/root/models/Qwen/Qwen2___5-3B-Instruct``

    Parameters
    ----------
    text        : messy / semi-structured input text
    model_path  : optional explicit path to the local model directory
    strict      : if True, raise ValueError when validation fails
    **filler_kwargs : forwarded to ``LocalQwenPDESchemaFiller(...)``

    Returns
    -------
    (PDESchema, ValidationResult)

    Example
    -------
    ::

        schema, vr = normalize_with_local_qwen(
            "Steel rod L=0.05m, rho=7800, k=50, right bc 300K, sensors at 0.01 0.03 m, T_end=60s",
            strict=False,
        )
        print(vr.valid, schema.summary())
    """
    # Lazy import to avoid loading torch/transformers at module import time
    from src.qwen_pde_filler import LocalQwenPDESchemaFiller

    filler = LocalQwenPDESchemaFiller(model_path=model_path, **filler_kwargs)
    return normalize_with_llm(text, filler, strict=strict)
