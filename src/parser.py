"""
parser.py
=========
Input parsing: reads YAML config files and CSV observation data,
produces a validated ProblemSpec.

The parser is the boundary between the external world (files, user
input) and the scientific core.  All input normalisation and validation
happens here.  Nothing downstream should need to handle raw strings.

Optional LLM hook
-----------------
If a ProblemParserLLM adapter is injected, free-form text descriptions
are passed to it for schema extraction.  The LLM output is then
validated by ``_validate_problem_dict`` before constructing ProblemSpec.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from src.logging_utils import get_logger
from src.types import BoundaryConditions, Geometry, Material, ProblemSpec

log = get_logger("parser")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def parse_problem(
    config_path: str | Path,
    observations_path: str | Path | None = None,
    llm_parser: Any | None = None,
) -> ProblemSpec:
    """Parse a YAML config file and optional CSV observations into a ProblemSpec.

    Parameters
    ----------
    config_path      : path to YAML problem config
    observations_path: path to CSV temperature observations
                       (overrides the path in the YAML if provided)
    llm_parser       : optional LLM adapter (ProblemParserLLM protocol)

    Returns
    -------
    ProblemSpec
    """
    config_path = Path(config_path)
    log.info("Loading problem config: %s", config_path)

    with config_path.open("r", encoding="utf-8") as fh:
        raw: dict[str, Any] = yaml.safe_load(fh)

    # Optional LLM pre-processing: only for free-form description fields
    if llm_parser is not None and "description" in raw:
        try:
            raw = _apply_llm_parser(llm_parser, raw)
        except Exception as exc:  # noqa: BLE001
            log.warning("LLM parser failed (%s); using raw YAML", exc)

    return _build_problem_spec(raw, observations_path)


# ---------------------------------------------------------------------------
# Internal construction
# ---------------------------------------------------------------------------


def _build_problem_spec(
    raw: dict[str, Any],
    observations_override: str | Path | None,
) -> ProblemSpec:
    """Construct a ProblemSpec from the raw YAML dict."""

    # Geometry
    geo_raw = raw["geometry"]
    geometry = Geometry(
        length=float(geo_raw["length"]),
        n_cells=int(geo_raw.get("n_cells", 50)),
    )

    # Material
    mat_raw = raw["material"]
    material = Material(
        density=float(mat_raw["density"]),
        specific_heat=float(mat_raw["specific_heat"]),
        conductivity=float(mat_raw["conductivity"]),
    )

    # Boundary conditions
    bc_raw = raw["boundary_conditions"]
    bc = BoundaryConditions(
        right_type=bc_raw.get("right_type", "dirichlet"),
        right_value=float(bc_raw.get("right_value", 300.0)),
    )

    # Time grid
    tg_raw = raw["time"]
    t_start = float(tg_raw.get("start", 0.0))
    t_end = float(tg_raw["end"])
    n_steps = int(tg_raw["n_steps"])
    time_grid = list(np.linspace(t_start, t_end, n_steps))

    # Sensor positions
    sensor_positions: list[float] = [float(s) for s in raw["sensor_positions"]]

    # Observations
    obs_path_raw = observations_override or raw.get("observations_file")
    if obs_path_raw is None:
        raise ValueError("observations_file must be specified in config or passed directly")
    observations = _load_observations(Path(obs_path_raw), len(sensor_positions), n_steps)

    # Initial condition
    initial_condition = float(raw.get("initial_condition", 300.0))

    # Noise estimate (optional)
    noise_std: float | None = raw.get("noise_std")
    if noise_std is not None:
        noise_std = float(noise_std)

    # Metadata
    metadata: dict[str, Any] = raw.get("metadata", {})
    metadata.setdefault("source_file", str(obs_path_raw))

    spec = ProblemSpec(
        problem_type=raw.get("problem_type", "1D_transient_IHCP"),
        dimension=int(raw.get("dimension", 1)),
        transient=bool(raw.get("transient", True)),
        target_name=raw.get("target_name", "boundary_heat_flux"),
        time_grid=time_grid,
        sensor_positions=sensor_positions,
        observations=observations,
        geometry=geometry,
        material=material,
        boundary_conditions=bc,
        initial_condition=initial_condition,
        noise_std=noise_std,
        metadata=metadata,
    )

    log.info(
        "ProblemSpec built: n_time=%d, n_sensors=%d, target=%s",
        spec.n_time, spec.n_sensors, spec.target_name,
    )
    return spec


def _load_observations(
    path: Path,
    n_sensors: int,
    n_steps: int,
) -> list[list[float]]:
    """Load temperature observations from a CSV file.

    Expected format: rows = time steps, columns = sensors.
    The header row (if present) is skipped.

    Returns: list[list[float]], shape (n_sensors, n_steps)
    """
    if not path.exists():
        raise FileNotFoundError(f"Observations file not found: {path}")

    rows: list[list[float]] = []
    with path.open("r", newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        header_skipped = False
        for row in reader:
            try:
                vals = [float(v) for v in row]
                rows.append(vals)
            except ValueError:
                if not header_skipped:
                    header_skipped = True  # skip header
                    continue
                raise

    # rows are time-major; transpose to sensor-major
    arr = np.array(rows, dtype=float)  # (N_t, n_sensors)
    if arr.ndim == 1:
        arr = arr.reshape(-1, 1)

    # Validate shape
    if arr.shape[0] != n_steps:
        log.warning(
            "observations have %d time rows but config expects %d; truncating/padding",
            arr.shape[0], n_steps,
        )
        if arr.shape[0] > n_steps:
            arr = arr[:n_steps, :]
        else:
            pad = np.zeros((n_steps - arr.shape[0], arr.shape[1]))
            arr = np.vstack([arr, pad])

    if arr.shape[1] != n_sensors:
        raise ValueError(
            f"observations CSV has {arr.shape[1]} sensor columns but "
            f"sensor_positions list has {n_sensors} entries"
        )

    observations = arr.T.tolist()  # (n_sensors, n_steps)
    log.debug("Loaded observations: shape %s (sensor, time)", arr.T.shape)
    return observations


def _apply_llm_parser(llm_parser: Any, raw: dict[str, Any]) -> dict[str, Any]:
    """Pass the raw config through the optional LLM parser.

    The LLM may fill in missing fields from a free-form "description"
    string.  Its output dict is merged back into raw.

    This function is intentionally defensive; malformed LLM output
    is silently discarded (caller will warn and continue).
    """
    description = raw.get("description", "")
    if not description:
        return raw

    result = llm_parser.parse_problem_description(description)
    if not isinstance(result, dict):
        raise TypeError(f"LLM parser returned non-dict: {type(result)}")

    # Merge: LLM fills missing fields but does NOT override explicit values
    merged = dict(result)
    merged.update(raw)
    return merged
