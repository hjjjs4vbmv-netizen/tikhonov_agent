"""
llm_hooks.py
============
Optional LLM integration layer – Protocol-style interfaces + a sample
placeholder adapter for Qwen-2.5-3B.

Architecture
------------
The scientific core of the agent does NOT depend on this module.
All LLM hooks are:
  - Optional (the system runs fully without them)
  - Defensive (malformed LLM output is discarded; fallback is always safe)
  - Clearly separated from the rule-based decision logic

LLM adapters must satisfy the protocol interfaces defined here.
They should NOT make final scientific decisions (lambda selection,
regularisation order, acceptance/rejection).

Protocol interfaces
-------------------
  ProblemParserLLM   – parses free-form text into structured schema dict
  ResultExplainerLLM – explains verification results in natural language
  ReportWriterLLM    – drafts markdown narrative sections
  LLMHooks           – composite container for all three

Qwen placeholder
----------------
The ``QwenLocalAdapter`` class is a skeleton.  The inference code is
deliberately left as a placeholder with a clear comment.  To activate:
  1. Install: pip install transformers torch
  2. Fill in the model loading and inference calls.
  3. Pass an instance to ``IHCPAgent(llm_hooks=QwenLocalHooks(...))``
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from src.logging_utils import get_logger

log = get_logger("llm_hooks")


# ---------------------------------------------------------------------------
# Protocol interfaces
# ---------------------------------------------------------------------------


@runtime_checkable
class ProblemParserLLM(Protocol):
    """Parse a free-form problem description into a partial schema dict.

    The returned dict is merged into the YAML-parsed config before
    ProblemSpec construction.  Missing or malformed fields are silently
    ignored.
    """

    def parse_problem_description(self, description: str) -> dict[str, Any]:
        ...


@runtime_checkable
class ResultExplainerLLM(Protocol):
    """Generate a natural-language explanation of a verification result."""

    def explain_verification(
        self,
        decision: str,
        reasons: list[str],
        metrics: dict[str, Any],
    ) -> str:
        ...


@runtime_checkable
class ReportWriterLLM(Protocol):
    """Draft the narrative section of the markdown report."""

    def write_report_narrative(self, summary: Any, problem: Any) -> str:
        ...


class LLMHooks:
    """Composite container for optional LLM adapters.

    Pass an instance of this to IHCPAgent.  Any adapter left as None
    is silently skipped.
    """

    def __init__(
        self,
        parser: ProblemParserLLM | None = None,
        explainer: ResultExplainerLLM | None = None,
        writer: ReportWriterLLM | None = None,
    ) -> None:
        self.parser = parser
        self.explainer = explainer
        self.writer = writer


# ---------------------------------------------------------------------------
# Qwen-2.5-3B placeholder adapter
# ---------------------------------------------------------------------------


class QwenLocalAdapter:
    """Placeholder adapter for a locally running Qwen-2.5-3B model.

    IMPORTANT: The inference code below is a PLACEHOLDER.
    It does not perform any actual inference.  Fill in the model
    loading and generation calls before use.

    To use:
        adapter = QwenLocalAdapter(model_path="/path/to/Qwen2.5-3B")
        hooks = LLMHooks(parser=adapter, explainer=adapter, writer=adapter)
        agent = IHCPAgent(llm_hooks=hooks)
    """

    def __init__(
        self,
        model_path: str = "Qwen/Qwen2.5-3B-Instruct",
        device: str = "cpu",
        max_new_tokens: int = 512,
    ) -> None:
        self.model_path = model_path
        self.device = device
        self.max_new_tokens = max_new_tokens
        self._model = None
        self._tokenizer = None

    def _ensure_loaded(self) -> None:
        """Lazy-load the model on first use.

        PLACEHOLDER: replace with actual transformers loading code.
        """
        if self._model is not None:
            return

        log.info("Loading Qwen model from %s …", self.model_path)
        try:
            # --- PLACEHOLDER START ---
            # from transformers import AutoModelForCausalLM, AutoTokenizer
            # self._tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            # self._model = AutoModelForCausalLM.from_pretrained(
            #     self.model_path, torch_dtype="auto"
            # ).to(self.device)
            # --- PLACEHOLDER END ---
            log.warning(
                "QwenLocalAdapter: model loading is a placeholder; "
                "no real inference will run."
            )
        except Exception as exc:  # noqa: BLE001
            log.error("Qwen model load failed: %s", exc)

    def _generate(self, prompt: str) -> str:
        """Run inference on *prompt* and return generated text.

        PLACEHOLDER: replace with actual generation code.
        """
        self._ensure_loaded()

        # --- PLACEHOLDER START ---
        # inputs = self._tokenizer(prompt, return_tensors="pt").to(self.device)
        # with torch.no_grad():
        #     output = self._model.generate(**inputs, max_new_tokens=self.max_new_tokens)
        # return self._tokenizer.decode(output[0], skip_special_tokens=True)
        # --- PLACEHOLDER END ---

        # Fallback: return an empty string so callers discard the result
        return ""

    # --- ProblemParserLLM interface ---

    def parse_problem_description(self, description: str) -> dict[str, Any]:
        """Extract structured fields from a free-form problem description.

        Returns an empty dict on failure so the caller falls back to YAML only.
        """
        prompt = (
            "You are a scientific assistant.  Extract the following fields from "
            "the description and return them as a JSON object:\n"
            "geometry.length, material.conductivity, material.density, "
            "material.specific_heat, initial_condition, noise_std\n\n"
            f"Description: {description}\n\nJSON:"
        )
        raw = self._generate(prompt)
        if not raw:
            return {}
        try:
            import json
            # Extract JSON from the model output (may contain preamble text)
            start = raw.find("{")
            end = raw.rfind("}") + 1
            if start < 0 or end <= start:
                return {}
            return json.loads(raw[start:end])
        except Exception:  # noqa: BLE001
            log.warning("QwenLocalAdapter.parse_problem_description: JSON parse failed")
            return {}

    # --- ResultExplainerLLM interface ---

    def explain_verification(
        self,
        decision: str,
        reasons: list[str],
        metrics: dict[str, Any],
    ) -> str:
        """Generate a natural-language explanation of the verification result."""
        reason_text = "\n".join(f"- {r}" for r in reasons)
        prompt = (
            f"The IHCP inversion result was classified as '{decision}'.\n"
            f"Reasons:\n{reason_text}\n"
            f"Key metrics: {metrics}\n\n"
            "Explain in two sentences what this means for the quality of the "
            "heat flux reconstruction."
        )
        result = self._generate(prompt)
        return result if result else f"Verification decision: {decision}."

    # --- ReportWriterLLM interface ---

    def write_report_narrative(self, summary: Any, problem: Any) -> str:
        """Draft a brief narrative section for the markdown report."""
        prompt = (
            f"Write two paragraphs summarising an inverse heat conduction "
            f"inversion result. Status: {summary.final_status}. "
            f"Target: {problem.target_name}. "
            f"Final residual norm: {summary.final_result.residual_norm:.4f}."
        )
        result = self._generate(prompt)
        return result if result else "_LLM narrative not available._"


def make_qwen_hooks(
    model_path: str = "Qwen/Qwen2.5-3B-Instruct",
    device: str = "cpu",
) -> LLMHooks:
    """Convenience factory that returns a fully wired LLMHooks with Qwen."""
    adapter = QwenLocalAdapter(model_path=model_path, device=device)
    return LLMHooks(parser=adapter, explainer=adapter, writer=adapter)
