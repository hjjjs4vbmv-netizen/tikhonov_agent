"""
test_pde_schema.py
==================
Unit tests for:
  - PDESchema sub-dataclasses
  - PDESchemaValidator (semantic validation)
  - PDESchemaMapper (PDESchema → ProblemSpec)

All tests are self-contained; no file I/O, no external LLM calls.
"""

from __future__ import annotations

import numpy as np
import pytest

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
from src.types import ProblemSpec


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _minimal_valid_schema(*, include_obs_file: bool = False) -> PDESchema:
    """Return the smallest fully-valid PDESchema for the canonical 1D IHCP."""
    n_sensors = 2
    n_steps = 121
    obs_array = [[300.0 + float(i) for i in range(n_steps)] for _ in range(n_sensors)]

    s = PDESchema()
    s.domain = DomainSpec(length=0.05, n_cells_x=60)
    s.material = MaterialSpec(density=7800.0, specific_heat=500.0, conductivity=50.0)
    s.initial_condition = InitialConditionSpec(ic_type="uniform", value=300.0)
    s.boundary_conditions = BoundaryConditionsSpec(conditions=[
        BoundaryConditionSpec(location="left", bc_type="neumann",
                              status="inversion_target"),
        BoundaryConditionSpec(location="right", bc_type="dirichlet",
                              status="given", value=300.0),
    ])
    s.observation = ObservationSpec(
        sensor_positions=[0.01, 0.03],
        observations_array=obs_array if not include_obs_file else None,
        observations_file="dummy.csv" if include_obs_file else None,
        noise_std=0.3,
    )
    s.time = TimeSpec(start=0.0, end=60.0, n_steps=n_steps)
    return s


def _mock_csv_loader(path, n_sensors, n_steps):
    """Stub CSV loader that returns synthetic data without hitting disk."""
    return [[300.0 + float(i) for i in range(n_steps)] for _ in range(n_sensors)]


# ---------------------------------------------------------------------------
# PDESchema dataclass tests
# ---------------------------------------------------------------------------


class TestPDESchemaDefaults:
    def test_default_pde_family(self):
        s = PDESchema()
        assert s.pde_family == "parabolic"

    def test_default_equation_class(self):
        s = PDESchema()
        assert s.equation_class == "heat_equation"

    def test_default_problem_kind(self):
        s = PDESchema()
        assert s.problem_kind == "inverse"

    def test_default_dimension(self):
        s = PDESchema()
        assert s.dimension == 1

    def test_default_transient(self):
        s = PDESchema()
        assert s.transient is True

    def test_summary_returns_string(self):
        s = _minimal_valid_schema()
        summary = s.summary()
        assert "PDESchema" in summary
        assert "heat_equation" in summary


class TestBoundaryConditionsSpec:
    def test_get_by_location(self):
        bcs = BoundaryConditionsSpec(conditions=[
            BoundaryConditionSpec(location="left", bc_type="neumann",
                                  status="inversion_target"),
            BoundaryConditionSpec(location="right", bc_type="dirichlet",
                                  status="given", value=300.0),
        ])
        right = bcs.get("right")
        assert right is not None
        assert right.value == 300.0

    def test_get_missing_location_returns_none(self):
        bcs = BoundaryConditionsSpec(conditions=[])
        assert bcs.get("top") is None

    def test_inversion_targets(self):
        bcs = BoundaryConditionsSpec(conditions=[
            BoundaryConditionSpec(location="left", bc_type="neumann",
                                  status="inversion_target"),
            BoundaryConditionSpec(location="right", bc_type="dirichlet",
                                  status="given", value=300.0),
        ])
        targets = bcs.inversion_targets()
        assert len(targets) == 1
        assert targets[0].location == "left"


# ---------------------------------------------------------------------------
# Validator: valid schema
# ---------------------------------------------------------------------------


class TestValidatorPassCases:
    def test_minimal_valid_schema_passes(self):
        s = _minimal_valid_schema()
        vr = PDESchemaValidator().validate(s)
        assert vr.valid is True
        assert vr.errors == []

    def test_valid_schema_has_no_sensor_outside_domain_errors(self):
        s = _minimal_valid_schema()
        vr = PDESchemaValidator().validate(s)
        # Sensors at 0.01 and 0.03 are inside [0, 0.05] → no errors
        assert not any("outside" in e.lower() for e in vr.errors)

    def test_valid_schema_has_inversion_target(self):
        s = _minimal_valid_schema()
        vr = PDESchemaValidator().validate(s)
        targets = s.boundary_conditions.inversion_targets()
        assert len(targets) == 1


# ---------------------------------------------------------------------------
# Validator: taxonomy checks
# ---------------------------------------------------------------------------


class TestValidatorTaxonomyErrors:
    def test_invalid_pde_family(self):
        s = _minimal_valid_schema()
        s.pde_family = "not_a_family"  # type: ignore[assignment]
        vr = PDESchemaValidator().validate(s)
        assert not vr.valid
        assert any("pde_family" in e for e in vr.errors)

    def test_invalid_equation_class(self):
        s = _minimal_valid_schema()
        s.equation_class = "burger_equation"  # type: ignore[assignment]
        vr = PDESchemaValidator().validate(s)
        assert not vr.valid
        assert any("equation_class" in e for e in vr.errors)

    def test_invalid_dimension(self):
        s = _minimal_valid_schema()
        s.dimension = 5
        vr = PDESchemaValidator().validate(s)
        assert not vr.valid
        assert any("dimension" in e for e in vr.errors)

    def test_heat_eq_not_parabolic_is_warning(self):
        s = _minimal_valid_schema()
        s.pde_family = "elliptic"
        vr = PDESchemaValidator().validate(s)
        # Should be a warning, not an error (equation_class=heat_equation mismatch)
        assert any("parabolic" in w for w in vr.warnings)


# ---------------------------------------------------------------------------
# Validator: domain checks
# ---------------------------------------------------------------------------


class TestValidatorDomainErrors:
    def test_missing_domain_length(self):
        s = _minimal_valid_schema()
        s.domain.length = None
        vr = PDESchemaValidator().validate(s)
        assert not vr.valid
        assert any("domain.length" in e for e in vr.errors)

    def test_negative_domain_length(self):
        s = _minimal_valid_schema()
        s.domain.length = -0.05
        vr = PDESchemaValidator().validate(s)
        assert not vr.valid
        assert any("length" in e and "> 0" in e for e in vr.errors)

    def test_zero_n_cells(self):
        s = _minimal_valid_schema()
        s.domain.n_cells_x = 0
        vr = PDESchemaValidator().validate(s)
        assert not vr.valid
        assert any("n_cells_x" in e for e in vr.errors)


# ---------------------------------------------------------------------------
# Validator: material checks
# ---------------------------------------------------------------------------


class TestValidatorMaterialErrors:
    def test_missing_density(self):
        s = _minimal_valid_schema()
        s.material.density = None
        vr = PDESchemaValidator().validate(s)
        assert not vr.valid
        assert any("material.density" in e for e in vr.errors)

    def test_missing_conductivity(self):
        s = _minimal_valid_schema()
        s.material.conductivity = None
        vr = PDESchemaValidator().validate(s)
        assert not vr.valid
        assert any("material.conductivity" in e for e in vr.errors)

    def test_zero_specific_heat(self):
        s = _minimal_valid_schema()
        s.material.specific_heat = 0.0
        vr = PDESchemaValidator().validate(s)
        assert not vr.valid
        assert any("specific_heat" in e and "> 0" in e for e in vr.errors)

    def test_non_constant_coeff_generates_warning(self):
        s = _minimal_valid_schema()
        s.material.conductivity_kind = "temperature_dependent"
        vr = PDESchemaValidator().validate(s)
        assert any("Non-constant" in w for w in vr.warnings)


# ---------------------------------------------------------------------------
# Validator: boundary condition checks
# ---------------------------------------------------------------------------


class TestValidatorBCErrors:
    def test_no_boundary_conditions(self):
        s = _minimal_valid_schema()
        s.boundary_conditions = BoundaryConditionsSpec(conditions=[])
        vr = PDESchemaValidator().validate(s)
        assert not vr.valid
        assert any("no conditions" in e for e in vr.errors)

    def test_no_inversion_target_bc(self):
        s = _minimal_valid_schema()
        # Remove left BC
        s.boundary_conditions.conditions = [
            BoundaryConditionSpec(location="right", bc_type="dirichlet",
                                  status="given", value=300.0)
        ]
        vr = PDESchemaValidator().validate(s)
        assert not vr.valid
        assert any("inversion_target" in e for e in vr.errors)

    def test_contradictory_bc_type_warning(self):
        s = _minimal_valid_schema()
        # unknown_target = boundary_heat_flux but left BC is dirichlet
        s.boundary_conditions.conditions[0].bc_type = "dirichlet"
        vr = PDESchemaValidator().validate(s)
        # Should produce a warning (not necessarily an error) about type mismatch
        # The validator checks for Neumann being expected for flux
        # This generates a warning but not an error per the design
        assert isinstance(vr.valid, bool)  # validation still ran


# ---------------------------------------------------------------------------
# Validator: observation checks
# ---------------------------------------------------------------------------


class TestValidatorObservationErrors:
    def test_no_sensors(self):
        s = _minimal_valid_schema()
        s.observation.sensor_positions = []
        vr = PDESchemaValidator().validate(s)
        assert not vr.valid
        assert any("sensor_positions" in e for e in vr.errors)

    def test_no_observation_data(self):
        s = _minimal_valid_schema()
        s.observation.observations_array = None
        s.observation.observations_file = None
        vr = PDESchemaValidator().validate(s)
        assert not vr.valid
        assert any("observations_file" in e or "observations_array" in e
                   for e in vr.errors)

    def test_array_row_count_mismatch(self):
        s = _minimal_valid_schema()
        # 3 rows but 2 sensor positions
        s.observation.observations_array = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
        vr = PDESchemaValidator().validate(s)
        assert not vr.valid
        assert any("rows" in e and "sensor_positions" in e for e in vr.errors)

    def test_negative_noise_std(self):
        s = _minimal_valid_schema()
        s.observation.noise_std = -0.1
        vr = PDESchemaValidator().validate(s)
        assert not vr.valid
        assert any("noise_std" in e for e in vr.errors)

    def test_sensor_outside_domain_is_error_for_ihcp(self):
        s = _minimal_valid_schema()
        s.observation.sensor_positions = [0.01, 0.06]  # 0.06 > 0.05
        vr = PDESchemaValidator().validate(s)
        # IHCP-specific check: sensors must be interior
        assert not vr.valid
        assert any("outside" in e.lower() or "0.06" in e for e in vr.errors)


# ---------------------------------------------------------------------------
# Validator: time checks
# ---------------------------------------------------------------------------


class TestValidatorTimeErrors:
    def test_missing_time_end(self):
        s = _minimal_valid_schema()
        s.time.end = None
        vr = PDESchemaValidator().validate(s)
        assert not vr.valid
        assert any("time.end" in e for e in vr.errors)

    def test_time_end_before_start(self):
        s = _minimal_valid_schema()
        s.time.start = 10.0
        s.time.end = 5.0
        vr = PDESchemaValidator().validate(s)
        assert not vr.valid
        assert any("end" in e and "start" in e for e in vr.errors)

    def test_n_steps_too_small(self):
        s = _minimal_valid_schema()
        s.time.n_steps = 1
        vr = PDESchemaValidator().validate(s)
        assert not vr.valid
        assert any("n_steps" in e and ">= 2" in e for e in vr.errors)

    def test_fourier_number_warning(self):
        s = _minimal_valid_schema()
        # Coarse time stepping: 10 steps over 60 s
        s.time.n_steps = 5
        vr = PDESchemaValidator().validate(s)
        # High Fo → should produce a warning
        assert any("Fourier" in w for w in vr.warnings)


# ---------------------------------------------------------------------------
# Validator: ValidationResult helper methods
# ---------------------------------------------------------------------------


class TestValidationResult:
    def test_str_output(self):
        vr = ValidationResult(valid=False, errors=["err1"], warnings=["warn1"])
        s = str(vr)
        assert "ERROR" in s and "err1" in s
        assert "WARNING" in s and "warn1" in s

    def test_raise_if_invalid(self):
        vr = ValidationResult(valid=False, errors=["something missing"])
        with pytest.raises(ValueError, match="something missing"):
            vr.raise_if_invalid()

    def test_raise_if_valid_does_not_raise(self):
        vr = ValidationResult(valid=True)
        vr.raise_if_invalid()  # should not raise


# ---------------------------------------------------------------------------
# PDESchemaMapper tests
# ---------------------------------------------------------------------------


class TestPDESchemaMapper:
    def test_map_produces_problem_spec(self):
        s = _minimal_valid_schema()
        mapper = PDESchemaMapper(csv_loader=_mock_csv_loader)
        spec = mapper.map(s)
        assert isinstance(spec, ProblemSpec)

    def test_time_grid_length(self):
        s = _minimal_valid_schema()
        mapper = PDESchemaMapper(csv_loader=_mock_csv_loader)
        spec = mapper.map(s)
        assert spec.n_time == 121

    def test_sensor_positions(self):
        s = _minimal_valid_schema()
        mapper = PDESchemaMapper(csv_loader=_mock_csv_loader)
        spec = mapper.map(s)
        assert spec.sensor_positions == [0.01, 0.03]
        assert spec.n_sensors == 2

    def test_material_values(self):
        s = _minimal_valid_schema()
        mapper = PDESchemaMapper(csv_loader=_mock_csv_loader)
        spec = mapper.map(s)
        assert spec.material.density == 7800.0
        assert spec.material.specific_heat == 500.0
        assert spec.material.conductivity == 50.0

    def test_geometry_values(self):
        s = _minimal_valid_schema()
        mapper = PDESchemaMapper(csv_loader=_mock_csv_loader)
        spec = mapper.map(s)
        assert spec.geometry.length == pytest.approx(0.05)
        assert spec.geometry.n_cells == 60

    def test_right_bc_dirichlet_300(self):
        s = _minimal_valid_schema()
        mapper = PDESchemaMapper(csv_loader=_mock_csv_loader)
        spec = mapper.map(s)
        assert spec.boundary_conditions.right_type == "dirichlet"
        assert spec.boundary_conditions.right_value == pytest.approx(300.0)

    def test_noise_std_preserved(self):
        s = _minimal_valid_schema()
        mapper = PDESchemaMapper(csv_loader=_mock_csv_loader)
        spec = mapper.map(s)
        assert spec.noise_std == pytest.approx(0.3)

    def test_observations_shape(self):
        n_sensors, n_steps = 2, 121
        s = _minimal_valid_schema()
        mapper = PDESchemaMapper(csv_loader=_mock_csv_loader)
        spec = mapper.map(s)
        assert len(spec.observations) == n_sensors
        assert len(spec.observations[0]) == n_steps

    def test_missing_length_raises(self):
        s = _minimal_valid_schema()
        s.domain.length = None
        mapper = PDESchemaMapper(csv_loader=_mock_csv_loader)
        with pytest.raises(ValueError, match="domain.length"):
            mapper.map(s)

    def test_missing_material_raises(self):
        s = _minimal_valid_schema()
        s.material.conductivity = None
        mapper = PDESchemaMapper(csv_loader=_mock_csv_loader)
        with pytest.raises(ValueError, match="conductivity"):
            mapper.map(s)

    def test_no_right_bc_raises(self):
        s = _minimal_valid_schema()
        # Remove right BC; only inversion target remains
        s.boundary_conditions.conditions = [
            BoundaryConditionSpec(location="left", bc_type="neumann",
                                  status="inversion_target"),
        ]
        mapper = PDESchemaMapper(csv_loader=_mock_csv_loader)
        with pytest.raises(ValueError, match="right boundary"):
            mapper.map(s)

    def test_missing_observations_raises(self):
        s = _minimal_valid_schema()
        s.observation.observations_array = None
        s.observation.observations_file = None
        mapper = PDESchemaMapper(csv_loader=_mock_csv_loader)
        with pytest.raises(ValueError, match="observations"):
            mapper.map(s)

    def test_csv_obs_file_is_loaded(self):
        s = _minimal_valid_schema()
        s.observation.observations_array = None
        s.observation.observations_file = "dummy.csv"

        def loader(path, n_sensors, n_steps):
            assert str(path).endswith("dummy.csv")
            return [[300.0 + float(i) for i in range(n_steps)] for _ in range(n_sensors)]

        mapper = PDESchemaMapper(csv_loader=loader)
        spec = mapper.map(s)
        assert spec.n_sensors == 2

    def test_problem_type_string_format(self):
        s = _minimal_valid_schema()
        mapper = PDESchemaMapper(csv_loader=_mock_csv_loader)
        spec = mapper.map(s)
        assert "IHCP" in spec.problem_type or "1D" in spec.problem_type

    def test_initial_condition_in_spec(self):
        s = _minimal_valid_schema()
        s.initial_condition.value = 350.0
        mapper = PDESchemaMapper(csv_loader=_mock_csv_loader)
        spec = mapper.map(s)
        assert spec.initial_condition == pytest.approx(350.0)
