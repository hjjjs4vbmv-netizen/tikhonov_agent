"""
pde_schema.py
=============
PDE-aware schema layer for the IHCP agent.

This module defines three things:

1.  **PDESchema** – a strongly-typed, format-agnostic description of a PDE
    inverse problem at the *problem level*, not at the level of a particular
    YAML layout.  It captures the full PDE taxonomy, domain geometry, material
    model, initial/boundary conditions, observation model, and solver prefs.

2.  **PDESchemaValidator** – a deterministic semantic validator that checks the
    schema for physical and mathematical consistency *before* any solver sees
    it.  Validation is always deterministic: the LLM never owns this step.

3.  **PDESchemaMapper** – converts a validated PDESchema into the repository's
    internal ``ProblemSpec`` (defined in ``src/types.py``).

Design principles
-----------------
* Separation of concerns:
    - Syntax normalisation   → pde_normalizer.py
    - PDE semantic validity  → PDESchemaValidator  (this module)
    - Downstream spec build  → PDESchemaMapper     (this module)

* The LLM path may produce a *candidate* PDESchema dict; that candidate MUST
  pass PDESchemaValidator before being accepted.  The LLM never bypasses the
  validator.

* All fields have sane defaults so that a partial schema can be inspected and
  diagnosed rather than silently exploding.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import numpy as np

from src.logging_utils import get_logger
from src.types import BoundaryConditions, Geometry, Material, ProblemSpec

log = get_logger("pde_schema")


# ---------------------------------------------------------------------------
# Enumerated literals (used as type constraints)
# ---------------------------------------------------------------------------

PDEFamily = Literal["parabolic", "elliptic", "hyperbolic", "mixed"]
EquationClass = Literal["heat_equation", "wave_equation", "poisson", "other"]
ProblemKind = Literal["inverse", "forward"]
UnknownTarget = Literal[
    "boundary_heat_flux",
    "initial_condition",
    "conductivity",
    "source_term",
    "other",
]
DomainType = Literal["interval", "rectangle", "cuboid", "annulus", "custom"]
CoordSystem = Literal["cartesian", "cylindrical", "spherical"]
BCType = Literal["dirichlet", "neumann", "robin", "unknown"]
BCStatus = Literal["given", "inversion_target", "unknown"]
CoefficientKind = Literal["constant", "variable", "temperature_dependent"]
ICType = Literal["uniform", "expression", "file"]
ObservedVariable = Literal["temperature", "heat_flux", "other"]
NoiseModel = Literal["gaussian", "uniform", "none", "unknown"]
SolverFamily = Literal["tikhonov", "tsvd", "adjoint", "mcmc", "other"]


# ---------------------------------------------------------------------------
# Sub-schemas
# ---------------------------------------------------------------------------


@dataclass
class DomainSpec:
    """Geometric/spatial domain description."""

    domain_type: DomainType = "interval"
    coord_system: CoordSystem = "cartesian"
    # Primary length (x-direction / radius / etc.)
    length: float | None = None             # [m]
    # Secondary dimensions (for 2-D/3-D; unused in 1-D)
    width: float | None = None              # [m]
    height: float | None = None             # [m]
    # Discretisation hint
    n_cells_x: int = 50
    n_cells_y: int | None = None
    n_cells_z: int | None = None
    # Free extra parameters
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class MaterialSpec:
    """Material / coefficient description."""

    density: float | None = None            # rho  [kg/m³]
    specific_heat: float | None = None      # cp   [J/(kg·K)]
    conductivity: float | None = None       # k    [W/(m·K)]
    density_kind: CoefficientKind = "constant"
    specific_heat_kind: CoefficientKind = "constant"
    conductivity_kind: CoefficientKind = "constant"
    source_term: float | None = None        # Q    [W/m³], None = no source
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class InitialConditionSpec:
    """Initial condition description."""

    ic_type: ICType = "uniform"
    value: float = 300.0                    # [K] – used when ic_type == "uniform"
    expression: str | None = None          # symbolic – for future use
    file: str | None = None                # CSV path – for future use
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class BoundaryConditionSpec:
    """One boundary condition (one side of the domain)."""

    location: str = "left"                 # "left", "right", "top", "bottom"
    bc_type: BCType = "neumann"
    status: BCStatus = "given"             # "given" | "inversion_target" | "unknown"
    value: float | None = None             # [K] for Dirichlet; [W/m²] for Neumann
    expression: str | None = None         # for non-constant BC (future)
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class BoundaryConditionsSpec:
    """Collection of boundary conditions."""

    conditions: list[BoundaryConditionSpec] = field(default_factory=list)

    def get(self, location: str) -> BoundaryConditionSpec | None:
        """Return the BC for *location*, or None if not found."""
        for bc in self.conditions:
            if bc.location == location:
                return bc
        return None

    def inversion_targets(self) -> list[BoundaryConditionSpec]:
        """Return all BCs marked as inversion targets."""
        return [bc for bc in self.conditions if bc.status == "inversion_target"]


@dataclass
class ObservationSpec:
    """Observation / measurement model."""

    sensor_positions: list[float] = field(default_factory=list)  # [m]
    observed_variable: ObservedVariable = "temperature"
    observations_file: str | None = None    # path to CSV
    observations_array: list[list[float]] | None = None  # shape (n_sensors, n_t)
    noise_std: float | None = None          # [K]
    noise_model: NoiseModel = "gaussian"
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class TimeSpec:
    """Time discretisation."""

    start: float = 0.0                      # [s]
    end: float | None = None                # [s]
    n_steps: int | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class SolverPrefsSpec:
    """Solver preferences and hints (passed through to the planner)."""

    preferred_solver: SolverFamily = "tikhonov"
    reg_order: int | None = None
    lambda_strategy: str | None = None
    lambda_value: float | None = None
    max_retries: int | None = None
    iteration_budget: int | None = None
    physical_bounds: tuple[float, float] | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class SchemaMetadata:
    """Provenance and parsing notes."""

    source: str = "unknown"
    parse_path: Literal["structured", "llm_assisted", "text_regex", "unknown"] = "unknown"
    confidence: float = 1.0                 # 0.0–1.0; LLM path may reduce this
    warnings: list[str] = field(default_factory=list)
    raw_input_preview: str = ""
    llm_model: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Top-level PDESchema
# ---------------------------------------------------------------------------


@dataclass
class PDESchema:
    """Unified PDE-level problem description.

    This is the single contract between the input layer and the scientific
    pipeline.  It is populated either by the deterministic structured parser
    (Path A) or by an LLM-assisted filler (Path B), then validated by
    PDESchemaValidator before being converted to ProblemSpec.

    All sub-schemas have sensible defaults; missing required fields will be
    caught by the validator rather than causing silent failures.
    """

    # --- Problem taxonomy ---
    pde_family: PDEFamily = "parabolic"
    equation_class: EquationClass = "heat_equation"
    problem_kind: ProblemKind = "inverse"
    dimension: int = 1
    transient: bool = True
    unknown_target: UnknownTarget = "boundary_heat_flux"

    # --- Sub-schemas ---
    domain: DomainSpec = field(default_factory=DomainSpec)
    material: MaterialSpec = field(default_factory=MaterialSpec)
    initial_condition: InitialConditionSpec = field(default_factory=InitialConditionSpec)
    boundary_conditions: BoundaryConditionsSpec = field(default_factory=BoundaryConditionsSpec)
    observation: ObservationSpec = field(default_factory=ObservationSpec)
    time: TimeSpec = field(default_factory=TimeSpec)
    solver_prefs: SolverPrefsSpec = field(default_factory=SolverPrefsSpec)
    metadata: SchemaMetadata = field(default_factory=SchemaMetadata)

    def summary(self) -> str:
        """One-line human-readable summary."""
        length = f"L={self.domain.length}m" if self.domain.length else "L=?"
        rho = f"ρ={self.material.density}" if self.material.density else "ρ=?"
        k = f"k={self.material.conductivity}" if self.material.conductivity else "k=?"
        n_sensors = len(self.observation.sensor_positions)
        return (
            f"PDESchema({self.equation_class}, {self.dimension}D, "
            f"{length}, {rho}, {k}, {n_sensors} sensors)"
        )


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


@dataclass
class ValidationResult:
    """Result of PDESchemaValidator.validate()."""

    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        lines = [f"ValidationResult(valid={self.valid})"]
        for e in self.errors:
            lines.append(f"  ERROR:   {e}")
        for w in self.warnings:
            lines.append(f"  WARNING: {w}")
        return "\n".join(lines)

    def raise_if_invalid(self) -> None:
        """Raise ValueError with all error messages if not valid."""
        if not self.valid:
            raise ValueError(
                "PDESchema validation failed:\n"
                + "\n".join(f"  - {e}" for e in self.errors)
            )


_VALID_PDE_FAMILIES: set[str] = {"parabolic", "elliptic", "hyperbolic", "mixed"}
_VALID_EQUATION_CLASSES: set[str] = {
    "heat_equation", "wave_equation", "poisson", "other"
}
_VALID_PROBLEM_KINDS: set[str] = {"inverse", "forward"}
_VALID_UNKNOWN_TARGETS: set[str] = {
    "boundary_heat_flux", "initial_condition",
    "conductivity", "source_term", "other",
}
_VALID_DOMAIN_TYPES: set[str] = {
    "interval", "rectangle", "cuboid", "annulus", "custom"
}
_VALID_COORD_SYSTEMS: set[str] = {"cartesian", "cylindrical", "spherical"}
_VALID_BC_TYPES: set[str] = {"dirichlet", "neumann", "robin", "unknown"}
_VALID_BC_STATUSES: set[str] = {"given", "inversion_target", "unknown"}
_VALID_IC_TYPES: set[str] = {"uniform", "expression", "file"}
_VALID_COEFF_KINDS: set[str] = {"constant", "variable", "temperature_dependent"}


class PDESchemaValidator:
    """Deterministic semantic validator for PDESchema.

    Checks are grouped into:
    - Taxonomy checks
    - Domain / geometry checks
    - Material checks
    - Initial-condition checks
    - Boundary-condition checks
    - Observation checks
    - Time-setting checks
    - IHCP-specific cross-checks (only when problem_kind == "inverse")

    All errors are collected before returning; there are no early exits.
    Warnings are non-fatal and informational.
    """

    def validate(self, schema: PDESchema) -> ValidationResult:
        result = ValidationResult(valid=True)
        self._check_taxonomy(schema, result)
        self._check_domain(schema, result)
        self._check_material(schema, result)
        self._check_initial_condition(schema, result)
        self._check_boundary_conditions(schema, result)
        self._check_observations(schema, result)
        self._check_time(schema, result)
        if schema.problem_kind == "inverse":
            self._check_ihcp_specific(schema, result)
        if result.errors:
            result.valid = False
        return result

    # ------------------------------------------------------------------
    # Private check methods
    # ------------------------------------------------------------------

    def _check_taxonomy(self, s: PDESchema, r: ValidationResult) -> None:
        if s.pde_family not in _VALID_PDE_FAMILIES:
            r.errors.append(
                f"pde_family '{s.pde_family}' is not one of {sorted(_VALID_PDE_FAMILIES)}"
            )
        if s.equation_class not in _VALID_EQUATION_CLASSES:
            r.errors.append(
                f"equation_class '{s.equation_class}' is not one of "
                f"{sorted(_VALID_EQUATION_CLASSES)}"
            )
        if s.problem_kind not in _VALID_PROBLEM_KINDS:
            r.errors.append(
                f"problem_kind '{s.problem_kind}' must be 'inverse' or 'forward'"
            )
        if s.unknown_target not in _VALID_UNKNOWN_TARGETS:
            r.errors.append(
                f"unknown_target '{s.unknown_target}' is not one of "
                f"{sorted(_VALID_UNKNOWN_TARGETS)}"
            )
        if s.dimension < 1 or s.dimension > 3:
            r.errors.append(f"dimension must be 1, 2, or 3; got {s.dimension}")
        if not isinstance(s.transient, bool):
            r.errors.append("transient must be a boolean")
        # Cross-check: heat equation is parabolic
        if s.equation_class == "heat_equation" and s.pde_family != "parabolic":
            r.warnings.append(
                f"equation_class='heat_equation' is typically 'parabolic', "
                f"but pde_family='{s.pde_family}' was given"
            )

    def _check_domain(self, s: PDESchema, r: ValidationResult) -> None:
        d = s.domain
        if d.domain_type not in _VALID_DOMAIN_TYPES:
            r.errors.append(
                f"domain.domain_type '{d.domain_type}' is not one of "
                f"{sorted(_VALID_DOMAIN_TYPES)}"
            )
        if d.coord_system not in _VALID_COORD_SYSTEMS:
            r.errors.append(
                f"domain.coord_system '{d.coord_system}' is not one of "
                f"{sorted(_VALID_COORD_SYSTEMS)}"
            )
        if d.length is None:
            r.errors.append("domain.length is required but missing")
        elif d.length <= 0:
            r.errors.append(f"domain.length must be > 0; got {d.length}")
        if d.n_cells_x <= 0:
            r.errors.append(f"domain.n_cells_x must be > 0; got {d.n_cells_x}")
        # Dimension consistency
        if s.dimension >= 2 and d.width is None:
            r.warnings.append(
                "dimension >= 2 but domain.width is not set; using 1-D approximation"
            )
        if s.dimension >= 3 and d.height is None:
            r.warnings.append(
                "dimension == 3 but domain.height is not set; using lower-D approximation"
            )

    def _check_material(self, s: PDESchema, r: ValidationResult) -> None:
        m = s.material
        for attr, name in [
            (m.density, "material.density"),
            (m.specific_heat, "material.specific_heat"),
            (m.conductivity, "material.conductivity"),
        ]:
            if attr is None:
                r.errors.append(f"{name} is required but missing")
            elif attr <= 0:
                r.errors.append(f"{name} must be > 0; got {attr}")
        for kind_attr, name in [
            (m.density_kind, "material.density_kind"),
            (m.specific_heat_kind, "material.specific_heat_kind"),
            (m.conductivity_kind, "material.conductivity_kind"),
        ]:
            if kind_attr not in _VALID_COEFF_KINDS:
                r.errors.append(
                    f"{name} '{kind_attr}' is not one of {sorted(_VALID_COEFF_KINDS)}"
                )
        # Warn on non-constant coefficients in the current 1-D FD solver
        if any(
            k != "constant"
            for k in (m.density_kind, m.specific_heat_kind, m.conductivity_kind)
        ):
            r.warnings.append(
                "Non-constant material coefficients are declared but the current "
                "1-D FD solver only supports constant properties; the variable "
                "declaration will be ignored at solve time."
            )

    def _check_initial_condition(self, s: PDESchema, r: ValidationResult) -> None:
        ic = s.initial_condition
        if ic.ic_type not in _VALID_IC_TYPES:
            r.errors.append(
                f"initial_condition.ic_type '{ic.ic_type}' is not one of "
                f"{sorted(_VALID_IC_TYPES)}"
            )
        if ic.ic_type == "uniform" and ic.value is None:
            r.warnings.append(
                "initial_condition.ic_type='uniform' but value is None; "
                "will default to 300.0 K"
            )
        if ic.ic_type == "expression" and not ic.expression:
            r.errors.append(
                "initial_condition.ic_type='expression' but expression is empty"
            )
        if ic.ic_type == "file" and not ic.file:
            r.errors.append(
                "initial_condition.ic_type='file' but no file path given"
            )

    def _check_boundary_conditions(self, s: PDESchema, r: ValidationResult) -> None:
        bcs = s.boundary_conditions.conditions
        if not bcs:
            r.errors.append("boundary_conditions: no conditions defined")
            return
        # Enum checks
        for bc in bcs:
            if bc.bc_type not in _VALID_BC_TYPES:
                r.errors.append(
                    f"boundary_conditions[{bc.location}].bc_type '{bc.bc_type}' "
                    f"is not one of {sorted(_VALID_BC_TYPES)}"
                )
            if bc.status not in _VALID_BC_STATUSES:
                r.errors.append(
                    f"boundary_conditions[{bc.location}].status '{bc.status}' "
                    f"is not one of {sorted(_VALID_BC_STATUSES)}"
                )
        # Duplicate location check
        locations = [bc.location for bc in bcs]
        seen: set[str] = set()
        for loc in locations:
            if loc in seen:
                r.warnings.append(
                    f"boundary_conditions: duplicate location '{loc}'"
                )
            seen.add(loc)
        # Dirichlet/Neumann need values
        for bc in bcs:
            if bc.status == "given" and bc.bc_type in ("dirichlet", "neumann"):
                if bc.value is None and bc.expression is None:
                    r.warnings.append(
                        f"boundary_conditions[{bc.location}]: type='{bc.bc_type}', "
                        "status='given' but no value or expression provided"
                    )

    def _check_observations(self, s: PDESchema, r: ValidationResult) -> None:
        obs = s.observation
        if not obs.sensor_positions:
            r.errors.append("observation.sensor_positions is empty; at least 1 sensor required")
        else:
            for i, pos in enumerate(obs.sensor_positions):
                try:
                    pos_f = float(pos)
                except (TypeError, ValueError):
                    r.errors.append(
                        f"observation.sensor_positions[{i}] = {pos!r} is not numeric"
                    )
                    continue
                if s.domain.length is not None and not (0 < pos_f < s.domain.length):
                    r.warnings.append(
                        f"sensor position {pos_f} m is outside the domain "
                        f"(0, {s.domain.length}) m"
                    )
        # Observation data source
        has_data = (
            obs.observations_file is not None
            or obs.observations_array is not None
        )
        if not has_data:
            r.errors.append(
                "observation: neither observations_file nor observations_array is set"
            )
        # If array given, check shape
        if obs.observations_array is not None:
            arr = obs.observations_array
            n_sensors = len(obs.sensor_positions)
            if arr and len(arr) != n_sensors:
                r.errors.append(
                    f"observation.observations_array has {len(arr)} rows "
                    f"but {n_sensors} sensor_positions declared"
                )
        # Noise
        if obs.noise_std is not None and obs.noise_std < 0:
            r.errors.append(
                f"observation.noise_std must be >= 0; got {obs.noise_std}"
            )

    def _check_time(self, s: PDESchema, r: ValidationResult) -> None:
        t = s.time
        if s.transient:
            if t.end is None:
                r.errors.append("time.end is required for transient problems")
            elif t.end <= t.start:
                r.errors.append(
                    f"time.end ({t.end}) must be > time.start ({t.start})"
                )
            if t.n_steps is None:
                r.errors.append("time.n_steps is required for transient problems")
            elif t.n_steps < 2:
                r.errors.append(
                    f"time.n_steps must be >= 2; got {t.n_steps}"
                )
        else:
            if t.end is not None or t.n_steps is not None:
                r.warnings.append(
                    "time.end and time.n_steps are set for a steady-state problem; "
                    "they will be ignored"
                )

    def _check_ihcp_specific(self, s: PDESchema, r: ValidationResult) -> None:
        """Cross-checks specific to the inverse heat conduction problem."""
        # Exactly one inversion target BC is expected for flux recovery
        targets = s.boundary_conditions.inversion_targets()
        if len(targets) == 0:
            r.errors.append(
                "problem_kind='inverse' but no boundary condition has "
                "status='inversion_target'; cannot determine what to recover"
            )
        elif len(targets) > 1:
            r.warnings.append(
                f"{len(targets)} boundary conditions marked as 'inversion_target'; "
                "current solver handles one unknown BC at a time"
            )
        # Unknown target consistency
        if s.unknown_target == "boundary_heat_flux":
            target_bcs = [
                bc for bc in targets if bc.bc_type in ("neumann", "unknown")
            ]
            if targets and not target_bcs:
                r.warnings.append(
                    "unknown_target='boundary_heat_flux' but inversion_target BC "
                    "is not Neumann or unknown; expected a Neumann-type BC at the "
                    "heated surface"
                )
        # Sensor positions must be inside domain
        if s.domain.length and s.observation.sensor_positions:
            outside = [
                p for p in s.observation.sensor_positions
                if not (0 < float(p) < s.domain.length)
            ]
            if outside:
                r.errors.append(
                    f"Sensor positions {outside} are outside the domain "
                    f"(0, {s.domain.length}) m; sensors must be interior for IHCP"
                )
        # Fourier number sanity (detect wildly under-resolved time stepping)
        mat = s.material
        dom = s.domain
        t = s.time
        if (
            mat.density is not None and mat.density > 0
            and mat.specific_heat is not None and mat.specific_heat > 0
            and mat.conductivity is not None and mat.conductivity > 0
            and dom.length is not None
            and dom.n_cells_x > 0
            and t.end is not None
            and t.n_steps is not None
            and t.n_steps > 1
        ):
            alpha = mat.conductivity / (mat.density * mat.specific_heat)
            dx = dom.length / dom.n_cells_x
            dt = (t.end - t.start) / (t.n_steps - 1)
            fo = alpha * dt / (dx ** 2)
            if fo > 10.0:
                r.warnings.append(
                    f"Fourier number Fo = {fo:.2f} >> 1; while the implicit "
                    "backward-Euler scheme is unconditionally stable, such coarse "
                    "temporal resolution may degrade solution accuracy."
                )


# ---------------------------------------------------------------------------
# Mapper: PDESchema → ProblemSpec
# ---------------------------------------------------------------------------


def _default_csv_loader(
    path: Path,
    n_sensors: int,
    n_steps: int,
) -> list[list[float]]:
    """Load CSV observations (rows=time, cols=sensors) → sensor-major list."""
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
            f"Observations CSV has {arr.shape[1]} sensor columns "
            f"but schema expects {n_sensors}"
        )
    return arr.T.tolist()


class PDESchemaMapper:
    """Convert a validated PDESchema into a ProblemSpec.

    Callers should run PDESchemaValidator.validate() first and pass a valid
    schema here.  The mapper will still raise ValueError for unrecoverable
    structural problems, but assumes the semantic checks have been done.

    Parameters
    ----------
    csv_loader
        Optional callable ``(path, n_sensors, n_steps) -> list[list[float]]``
        for loading observation data from CSV.  Defaults to the built-in
        loader (same logic as parser.py).  Useful for injection in tests.
    """

    def __init__(self, csv_loader=None) -> None:
        self._csv_loader = csv_loader or _default_csv_loader

    def map(self, schema: PDESchema) -> ProblemSpec:
        """Convert *schema* to a ProblemSpec.

        Raises
        ------
        ValueError
            If any required field is still missing at conversion time.
        """
        # --- Geometry ---
        if schema.domain.length is None:
            raise ValueError("PDESchema.domain.length is required for ProblemSpec")
        geometry = Geometry(
            length=schema.domain.length,
            n_cells=schema.domain.n_cells_x,
        )

        # --- Material ---
        mat = schema.material
        if any(v is None for v in (mat.density, mat.specific_heat, mat.conductivity)):
            raise ValueError(
                "PDESchema.material: density, specific_heat, and conductivity "
                "are all required for ProblemSpec"
            )
        material = Material(
            density=mat.density,           # type: ignore[arg-type]
            specific_heat=mat.specific_heat,  # type: ignore[arg-type]
            conductivity=mat.conductivity,    # type: ignore[arg-type]
        )

        # --- Boundary conditions ---
        # Map to ProblemSpec's right-only BC model
        right_bc = schema.boundary_conditions.get("right")
        if right_bc is None:
            # Fall back: find the first non-inversion-target BC
            non_target = [
                bc for bc in schema.boundary_conditions.conditions
                if bc.status != "inversion_target"
            ]
            right_bc = non_target[0] if non_target else None
        if right_bc is None:
            raise ValueError(
                "PDESchema must have at least one non-inversion-target BC "
                "for the right boundary; none found"
            )
        bc = BoundaryConditions(
            right_type=right_bc.bc_type if right_bc.bc_type != "unknown" else "dirichlet",  # type: ignore[arg-type]
            right_value=right_bc.value if right_bc.value is not None else 300.0,
        )

        # --- Time grid ---
        t = schema.time
        if t.end is None or t.n_steps is None:
            raise ValueError("PDESchema.time: end and n_steps are required")
        time_grid = list(np.linspace(t.start, t.end, t.n_steps))

        # --- Initial condition ---
        ic_value = (
            schema.initial_condition.value
            if schema.initial_condition.value is not None
            else 300.0
        )

        # --- Observations ---
        obs = schema.observation
        if obs.observations_array is not None:
            observations = obs.observations_array
        elif obs.observations_file is not None:
            observations = self._csv_loader(
                Path(obs.observations_file),
                len(obs.sensor_positions),
                t.n_steps,  # type: ignore[arg-type]
            )
        else:
            raise ValueError(
                "PDESchema.observation: either observations_array or "
                "observations_file must be set"
            )

        # --- Metadata ---
        meta: dict[str, Any] = dict(schema.metadata.extra)
        if obs.observations_file:
            meta.setdefault("source_file", obs.observations_file)
        meta["parse_path"] = schema.metadata.parse_path
        if schema.metadata.warnings:
            meta["schema_warnings"] = schema.metadata.warnings

        spec = ProblemSpec(
            problem_type=f"{schema.dimension}D_{'' if not schema.transient else 'transient_'}"
                         f"{'IHCP' if schema.problem_kind == 'inverse' else 'FP'}",
            dimension=schema.dimension,
            transient=schema.transient,
            target_name=schema.unknown_target,
            time_grid=time_grid,
            sensor_positions=list(obs.sensor_positions),
            observations=observations,
            geometry=geometry,
            material=material,
            boundary_conditions=bc,
            initial_condition=ic_value,
            noise_std=obs.noise_std,
            metadata=meta,
        )
        log.info(
            "PDESchemaMapper: PDESchema → ProblemSpec n_time=%d n_sensors=%d",
            spec.n_time, spec.n_sensors,
        )
        return spec
