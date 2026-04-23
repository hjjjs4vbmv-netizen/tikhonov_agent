"""
logging_utils.py
================
Structured logging configuration for the IHCP agent.

Uses Python's stdlib logging with a consistent format so that every
decision and solver call is traceable without an external dependency.
"""

from __future__ import annotations

import logging
import sys
from typing import Any


_FMT = "%(asctime)s [%(levelname)-8s] %(name)s — %(message)s"
_DATE_FMT = "%H:%M:%S"


def get_logger(name: str) -> logging.Logger:
    """Return a named logger with the project-standard format.

    Calling this multiple times with the same name is safe; the handler
    is added only once.
    """
    logger = logging.getLogger(f"ihcp.{name}")
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(_FMT, datefmt=_DATE_FMT))
        logger.addHandler(handler)
        logger.propagate = False
    return logger


def set_level(level: int | str = logging.INFO) -> None:
    """Set the log level for all ihcp.* loggers."""
    root = logging.getLogger("ihcp")
    root.setLevel(level)
    for child in root.manager.loggerDict.values():  # type: ignore[attr-defined]
        if isinstance(child, logging.Logger):
            child.setLevel(level)


def log_decision(logger: logging.Logger, tag: str, details: dict[str, Any]) -> None:
    """Log a structured scientific decision for traceability.

    Args:
        logger: The module logger.
        tag: Short identifier (e.g. "PLANNER", "VERIFIER", "REPLANNER").
        details: Key-value pairs to include in the log message.
    """
    parts = ", ".join(f"{k}={v!r}" for k, v in details.items())
    logger.info("[%s] %s", tag, parts)
