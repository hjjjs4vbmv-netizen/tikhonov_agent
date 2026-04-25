"""
qwen_pde_filler.py
==================
Real local-Qwen-backed implementation of the LLMPDESchemaFiller protocol.

This module provides ``LocalQwenPDESchemaFiller``, which loads a local
Qwen2.5-3B-Instruct model (or any compatible Qwen checkpoint) using
Hugging Face Transformers and uses it to normalise messy / semi-structured
PDE problem descriptions into the repository's PDESchema format.

Architecture position
---------------------
::

  messy text
    └─ LocalQwenPDESchemaFiller.fill_schema(text)
         │  (direct Transformers inference, no external server)
         ↓
       candidate dict  (JSON parsed from LLM output)
         ↓
       StructuredInputParser   (alias resolution, type coercion)
         ↓
       PDESchemaValidator      (deterministic semantic checks)
         ↓
       PDESchemaMapper → ProblemSpec

The LLM NEVER bypasses the deterministic validator.

Model path configuration
------------------------
Priority (highest to lowest):

1. Explicit ``model_path`` argument to ``LocalQwenPDESchemaFiller(...)``
2. Environment variable ``QWEN_MODEL_PATH``
3. Compiled-in default: ``/root/models/Qwen/Qwen2___5-3B-Instruct``

The default matches the container layout used in development.
Override for any other path::

    export QWEN_MODEL_PATH=/path/to/your/Qwen2.5-3B-Instruct
    # or
    filler = LocalQwenPDESchemaFiller(model_path="/path/to/model")

Usage
-----
::

    from src.qwen_pde_filler import LocalQwenPDESchemaFiller
    from src.pde_normalizer import normalize_with_llm

    filler = LocalQwenPDESchemaFiller()          # loads model on first call
    schema, vr = normalize_with_llm(messy_text, filler, strict=False)
    # or use the convenience wrapper:
    from src.pde_normalizer import normalize_with_local_qwen
    schema, vr = normalize_with_local_qwen(messy_text)

Prompt design
-------------
The model is instructed to:
- output ONLY valid JSON (no markdown, no prose)
- follow the exact PDESchema field names
- use SI units
- map common aliases (rho→density, cp→specific_heat, k/kappa→conductivity, …)
- set missing fields to null, never invent values
- record its own confidence and any extraction warnings

A single few-shot example is included in the system message so the 3B model
sees exactly what output format is expected.
"""

from __future__ import annotations

import json
import os
import re
import time
from typing import Any

from src.logging_utils import get_logger

log = get_logger("qwen_pde_filler")

# ---------------------------------------------------------------------------
# Default model path
# ---------------------------------------------------------------------------

_DEFAULT_MODEL_PATH = "/root/models/Qwen/Qwen2___5-3B-Instruct"


def _resolve_model_path(explicit: str | None = None) -> str:
    """Return the model path to use, in priority order."""
    if explicit:
        return explicit
    env = os.environ.get("QWEN_MODEL_PATH", "").strip()
    if env:
        return env
    return _DEFAULT_MODEL_PATH


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """You are a PDE problem normalizer for an inverse heat conduction solver.

YOUR ONLY TASK: extract numerical parameters from the user's text and output them
as a single valid JSON object. Nothing else.

STRICT RULES:
1. Output ONLY the JSON object — no markdown, no code fences, no explanations.
2. If a value is not mentioned or is ambiguous, use null. NEVER invent values.
3. Use SI units: length in metres, density in kg/m³, specific_heat in J/(kg·K),
   conductivity in W/(m·K), temperature in K, time in seconds.
4. Convert common aliases:
   rho / ρ / mass_density → density
   cp / c_p / heat_capacity / specific heat → specific_heat
   k / kappa / λ / thermal_conductivity → conductivity
   T0 / T_0 / T_initial / initial temperature → initial_condition
   T_end / t_end / t_final / final_time / end_time → time_end
   n_steps / num_steps / nt / number_of_steps → time_n_steps
   L / rod_length / domain_length → geometry_length
5. left_is_inversion_target should be true when the left boundary heat flux
   is the unknown to be recovered (inverse problem target).
6. Set _confidence between 0.0 (completely uncertain) and 1.0 (certain).
   Reduce it when units are ambiguous, values seem physically unreasonable,
   or important fields are missing.
7. List any extraction issues in _llm_warnings (empty list if none).

OUTPUT SCHEMA (always output ALL keys, use null for missing values):
{
  "geometry": {
    "length": <float|null>,
    "n_cells": <int|null>
  },
  "material": {
    "density": <float|null>,
    "specific_heat": <float|null>,
    "conductivity": <float|null>
  },
  "initial_condition": <float|null>,
  "boundary_conditions": {
    "right_type": "dirichlet"|"neumann"|"unknown",
    "right_value": <float|null>,
    "left_is_inversion_target": <bool>
  },
  "time": {
    "start": 0.0,
    "end": <float|null>,
    "n_steps": <int|null>
  },
  "sensor_positions": [<float>, ...],
  "observation": {
    "noise_std": <float|null>,
    "observations_file": <string|null>
  },
  "_confidence": <float>,
  "_llm_warnings": [<string>, ...]
}

EXAMPLE:
Input: "Steel rod, L=0.05 m, rho=7800, cp=500, k=50 W/mK. Right end fixed at 300 K. Left flux unknown. Sensors at 0.01 m and 0.03 m. T_end=60 s, n_steps=121. noise=0.3 K. Data in obs.csv."
Output:
{
  "geometry": {"length": 0.05, "n_cells": null},
  "material": {"density": 7800.0, "specific_heat": 500.0, "conductivity": 50.0},
  "initial_condition": null,
  "boundary_conditions": {"right_type": "dirichlet", "right_value": 300.0, "left_is_inversion_target": true},
  "time": {"start": 0.0, "end": 60.0, "n_steps": 121},
  "sensor_positions": [0.01, 0.03],
  "observation": {"noise_std": 0.3, "observations_file": "obs.csv"},
  "_confidence": 0.97,
  "_llm_warnings": []
}"""


def _build_user_message(text: str) -> str:
    return f"Extract PDE parameters from the following text:\n\n{text.strip()}"


# ---------------------------------------------------------------------------
# JSON extraction helpers
# ---------------------------------------------------------------------------

def _extract_json(raw: str) -> dict[str, Any] | None:
    """Robustly extract a JSON object from the model's raw output.

    Tries three strategies in order:
    1. Direct json.loads on the stripped output.
    2. Extract the first {...} block (handles preamble/suffix).
    3. Extract from a markdown code fence if present.
    """
    text = raw.strip()

    # Strategy 1: direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Strategy 2: first {...} block
    start = text.find("{")
    end = text.rfind("}") + 1
    if start >= 0 and end > start:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass

    # Strategy 3: markdown code fence
    fence_m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence_m:
        try:
            return json.loads(fence_m.group(1))
        except json.JSONDecodeError:
            pass

    return None


def _candidate_from_json(parsed: dict[str, Any]) -> dict[str, Any]:
    """Translate the model's flat output schema to the StructuredInputParser format.

    The LLM output uses a slightly different nesting than what
    StructuredInputParser expects.  This function normalises that.
    """
    out: dict[str, Any] = {}

    # Geometry
    geo = parsed.get("geometry", {}) or {}
    if geo:
        out["geometry"] = {}
        if geo.get("length") is not None:
            out["geometry"]["length"] = float(geo["length"])
        if geo.get("n_cells") is not None:
            out["geometry"]["n_cells"] = int(geo["n_cells"])

    # Material
    mat = parsed.get("material", {}) or {}
    if mat:
        out["material"] = {}
        if mat.get("density") is not None:
            out["material"]["density"] = float(mat["density"])
        if mat.get("specific_heat") is not None:
            out["material"]["specific_heat"] = float(mat["specific_heat"])
        if mat.get("conductivity") is not None:
            out["material"]["conductivity"] = float(mat["conductivity"])

    # Initial condition
    ic = parsed.get("initial_condition")
    if ic is not None:
        out["initial_condition"] = float(ic)

    # Boundary conditions
    bc_raw = parsed.get("boundary_conditions", {}) or {}
    if bc_raw:
        bc_out: dict[str, Any] = {}
        rtype = bc_raw.get("right_type", "dirichlet")
        rval = bc_raw.get("right_value")
        bc_out["right_type"] = rtype
        if rval is not None:
            bc_out["right_value"] = float(rval)
        out["boundary_conditions"] = bc_out
        # Signal inversion target
        if bc_raw.get("left_is_inversion_target", False):
            out["_left_bc_is_target"] = True

    # Time
    t_raw = parsed.get("time", {}) or {}
    if t_raw:
        out["time"] = {}
        start = t_raw.get("start", 0.0)
        if start is not None:
            out["time"]["start"] = float(start)
        if t_raw.get("end") is not None:
            out["time"]["end"] = float(t_raw["end"])
        if t_raw.get("n_steps") is not None:
            out["time"]["n_steps"] = int(t_raw["n_steps"])

    # Sensor positions
    sensors = parsed.get("sensor_positions", []) or []
    if sensors:
        out["sensor_positions"] = [float(s) for s in sensors]

    # Observation
    obs_raw = parsed.get("observation", {}) or {}
    if obs_raw:
        out["observation"] = {}
        if obs_raw.get("noise_std") is not None:
            out["observation"]["noise_std"] = float(obs_raw["noise_std"])
        if obs_raw.get("observations_file"):
            out["observation"]["observations_file"] = str(obs_raw["observations_file"])

    # Pass through metadata keys
    out["_confidence"] = float(parsed.get("_confidence", 1.0))
    out["_llm_warnings"] = list(parsed.get("_llm_warnings", []))

    return out


# ---------------------------------------------------------------------------
# LocalQwenPDESchemaFiller
# ---------------------------------------------------------------------------


class LocalQwenPDESchemaFiller:
    """Real local-Qwen-backed implementation of the LLMPDESchemaFiller protocol.

    Loads a Qwen2.5-3B-Instruct (or compatible) model using Hugging Face
    Transformers and runs local inference to extract PDE parameters from
    messy input text.

    Parameters
    ----------
    model_path
        Path to the local model directory.  If None, resolved via
        ``QWEN_MODEL_PATH`` env var or the compiled-in default.
    device
        PyTorch device string (``"cuda"``, ``"cpu"``, ``"auto"``).
        Defaults to ``"cuda"`` when CUDA is available, else ``"cpu"``.
    max_new_tokens
        Maximum tokens to generate.  512 is plenty for a JSON schema.
    temperature
        Sampling temperature.  Use 0 for greedy decoding (most reliable
        for structured output).
    dtype
        Model dtype.  Defaults to ``torch.bfloat16`` when available.
    """

    def __init__(
        self,
        model_path: str | None = None,
        device: str | None = None,
        max_new_tokens: int = 512,
        temperature: float = 0.0,
        dtype: str = "bfloat16",
    ) -> None:
        self.model_path = _resolve_model_path(model_path)
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.dtype_str = dtype
        self._model = None
        self._tokenizer = None
        self._loaded_device: str | None = None

        # Resolve device
        if device is not None:
            self._target_device = device
        else:
            try:
                import torch
                self._target_device = "cuda" if torch.cuda.is_available() else "cpu"
            except ImportError:
                self._target_device = "cpu"

        log.info(
            "LocalQwenPDESchemaFiller created: path=%s device=%s",
            self.model_path, self._target_device,
        )

    # ------------------------------------------------------------------
    # Model loading
    # ------------------------------------------------------------------

    def _ensure_loaded(self) -> None:
        """Lazy-load the model and tokenizer on first use."""
        if self._model is not None:
            return

        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        dtype_map = {
            "bfloat16": torch.bfloat16,
            "float16": torch.float16,
            "float32": torch.float32,
            "auto": "auto",
        }
        torch_dtype = dtype_map.get(self.dtype_str, torch.bfloat16)

        log.info(
            "Loading Qwen model from %s (device=%s, dtype=%s) …",
            self.model_path, self._target_device, self.dtype_str,
        )
        t0 = time.time()

        self._tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            trust_remote_code=True,
        )
        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            torch_dtype=torch_dtype,
            device_map="auto" if self._target_device in ("cuda", "auto") else None,
            trust_remote_code=True,
        )
        if self._target_device == "cpu":
            self._model = self._model.to("cpu")
        self._model.eval()

        actual_device = str(next(self._model.parameters()).device)
        self._loaded_device = actual_device
        elapsed = time.time() - t0
        log.info(
            "Qwen model loaded in %.1f s  device=%s  path=%s",
            elapsed, actual_device, self.model_path,
        )

    # ------------------------------------------------------------------
    # Inference
    # ------------------------------------------------------------------

    def _generate(self, user_text: str) -> tuple[str, dict[str, Any]]:
        """Run inference and return (raw_output, inference_metadata)."""
        self._ensure_loaded()

        import torch

        messages = [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user",   "content": _build_user_message(user_text)},
        ]

        text_input = self._tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = self._tokenizer([text_input], return_tensors="pt").to(
            next(self._model.parameters()).device
        )
        prompt_len = inputs["input_ids"].shape[1]

        t0 = time.time()
        with torch.no_grad():
            if self.temperature == 0.0:
                output_ids = self._model.generate(
                    **inputs,
                    max_new_tokens=self.max_new_tokens,
                    do_sample=False,
                    pad_token_id=self._tokenizer.eos_token_id,
                )
            else:
                output_ids = self._model.generate(
                    **inputs,
                    max_new_tokens=self.max_new_tokens,
                    temperature=self.temperature,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self._tokenizer.eos_token_id,
                )
        elapsed = time.time() - t0

        new_ids = output_ids[0][prompt_len:]
        raw_output = self._tokenizer.decode(new_ids, skip_special_tokens=True)
        completion_tokens = len(new_ids)

        meta = {
            "backend": "local_qwen_transformers",
            "model_path": self.model_path,
            "device": self._loaded_device,
            "prompt_tokens": prompt_len,
            "completion_tokens": completion_tokens,
            "inference_time_s": round(elapsed, 2),
        }
        log.info(
            "Qwen inference: %d prompt + %d completion tokens in %.2f s",
            prompt_len, completion_tokens, elapsed,
        )
        return raw_output, meta

    # ------------------------------------------------------------------
    # LLMPDESchemaFiller protocol
    # ------------------------------------------------------------------

    def fill_schema(self, text: str) -> dict[str, Any]:
        """Extract PDE parameters from *text* using local Qwen inference.

        Returns a candidate dict in StructuredInputParser format, plus the
        following metadata keys consumed by ``normalize_with_llm()``:

        ``_confidence``        float 0–1 from the model's self-assessment
        ``_llm_warnings``      list of strings (model-reported issues)
        ``_left_bc_is_target`` bool (True when left BC is inversion target)
        ``_inference_meta``    dict with backend/device/timing info

        On any inference or parse error, returns a minimal dict with
        ``_confidence=0.0`` and the error message in ``_llm_warnings``.
        """
        log.info("fill_schema: %d chars of input", len(text))

        raw_output = ""
        inference_meta: dict[str, Any] = {}

        try:
            raw_output, inference_meta = self._generate(text)
            log.debug("Raw LLM output:\n%s", raw_output)
        except Exception as exc:
            msg = f"Qwen inference failed: {exc}"
            log.error(msg)
            return {
                "_confidence": 0.0,
                "_llm_warnings": [msg],
                "_inference_meta": {"error": msg},
            }

        # Parse JSON from model output
        parsed = _extract_json(raw_output)
        if parsed is None:
            msg = f"LLM output is not valid JSON. Raw output (first 300 chars): {raw_output[:300]!r}"
            log.warning(msg)
            return {
                "_confidence": 0.0,
                "_llm_warnings": [msg],
                "_raw_output": raw_output[:500],
                "_inference_meta": inference_meta,
            }

        # Translate to StructuredInputParser format
        candidate = _candidate_from_json(parsed)
        candidate["_raw_output"] = raw_output[:500]   # keep for traceability
        candidate["_inference_meta"] = inference_meta

        log.info(
            "fill_schema: JSON parsed OK, confidence=%.2f, warnings=%s",
            candidate.get("_confidence", 1.0),
            candidate.get("_llm_warnings", []),
        )
        return candidate

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    @property
    def is_loaded(self) -> bool:
        """True if the model has been loaded into memory."""
        return self._model is not None

    def unload(self) -> None:
        """Release model from memory (useful in tests to free GPU RAM)."""
        import gc
        self._model = None
        self._tokenizer = None
        self._loaded_device = None
        gc.collect()
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except ImportError:
            pass
        log.info("LocalQwenPDESchemaFiller: model unloaded")
