"""
heat2d_simulator.py
===================
2D transient heat conduction forward simulator (explicit finite differences).

PDE
---
    u_t = alpha * (u_xx + u_yy)

Domain
------
    x ∈ [0, Lx],  y ∈ [0, Ly],  t ∈ [0, T_total]

Boundary conditions
-------------------
    x = 0  (left):  Neumann  →  −k · ∂u/∂x = q(y, t)  (inversion target)
    x = Lx (right): insulated (Neumann = 0)
    y = 0  (bottom): insulated (Neumann = 0)
    y = Ly (top):    insulated (Neumann = 0)

Initial condition
-----------------
    u(x, y, 0) = T0  (uniform)

Numerical scheme
----------------
Explicit Euler in time, second-order central differences in space.
The time step is chosen automatically to satisfy the Von Neumann stability
criterion:  dt ≤ dx² / (2 · alpha · (1/dx² + 1/dy²)).

The stability condition for the 2D explicit scheme is:

    dt < dx² * dy² / (2 * alpha * (dx² + dy²))

For a uniform grid (dx = dy):  dt < dx² / (4 * alpha)

This module also provides:
    - generate_sensor_grid(config, Lx, Ly)   — deterministic sensor positions
    - generate_flux_2d(target_type, ...)      — benchmark ground-truth flux
"""

from __future__ import annotations

from itertools import product
from typing import Literal

import numpy as np
from scipy.interpolate import RegularGridInterpolator


# ---------------------------------------------------------------------------
# Physical defaults (SI units)
# ---------------------------------------------------------------------------

DEFAULT_LX: float = 0.1          # [m] domain length in x
DEFAULT_LY: float = 0.1          # [m] domain length in y
DEFAULT_ALPHA: float = 1e-5      # [m^2/s] thermal diffusivity
DEFAULT_K: float = 1.0           # [W/(m·K)] conductivity (used only for BC)
DEFAULT_T0: float = 300.0        # [K] uniform initial temperature
DEFAULT_T_TOTAL: float = 100.0   # [s] simulation horizon
DEFAULT_NX: int = 20             # spatial cells in x
DEFAULT_NY: int = 20             # spatial cells in y

# Benchmark flux amplitude [W/m^2]
# Chosen so that peak temperature rise ≈ 5–10 K above noise level (0.1–1 K)
DEFAULT_Q_MAX: float = 1_000.0   # gives ~5 K rise over 100 s for above params


# ---------------------------------------------------------------------------
# Sensor grid generator
# ---------------------------------------------------------------------------

SensorConfig = Literal["sparse", "medium", "dense"]

_SENSOR_GRID_SIZES: dict[str, tuple[int, int]] = {
    "sparse": (2, 2),    # 4 sensors
    "medium": (3, 3),    # 9 sensors
    "dense":  (4, 4),    # 16 sensors
}


def generate_sensor_grid(
    config: SensorConfig,
    Lx: float = DEFAULT_LX,
    Ly: float = DEFAULT_LY,
    jitter_frac: float = 0.0,
    rng: np.random.Generator | None = None,
) -> list[tuple[float, float]]:
    """Generate a deterministic 2D sensor grid.

    Sensors are placed on a uniform interior grid, avoiding domain boundaries.

    Parameters
    ----------
    config      : "sparse" (2×2=4), "medium" (3×3=9), or "dense" (4×4=16)
    Lx, Ly      : domain dimensions [m]
    jitter_frac : optional fractional jitter (<= 0.02 for realism).
                  Jitter is added from `rng` but sensor COUNT / layout are
                  fully deterministic.  Set to 0 (default) for pure
                  determinism.
    rng         : random generator for reproducible jitter (ignored if
                  jitter_frac == 0)

    Returns
    -------
    List of (x, y) sensor positions in [m], length n_sensor.
    """
    nx_s, ny_s = _SENSOR_GRID_SIZES[config]
    xs = np.linspace(0.1 * Lx, 0.9 * Lx, nx_s)
    ys = np.linspace(0.1 * Ly, 0.9 * Ly, ny_s)

    positions: list[tuple[float, float]] = []
    for xi, yj in product(xs, ys):
        x = float(xi)
        y = float(yj)
        if jitter_frac > 0.0 and rng is not None:
            dx_jitter = rng.uniform(-jitter_frac * Lx, jitter_frac * Lx)
            dy_jitter = rng.uniform(-jitter_frac * Ly, jitter_frac * Ly)
            x = float(np.clip(x + dx_jitter, 0.0, Lx))
            y = float(np.clip(y + dy_jitter, 0.0, Ly))
        positions.append((x, y))

    return positions


# ---------------------------------------------------------------------------
# Ground-truth flux generators
# ---------------------------------------------------------------------------

TargetType = Literal["smooth", "localized", "multi_spot"]


def generate_flux_2d(
    target_type: TargetType,
    y_grid: np.ndarray,
    t_grid: np.ndarray,
    Ly: float = DEFAULT_LY,
    T_total: float = DEFAULT_T_TOTAL,
    q_max: float = DEFAULT_Q_MAX,
) -> np.ndarray:
    """Generate a 2D ground-truth boundary heat flux q(y, t).

    Parameters
    ----------
    target_type : "smooth", "localized", or "multi_spot"
    y_grid      : 1-D array of y-coordinates [m], shape (ny,)
    t_grid      : 1-D array of time points [s], shape (nt,)
    Ly, T_total : domain dimensions
    q_max       : peak amplitude [W/m^2]

    Returns
    -------
    q : ndarray of shape (len(y_grid), len(t_grid)) [W/m^2]
        q[j, n] = flux at y=y_grid[j], t=t_grid[n]
    """
    y = np.asarray(y_grid, dtype=float)   # (ny,)
    t = np.asarray(t_grid, dtype=float)   # (nt,)
    Y, T = np.meshgrid(y, t, indexing="ij")  # both (ny, nt)

    if target_type == "smooth":
        # Low-frequency sinusoidal: single half-period in y and t
        q = q_max * np.sin(np.pi * Y / Ly) * np.sin(np.pi * T / T_total)

    elif target_type == "localized":
        # Single Gaussian pulse centred at (y0, t0)
        y0 = 0.50 * Ly
        t0 = 0.50 * T_total
        sigma_y = 0.10 * Ly
        sigma_t = 0.10 * T_total
        exponent = (
            ((Y - y0) ** 2) / (2 * sigma_y ** 2)
            + ((T - t0) ** 2) / (2 * sigma_t ** 2)
        )
        q = q_max * np.exp(-exponent)

    elif target_type == "multi_spot":
        # Three Gaussian pulses at different (y, t) locations
        spots = [
            # (amplitude_fraction, y_frac, t_frac, sigma_y_frac, sigma_t_frac)
            (0.90, 0.25, 0.30, 0.08, 0.08),
            (1.00, 0.70, 0.60, 0.08, 0.08),
            (0.70, 0.50, 0.80, 0.08, 0.08),
        ]
        q = np.zeros_like(Y)
        for amp_frac, y_frac, t_frac, sy_frac, st_frac in spots:
            y0 = y_frac * Ly
            t0 = t_frac * T_total
            sigma_y = sy_frac * Ly
            sigma_t = st_frac * T_total
            exponent = (
                ((Y - y0) ** 2) / (2 * sigma_y ** 2)
                + ((T - t0) ** 2) / (2 * sigma_t ** 2)
            )
            q += amp_frac * q_max * np.exp(-exponent)

    else:
        raise ValueError(
            f"Unknown target_type {target_type!r}. "
            "Choose from: 'smooth', 'localized', 'multi_spot'."
        )

    return q  # shape (ny, nt)


# ---------------------------------------------------------------------------
# 2D heat conduction forward solver
# ---------------------------------------------------------------------------


class HeatConduction2DFD:
    """2D transient heat conduction solver using explicit finite differences.

    Grid
    ----
    Cell centres at x_i = (i + 0.5) * dx, y_j = (j + 0.5) * dy
    for i = 0…nx-1, j = 0…ny-1.

    The solution array u has shape (nx, ny).

    Boundary conditions use ghost nodes:
        Left  (x=0):  u_ghost[j] = u[0,j] + dx * q[j,n] / k  (Neumann with flux)
        Right (x=Lx): u_ghost[j] = u[-1,j]                    (insulated)
        Bottom(y=0):  u_ghost[i] = u[i,0]                     (insulated)
        Top   (y=Ly): u_ghost[i] = u[i,-1]                    (insulated)

    Parameters
    ----------
    Lx, Ly   : domain dimensions [m]
    nx, ny   : number of cells in x and y
    alpha    : thermal diffusivity [m^2/s]
    k        : thermal conductivity [W/(m·K)] — used only for BC application
    dt       : time step [s].  If None, computed automatically from the
               stability criterion with a safety factor of 0.9.
    """

    def __init__(
        self,
        Lx: float = DEFAULT_LX,
        Ly: float = DEFAULT_LY,
        nx: int = DEFAULT_NX,
        ny: int = DEFAULT_NY,
        alpha: float = DEFAULT_ALPHA,
        k: float = DEFAULT_K,
        dt: float | None = None,
    ) -> None:
        self.Lx = float(Lx)
        self.Ly = float(Ly)
        self.nx = int(nx)
        self.ny = int(ny)
        self.alpha = float(alpha)
        self.k = float(k)

        self.dx = Lx / nx
        self.dy = Ly / ny

        # Cell centre coordinates
        self.x_centers = np.linspace(self.dx / 2, Lx - self.dx / 2, nx)
        self.y_centers = np.linspace(self.dy / 2, Ly - self.dy / 2, ny)

        # Stability criterion: dt < 0.5 / (alpha * (1/dx² + 1/dy²))
        dt_max = 0.5 / (alpha * (1.0 / self.dx ** 2 + 1.0 / self.dy ** 2))
        if dt is None:
            self._dt = 0.9 * dt_max   # 10% safety margin
        else:
            if dt > dt_max:
                raise ValueError(
                    f"Provided dt={dt:.4g} exceeds stability limit "
                    f"dt_max={dt_max:.4g}.  Use dt <= {dt_max:.4g}."
                )
            self._dt = float(dt)

        # Courant numbers
        self._rx = alpha * self._dt / self.dx ** 2
        self._ry = alpha * self._dt / self.dy ** 2

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    @property
    def dt(self) -> float:
        return self._dt

    def simulate(
        self,
        q_flux_2d: np.ndarray,
        T0: float,
        sensor_positions: list[tuple[float, float]],
        t_end: float = DEFAULT_T_TOTAL,
        obs_every: int = 1,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Run the forward model for a given 2D heat-flux.

        Parameters
        ----------
        q_flux_2d       : shape (ny, nt_q) array [W/m^2].
                          Flux at left boundary, q[j, n] = q(y_j, t_n_q).
                          The time dimension will be linearly interpolated to
                          the internal dt time steps.
        T0              : uniform initial temperature [K]
        sensor_positions: list of (x, y) tuples [m]
        t_end           : simulation end time [s]
        obs_every       : record sensor readings every this many internal steps.
                          obs_every=1 records every step (default).

        Returns
        -------
        T_sensors : shape (n_sensors, n_obs) — temperature at each sensor.
        obs_times : shape (n_obs,) — times at which observations are recorded.
        """
        dt = self._dt
        n_steps = int(np.ceil(t_end / dt))
        sim_times = np.arange(n_steps + 1, dtype=float) * dt  # length n_steps+1

        nx, ny = self.nx, self.ny
        rx, ry = self._rx, self._ry

        # Interpolate q to internal time grid
        # q_flux_2d has shape (ny, nt_q); we interpolate in time to get (ny, n_steps+1)
        nt_q = q_flux_2d.shape[1]
        t_q = np.linspace(0.0, t_end, nt_q)
        q_fine = np.zeros((ny, n_steps + 1), dtype=float)
        for j in range(ny):
            q_fine[j, :] = np.interp(sim_times, t_q, q_flux_2d[j, :])

        # Map sensor positions to cell indices
        sensor_indices = self._sensor_to_indices(sensor_positions)
        n_sensors = len(sensor_indices)

        # Determine observation time indices
        obs_steps = list(range(0, n_steps + 1, obs_every))
        n_obs = len(obs_steps)
        T_sensors = np.zeros((n_sensors, n_obs), dtype=float)
        obs_times = sim_times[obs_steps]

        # Initialise temperature field
        u = np.full((nx, ny), T0, dtype=float)

        # Record initial condition
        obs_idx = 0
        if 0 in obs_steps:
            for k, (si, sj) in enumerate(sensor_indices):
                T_sensors[k, obs_idx] = u[si, sj]
            obs_idx += 1

        # Time-march
        for n in range(1, n_steps + 1):
            q_t = q_fine[:, n]   # shape (ny,) — left boundary flux at step n

            # Ghost nodes:
            #   left  (x=-dx/2): u_ghost[j] = u[0,j] + dx*q[j]/k
            #   right (x=Lx+dx/2): u_ghost[j] = u[-1,j]   (insulated)
            #   bottom (y=-dy/2): u_ghost[i] = u[i,0]      (insulated)
            #   top   (y=Ly+dy/2): u_ghost[i] = u[i,-1]    (insulated)

            # X-direction Laplacian with ghost nodes
            # u_ext_x shape (nx+2, ny)
            u_left_ghost = u[0, :] + self.dx * q_t / self.k   # (ny,)
            u_right_ghost = u[-1, :]                            # (ny,)
            u_ext_x = np.vstack([
                u_left_ghost[np.newaxis, :],   # row 0: left ghost
                u,                              # rows 1..nx
                u_right_ghost[np.newaxis, :],  # row nx+1: right ghost
            ])  # shape (nx+2, ny)
            laplx = (
                u_ext_x[:-2, :]         # u[i-1, j]
                - 2.0 * u_ext_x[1:-1, :]  # u[i, j]
                + u_ext_x[2:, :]        # u[i+1, j]
            ) / self.dx ** 2  # shape (nx, ny)

            # Y-direction Laplacian with ghost nodes
            u_bottom_ghost = u[:, 0]   # (nx,) — insulated
            u_top_ghost = u[:, -1]     # (nx,) — insulated
            u_ext_y = np.hstack([
                u_bottom_ghost[:, np.newaxis],  # col 0: bottom ghost
                u,                               # cols 1..ny
                u_top_ghost[:, np.newaxis],     # col ny+1: top ghost
            ])  # shape (nx, ny+2)
            laply = (
                u_ext_y[:, :-2]          # u[i, j-1]
                - 2.0 * u_ext_y[:, 1:-1]  # u[i, j]
                + u_ext_y[:, 2:]         # u[i, j+1]
            ) / self.dy ** 2  # shape (nx, ny)

            # Explicit Euler update
            u = u + dt * self.alpha * (laplx + laply)

            # Record observations
            if n in obs_steps:
                for k, (si, sj) in enumerate(sensor_indices):
                    T_sensors[k, obs_idx] = u[si, sj]
                obs_idx += 1

        return T_sensors, obs_times

    def build_sensitivity_matrix(
        self,
        sensor_positions: list[tuple[float, float]],
        t_end: float,
        ny_q: int,
        nt_q: int,
        obs_every: int = 1,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Compute the linear sensitivity matrix S for the 2D IHCP.

        The flux q(y, t) is parametrised on a coarse (ny_q × nt_q) grid.
        Bilinear interpolation maps coarse q to the full FD resolution.

        S maps the flattened coarse-q vector to flattened sensor observations
        (after subtracting the zero-flux baseline).

        Returns
        -------
        S          : (n_sensors * n_obs, ny_q * nt_q) sensitivity matrix
        obs_times  : (n_obs,) observation time array
        y_q_grid   : (ny_q,) y-coordinates of coarse flux grid
        t_q_grid   : (nt_q,) t-coordinates of coarse flux grid
        """
        n_params = ny_q * nt_q
        n_sensors = len(sensor_positions)

        # Coarse-flux grid
        y_q_grid = np.linspace(0.0, self.Ly, ny_q)
        t_q_grid = np.linspace(0.0, t_end, nt_q)

        # Run one zero-flux simulation to determine n_obs (and verify shape)
        q_zero_fine = np.zeros((self.ny, nt_q))
        T_base, obs_times = self.simulate(
            q_zero_fine, T0=0.0, sensor_positions=sensor_positions,
            t_end=t_end, obs_every=obs_every,
        )
        n_obs = len(obs_times)
        S = np.zeros((n_sensors * n_obs, n_params), dtype=float)

        # Unit-impulse superposition
        for k in range(n_params):
            q_unit_coarse = np.zeros(n_params, dtype=float)
            q_unit_coarse[k] = 1.0
            q_unit_fine = self._interpolate_q_coarse(
                q_unit_coarse.reshape(ny_q, nt_q),
                y_q_grid, t_q_grid, t_end,
            )
            T_sensors, _ = self.simulate(
                q_unit_fine, T0=0.0, sensor_positions=sensor_positions,
                t_end=t_end, obs_every=obs_every,
            )
            S[:, k] = T_sensors.flatten()

        return S, obs_times, y_q_grid, t_q_grid

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _sensor_to_indices(
        self, sensor_positions: list[tuple[float, float]]
    ) -> list[tuple[int, int]]:
        """Map (x, y) positions to nearest FD cell-centre indices."""
        indices = []
        for (xp, yp) in sensor_positions:
            i = int(np.argmin(np.abs(self.x_centers - xp)))
            j = int(np.argmin(np.abs(self.y_centers - yp)))
            indices.append((i, j))
        return indices

    def _interpolate_q_coarse(
        self,
        q_coarse: np.ndarray,
        y_q_grid: np.ndarray,
        t_q_grid: np.ndarray,
        t_end: float,
    ) -> np.ndarray:
        """Bilinear-interpolate q from coarse (ny_q, nt_q) to fine (ny, n_steps_q).

        Returns q_fine of shape (ny, nt_q) — same nt_q as input; the caller's
        simulate() method will then do time interpolation from t_q_grid to
        the internal simulation time steps.
        """
        # Build interpolator on the coarse grid
        interp = RegularGridInterpolator(
            (y_q_grid, t_q_grid),
            q_coarse,
            method="linear",
            bounds_error=False,
            fill_value=0.0,
        )

        # Evaluate on fine y-grid, same t_q_grid
        Y_fine, T_fine = np.meshgrid(self.y_centers, t_q_grid, indexing="ij")
        points = np.column_stack([Y_fine.ravel(), T_fine.ravel()])
        q_fine_vals = interp(points).reshape(self.ny, len(t_q_grid))
        return q_fine_vals  # shape (ny, nt_q)
