"""
input_normalizer.py
===================
Input normalization layer: converts multiple input representations into a
single unified internal schema (NormalizedSchema), then builds a ProblemSpec.

This sits in front of the existing parser so that different input formats
can feed into the same downstream scientific pipeline without any changes
to the core solver, verifier, or replanner modules.

Supported input formats
-----------------------
1. Structured YAML config  – ``normalize_from_yaml`` reads the YAML file
   directly (not via parser.py) and maps its nested dict into a flat
   NormalizedSchema.  This path produces a schema that, when converted via
   ``to_problem_spec()``, is byte-for-byte identical to what parser.py
   produces.  Both paths coexist intentionally: parser.py remains the
   low-level canonical parser; normalize_from_yaml is the higher-level
   path that returns an inspectable intermediate schema.

2. Python dict with partial or full problem data  – ``normalize_from_dict``.
   The dict may use YAML-style nesting or the flat NormalizedSchema field
   names (e.g. ``rod_length_m``).

3. Minimal semi-structured text  – ``normalize_from_text``.  Deterministic
   regex extraction only; not a general natural-language parser.  Recognizes
   patterns like "k = 50 W/(m·K)", "T_end = 60 s", "sensors at 0.01 m and
   0.03 m".

CSV loading note
----------------
``_load_observations_csv`` in this module mirrors ``_load_observations`` in
parser.py.  They are kept separate so this module has no import dependency on
parser.py.  If parser.py's CSV logic changes, update both functions.

Extension note
--------------
A future version can add a ``normalize_from_excel()`` entry point or plug in
an LLM-based text extractor by implementing the ``ProblemParserLLM`` protocol
from ``llm_hooks.py``.  The NormalizedSchema and its ``to_problem_spec()``
method remain stable regardless of how the schema was populated.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from src.logging_utils import get_logger
from src.types import BoundaryConditions, Geometry, Material, ProblemSpec

log = get_logger("input_normalizer")


# ---------------------------------------------------------------------------
# Unified internal schema
# ---------------------------------------------------------------------------


@dataclass
class NormalizedSchema:
    """Unified internal representation of an IHCP problem instance.

    Every field is explicit.  The schema is input-format agnostic: it does not
    matter whether the data came from a YAML file, a Python dict, or a text
    extraction.

    Fields marked with a default of None are optional; downstream code must
    handle the None case appropriately.

    Design intent
    -------------
    This schema is the single contract between input parsing and the scientific
    core.  It mirrors the logical structure of the inverse problem rather than
    the syntax of any particular file format.
    """

    # --- Problem taxonomy ---
    pde_family: str = "parabolic"              # "parabolic" (heat eq.)
    problem_type: str = "1D_transient_IHCP"
    dimension: int = 1
    transient: bool = True
    unknown_target: str = "boundary_heat_flux"

    # --- Geometry ---
    rod_length_m: float | None = None          # [m]
    n_cells: int = 50

    # --- Material properties ---
    density_kg_m3: float | None = None         # rho [kg/m³]
    specific_heat_J_kgK: float | None = None   # cp [J/(kg·K)]
    conductivity_W_mK: float | None = None     # k [W/(m·K)]

    # --- Initial condition ---
    initial_temperature_K: float = 300.0       # uniform T(x, t=0) [K]

    # --- Boundary conditions ---
    bc_right_type: str = "dirichlet"           # "dirichlet" or "neumann"
    bc_right_value: float = 300.0              # T_right [K] or q_right [W/m²]
    # Left BC (x=0) is the UNKNOWN to be recovered; not stored here.

    # --- Time discretisation ---
    time_start_s: float = 0.0                  # [s]
    time_end_s: float | None = None            # [s]
    time_n_steps: int | None = None

    # --- Observations ---
    sensor_positions_m: list[float] = field(default_factory=list)
    observations_file: str | None = None       # path to CSV
    observations_array: list[list[float]] | None = None  # shape (n_sensors, n_t)

    # --- Noise ---
    noise_std_K: float | None = None           # measurement noise [K]

    # --- Solver preferences (optional) ---
    solver_preferences: dict[str, Any] = field(default_factory=dict)

    # --- Free-form metadata ---
    metadata: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Derived helpers
    # ------------------------------------------------------------------

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
        obs_ok = (self.observations_file is not None) or (self.observations_array is not None)
        return all(v is not None for v in required) and obs_ok

    def missing_fields(self) -> list[str]:
        """Return a list of names of required fields that are not yet set."""
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

    def to_problem_spec(self) -> ProblemSpec:
        """Convert this schema to a ProblemSpec.

        Raises ValueError if any required field is missing.
        """
        missing = self.missing_fields()
        if missing:
            raise ValueError(
                f"NormalizedSchema is incomplete; missing: {missing}"
            )

        geometry = Geometry(
            length=self.rod_length_m,       # type: ignore[arg-type]
            n_cells=self.n_cells,
        )
        material = Material(
            density=self.density_kg_m3,           # type: ignore[arg-type]
            specific_heat=self.specific_heat_J_kgK,  # type: ignore[arg-type]
            conductivity=self.conductivity_W_mK,     # type: ignore[arg-type]
        )
        bc = BoundaryConditions(
            right_type=self.bc_right_type,   # type: ignore[arg-type]
            right_value=self.bc_right_value,
        )
        time_grid = list(
            np.linspace(self.time_start_s, self.time_end_s, self.time_n_steps)  # type: ignore[arg-type]
        )

        # Resolve observations
        if self.observations_array is not None:
            observations = self.observations_array
        else:
            observations = _load_observations_csv(
                Path(self.observations_file),       # type: ignore[arg-type]
                len(self.sensor_positions_m),
                self.time_n_steps,                  # type: ignore[arg-type]
            )

        meta = dict(self.metadata)
        if self.observations_file:
            meta.setdefault("source_file", self.observations_file)

        spec = ProblemSpec(
            problem_type=self.problem_type,
            dimension=self.dimension,
            transient=self.transient,
            target_name=self.unknown_target,
            time_grid=time_grid,
            sensor_positions=self.sensor_positions_m,
            observations=observations,
            geometry=geometry,
            material=material,
            boundary_conditions=bc,
            initial_condition=self.initial_temperature_K,
            noise_std=self.noise_std_K,
            metadata=meta,
        )
        log.info(
            "NormalizedSchema → ProblemSpec: n_time=%d, n_sensors=%d",
            spec.n_time, spec.n_sensors,
        )
        return spec


# ---------------------------------------------------------------------------
# Public normalizer entry points
# ---------------------------------------------------------------------------


def normalize_from_yaml(
    config_path: str | Path,
    observations_path: str | Path | None = None,
) -> NormalizedSchema:
    """Build a NormalizedSchema from a YAML problem config file.

    This is the primary entry point for the existing structured workflow.
    Observations can be embedded as a file reference in the YAML or passed
    directly via *observations_path*.

    Parameters
    ----------
    config_path       : path to YAML config
    observations_path : optional CSV path override
    """
    config_path = Path(config_path)
    log.info("normalize_from_yaml: %s", config_path)
    with config_path.open("r", encoding="utf-8") as fh:
        raw: dict[str, Any] = yaml.safe_load(fh)
    schema = _dict_to_schema(raw)
    # Override observations path if explicitly supplied
    if observations_path is not None:
        schema.observations_file = str(observations_path)
    log.info(
        "Normalized schema from YAML: complete=%s", schema.is_complete()
    )
    return schema


def normalize_from_dict(data: dict[str, Any]) -> NormalizedSchema:
    """Build a NormalizedSchema from a Python dict.

    The dict may use the same structure as the YAML config (nested keys) or
    the flat field names of NormalizedSchema (e.g. ``rod_length_m``).

    Both structural representations are supported; YAML-style nesting takes
    priority if both are present.
    """
    log.info("normalize_from_dict: keys=%s", list(data.keys()))
    schema = _dict_to_schema(data)
    log.info(
        "Normalized schema from dict: complete=%s, missing=%s",
        schema.is_complete(), schema.missing_fields(),
    )
    return schema


def normalize_from_text(text: str) -> NormalizedSchema:
    """Build a NormalizedSchema from a semi-structured text description.

    This is a *lightweight, deterministic* text extractor — not a full
    natural-language parser.  It looks for recognizable numeric patterns
    (e.g. "L = 0.05 m", "k = 50 W/(m·K)", "T_end = 60 s") and maps them
    to schema fields.

    Limitations
    -----------
    - Only the patterns listed in _TEXT_PATTERNS are recognized.
    - Observations must still be supplied separately (as a file path in the
      text or via a follow-up call to schema.observations_file = ...).
    - No LLM inference; only deterministic regex.
    - For production use with free-form natural language, plug in a
      ProblemParserLLM adapter instead.
    """
    log.info("normalize_from_text: len=%d chars", len(text))
    schema = NormalizedSchema()
    extracted = _extract_from_text(text)
    log.debug("Text extraction results: %s", extracted)
    schema = _apply_flat_dict(schema, extracted)
    schema.metadata["source"] = "text_extraction"
    schema.metadata["raw_text"] = text[:200]  # keep first 200 chars for traceability
    log.info(
        "Normalized schema from text: complete=%s, missing=%s",
        schema.is_complete(), schema.missing_fields(),
    )
    return schema


# ---------------------------------------------------------------------------
# Internal: dict → schema
# ---------------------------------------------------------------------------


def _dict_to_schema(raw: dict[str, Any]) -> NormalizedSchema:
    """Convert a YAML-style dict (or flat dict) into a NormalizedSchema."""
    schema = NormalizedSchema()

    # --- Problem taxonomy ---
    schema.problem_type = str(raw.get("problem_type", schema.problem_type))
    schema.dimension = int(raw.get("dimension", schema.dimension))
    schema.transient = bool(raw.get("transient", schema.transient))
    schema.unknown_target = str(raw.get("target_name", schema.unknown_target))

    # --- Geometry ---
    if "geometry" in raw:
        geo = raw["geometry"]
        schema.rod_length_m = float(geo["length"])
        schema.n_cells = int(geo.get("n_cells", schema.n_cells))
    # also accept flat keys
    if "rod_length_m" in raw:
        schema.rod_length_m = float(raw["rod_length_m"])
    if "n_cells" in raw:
        schema.n_cells = int(raw["n_cells"])

    # --- Material ---
    if "material" in raw:
        mat = raw["material"]
        schema.density_kg_m3 = float(mat["density"])
        schema.specific_heat_J_kgK = float(mat["specific_heat"])
        schema.conductivity_W_mK = float(mat["conductivity"])
    for flat_key, attr in [
        ("density_kg_m3", "density_kg_m3"),
        ("specific_heat_J_kgK", "specific_heat_J_kgK"),
        ("conductivity_W_mK", "conductivity_W_mK"),
    ]:
        if flat_key in raw:
            setattr(schema, attr, float(raw[flat_key]))

    # --- Initial condition ---
    if "initial_condition" in raw:
        schema.initial_temperature_K = float(raw["initial_condition"])
    if "initial_temperature_K" in raw:
        schema.initial_temperature_K = float(raw["initial_temperature_K"])

    # --- Boundary conditions ---
    if "boundary_conditions" in raw:
        bc = raw["boundary_conditions"]
        schema.bc_right_type = str(bc.get("right_type", schema.bc_right_type))
        schema.bc_right_value = float(bc.get("right_value", schema.bc_right_value))
    if "bc_right_type" in raw:
        schema.bc_right_type = str(raw["bc_right_type"])
    if "bc_right_value" in raw:
        schema.bc_right_value = float(raw["bc_right_value"])

    # --- Time ---
    if "time" in raw:
        tg = raw["time"]
        schema.time_start_s = float(tg.get("start", schema.time_start_s))
        schema.time_end_s = float(tg["end"])
        schema.time_n_steps = int(tg["n_steps"])
    for flat_key, attr in [
        ("time_start_s", "time_start_s"),
        ("time_end_s", "time_end_s"),
        ("time_n_steps", "time_n_steps"),
    ]:
        if flat_key in raw:
            setattr(schema, attr, float(raw[flat_key]) if attr.endswith("_s") else int(raw[flat_key]))

    # --- Sensors ---
    if "sensor_positions" in raw:
        schema.sensor_positions_m = [float(s) for s in raw["sensor_positions"]]
    if "sensor_positions_m" in raw:
        schema.sensor_positions_m = [float(s) for s in raw["sensor_positions_m"]]

    # --- Observations ---
    if "observations_file" in raw:
        schema.observations_file = str(raw["observations_file"])
    if "observations_file_path" in raw:
        schema.observations_file = str(raw["observations_file_path"])

    # --- Noise ---
    if "noise_std" in raw and raw["noise_std"] is not None:
        schema.noise_std_K = float(raw["noise_std"])
    if "noise_std_K" in raw and raw["noise_std_K"] is not None:
        schema.noise_std_K = float(raw["noise_std_K"])

    # --- Solver preferences ---
    if "planner" in raw and isinstance(raw["planner"], dict):
        schema.solver_preferences = dict(raw["planner"])
    if "solver_preferences" in raw and isinstance(raw["solver_preferences"], dict):
        schema.solver_preferences.update(raw["solver_preferences"])

    # --- Metadata ---
    if "metadata" in raw and isinstance(raw["metadata"], dict):
        schema.metadata.update(raw["metadata"])

    return schema


# ---------------------------------------------------------------------------
# Internal: text extraction
# ---------------------------------------------------------------------------

# Recognizable patterns in semi-structured text.
# Each entry: (field_name_in_NormalizedSchema, compiled_regex)
# The regex must have one capturing group for the numeric value.
_TEXT_PATTERNS: list[tuple[str, re.Pattern]] = [
    # Geometry
    ("rod_length_m",         re.compile(r"[Ll](?:ength)?\s*[=:]\s*([\d.eE+\-]+)\s*m", re.I)),
    ("n_cells",              re.compile(r"n_cells\s*[=:]\s*(\d+)", re.I)),
    # Material
    ("density_kg_m3",        re.compile(r"rho\s*[=:]\s*([\d.eE+\-]+)\s*kg", re.I)),
    ("specific_heat_J_kgK",  re.compile(r"cp\s*[=:]\s*([\d.eE+\-]+)\s*J", re.I)),
    ("conductivity_W_mK",    re.compile(r"k\s*[=:]\s*([\d.eE+\-]+)\s*W", re.I)),
    # Temperature
    ("initial_temperature_K",re.compile(r"T0\s*[=:]\s*([\d.eE+\-]+)\s*K", re.I)),
    ("bc_right_value",       re.compile(r"T_right\s*[=:]\s*([\d.eE+\-]+)\s*K", re.I)),
    # Time
    ("time_end_s",           re.compile(r"T_end\s*[=:]\s*([\d.eE+\-]+)\s*s", re.I)),
    ("time_n_steps",         re.compile(r"n_steps\s*[=:]\s*(\d+)", re.I)),
    # Noise
    ("noise_std_K",          re.compile(r"noise_std\s*[=:]\s*([\d.eE+\-]+)\s*K", re.I)),
    # Observations file
    ("observations_file",    re.compile(r"observations\s*[=:]\s*[\"']?([^\s\"']+\.csv)[\"']?", re.I)),
]


def _extract_from_text(text: str) -> dict[str, Any]:
    """Apply _TEXT_PATTERNS to extract field values from a text string."""
    extracted: dict[str, Any] = {}
    for field_name, pattern in _TEXT_PATTERNS:
        m = pattern.search(text)
        if m:
            raw_val = m.group(1)
            try:
                # Sensor positions are special — handle separately below
                if field_name in ("n_cells", "time_n_steps"):
                    extracted[field_name] = int(raw_val)
                elif field_name == "observations_file":
                    extracted[field_name] = raw_val
                else:
                    extracted[field_name] = float(raw_val)
            except ValueError:
                log.warning("Text extraction: could not parse '%s' for field '%s'", raw_val, field_name)

    # Sensor positions: look for "sensors at X m and Y m" or "sensors: [X, Y]"
    sensor_patterns = [
        re.compile(r"sensors?\s+at\s+([\d.,\s]+(?:m\s+and\s+[\d.,\s]+)?)\s*m", re.I),
        re.compile(r"sensor_positions\s*[=:]\s*\[([\d.,\s]+)\]", re.I),
    ]
    for sp in sensor_patterns:
        sm = sp.search(text)
        if sm:
            vals_str = sm.group(1)
            # Remove trailing "m", "and", spaces, keep only numbers / decimal points
            cleaned = re.sub(r"\band\b", " ", vals_str, flags=re.I)
            try:
                positions = [float(v.strip()) for v in re.split(r"[,\s]+", cleaned) if re.match(r"[\d.eE+\-]+", v.strip())]
                if positions:
                    extracted["sensor_positions_m"] = positions
                    break
            except ValueError:
                pass

    return extracted


def _apply_flat_dict(schema: NormalizedSchema, data: dict[str, Any]) -> NormalizedSchema:
    """Apply a flat dict of field_name → value to a NormalizedSchema."""
    float_fields = {
        "rod_length_m", "density_kg_m3", "specific_heat_J_kgK",
        "conductivity_W_mK", "initial_temperature_K", "bc_right_value",
        "time_start_s", "time_end_s", "noise_std_K",
    }
    int_fields = {"n_cells", "time_n_steps", "dimension"}
    for key, val in data.items():
        if not hasattr(schema, key):
            continue
        if key in float_fields:
            setattr(schema, key, float(val))
        elif key in int_fields:
            setattr(schema, key, int(val))
        else:
            setattr(schema, key, val)
    return schema


# ---------------------------------------------------------------------------
# CSV loading helper (mirrors parser.py logic)
# ---------------------------------------------------------------------------


def _load_observations_csv(
    path: Path,
    n_sensors: int,
    n_steps: int,
) -> list[list[float]]:
    """Load CSV observations (rows=time, cols=sensors) into sensor-major form."""
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
