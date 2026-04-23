"""
sensitivity.py
==============
Build the sensitivity (response) matrix G for the 1D IHCP.

Physics background
------------------
For a *linear* forward model and a piecewise-constant parameterisation
of the unknown boundary heat flux q(t), the relationship between the
N_params flux parameters x and the M observation values y (stacked
sensor×time) is:

    y = G x + y_0

where
  y_0 = forward model output with q ≡ 0   (baseline / natural response)
  G   = response matrix  (M × N_params)

Column j of G is the incremental sensor output when x_j = 1 and all
other x_k = 0  (unit-pulse simulation minus baseline).

For piecewise-constant parameterisation with N_params segments, each
segment covers time steps  [j * seg_len, (j+1) * seg_len).

Extension notes
---------------
- Piecewise-linear or B-spline parameterisations can be handled by
  replacing ``_build_q_from_params`` and adjusting the column loop.
- Non-linear forward models require an iterative / adjoint approach
  and are out of scope for Version 1.
"""

from __future__ import annotations

import numpy as np

from src.forward_model import HeatConductionFD
from src.types import InversionConfig, ProblemSpec


def build_sensitivity_matrix(
    problem: ProblemSpec,
    config: InversionConfig,
    model: HeatConductionFD,
    sensor_indices: list[int],
) -> tuple[np.ndarray, np.ndarray]:
    """Compute the response matrix G and the baseline observation vector y_0.

    Parameters
    ----------
    problem       : parsed problem specification
    config        : inversion configuration (parameterisation details)
    model         : pre-built forward model instance
    sensor_indices: spatial cell indices of each sensor

    Returns
    -------
    G    : ndarray, shape (n_obs, n_params)
           n_obs   = n_sensors * N_t
           n_params = config.num_parameters
    y_0  : ndarray, shape (n_obs,)
           Baseline (zero-flux) observation vector.
    """
    N_t = problem.n_time
    n_sensors = problem.n_sensors
    n_params = config.num_parameters
    T0 = problem.initial_condition

    # ------------------------------------------------------------------
    # Baseline: run forward model with q ≡ 0
    # ------------------------------------------------------------------
    q_zero = np.zeros(N_t)
    T_baseline = model.simulate(q_zero, T0, sensor_indices)  # (n_sensors, N_t)
    y_0 = T_baseline.flatten(order="C")                      # row-major flatten

    # ------------------------------------------------------------------
    # Segment boundaries for piecewise-constant parameterisation
    # ------------------------------------------------------------------
    seg_boundaries = _segment_boundaries(N_t, n_params)

    # ------------------------------------------------------------------
    # Response matrix: one column per parameter
    # ------------------------------------------------------------------
    M = n_sensors * N_t
    G = np.zeros((M, n_params))

    for j in range(n_params):
        q_unit = np.zeros(N_t)
        t_start, t_end = seg_boundaries[j]
        q_unit[t_start:t_end] = 1.0   # unit pulse in segment j

        T_response = model.simulate(q_unit, T0, sensor_indices)
        y_response = T_response.flatten(order="C")

        # Incremental response = response - baseline (linearity)
        G[:, j] = y_response - y_0

    return G, y_0


def _segment_boundaries(N_t: int, n_params: int) -> list[tuple[int, int]]:
    """Return (start, end) time-index pairs for each piecewise-constant segment.

    The last segment absorbs any remainder so that all time steps are
    covered exactly once.
    """
    seg_len = N_t // n_params
    boundaries: list[tuple[int, int]] = []
    for j in range(n_params):
        t_start = j * seg_len
        t_end = (j + 1) * seg_len if j < n_params - 1 else N_t
        boundaries.append((t_start, t_end))
    return boundaries


def params_to_flux(
    x: np.ndarray,
    N_t: int,
) -> np.ndarray:
    """Expand inversion parameters x back to a full time-series flux array.

    For piecewise-constant parameterisation: each parameter fills its
    corresponding time segment.

    Parameters
    ----------
    x    : shape (n_params,) – recovered flux parameters
    N_t  : total number of time steps

    Returns
    -------
    q    : shape (N_t,) – heat flux at every time step
    """
    n_params = len(x)
    seg_boundaries = _segment_boundaries(N_t, n_params)
    q = np.zeros(N_t)
    for j, (t_start, t_end) in enumerate(seg_boundaries):
        q[t_start:t_end] = x[j]
    return q
