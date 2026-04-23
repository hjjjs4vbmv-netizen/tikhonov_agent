"""
utils.py
========
General-purpose utilities used across the IHCP agent.

Keep this module free of domain-specific logic; domain helpers belong in
the module that owns them.
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict, fields, is_dataclass
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Serialisation helpers
# ---------------------------------------------------------------------------


def dataclass_to_dict(obj: Any) -> Any:
    """Recursively convert a dataclass (nested or not) to a plain dict.

    Handles lists, tuples, and primitive types so the result is
    JSON-serialisable (assuming no numpy arrays are stored at root level).
    Numpy arrays should be converted to lists before reaching here.
    """
    if is_dataclass(obj) and not isinstance(obj, type):
        return {f.name: dataclass_to_dict(getattr(obj, f.name)) for f in fields(obj)}
    if isinstance(obj, (list, tuple)):
        return [dataclass_to_dict(v) for v in obj]
    if isinstance(obj, dict):
        return {k: dataclass_to_dict(v) for k, v in obj.items()}
    # numpy scalar / array guard (avoid hard dependency on numpy here)
    t = type(obj).__module__
    if t == "numpy":
        return obj.tolist() if hasattr(obj, "tolist") else float(obj)
    return obj


def write_json(path: Path, data: Any, indent: int = 2) -> None:
    """Write *data* to *path* as JSON, creating parent dirs as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=indent, default=str)


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# Timing
# ---------------------------------------------------------------------------


class Timer:
    """Simple wall-clock timer context manager."""

    def __init__(self) -> None:
        self._start: float = 0.0
        self.elapsed: float = 0.0

    def __enter__(self) -> "Timer":
        self._start = time.perf_counter()
        return self

    def __exit__(self, *_: Any) -> None:
        self.elapsed = time.perf_counter() - self._start


# ---------------------------------------------------------------------------
# Array helpers (light wrappers to keep numpy isolated in one place)
# ---------------------------------------------------------------------------


def linspace(start: float, stop: float, n: int) -> list[float]:
    """Pure-Python linspace – used when numpy is not yet imported."""
    if n == 1:
        return [start]
    step = (stop - start) / (n - 1)
    return [start + i * step for i in range(n)]


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))
