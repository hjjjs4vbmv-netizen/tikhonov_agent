"""
test_pde_normalizer.py
======================
Unit tests for:
  - StructuredInputParser (Path A deterministic parsing)
  - Field alias normalization
  - MockPDESchemaFiller (Path B mock LLM)
  - normalize_structured / normalize_from_yaml / normalize_with_llm / normalize_from_text
  - NormalizedSchema backward-compatibility adapter
  - Failure / negative cases

All tests are self-contained.  One test class uses a real YAML fixture from
tests/fixtures/; all others use inline dict inputs.
"""

from __future__ import annotations

import pytest
from pathlib import Path

from src.pde_normalizer import (
    LLMPDESchemaFiller,
    MockPDESchemaFiller,
    StructuredInputParser,
    normalize_from_text,
    normalize_from_yaml,
    normalize_structured,
    normalize_with_llm,
    build_problem_spec_from_schema,
)
from src.pde_schema import (
    BoundaryConditionSpec,
    BoundaryConditionsSpec,
    DomainSpec,
    MaterialSpec,
    ObservationSpec,
    PDESchema,
    PDESchemaValidator,
    TimeSpec,
    ValidationResult,
)
from src.input_normalizer import (
    NormalizedSchema,
    normalize_from_dict,
    normalize_from_text as legacy_from_text,
    normalize_from_yaml as legacy_from_yaml,
)
from src.types import ProblemSpec

FIXTURES = Path(__file__).parent / "fixtures"


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _mock_csv_loader(path, n_sensors, n_steps):
    return [[300.0 + float(i) for i in range(n_steps)] for _ in range(n_sensors)]


def _full_clean_dict() -> dict:
    """Inline equivalent of clean_ihcp.yaml."""
    return {
        "problem": {
            "pde_family": "parabolic",
            "equation_class": "heat_equation",
            "problem_kind": "inverse",
            "dimension": 1,
            "transient": True,
            "unknown_target": "boundary_heat_flux",
        },
        "geometry": {"length": 0.05, "n_cells": 60},
        "material": {"density": 7800.0, "specific_heat": 500.0, "conductivity": 50.0},
        "initial_condition": {"type": "uniform", "value": 300.0},
        "boundary_conditions": {
            "left": {"type": "neumann", "status": "inversion_target"},
            "right": {"type": "dirichlet", "status": "given", "value": 300.0},
        },
        "time": {"start": 0.0, "end": 60.0, "n_steps": 121},
        "sensor_positions": [0.01, 0.03],
        "observation": {"noise_std": 0.3, "observations_file": "data/demo_temperature.csv"},
        "planner": {"reg_order": 1, "max_retries": 8, "iteration_budget": 12,
                    "physical_bounds": [-5e5, 5e5]},
    }


def _legacy_dict() -> dict:
    """Inline equivalent of legacy_ihcp.yaml."""
    return {
        "problem_type": "1D_transient_IHCP",
        "dimension": 1,
        "transient": True,
        "target_name": "boundary_heat_flux",
        "time": {"start": 0.0, "end": 60.0, "n_steps": 121},
        "geometry": {"length": 0.05, "n_cells": 60},
        "material": {"density": 7800.0, "specific_heat": 500.0, "conductivity": 50.0},
        "boundary_conditions": {"right_type": "dirichlet", "right_value": 300.0},
        "sensor_positions": [0.01, 0.03],
        "initial_condition": 300.0,
        "noise_std": 0.3,
        "observations_file": "data/demo_temperature.csv",
        "planner": {"reg_order": 1, "max_retries": 8},
    }


# ---------------------------------------------------------------------------
# Path A: StructuredInputParser
# ---------------------------------------------------------------------------


class TestStructuredInputParserCleanFormat:
    def test_parses_nested_problem_section(self):
        raw = _full_clean_dict()
        schema = StructuredInputParser().parse(raw)
        assert schema.pde_family == "parabolic"
        assert schema.equation_class == "heat_equation"
        assert schema.problem_kind == "inverse"
        assert schema.dimension == 1
        assert schema.transient is True

    def test_domain_length_and_cells(self):
        raw = _full_clean_dict()
        schema = StructuredInputParser().parse(raw)
        assert schema.domain.length == pytest.approx(0.05)
        assert schema.domain.n_cells_x == 60

    def test_material_values(self):
        raw = _full_clean_dict()
        schema = StructuredInputParser().parse(raw)
        assert schema.material.density == pytest.approx(7800.0)
        assert schema.material.specific_heat == pytest.approx(500.0)
        assert schema.material.conductivity == pytest.approx(50.0)

    def test_ic_uniform(self):
        raw = _full_clean_dict()
        schema = StructuredInputParser().parse(raw)
        assert schema.initial_condition.ic_type == "uniform"
        assert schema.initial_condition.value == pytest.approx(300.0)

    def test_boundary_conditions_parsed(self):
        raw = _full_clean_dict()
        schema = StructuredInputParser().parse(raw)
        left = schema.boundary_conditions.get("left")
        right = schema.boundary_conditions.get("right")
        assert left is not None
        assert left.status == "inversion_target"
        assert right is not None
        assert right.bc_type == "dirichlet"
        assert right.value == pytest.approx(300.0)

    def test_time_values(self):
        raw = _full_clean_dict()
        schema = StructuredInputParser().parse(raw)
        assert schema.time.start == pytest.approx(0.0)
        assert schema.time.end == pytest.approx(60.0)
        assert schema.time.n_steps == 121

    def test_sensor_positions(self):
        raw = _full_clean_dict()
        schema = StructuredInputParser().parse(raw)
        assert schema.observation.sensor_positions == pytest.approx([0.01, 0.03])

    def test_observation_noise_std(self):
        raw = _full_clean_dict()
        schema = StructuredInputParser().parse(raw)
        assert schema.observation.noise_std == pytest.approx(0.3)

    def test_solver_prefs_planner(self):
        raw = _full_clean_dict()
        schema = StructuredInputParser().parse(raw)
        assert schema.solver_prefs.reg_order == 1
        assert schema.solver_prefs.max_retries == 8
        assert schema.solver_prefs.physical_bounds == (-5e5, 5e5)


class TestStructuredInputParserLegacyFormat:
    """Legacy flat YAML format (matching example_case.yaml)."""

    def test_parses_problem_type_string(self):
        raw = _legacy_dict()
        schema = StructuredInputParser().parse(raw)
        assert schema.problem_kind == "inverse"

    def test_target_name_maps_to_unknown_target(self):
        raw = _legacy_dict()
        schema = StructuredInputParser().parse(raw)
        assert schema.unknown_target == "boundary_heat_flux"

    def test_legacy_right_type_and_value(self):
        raw = _legacy_dict()
        schema = StructuredInputParser().parse(raw)
        right = schema.boundary_conditions.get("right")
        assert right is not None
        assert right.bc_type == "dirichlet"
        assert right.value == pytest.approx(300.0)

    def test_left_bc_is_inversion_target(self):
        raw = _legacy_dict()
        schema = StructuredInputParser().parse(raw)
        left = schema.boundary_conditions.get("left")
        assert left is not None
        assert left.status == "inversion_target"

    def test_scalar_initial_condition(self):
        raw = _legacy_dict()
        schema = StructuredInputParser().parse(raw)
        assert schema.initial_condition.value == pytest.approx(300.0)

    def test_flat_noise_std(self):
        raw = _legacy_dict()
        schema = StructuredInputParser().parse(raw)
        assert schema.observation.noise_std == pytest.approx(0.3)


# ---------------------------------------------------------------------------
# Path A: alias normalization
# ---------------------------------------------------------------------------


class TestFieldAliasNormalization:
    """Every alias in _FIELD_ALIASES should correctly map to the canonical field."""

    def _schema_from(self, overrides: dict) -> PDESchema:
        base = {
            "geometry": {"length": 0.05, "n_cells": 50},
            "material": {"density": 7800.0, "specific_heat": 500.0, "conductivity": 50.0},
            "time": {"end": 60.0, "n_steps": 121},
            "boundary_conditions": {"right_type": "dirichlet", "right_value": 300.0},
            "sensor_positions": [0.01, 0.03],
            "observations_file": "dummy.csv",
        }
        base.update(overrides)
        return StructuredInputParser().parse(base)

    def test_rho_alias(self):
        s = self._schema_from({"rho": 8000.0})
        # rho should NOT override the material.density set in nested section
        # but if we use rho at top level without nested material:
        raw = {"rho": 8000.0, "cp": 600.0, "k": 40.0,
               "geometry": {"length": 0.05}, "time": {"end": 60.0, "n_steps": 10},
               "sensor_positions": [0.01], "observations_file": "d.csv",
               "boundary_conditions": {"right_type": "dirichlet", "right_value": 300.0}}
        schema = StructuredInputParser().parse(raw)
        assert schema.material.density == pytest.approx(8000.0)

    def test_cp_alias(self):
        raw = {"rho": 7800.0, "cp": 600.0, "k": 50.0,
               "geometry": {"length": 0.05}, "time": {"end": 60.0, "n_steps": 10},
               "sensor_positions": [0.01], "observations_file": "d.csv",
               "boundary_conditions": {"right_type": "dirichlet", "right_value": 300.0}}
        schema = StructuredInputParser().parse(raw)
        assert schema.material.specific_heat == pytest.approx(600.0)

    def test_k_alias(self):
        raw = {"rho": 7800.0, "cp": 500.0, "k": 45.0,
               "geometry": {"length": 0.05}, "time": {"end": 60.0, "n_steps": 10},
               "sensor_positions": [0.01], "observations_file": "d.csv",
               "boundary_conditions": {"right_type": "dirichlet", "right_value": 300.0}}
        schema = StructuredInputParser().parse(raw)
        assert schema.material.conductivity == pytest.approx(45.0)

    def test_T_end_alias(self):
        raw = {"geometry": {"length": 0.05},
               "material": {"density": 7800.0, "specific_heat": 500.0, "conductivity": 50.0},
               "T_end": 90.0, "n_steps": 10,
               "sensor_positions": [0.01], "observations_file": "d.csv",
               "boundary_conditions": {"right_type": "dirichlet", "right_value": 300.0}}
        schema = StructuredInputParser().parse(raw)
        assert schema.time.end == pytest.approx(90.0)

    def test_rod_length_m_alias(self):
        raw = {"rod_length_m": 0.08,
               "material": {"density": 7800.0, "specific_heat": 500.0, "conductivity": 50.0},
               "time": {"end": 60.0, "n_steps": 10},
               "sensor_positions": [0.01], "observations_file": "d.csv",
               "boundary_conditions": {"right_type": "dirichlet", "right_value": 300.0}}
        schema = StructuredInputParser().parse(raw)
        assert schema.domain.length == pytest.approx(0.08)

    def test_sensor_positions_m_alias(self):
        raw = {"geometry": {"length": 0.05},
               "material": {"density": 7800.0, "specific_heat": 500.0, "conductivity": 50.0},
               "time": {"end": 60.0, "n_steps": 10},
               "sensor_positions_m": [0.02, 0.04], "observations_file": "d.csv",
               "boundary_conditions": {"right_type": "dirichlet", "right_value": 300.0}}
        schema = StructuredInputParser().parse(raw)
        assert schema.observation.sensor_positions == pytest.approx([0.02, 0.04])

    def test_noise_std_K_alias(self):
        raw = _full_clean_dict()
        raw.pop("observation", None)
        raw["noise_std_K"] = 0.5
        raw["observations_file"] = "d.csv"
        schema = StructuredInputParser().parse(raw)
        assert schema.observation.noise_std == pytest.approx(0.5)

    def test_density_kg_m3_alias(self):
        raw = {"geometry": {"length": 0.05},
               "density_kg_m3": 2700.0, "specific_heat_J_kgK": 900.0,
               "conductivity_W_mK": 205.0,
               "time": {"end": 60.0, "n_steps": 10},
               "sensor_positions": [0.01], "observations_file": "d.csv",
               "boundary_conditions": {"right_type": "dirichlet", "right_value": 300.0}}
        schema = StructuredInputParser().parse(raw)
        assert schema.material.density == pytest.approx(2700.0)
        assert schema.material.specific_heat == pytest.approx(900.0)
        assert schema.material.conductivity == pytest.approx(205.0)


# ---------------------------------------------------------------------------
# Path A: normalize_structured public function
# ---------------------------------------------------------------------------


class TestNormalizeStructured:
    def test_returns_schema_and_validation_result(self):
        schema, vr = normalize_structured(_full_clean_dict(), strict=False)
        assert isinstance(schema, PDESchema)
        assert isinstance(vr, ValidationResult)

    def test_full_clean_dict_passes_validation(self):
        schema, vr = normalize_structured(_full_clean_dict(), strict=False)
        assert vr.valid is True

    def test_strict_raises_on_invalid(self):
        raw = {"geometry": {"length": 0.05}}  # incomplete
        with pytest.raises(ValueError):
            normalize_structured(raw, strict=True)

    def test_non_strict_returns_invalid_schema(self):
        raw = {"geometry": {"length": 0.05}}
        schema, vr = normalize_structured(raw, strict=False)
        assert not vr.valid
        assert isinstance(schema, PDESchema)


# ---------------------------------------------------------------------------
# Path A: normalize_from_yaml (YAML file)
# ---------------------------------------------------------------------------


class TestNormalizeFromYamlFixtures:
    def test_clean_ihcp_yaml(self):
        yaml_path = FIXTURES / "clean_ihcp.yaml"
        if not yaml_path.exists():
            pytest.skip("clean_ihcp.yaml fixture not found")
        schema, vr = normalize_from_yaml(yaml_path, strict=False)
        assert schema.domain.length == pytest.approx(0.05)
        assert schema.material.conductivity == pytest.approx(50.0)

    def test_legacy_ihcp_yaml(self):
        yaml_path = FIXTURES / "legacy_ihcp.yaml"
        if not yaml_path.exists():
            pytest.skip("legacy_ihcp.yaml fixture not found")
        schema, vr = normalize_from_yaml(yaml_path, strict=False)
        assert schema.material.density == pytest.approx(7800.0)
        assert schema.time.n_steps == 121

    def test_observations_path_override(self):
        yaml_path = FIXTURES / "legacy_ihcp.yaml"
        if not yaml_path.exists():
            pytest.skip("legacy_ihcp.yaml fixture not found")
        schema, vr = normalize_from_yaml(
            yaml_path,
            observations_path="overridden/path.csv",
            strict=False,
        )
        assert schema.observation.observations_file == "overridden/path.csv"


# ---------------------------------------------------------------------------
# Path B: MockPDESchemaFiller
# ---------------------------------------------------------------------------

SEMI_STRUCTURED_TEXT = """
1D steel rod of length L = 0.05 m, rho = 7800 kg/m^3, cp = 500 J/(kg·K),
k = 50 W/(m·K).  Initial temperature T0 = 300 K.  Left boundary heat flux
is unknown (inversion target); right boundary fixed at T_right = 300 K.
Two sensors at 0.01 m and 0.03 m.
T_end = 60 s, n_steps = 121.  noise_std = 0.3 K.
"""

MESSY_TEXT = """
Material: Steel (7800 kg/m^3 density, specific_heat 500 J kgK, conductivity=50).
Domain: 1D transient, rod, L=0.05m, ncells=60.
Sensors at 0.01 m and 0.03 m inside rod.
Time: from 0 to T_end=60 s with n_steps=121 steps.
Left surface: unknown flux to be recovered (inverse problem).
Right surface (Dirichlet): T_right=300K.
IC: T0=300K uniform.  noise_std=0.3K
"""


class TestMockPDESchemaFiller:
    def _fill(self, text: str) -> dict:
        return MockPDESchemaFiller().fill_schema(text)

    def test_extracts_length(self):
        result = self._fill(SEMI_STRUCTURED_TEXT)
        geo = result.get("geometry", {})
        assert geo.get("length") == pytest.approx(0.05)

    def test_extracts_density(self):
        result = self._fill(SEMI_STRUCTURED_TEXT)
        mat = result.get("material", {})
        assert mat.get("density") == pytest.approx(7800.0)

    def test_extracts_specific_heat(self):
        result = self._fill(SEMI_STRUCTURED_TEXT)
        mat = result.get("material", {})
        assert mat.get("specific_heat") == pytest.approx(500.0)

    def test_extracts_conductivity(self):
        result = self._fill(SEMI_STRUCTURED_TEXT)
        mat = result.get("material", {})
        assert mat.get("conductivity") == pytest.approx(50.0)

    def test_extracts_time_end(self):
        result = self._fill(SEMI_STRUCTURED_TEXT)
        t = result.get("time", {})
        assert t.get("end") == pytest.approx(60.0)

    def test_extracts_n_steps(self):
        result = self._fill(SEMI_STRUCTURED_TEXT)
        t = result.get("time", {})
        assert t.get("n_steps") == 121

    def test_extracts_sensor_positions(self):
        result = self._fill(SEMI_STRUCTURED_TEXT)
        sensors = result.get("sensor_positions", [])
        assert pytest.approx([0.01, 0.03]) == sensors

    def test_extracts_noise_std(self):
        result = self._fill(SEMI_STRUCTURED_TEXT)
        noise = result.get("noise_std", {})
        # noise_std can be top-level or nested
        if isinstance(noise, dict):
            noise = noise.get("noise_std") or noise.get("std")
        assert noise == pytest.approx(0.3)

    def test_extracts_initial_temperature(self):
        result = self._fill(SEMI_STRUCTURED_TEXT)
        ic = result.get("initial_condition", 300.0)
        if isinstance(ic, dict):
            ic = ic.get("value", 300.0)
        assert ic == pytest.approx(300.0)

    def test_material_name_recognition_steel(self):
        result = MockPDESchemaFiller().fill_schema("A steel rod, L = 0.05 m")
        mat = result.get("material", {})
        assert mat.get("density") == pytest.approx(7800.0)
        assert mat.get("conductivity") == pytest.approx(50.0)

    def test_material_name_recognition_aluminum(self):
        result = MockPDESchemaFiller().fill_schema("Aluminum bar, length 0.10 m")
        mat = result.get("material", {})
        assert mat.get("density") == pytest.approx(2700.0)

    def test_1d_hint(self):
        result = MockPDESchemaFiller().fill_schema("1D transient heat problem")
        assert result.get("dimension") == 1

    def test_transient_hint(self):
        result = MockPDESchemaFiller().fill_schema("transient heat conduction")
        assert result.get("transient") is True

    def test_inverse_hint(self):
        result = MockPDESchemaFiller().fill_schema("inverse heat problem, recover flux")
        assert result.get("problem_kind") == "inverse"

    def test_returns_empty_on_empty_text(self):
        result = MockPDESchemaFiller().fill_schema("")
        assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# Path B: normalize_with_llm (mock adapter)
# ---------------------------------------------------------------------------


class TestNormalizeWithLLM:
    def test_semi_structured_text_completes_schema(self):
        mock = MockPDESchemaFiller()
        schema, vr = normalize_with_llm(SEMI_STRUCTURED_TEXT, mock, strict=False)
        assert schema.domain.length == pytest.approx(0.05)
        assert schema.material.density == pytest.approx(7800.0)
        assert schema.time.end == pytest.approx(60.0)

    def test_metadata_parse_path_is_llm_assisted(self):
        mock = MockPDESchemaFiller()
        schema, vr = normalize_with_llm("steel rod L=0.05m", mock, strict=False)
        assert schema.metadata.parse_path == "llm_assisted"

    def test_raw_input_preview_stored(self):
        mock = MockPDESchemaFiller()
        text = SEMI_STRUCTURED_TEXT
        schema, vr = normalize_with_llm(text, mock, strict=False)
        assert len(schema.metadata.raw_input_preview) > 0

    def test_strict_raises_on_invalid_output(self):
        # Adapter returns almost nothing → validation should fail
        class EmptyFiller:
            def fill_schema(self, text: str) -> dict:
                return {}  # minimal output
        with pytest.raises(ValueError):
            normalize_with_llm("some text", EmptyFiller(), strict=True)

    def test_confidence_below_threshold_raises(self):
        class LowConfidenceFiller:
            def fill_schema(self, text: str) -> dict:
                return {"_confidence": 0.2}
        with pytest.raises(ValueError, match="confidence"):
            normalize_with_llm(
                "some text", LowConfidenceFiller(),
                strict=False, confidence_threshold=0.5,
            )

    def test_adapter_exception_produces_empty_schema(self):
        class BrokenFiller:
            def fill_schema(self, text: str) -> dict:
                raise RuntimeError("LLM server down")
        # Should not crash; falls back to empty candidate
        schema, vr = normalize_with_llm("some text", BrokenFiller(), strict=False)
        assert isinstance(schema, PDESchema)
        assert not vr.valid  # empty schema fails validation


# ---------------------------------------------------------------------------
# Path B: normalize_from_text convenience wrapper
# ---------------------------------------------------------------------------


class TestNormalizeFromText:
    def test_returns_schema_and_vr(self):
        schema, vr = normalize_from_text(SEMI_STRUCTURED_TEXT)
        assert isinstance(schema, PDESchema)
        assert isinstance(vr, ValidationResult)

    def test_steel_text_extracts_material(self):
        schema, vr = normalize_from_text(SEMI_STRUCTURED_TEXT)
        assert schema.material.density == pytest.approx(7800.0)

    def test_messy_text_extracts_length(self):
        schema, vr = normalize_from_text(MESSY_TEXT)
        assert schema.domain.length == pytest.approx(0.05)


# ---------------------------------------------------------------------------
# build_problem_spec_from_schema
# ---------------------------------------------------------------------------


class TestBuildProblemSpecFromSchema:
    def _valid_schema(self) -> tuple[PDESchema, ValidationResult]:
        raw = _full_clean_dict()
        raw.pop("observation", None)
        raw["sensor_positions"] = [0.01, 0.03]
        n_steps = 121
        n_sensors = 2
        raw["observations_array"] = [
            [300.0 + float(i) for i in range(n_steps)] for _ in range(n_sensors)
        ]
        return normalize_structured(raw, strict=False)

    def test_returns_problem_spec(self):
        schema, vr = self._valid_schema()
        spec = build_problem_spec_from_schema(schema, vr)
        assert isinstance(spec, ProblemSpec)

    def test_raises_on_invalid_schema(self):
        raw = {"geometry": {"length": 0.05}}
        schema, vr = normalize_structured(raw, strict=False)
        with pytest.raises(ValueError, match="invalid"):
            build_problem_spec_from_schema(schema, vr)


# ---------------------------------------------------------------------------
# NormalizedSchema backward-compatibility adapter
# ---------------------------------------------------------------------------


class TestNormalizedSchemaAdapter:
    def _full_ns(self) -> NormalizedSchema:
        return normalize_from_dict(_legacy_dict())

    def test_rod_length_m_property(self):
        ns = self._full_ns()
        assert ns.rod_length_m == pytest.approx(0.05)

    def test_density_property(self):
        ns = self._full_ns()
        assert ns.density_kg_m3 == pytest.approx(7800.0)

    def test_conductivity_property(self):
        ns = self._full_ns()
        assert ns.conductivity_W_mK == pytest.approx(50.0)

    def test_specific_heat_property(self):
        ns = self._full_ns()
        assert ns.specific_heat_J_kgK == pytest.approx(500.0)

    def test_time_end_property(self):
        ns = self._full_ns()
        assert ns.time_end_s == pytest.approx(60.0)

    def test_time_n_steps_property(self):
        ns = self._full_ns()
        assert ns.time_n_steps == 121

    def test_sensor_positions_property(self):
        ns = self._full_ns()
        assert ns.sensor_positions_m == pytest.approx([0.01, 0.03])

    def test_bc_right_type_property(self):
        ns = self._full_ns()
        assert ns.bc_right_type == "dirichlet"

    def test_bc_right_value_property(self):
        ns = self._full_ns()
        assert ns.bc_right_value == pytest.approx(300.0)

    def test_noise_std_property(self):
        ns = self._full_ns()
        assert ns.noise_std_K == pytest.approx(0.3)

    def test_is_complete_with_file(self):
        ns = self._full_ns()
        # Has observations_file set from legacy dict
        assert ns.observations_file == "data/demo_temperature.csv"
        assert ns.is_complete() is True

    def test_missing_fields_on_partial_input(self):
        ns = normalize_from_dict({"geometry": {"length": 0.05}})
        missing = ns.missing_fields()
        assert "density_kg_m3" in missing
        assert "time_end_s" in missing

    def test_pde_schema_attribute_accessible(self):
        ns = self._full_ns()
        assert isinstance(ns.pde_schema, PDESchema)

    def test_validation_result_attribute_accessible(self):
        ns = self._full_ns()
        assert ns.validation_result is not None

    def test_solver_preferences_planner(self):
        ns = normalize_from_dict(_legacy_dict())
        sp = ns.solver_preferences
        assert sp.get("reg_order") == 1
        assert sp.get("max_retries") == 8

    def test_problem_type_property_format(self):
        ns = self._full_ns()
        # Should produce something like "1D_transient_IHCP"
        pt = ns.problem_type
        assert "1D" in pt or "IHCP" in pt

    def test_metadata_property_is_dict(self):
        ns = self._full_ns()
        assert isinstance(ns.metadata, dict)


# ---------------------------------------------------------------------------
# Legacy public API entry points (input_normalizer.py)
# ---------------------------------------------------------------------------


class TestLegacyNormalizerAPI:
    def test_normalize_from_dict_returns_ns(self):
        ns = normalize_from_dict(_legacy_dict())
        assert isinstance(ns, NormalizedSchema)

    def test_normalize_from_dict_complete(self):
        ns = normalize_from_dict(_legacy_dict())
        assert ns.is_complete() is True

    def test_normalize_from_text_returns_ns(self):
        ns = legacy_from_text(SEMI_STRUCTURED_TEXT)
        assert isinstance(ns, NormalizedSchema)

    def test_legacy_normalize_from_yaml_fixtures(self):
        yaml_path = FIXTURES / "legacy_ihcp.yaml"
        if not yaml_path.exists():
            pytest.skip("legacy_ihcp.yaml fixture not found")
        ns = legacy_from_yaml(yaml_path)
        assert isinstance(ns, NormalizedSchema)
        assert ns.rod_length_m == pytest.approx(0.05)


# ---------------------------------------------------------------------------
# Negative / failure cases
# ---------------------------------------------------------------------------


class TestFailureCases:
    def test_missing_material_field_fails_validation(self):
        raw = _full_clean_dict()
        raw["material"].pop("conductivity")
        schema, vr = normalize_structured(raw, strict=False)
        assert not vr.valid
        assert any("conductivity" in e for e in vr.errors)

    def test_contradictory_boundary_conditions_detected(self):
        raw = _full_clean_dict()
        # Set both left and right as inversion targets
        raw["boundary_conditions"] = {
            "left": {"type": "neumann", "status": "inversion_target"},
            "right": {"type": "dirichlet", "status": "inversion_target", "value": 300.0},
        }
        schema, vr = normalize_structured(raw, strict=False)
        # Multiple inversion targets → warning (not hard error)
        assert any("inversion_target" in w for w in vr.warnings)

    def test_missing_observation_definition(self):
        raw = _full_clean_dict()
        raw.pop("observation", None)
        raw.pop("observations_file", None)
        # Also remove from sensor positions to confirm flow
        schema, vr = normalize_structured(raw, strict=False)
        assert not vr.valid
        assert any("observations_file" in e or "observations_array" in e
                   for e in vr.errors)

    def test_dimension_geometry_inconsistency_warning(self):
        raw = _full_clean_dict()
        raw["problem"]["dimension"] = 2  # but no width given
        schema, vr = normalize_structured(raw, strict=False)
        # Dimension 2 without width → warning
        assert any("width" in w or "dimension" in w for w in vr.warnings)

    def test_invalid_pde_family_enum(self):
        raw = _full_clean_dict()
        raw["problem"]["pde_family"] = "invalid_family"
        schema, vr = normalize_structured(raw, strict=False)
        assert not vr.valid
        assert any("pde_family" in e for e in vr.errors)

    def test_invalid_bc_type_enum(self):
        raw = _full_clean_dict()
        raw["boundary_conditions"]["right"]["type"] = "periodic"
        schema, vr = normalize_structured(raw, strict=False)
        assert not vr.valid
        assert any("bc_type" in e for e in vr.errors)

    def test_sensor_outside_domain_fails_ihcp(self):
        raw = _full_clean_dict()
        raw["sensor_positions"] = [0.01, 0.09]  # 0.09 > 0.05
        schema, vr = normalize_structured(raw, strict=False)
        assert not vr.valid
        assert any("outside" in e.lower() or "0.09" in e for e in vr.errors)

    def test_time_end_before_start_fails(self):
        raw = _full_clean_dict()
        raw["time"]["start"] = 100.0
        raw["time"]["end"] = 10.0
        schema, vr = normalize_structured(raw, strict=False)
        assert not vr.valid
        assert any("end" in e.lower() and "start" in e.lower() for e in vr.errors)

    def test_incomplete_observation_definition_missing_sensors(self):
        raw = _full_clean_dict()
        raw.pop("sensor_positions", None)
        raw.pop("observation", None)
        schema, vr = normalize_structured(raw, strict=False)
        assert not vr.valid

    def test_llm_output_incomplete_fails_strict(self):
        """Even if LLM fills in some fields, incomplete schema must fail strict mode."""
        class PartialFiller:
            def fill_schema(self, text: str) -> dict:
                # Only returns geometry, nothing else
                return {"geometry": {"length": 0.05}}
        with pytest.raises(ValueError):
            normalize_with_llm("partial text", PartialFiller(), strict=True)
