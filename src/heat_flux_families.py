"""
heat_flux_families.py
=====================
Heat-flux family taxonomy for the 2D inverse heat conduction benchmark.

Each family represents a class of boundary heat-flux signals q(y, t)
parameterised by:
  - a PRIMARY AXIS: the core difficulty dimension of this family
  - one or more SECONDARY AXES: subordinate modifiers

Families
--------
A. fourier_kl_smooth       — smooth, low-rank spatiotemporal signals
B. gaussian_localized      — single localised Gaussian hotspot
C. overlapping_multi_spot  — two spots with controllable overlap severity
D. moving_hotspot          — hotspot translating along the boundary
E. matern_grf              — random field with controlled roughness
F. discontinuous_piecewise — piecewise / front-like flux with jumps

Family metadata is stored in FAMILY_REGISTRY (see bottom of file).

Public API
----------
    generate_family_flux(
        family_name,
        y_grid, t_grid,
        primary_axis_level,    # int index into primary_axis_levels
        secondary_axis_values, # dict of secondary axis name → value (optional)
        Ly, T_total, q_max,
        seed,
    ) -> np.ndarray  of shape (len(y_grid), len(t_grid))

    FAMILY_REGISTRY : dict[family_name → FamilyDef]

    get_family(name) -> FamilyDef
    list_families() -> list[str]
    n_peaks_for_family(family_name, primary_axis_level) -> int
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class FamilyDef:
    """Metadata for a heat-flux family."""
    family_name:           str
    support_type:          str        # "global", "localised", "multi-peak", "moving", "stochastic", "piecewise"
    primary_axis_name:     str
    primary_axis_levels:   list[Any]  # ordered from easy to hard
    secondary_axis_names:  list[str]
    secondary_axis_levels: dict[str, list[Any]]   # name → list of representative values
    description:           str
    complexity_metadata:   dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Helper: Gaussian kernel
# ---------------------------------------------------------------------------

def _gaussian_2d(
    Y: np.ndarray,
    T: np.ndarray,
    y0: float,
    t0: float,
    sigma_y: float,
    sigma_t: float,
    amp: float,
) -> np.ndarray:
    exponent = (
        (Y - y0) ** 2 / (2 * sigma_y ** 2)
        + (T - t0) ** 2 / (2 * sigma_t ** 2)
    )
    return amp * np.exp(-exponent)


# ---------------------------------------------------------------------------
# Family A — fourier_kl_smooth
# ---------------------------------------------------------------------------

def _gen_fourier_kl_smooth(
    y: np.ndarray,
    t: np.ndarray,
    n_modes: int,          # primary axis: effective rank (few=easy, many=hard)
    temporal_anisotropy: float = 1.0,   # secondary: σ_t / σ_y scale ratio
    amplitude_contrast:  float = 1.0,   # secondary: spread of mode amplitudes
    phase_skew:          float = 0.0,   # secondary: shift in phase distribution
    q_max: float = 1000.0,
    seed: int = 0,
) -> np.ndarray:
    """Family A: smooth Fourier KL signal.

    primary axis  = n_modes (1..8)
    secondary axes = temporal_anisotropy, amplitude_contrast, phase_skew
    """
    Ly   = y[-1] if len(y) > 1 else 1.0
    T_t  = t[-1] if len(t) > 1 else 1.0
    Y, T = np.meshgrid(y, t, indexing="ij")

    rng = np.random.default_rng(seed)
    q   = np.zeros_like(Y)

    for m in range(1, n_modes + 1):
        # Amplitude decays with mode index; contrast controls how fast
        amp = q_max * (1.0 / m) ** amplitude_contrast
        # Phase: uniform + optional skew
        phi_y = rng.uniform(0, 2 * np.pi) + phase_skew * m
        phi_t = rng.uniform(0, 2 * np.pi)
        # Spatial frequency
        ky = m * np.pi / Ly
        kt = m * np.pi / T_t * temporal_anisotropy
        q += amp * np.sin(ky * Y + phi_y) * np.sin(kt * T + phi_t)

    # Normalise to q_max
    q_abs_max = np.max(np.abs(q))
    if q_abs_max > 1e-12:
        q = q * (q_max / q_abs_max)

    return q


# ---------------------------------------------------------------------------
# Family B — gaussian_localized
# ---------------------------------------------------------------------------

def _gen_gaussian_localized(
    y: np.ndarray,
    t: np.ndarray,
    sigma_y_frac: float,        # primary: localization width (as fraction of Ly)
    anisotropy_ratio: float = 1.0,    # secondary: sigma_t / sigma_y
    temporal_duration_frac: float = 0.2,  # secondary: absolute sigma_t fraction
    peak_amplitude: float = 1.0,      # secondary: amplitude scale
    q_max: float = 1000.0,
    seed: int = 0,
) -> np.ndarray:
    """Family B: single Gaussian hotspot.

    primary axis  = sigma_y_frac (small=sharp, large=broad)
    secondary axes = anisotropy_ratio, temporal_duration_frac, peak_amplitude
    """
    Ly  = y[-1] if len(y) > 1 else 1.0
    T_t = t[-1] if len(t) > 1 else 1.0
    Y, T = np.meshgrid(y, t, indexing="ij")

    y0     = 0.5 * Ly
    t0     = 0.5 * T_t
    sig_y  = sigma_y_frac * Ly
    sig_t  = temporal_duration_frac * T_t * anisotropy_ratio

    q = _gaussian_2d(Y, T, y0, t0, sig_y, sig_t, peak_amplitude * q_max)
    return q


# ---------------------------------------------------------------------------
# Family C — overlapping_multi_spot
# ---------------------------------------------------------------------------

def _gen_overlapping_multi_spot(
    y: np.ndarray,
    t: np.ndarray,
    separation_frac: float,      # primary: peak separation / Ly (large=easy, small=hard)
    amplitude_imbalance: float = 0.0,   # secondary: relative amplitude diff (0=equal)
    width_mismatch: float = 0.0,        # secondary: sigma1/sigma2 - 1 (0=same width)
    temporal_offset_frac: float = 0.0,  # secondary: t_offset / T_total
    base_sigma_frac: float = 0.10,      # fixed: base Gaussian width
    q_max: float = 1000.0,
    seed: int = 0,
) -> np.ndarray:
    """Family C: two overlapping Gaussian spots.

    primary axis  = separation_frac (large=well-separated, small=merged)
    secondary axes = amplitude_imbalance, width_mismatch, temporal_offset_frac
    """
    Ly  = y[-1] if len(y) > 1 else 1.0
    T_t = t[-1] if len(t) > 1 else 1.0
    Y, T = np.meshgrid(y, t, indexing="ij")

    # Two spot positions: symmetric around centre
    y0_1 = 0.5 * Ly - 0.5 * separation_frac * Ly
    y0_2 = 0.5 * Ly + 0.5 * separation_frac * Ly
    y0_1 = float(np.clip(y0_1, 0.05 * Ly, 0.95 * Ly))
    y0_2 = float(np.clip(y0_2, 0.05 * Ly, 0.95 * Ly))

    t0_1 = 0.5 * T_t - temporal_offset_frac * T_t
    t0_2 = 0.5 * T_t + temporal_offset_frac * T_t

    sig_y_base = base_sigma_frac * Ly
    sig_y_1    = sig_y_base
    sig_y_2    = sig_y_base * (1.0 + width_mismatch)
    sig_t      = 0.15 * T_t

    amp1 = q_max * (1.0 - 0.5 * amplitude_imbalance)
    amp2 = q_max * (1.0 + 0.5 * amplitude_imbalance)

    q  = _gaussian_2d(Y, T, y0_1, t0_1, sig_y_1, sig_t, amp1)
    q += _gaussian_2d(Y, T, y0_2, t0_2, sig_y_2, sig_t, amp2)
    return q


# ---------------------------------------------------------------------------
# Family D — moving_hotspot
# ---------------------------------------------------------------------------

def _gen_moving_hotspot(
    y: np.ndarray,
    t: np.ndarray,
    speed_frac: float,             # primary: normalised speed (0=still, 1=traverse in T_total)
    amplitude_modulation: float = 0.0,  # secondary: sine modulation of amplitude (0=none)
    width_modulation: float = 0.0,      # secondary: sine modulation of sigma_y (0=none)
    direction_reversal: bool = False,   # secondary: reversal at midpoint
    base_sigma_frac: float = 0.10,
    q_max: float = 1000.0,
    seed: int = 0,
) -> np.ndarray:
    """Family D: moving Gaussian hotspot.

    primary axis  = speed_frac (0=slow/stationary, 1=fast/transiting)
    secondary axes = amplitude_modulation, width_modulation, direction_reversal
    """
    Ly  = y[-1] if len(y) > 1 else 1.0
    T_t = t[-1] if len(t) > 1 else 1.0
    Y, T = np.meshgrid(y, t, indexing="ij")

    # Trajectory: y_center(t)
    # Start at y=0.15*Ly, end at y=0.15+speed_frac*Ly (clamped to [0,Ly])
    t_norm = T / T_t   # (ny, nt) normalised time

    if direction_reversal:
        # Goes forward first half, then backwards
        t_fwd = np.minimum(t_norm, 0.5) * 2.0
        t_bwd = np.maximum(t_norm - 0.5, 0.0) * 2.0
        y_center = (0.15 + speed_frac * 0.70 * t_fwd) * Ly
        y_center = y_center + (-speed_frac * 0.70 * t_bwd) * Ly
    else:
        y_start  = 0.15 * Ly
        y_range  = speed_frac * 0.70 * Ly
        y_center = y_start + y_range * t_norm

    y_center = np.clip(y_center, 0.0, Ly)

    # Amplitude modulation
    amp_t = q_max * (1.0 + amplitude_modulation * np.sin(2 * np.pi * t_norm))

    # Width modulation
    sig_y_t = base_sigma_frac * Ly * (1.0 + width_modulation * np.abs(np.sin(np.pi * t_norm)))

    # Gaussian centered at y_center(t)
    exponent = (Y - y_center) ** 2 / (2 * sig_y_t ** 2)
    q = amp_t * np.exp(-exponent)
    return q


# ---------------------------------------------------------------------------
# Family E — matern_grf (simulated via squared-exponential covariance)
# ---------------------------------------------------------------------------

def _gen_matern_grf(
    y: np.ndarray,
    t: np.ndarray,
    corr_length_frac: float,       # primary: correlation length / Ly
    anisotropy_ratio: float = 1.0, # secondary: corr_t / (corr_length_frac * T_total)
    orientation_deg: float = 0.0,  # secondary: rotation of correlation ellipse [degrees]
    nonstationarity: float = 0.0,  # secondary: linear variation of amplitude across y
    q_max: float = 1000.0,
    seed: int = 0,
) -> np.ndarray:
    """Family E: Random field with controlled roughness (Matérn-like via RBF).

    primary axis  = corr_length_frac (large=smooth, small=rough)
    secondary axes = anisotropy_ratio, orientation_deg, nonstationarity

    Uses squared-exponential (RBF) covariance with specified length scale.
    Samples are drawn from a multivariate normal with this covariance.
    For benchmark reproducibility, the seed is always honoured.
    """
    Ly  = y[-1] if len(y) > 1 else 1.0
    T_t = t[-1] if len(t) > 1 else 1.0

    ny = len(y)
    nt = len(t)

    corr_y = corr_length_frac * Ly
    corr_t = corr_length_frac * T_t * anisotropy_ratio

    # Build covariance matrix on the flattened (y, t) grid
    # C((y1,t1), (y2,t2)) = exp(-0.5 * [(Δy/ℓ_y)² + (Δt/ℓ_t)²])
    # We use a Kronecker-product factorisation for efficiency
    # Cy = (ny, ny), Ct = (nt, nt)
    Yg = y[:, None] - y[None, :]   # (ny, ny)
    Tg = t[:, None] - t[None, :]   # (nt, nt)

    # Optional rotation of the y-t correlation ellipse
    if abs(orientation_deg) > 0.1:
        theta = float(np.deg2rad(orientation_deg))
        # Rotate Δy, Δt by theta
        Y1, T1 = np.meshgrid(y, t, indexing="ij")  # (ny, nt)
        Y2, T2 = np.meshgrid(y, t, indexing="ij")
        dY = Y1.ravel()[:, None] - Y2.ravel()[None, :]  # (ny*nt, ny*nt)
        dT = T1.ravel()[:, None] - T2.ravel()[None, :]
        dY_rot =  dY * np.cos(theta) + dT * np.sin(theta)
        dT_rot = -dY * np.sin(theta) + dT * np.cos(theta)
        K = np.exp(
            -0.5 * (dY_rot / (corr_y + 1e-12)) ** 2
            -0.5 * (dT_rot / (corr_t + 1e-12)) ** 2
        )
        rng = np.random.default_rng(seed)
        K   += 1e-6 * np.eye(ny * nt)
        L    = np.linalg.cholesky(K)
        z    = rng.standard_normal(ny * nt)
        q_flat = L @ z
        q = q_flat.reshape(ny, nt)
    else:
        # Kronecker factorisation: much cheaper
        Cy = np.exp(-0.5 * (Yg / (corr_y + 1e-12)) ** 2) + 1e-6 * np.eye(ny)
        Ct = np.exp(-0.5 * (Tg / (corr_t + 1e-12)) ** 2) + 1e-6 * np.eye(nt)
        Ly_chol = np.linalg.cholesky(Cy)   # (ny, ny)
        Lt_chol = np.linalg.cholesky(Ct)   # (nt, nt)
        rng = np.random.default_rng(seed)
        Z   = rng.standard_normal((ny, nt))
        q   = Ly_chol @ Z @ Lt_chol.T     # (ny, nt)

    # Nonstationarity: amplitude varies linearly across y
    if abs(nonstationarity) > 1e-4:
        amp_y = 1.0 + nonstationarity * (y / Ly - 0.5)[:, None]  # (ny, 1)
        q *= amp_y

    # Normalise to q_max
    q_abs_max = np.max(np.abs(q))
    if q_abs_max > 1e-12:
        q = q * (q_max / q_abs_max)

    return q


# ---------------------------------------------------------------------------
# Family F — discontinuous_piecewise
# ---------------------------------------------------------------------------

def _gen_discontinuous_piecewise(
    y: np.ndarray,
    t: np.ndarray,
    jump_sharpness: float,         # primary: controls smoothing (large=sharp, small=soft)
    plateau_width_frac: float = 0.3,   # secondary: fractional width of hot zone
    n_jumps: int = 1,                  # secondary: number of jump fronts
    asymmetry: float = 0.0,            # secondary: offset of jump from centre
    q_max: float = 1000.0,
    seed: int = 0,
) -> np.ndarray:
    """Family F: piecewise/front-like flux with controllable jump sharpness.

    primary axis  = jump_sharpness (small=soft ramp, large=near-delta)
    secondary axes = plateau_width_frac, n_jumps, asymmetry
    """
    Ly  = y[-1] if len(y) > 1 else 1.0
    T_t = t[-1] if len(t) > 1 else 1.0
    Y, T = np.meshgrid(y, t, indexing="ij")  # (ny, nt)

    q = np.zeros_like(Y)

    for k in range(n_jumps):
        # Jump front location in y
        y_mid = (0.3 + k * (0.4 / max(n_jumps, 1)) + asymmetry * 0.1) * Ly
        y_mid = float(np.clip(y_mid, 0.05 * Ly, 0.95 * Ly))
        y_lo  = y_mid - 0.5 * plateau_width_frac * Ly
        y_hi  = y_mid + 0.5 * plateau_width_frac * Ly

        # Smoothed step: tanh with sharpness parameter
        # sigma_step = Ly / (2 * jump_sharpness) controls the transition width
        sigma_step = Ly / (2.0 * max(jump_sharpness, 0.1))

        # Spatial profile: smooth step up then down
        step_lo = 0.5 * (1.0 + np.tanh((Y - y_lo) / sigma_step))
        step_hi = 0.5 * (1.0 - np.tanh((Y - y_hi) / sigma_step))
        spatial = step_lo * step_hi   # (ny, nt) ≈ 1 in hot zone, 0 outside

        # Temporal profile: constant (or slowly varying)
        # Amplitude ramps up from 0 to 1 over first 20% of time
        t_ramp = np.clip(T / (0.2 * T_t), 0.0, 1.0)
        q += q_max * spatial * t_ramp * (1.0 / n_jumps)

    # Normalise to q_max
    q_abs_max = np.max(np.abs(q))
    if q_abs_max > 1e-12:
        q = q * (q_max / q_abs_max)

    return q


# ---------------------------------------------------------------------------
# Unified generator
# ---------------------------------------------------------------------------

def generate_family_flux(
    family_name: str,
    y_grid: np.ndarray,
    t_grid: np.ndarray,
    primary_axis_level: int,           # index into family.primary_axis_levels
    secondary_axis_values: dict[str, Any] | None = None,
    Ly: float = 0.1,
    T_total: float = 100.0,
    q_max: float = 1000.0,
    seed: int = 0,
) -> np.ndarray:
    """Generate q(y, t) for a named family and primary-axis level.

    Parameters
    ----------
    family_name          : one of the family names in FAMILY_REGISTRY
    y_grid, t_grid       : coordinate arrays (physical units [m], [s])
    primary_axis_level   : integer index (0 = easiest, len-1 = hardest)
    secondary_axis_values: dict mapping axis name to value (optional override)
    Ly, T_total, q_max   : domain and amplitude parameters
    seed                 : random seed for stochastic families

    Returns
    -------
    q : ndarray of shape (len(y_grid), len(t_grid))  [W/m^2]
    """
    if secondary_axis_values is None:
        secondary_axis_values = {}

    fam = get_family(family_name)
    # Get primary axis value
    levels = fam.primary_axis_levels
    idx    = max(0, min(primary_axis_level, len(levels) - 1))
    primary_val = levels[idx]

    # Get secondary axis default values
    sec_defaults: dict[str, Any] = {}
    for ax_name, ax_levels in fam.secondary_axis_levels.items():
        # Default = mid-point value
        mid = len(ax_levels) // 2
        sec_defaults[ax_name] = ax_levels[mid]
    sec_defaults.update(secondary_axis_values)   # caller overrides take priority

    kwargs: dict[str, Any] = dict(q_max=q_max, seed=seed)

    if family_name == "fourier_kl_smooth":
        kwargs["n_modes"]             = int(primary_val)
        kwargs["temporal_anisotropy"] = float(sec_defaults.get("temporal_anisotropy", 1.0))
        kwargs["amplitude_contrast"]  = float(sec_defaults.get("amplitude_contrast", 1.0))
        kwargs["phase_skew"]          = float(sec_defaults.get("phase_skew", 0.0))
        return _gen_fourier_kl_smooth(y_grid, t_grid, **kwargs)

    elif family_name == "gaussian_localized":
        kwargs["sigma_y_frac"]            = float(primary_val)
        kwargs["anisotropy_ratio"]        = float(sec_defaults.get("anisotropy_ratio", 1.0))
        kwargs["temporal_duration_frac"]  = float(sec_defaults.get("temporal_duration_frac", 0.2))
        kwargs["peak_amplitude"]          = float(sec_defaults.get("peak_amplitude", 1.0))
        return _gen_gaussian_localized(y_grid, t_grid, **kwargs)

    elif family_name == "overlapping_multi_spot":
        kwargs["separation_frac"]      = float(primary_val)
        kwargs["amplitude_imbalance"]  = float(sec_defaults.get("amplitude_imbalance", 0.0))
        kwargs["width_mismatch"]       = float(sec_defaults.get("width_mismatch", 0.0))
        kwargs["temporal_offset_frac"] = float(sec_defaults.get("temporal_offset_frac", 0.0))
        return _gen_overlapping_multi_spot(y_grid, t_grid, **kwargs)

    elif family_name == "moving_hotspot":
        kwargs["speed_frac"]            = float(primary_val)
        kwargs["amplitude_modulation"]  = float(sec_defaults.get("amplitude_modulation", 0.0))
        kwargs["width_modulation"]      = float(sec_defaults.get("width_modulation", 0.0))
        kwargs["direction_reversal"]    = bool(sec_defaults.get("direction_reversal", False))
        return _gen_moving_hotspot(y_grid, t_grid, **kwargs)

    elif family_name == "matern_grf":
        kwargs["corr_length_frac"]  = float(primary_val)
        kwargs["anisotropy_ratio"]  = float(sec_defaults.get("anisotropy_ratio", 1.0))
        kwargs["orientation_deg"]   = float(sec_defaults.get("orientation_deg", 0.0))
        kwargs["nonstationarity"]   = float(sec_defaults.get("nonstationarity", 0.0))
        return _gen_matern_grf(y_grid, t_grid, **kwargs)

    elif family_name == "discontinuous_piecewise":
        kwargs["jump_sharpness"]    = float(primary_val)
        kwargs["plateau_width_frac"]= float(sec_defaults.get("plateau_width_frac", 0.3))
        kwargs["n_jumps"]           = int(sec_defaults.get("n_jumps", 1))
        kwargs["asymmetry"]         = float(sec_defaults.get("asymmetry", 0.0))
        return _gen_discontinuous_piecewise(y_grid, t_grid, **kwargs)

    else:
        raise ValueError(
            f"Unknown family {family_name!r}. "
            f"Available: {list_families()}"
        )


# ---------------------------------------------------------------------------
# Family registry
# ---------------------------------------------------------------------------

FAMILY_REGISTRY: dict[str, FamilyDef] = {

    "fourier_kl_smooth": FamilyDef(
        family_name="fourier_kl_smooth",
        support_type="global",
        primary_axis_name="n_modes",
        primary_axis_levels=[2, 4, 8],   # easy=few, hard=many
        secondary_axis_names=["temporal_anisotropy", "amplitude_contrast", "phase_skew"],
        secondary_axis_levels={
            "temporal_anisotropy": [0.5, 1.0, 2.0],
            "amplitude_contrast":  [0.5, 1.0, 2.0],
            "phase_skew":          [0.0, 0.5, 1.5],
        },
        description=(
            "Smooth low-rank Fourier series signal. "
            "Primary axis = effective mode count (rank richness). "
            "Higher mode count = harder reconstruction."
        ),
        complexity_metadata={"ill_posed_regime": "low", "peak_applicable": False},
    ),

    "gaussian_localized": FamilyDef(
        family_name="gaussian_localized",
        support_type="localised",
        primary_axis_name="sigma_y_frac",
        primary_axis_levels=[0.05, 0.15, 0.30],   # sharp, medium, broad
        secondary_axis_names=["anisotropy_ratio", "temporal_duration_frac", "peak_amplitude"],
        secondary_axis_levels={
            "anisotropy_ratio":       [0.5, 1.0, 2.0],
            "temporal_duration_frac": [0.10, 0.20, 0.35],
            "peak_amplitude":         [0.5, 1.0, 2.0],
        },
        description=(
            "Single localised Gaussian hotspot. "
            "Primary axis = spatial width (sharp to broad). "
            "Sharper = harder (more ill-posed)."
        ),
        complexity_metadata={"ill_posed_regime": "high_for_sharp", "peak_applicable": True},
    ),

    "overlapping_multi_spot": FamilyDef(
        family_name="overlapping_multi_spot",
        support_type="multi-peak",
        primary_axis_name="separation_frac",
        primary_axis_levels=[0.45, 0.20, 0.07],   # well-sep, marginal, merged
        secondary_axis_names=["amplitude_imbalance", "width_mismatch", "temporal_offset_frac"],
        secondary_axis_levels={
            "amplitude_imbalance":   [0.0, 0.3, 0.8],
            "width_mismatch":        [0.0, 0.3, 0.8],
            "temporal_offset_frac":  [0.0, 0.1, 0.3],
        },
        description=(
            "Two overlapping Gaussian spots. "
            "Primary axis = peak separation (large=well-separated, small=merged). "
            "Small separation = hardest (spots unresolvable)."
        ),
        complexity_metadata={"ill_posed_regime": "high_for_overlap", "peak_applicable": True},
    ),

    "moving_hotspot": FamilyDef(
        family_name="moving_hotspot",
        support_type="moving",
        primary_axis_name="speed_frac",
        primary_axis_levels=[0.2, 0.5, 1.0],   # slow, medium, fast
        secondary_axis_names=["amplitude_modulation", "width_modulation", "direction_reversal"],
        secondary_axis_levels={
            "amplitude_modulation": [0.0, 0.3, 0.7],
            "width_modulation":     [0.0, 0.3, 0.7],
            "direction_reversal":   [False, True],
        },
        description=(
            "Gaussian hotspot translating along the boundary. "
            "Primary axis = normalised speed (0=stationary, 1=full traverse). "
            "High speed = harder (smearing effect in time)."
        ),
        complexity_metadata={"ill_posed_regime": "medium", "peak_applicable": True},
    ),

    "matern_grf": FamilyDef(
        family_name="matern_grf",
        support_type="stochastic",
        primary_axis_name="corr_length_frac",
        primary_axis_levels=[0.30, 0.12, 0.04],   # smooth, medium, rough
        secondary_axis_names=["anisotropy_ratio", "orientation_deg", "nonstationarity"],
        secondary_axis_levels={
            "anisotropy_ratio":  [0.5, 1.0, 2.0],
            "orientation_deg":   [0.0, 30.0, 60.0],
            "nonstationarity":   [0.0, 0.5, 1.0],
        },
        description=(
            "Random field with squared-exponential (Matérn-like) covariance. "
            "Primary axis = correlation length (large=smooth, small=rough). "
            "Short correlation = hardest."
        ),
        complexity_metadata={"ill_posed_regime": "high_for_rough", "peak_applicable": False},
    ),

    "discontinuous_piecewise": FamilyDef(
        family_name="discontinuous_piecewise",
        support_type="piecewise",
        primary_axis_name="jump_sharpness",
        primary_axis_levels=[2.0, 8.0, 30.0],   # soft, sharp, near-step
        secondary_axis_names=["plateau_width_frac", "n_jumps", "asymmetry"],
        secondary_axis_levels={
            "plateau_width_frac": [0.15, 0.30, 0.50],
            "n_jumps":            [1, 2, 3],
            "asymmetry":          [0.0, 0.2, 0.5],
        },
        description=(
            "Piecewise flux with smooth-to-sharp jumps. "
            "Primary axis = jump_sharpness (small=ramp, large=step). "
            "Sharp jump = hardest (Gibbs/oscillation in smooth-basis solvers)."
        ),
        complexity_metadata={"ill_posed_regime": "high_for_sharp", "peak_applicable": True},
    ),
}


# ---------------------------------------------------------------------------
# Convenience accessors
# ---------------------------------------------------------------------------

def get_family(name: str) -> FamilyDef:
    """Return the FamilyDef for *name*, raising ValueError if not found."""
    if name not in FAMILY_REGISTRY:
        raise ValueError(
            f"Unknown heat-flux family {name!r}. "
            f"Available: {list_families()}"
        )
    return FAMILY_REGISTRY[name]


def list_families() -> list[str]:
    """Return sorted list of registered family names."""
    return sorted(FAMILY_REGISTRY.keys())


def n_peaks_for_family(family_name: str, primary_axis_level: int = 0) -> int:
    """Return expected number of peaks for a family at a given primary-axis level."""
    if family_name == "overlapping_multi_spot":
        return 2
    if family_name in ("gaussian_localized", "moving_hotspot", "discontinuous_piecewise"):
        return 1
    return 1   # default: treat as 1 or NA (caller handles np.nan)
