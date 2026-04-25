"""
input_normalizer.py
===================
Backward-compatible input normalization layer.

This module preserves the original public API (``NormalizedSchema``,
``normalize_from_yaml``, ``normalize_from_dict``, ``normalize_from_text``)
while delegating the heavy lifting to the new PDE-schema layer in
``src/pde_normalizer.py``.

Architecture overview
---------------------

Old design (pre-upgrade)
  Raw input → NormalizedSchema (flat, IHCP-only) → ProblemSpec

New design (post-upgrade)
  Raw input
    ├─ Path A (clean structured) → PDESchema → PDESchemaValidator → ProblemSpec
    └─ Path B (messy / LLM-assisted) → PDESchema → PDESchemaValidator → ProblemSpec

``NormalizedSchema`` is now a *thin adapter* on top of ``PDESchema``.  Its
``to_problem_spec()`` method delegates to ``PDESchemaMapper``.  All public
entry points (``normalize_from_yaml``, ``normalize_from_dict``,
``normalize_from_text``) now return a ``NormalizedSchema`` instance that
internally holds the full ``PDESchema`` so callers can inspect it.

Diagnosis of the old design
----------------------------
1. ``NormalizedSchema`` was a *flat dataclass* mirroring IHCP-specific config
   keys (``rod_length_m``, ``bc_right_type``, etc.).  There was no PDE-level
   concept (equation class, domain type, coordinate system, coefficient
   variability, BC status, observation layout, …).

2. ``_dict_to_schema()`` was a single ~100-line function that parsed both
   YAML-nested and flat keys with ad-hoc ``if "X" in raw`` guards.  It had no
   alias table and no concept of field precedence.

3. ``normalize_from_text()`` used 13 hardcoded regex patterns.  It had no
   material name recognition, no LLM path, and no confidence tracking.

4. Validation was limited to ``is_complete()`` / ``missing_fields()``.  There
   were no PDE semantic checks (Fourier number, sensor-in-domain, BC
   consistency, inversion-target designation).

5. The LLM path was a stub comment ("Future version can add …"); it did not
   target a PDE schema object and could not be tested independently.

What changed
------------
* NormalizedSchema now wraps PDESchema (added ``pde_schema`` attribute).
* All parsing delegates to ``pde_normalizer.StructuredInputParser`` (Path A)
  or ``pde_normalizer.MockPDESchemaFiller`` (Path B).
* ``to_problem_spec()`` delegates to ``PDESchemaMapper``.
* Backward-compatible properties expose old flat field names.
* Old public API is 100 % preserved; existing tests and demos still pass.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from src.logging_utils import get_logger
from src.pde_normalizer import (
    MockPDESchemaFiller,
    PDESchemaMapper,
    PDESchemaValidator,
    StructuredInputParser,
    normalize_from_text as _pde_normalize_from_text,
    normalize_from_yaml as _pde_normalize_from_yaml,
    normalize_structured as _pde_normalize_structured,
    normalize_with_llm as _pde_normalize_with_llm,
)
from src.pde_schema import PDESchema, ValidationResult
from src.types import BoundaryConditions, Geometry, Material, ProblemSpec

log = get_logger("input_normalizer")


# ---------------------------------------------------------------------------
# NormalizedSchema – backward-compatible adapter
# ---------------------------------------------------------------------------


@dataclass
class NormalizedSchema:
    """Backward-compatible adapter wrapping the new PDESchema.

    Exposes all original flat field names as properties for compatibility
    with existing code.  Internally delegates to a ``PDESchema`` instance.

    NEW: ``pde_schema`` attribute holds the full PDE-level schema for callers
    that want richer introspection.  ``validation_result`` holds the last
    validation outcome.
    """

    # The underlying PDE schema – the source of truth
    pde_schema: PDESchema = field(default_factory=PDESchema)
    validation_result: ValidationResult | None = None

    # -----------------------------------------------------------------
    # Properties: expose old flat field names for backward compatibility
    # -----------------------------------------------------------------

    @property
    def pde_family(self) -> str:
        return self.pde_schema.pde_family

    @property
    def problem_type(self) -> str:
        dim = self.pde_schema.dimension
        kind = "IHCP" if self.pde_schema.problem_kind == "inverse" else "FP"
        tr = "transient_" if self.pde_schema.transient else ""
        return f"{dim}D_{tr}{kind}"

    @property
    def dimension(self) -> int:
        return self.pde_schema.dimension

    @property
    def transient(self) -> bool:
        return self.pde_schema.transient

    @property
    def unknown_target(self) -> str:
        return self.pde_schema.unknown_target

    @property
    def rod_length_m(self) -> float | None:
        return self.pde_schema.domain.length

    @rod_length_m.setter
    def rod_length_m(self, v: float | None) -> None:
        self.pde_schema.domain.length = v

    @property
    def n_cells(self) -> int:
        return self.pde_schema.domain.n_cells_x

    @n_cells.setter
    def n_cells(self, v: int) -> None:
        self.pde_schema.domain.n_cells_x = v

    @property
    def density_kg_m3(self) -> float | None:
        return self.pde_schema.material.density

    @density_kg_m3.setter
    def density_kg_m3(self, v: float | None) -> None:
        self.pde_schema.material.density = v

    @property
    def specific_heat_J_kgK(self) -> float | None:
        return self.pde_schema.material.specific_heat

    @specific_heat_J_kgK.setter
    def specific_heat_J_kgK(self, v: float | None) -> None:
        self.pde_schema.material.specific_heat = v

    @property
    def conductivity_W_mK(self) -> float | None:
        return self.pde_schema.material.conductivity

    @conductivity_W_mK.setter
    def conductivity_W_mK(self, v: float | None) -> None:
        self.pde_schema.material.conductivity = v

    @property
    def initial_temperature_K(self) -> float:
        return self.pde_schema.initial_condition.value

    @initial_temperature_K.setter
    def initial_temperature_K(self, v: float) -> None:
        self.pde_schema.initial_condition.value = v

    @property
    def bc_right_type(self) -> str:
        bc = self.pde_schema.boundary_conditions.get("right")
        return bc.bc_type if bc is not None else "dirichlet"

    @bc_right_type.setter
    def bc_right_type(self, v: str) -> None:
        bc = self.pde_schema.boundary_conditions.get("right")
        if bc is not None:
            bc.bc_type = v  # type: ignore[assignment]

    @property
    def bc_right_value(self) -> float:
        bc = self.pde_schema.boundary_conditions.get("right")
        return bc.value if (bc is not None and bc.value is not None) else 300.0

    @bc_right_value.setter
    def bc_right_value(self, v: float) -> None:
        bc = self.pde_schema.boundary_conditions.get("right")
        if bc is not None:
            bc.value = float(v)

    @property
    def time_start_s(self) -> float:
        return self.pde_schema.time.start

    @time_start_s.setter
    def time_start_s(self, v: float) -> None:
        self.pde_schema.time.start = v

    @property
    def time_end_s(self) -> float | None:
        return self.pde_schema.time.end

    @time_end_s.setter
    def time_end_s(self, v: float | None) -> None:
        self.pde_schema.time.end = v

    @property
    def time_n_steps(self) -> int | None:
        return self.pde_schema.time.n_steps

    @time_n_steps.setter
    def time_n_steps(self, v: int | None) -> None:
        self.pde_schema.time.n_steps = v

    @property
    def sensor_positions_m(self) -> list[float]:
        return self.pde_schema.observation.sensor_positions

    @sensor_positions_m.setter
    def sensor_positions_m(self, v: list[float]) -> None:
        self.pde_schema.observation.sensor_positions = v

    @property
    def observations_file(self) -> str | None:
        return self.pde_schema.observation.observations_file

    @observations_file.setter
    def observations_file(self, v: str | None) -> None:
        self.pde_schema.observation.observations_file = v

    @property
    def observations_array(self) -> list[list[float]] | None:
        return self.pde_schema.observation.observations_array

    @observations_array.setter
    def observations_array(self, v: list[list[float]] | None) -> None:
        self.pde_schema.observation.observations_array = v

    @property
    def noise_std_K(self) -> float | None:
        return self.pde_schema.observation.noise_std

    @noise_std_K.setter
    def noise_std_K(self, v: float | None) -> None:
        self.pde_schema.observation.noise_std = v

    @property
    def solver_preferences(self) -> dict[str, Any]:
        sp = self.pde_schema.solver_prefs
        d: dict[str, Any] = {}
        if sp.reg_order is not None:
            d["reg_order"] = sp.reg_order
        if sp.lambda_strategy is not None:
            d["lambda_strategy"] = sp.lambda_strategy
        if sp.lambda_value is not None:
            d["lambda_value"] = sp.lambda_value
        if sp.max_retries is not None:
            d["max_retries"] = sp.max_retries
        if sp.iteration_budget is not None:
            d["iteration_budget"] = sp.iteration_budget
        if sp.physical_bounds is not None:
            d["physical_bounds"] = list(sp.physical_bounds)
        return d

    @property
    def metadata(self) -> dict[str, Any]:
        return self.pde_schema.metadata.extra

    # -----------------------------------------------------------------
    # Completeness checks (preserved API)
    # -----------------------------------------------------------------

    def is_complete(self) -> bool:
        """Return True if all required fields are populated."""
        required = [
            self.rod_length_m,
            self.density_kg_m3,
            self.specific_heat_J_kgK,
            self.conductivity_W_mK,
            self.time_end_s,
            self.time_n_steps,
            self.sensor_positions_m,
        ]
        obs_ok = (
            self.observations_file is not None
            or self.observations_array is not None
        )
        return all(v is not None for v in required) and obs_ok

    def missing_fields(self) -> list[str]:
        """Return names of required fields that are not yet populated."""
        missing = []
        if self.rod_length_m is None:
            missing.append("rod_length_m")
        if self.density_kg_m3 is None:
            missing.append("density_kg_m3")
        if self.specific_heat_J_kgK is None:
            missing.append("specific_heat_J_kgK")
        if self.conductivity_W_mK is None:
            missing.append("conductivity_W_mK")
        if self.time_end_s is None:
            missing.append("time_end_s")
        if self.time_n_steps is None:
            missing.append("time_n_steps")
        if not self.sensor_positions_m:
            missing.append("sensor_positions_m")
        if self.observations_file is None and self.observations_array is None:
            missing.append("observations (file or array)")
        return missing

    # -----------------------------------------------------------------
    # Conversion (preserved API)
    # -----------------------------------------------------------------

    def to_problem_spec(self) -> ProblemSpec:
        """Convert this schema to a ProblemSpec.

        Delegates to PDESchemaMapper for the actual conversion.
        Raises ValueError if any required field is missing.
        """
        missing = self.missing_fields()
        if missing:
            raise ValueError(
                f"NormalizedSchema is incomplete; missing: {missing}"
            )
        # Re-run validation before mapping
        vr = PDESchemaValidator().validate(self.pde_schema)
        if not vr.valid:
            raise ValueError(
                f"PDESchema is invalid; errors: {vr.errors}"
            )
        mapper = PDESchemaMapper()
        spec = mapper.map(self.pde_schema)
        log.info(
            "NormalizedSchema → ProblemSpec: n_time=%d, n_sensors=%d",
            spec.n_time, spec.n_sensors,
        )
        return spec


# ---------------------------------------------------------------------------
# Public normalizer entry points (preserved API)
# ---------------------------------------------------------------------------


def normalize_from_yaml(
    config_path: str | Path,
    observations_path: str | Path | None = None,
) -> NormalizedSchema:
    """Build a NormalizedSchema from a YAML problem config file.

    Delegates to the new PDE-schema layer (Path A / structured).

    Parameters
    ----------
    config_path       : path to YAML config
    observations_path : optional CSV path override
    """
    config_path = Path(config_path)
    log.info("normalize_from_yaml: %s", config_path)
    pde_schema, vr = _pde_normalize_from_yaml(
        config_path,
        observations_path,
        strict=False,    # we want to return the schema even if partially invalid
    )
    ns = NormalizedSchema(pde_schema=pde_schema, validation_result=vr)
    log.info(
        "normalize_from_yaml: complete=%s valid=%s",
        ns.is_complete(), vr.valid,
    )
    return ns


def normalize_from_dict(data: dict[str, Any]) -> NormalizedSchema:
    """Build a NormalizedSchema from a Python dict.

    The dict may use YAML-style nesting or flat ``NormalizedSchema`` field names.
    Delegates to the new PDE-schema layer (Path A / structured).
    """
    log.info("normalize_from_dict: keys=%s", list(data.keys()))
    pde_schema, vr = _pde_normalize_structured(data, strict=False)
    ns = NormalizedSchema(pde_schema=pde_schema, validation_result=vr)
    log.info(
        "normalize_from_dict: complete=%s valid=%s missing=%s",
        ns.is_complete(), vr.valid, ns.missing_fields(),
    )
    return ns


def normalize_from_text(text: str) -> NormalizedSchema:
    """Build a NormalizedSchema from semi-structured text.

    Delegates to the new Path B (MockPDESchemaFiller) for regex/keyword
    extraction, then runs the deterministic validator.

    Limitations: only deterministic regex patterns; no LLM inference.
    For production use with free-form text, call
    ``pde_normalizer.normalize_with_llm()`` with a real LLM adapter.
    """
    log.info("normalize_from_text: len=%d chars", len(text))
    pde_schema, vr = _pde_normalize_from_text(text, strict=False)
    pde_schema.metadata.extra["raw_text"] = text[:200]
    ns = NormalizedSchema(pde_schema=pde_schema, validation_result=vr)
    log.info(
        "normalize_from_text: complete=%s valid=%s missing=%s",
        ns.is_complete(), vr.valid, ns.missing_fields(),
    )
    return ns


# ---------------------------------------------------------------------------
# CSV loading helper (preserved for external callers)
# ---------------------------------------------------------------------------


def _load_observations_csv(
    path: Path,
    n_sensors: int,
    n_steps: int,
) -> list[list[float]]:
    """Load CSV observations (rows=time, cols=sensors) into sensor-major form.

    This function is kept for backward compatibility with callers that import
    it directly.  The canonical implementation is now in ``pde_schema.py``
    (``_default_csv_loader``).
    """
    import csv as _csv

    if not path.exists():
        raise FileNotFoundError(f"Observations file not found: {path}")

    rows: list[list[float]] = []
    with path.open("r", newline="", encoding="utf-8") as fh:
        reader = _csv.reader(fh)
        header_skipped = False
        for row in reader:
            try:
                vals = [float(v) for v in row]
                rows.append(vals)
            except ValueError:
                if not header_skipped:
                    header_skipped = True
                    continue
                raise

    arr = np.array(rows, dtype=float)
    if arr.ndim == 1:
        arr = arr.reshape(-1, 1)
    if arr.shape[0] > n_steps:
        arr = arr[:n_steps, :]
    elif arr.shape[0] < n_steps:
        pad = np.zeros((n_steps - arr.shape[0], arr.shape[1]))
        arr = np.vstack([arr, pad])
    if arr.shape[1] != n_sensors:
        raise ValueError(
            f"Observations CSV has {arr.shape[1]} sensor columns but "
            f"schema expects {n_sensors}"
        )
    return arr.T.tolist()
