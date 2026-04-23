"""
test_case_generation.py
=======================
Tests for experiments/generate_cases.py — verify reproducibility and file layout.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

# Allow imports from project root
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from experiments.utils import (
    build_time_grid,
    generate_flux,
    make_ramp_flux,
    make_single_pulse_flux,
    make_step_flux,
    make_smooth_sinusoid_flux,
    make_multi_pulse_flux,
)
from experiments.generate_cases import generate_case, _write_case_config
from src.types import BoundaryConditions, Geometry, Material


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def small_setup():
    """Minimal physical setup for fast testing."""
    geometry = Geometry(length=0.05, n_cells=20)
    material = Material(density=7800.0, specific_heat=500.0, conductivity=50.0)
    bc = BoundaryConditions(right_type="dirichlet", right_value=300.0)
    time_grid = build_time_grid(0.0, 10.0, 21)   # 21 steps, dt=0.5 s
    sensor_positions = [0.01, 0.03]
    return geometry, material, bc, time_grid, sensor_positions


# ---------------------------------------------------------------------------
# Flux generator tests
# ---------------------------------------------------------------------------

class TestFluxGenerators:
    def test_step_shape(self):
        tg = build_time_grid(0.0, 10.0, 21)
        q = make_step_flux(tg, q_base=0.0, q_step=50_000.0, t_on_frac=0.3)
        assert q.shape == (21,)
        assert q[0] == 0.0           # before step
        assert q[-1] == pytest.approx(50_000.0)  # after step

    def test_ramp_shape(self):
        tg = build_time_grid(0.0, 10.0, 21)
        q = make_ramp_flux(tg, q_start=0.0, q_end=80_000.0)
        assert q.shape == (21,)
        assert q[0] == pytest.approx(0.0)
        assert q[-1] == pytest.approx(80_000.0)

    def test_single_pulse_peak(self):
        tg = build_time_grid(0.0, 10.0, 101)
        q = make_single_pulse_flux(tg, q_base=0.0, q_peak=60_000.0,
                                   t_center_frac=0.5, t_width_frac=0.1)
        assert q.shape == (101,)
        assert q.max() == pytest.approx(60_000.0, rel=1e-3)
        # Peak should be near the centre
        peak_idx = int(np.argmax(q))
        assert abs(peak_idx - 50) <= 3

    def test_multi_pulse_n_peaks(self):
        tg = build_time_grid(0.0, 10.0, 201)
        q = make_multi_pulse_flux(tg, q_base=0.0, q_peak=50_000.0,
                                  n_pulses=3, t_width_frac=0.04)
        # Should have roughly 3 local maxima
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(q, prominence=10_000)
        assert len(peaks) == 3

    def test_sinusoid_mean(self):
        tg = build_time_grid(0.0, 10.0, 201)
        q = make_smooth_sinusoid_flux(tg, q_mean=40_000.0, q_amplitude=20_000.0)
        assert np.mean(q) == pytest.approx(40_000.0, rel=0.05)

    def test_generate_flux_dispatch(self):
        tg = build_time_grid(0.0, 10.0, 21)
        for family in ["step", "ramp", "single_pulse", "multi_pulse", "smooth_sinusoid"]:
            q = generate_flux(family, tg, {})
            assert q.shape == (21,), f"Wrong shape for {family}"

    def test_generate_flux_unknown_raises(self):
        tg = build_time_grid(0.0, 10.0, 21)
        with pytest.raises(ValueError, match="Unknown flux family"):
            generate_flux("bogus", tg, {})


# ---------------------------------------------------------------------------
# Case generation tests
# ---------------------------------------------------------------------------

class TestGenerateCase:
    def test_case_files_created(self, tmp_path, small_setup):
        geometry, material, bc, time_grid, sensor_positions = small_setup
        rng = np.random.default_rng(42)
        case_dir = tmp_path / "case_0001"

        generate_case(
            case_dir=case_dir,
            time_grid=time_grid,
            geometry=geometry,
            material=material,
            bc=bc,
            initial_condition=300.0,
            sensor_positions=sensor_positions,
            flux_family="step",
            flux_params={"q_base": 0.0, "q_step": 50_000.0, "t_on_frac": 0.3},
            noise_level=0.5,
            noise_std_in_config=None,
            rng=rng,
        )

        assert (case_dir / "config.yaml").exists()
        assert (case_dir / "observations.csv").exists()
        assert (case_dir / "truth.npz").exists()

    def test_truth_arrays_shape(self, tmp_path, small_setup):
        geometry, material, bc, time_grid, sensor_positions = small_setup
        rng = np.random.default_rng(42)
        case_dir = tmp_path / "case_0001"

        generate_case(
            case_dir=case_dir,
            time_grid=time_grid,
            geometry=geometry,
            material=material,
            bc=bc,
            initial_condition=300.0,
            sensor_positions=sensor_positions,
            flux_family="ramp",
            flux_params={"q_start": 0.0, "q_end": 60_000.0},
            noise_level=0.3,
            noise_std_in_config=None,
            rng=rng,
        )

        data = np.load(case_dir / "truth.npz")
        assert "q_true" in data
        assert "time_grid" in data
        assert data["q_true"].shape == (len(time_grid),)
        assert data["time_grid"].shape == (len(time_grid),)

    def test_observations_csv_shape(self, tmp_path, small_setup):
        geometry, material, bc, time_grid, sensor_positions = small_setup
        rng = np.random.default_rng(42)
        case_dir = tmp_path / "case_0001"

        generate_case(
            case_dir=case_dir,
            time_grid=time_grid,
            geometry=geometry,
            material=material,
            bc=bc,
            initial_condition=300.0,
            sensor_positions=sensor_positions,
            flux_family="step",
            flux_params={},
            noise_level=0.1,
            noise_std_in_config=None,
            rng=rng,
        )

        import pandas as pd
        obs = pd.read_csv(case_dir / "observations.csv")
        n_t = len(time_grid)
        n_s = len(sensor_positions)
        assert obs.shape == (n_t, n_s), f"Expected ({n_t}, {n_s}), got {obs.shape}"

    def test_reproducibility(self, tmp_path, small_setup):
        """Same seed → same observations."""
        geometry, material, bc, time_grid, sensor_positions = small_setup
        import pandas as pd

        for run_idx in range(2):
            rng = np.random.default_rng(99)
            case_dir = tmp_path / f"run_{run_idx}" / "case_0001"
            generate_case(
                case_dir=case_dir,
                time_grid=time_grid,
                geometry=geometry,
                material=material,
                bc=bc,
                initial_condition=300.0,
                sensor_positions=sensor_positions,
                flux_family="step",
                flux_params={},
                noise_level=0.5,
                noise_std_in_config=None,
                rng=rng,
            )

        obs0 = pd.read_csv(tmp_path / "run_0" / "case_0001" / "observations.csv")
        obs1 = pd.read_csv(tmp_path / "run_1" / "case_0001" / "observations.csv")
        np.testing.assert_allclose(obs0.values, obs1.values)

    def test_config_yaml_parseable(self, tmp_path, small_setup):
        """Generated config.yaml is parseable by src.parser.parse_problem."""
        geometry, material, bc, time_grid, sensor_positions = small_setup
        rng = np.random.default_rng(7)
        case_dir = tmp_path / "case_yaml"

        generate_case(
            case_dir=case_dir,
            time_grid=time_grid,
            geometry=geometry,
            material=material,
            bc=bc,
            initial_condition=300.0,
            sensor_positions=sensor_positions,
            flux_family="smooth_sinusoid",
            flux_params={"q_mean": 40_000.0, "q_amplitude": 20_000.0},
            noise_level=0.5,
            noise_std_in_config=None,
            rng=rng,
        )

        from src.parser import parse_problem
        spec = parse_problem(case_dir / "config.yaml")
        assert spec.n_time == len(time_grid)
        assert spec.n_sensors == len(sensor_positions)
        assert spec.noise_std == pytest.approx(0.5)
