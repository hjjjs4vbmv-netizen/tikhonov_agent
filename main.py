"""
main.py
=======
CLI entry point for the IHCP Tikhonov agent.

Usage
-----
    python main.py --config configs/example_case.yaml
    python main.py --config configs/example_case.yaml --observations data/demo_temperature.csv
    python main.py --config configs/example_case.yaml --loglevel DEBUG
    python main.py --config configs/example_case.yaml --output outputs/my_run
    python main.py --config configs/example_case.yaml --use-qwen  # enable Qwen LLM hooks
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from src.agent import IHCPAgent
from src.logging_utils import set_level


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Rule-based Tikhonov inversion agent for 1D transient IHCP"
    )
    p.add_argument(
        "--config", "-c",
        required=True,
        help="Path to YAML problem config file",
    )
    p.add_argument(
        "--observations", "-o",
        default=None,
        help="Path to CSV observations file (overrides config)",
    )
    p.add_argument(
        "--output-dir",
        default="outputs",
        help="Directory for reports (default: outputs/)",
    )
    p.add_argument(
        "--loglevel",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Log level (default: INFO)",
    )
    p.add_argument(
        "--use-qwen",
        action="store_true",
        default=False,
        help="Enable optional Qwen-2.5-3B LLM hooks (requires transformers + torch)",
    )
    p.add_argument(
        "--qwen-model",
        default="Qwen/Qwen2.5-3B-Instruct",
        help="Qwen model path or HuggingFace ID",
    )
    p.add_argument(
        "--qwen-device",
        default="cpu",
        help="Device for Qwen inference (cpu / cuda / mps)",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    # Configure logging
    set_level(getattr(logging, args.loglevel))

    # Optional LLM hooks
    llm_hooks = None
    if args.use_qwen:
        from src.llm_hooks import make_qwen_hooks
        llm_hooks = make_qwen_hooks(
            model_path=args.qwen_model,
            device=args.qwen_device,
        )

    # Load planner overrides from config YAML if present
    import yaml
    with open(args.config, encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)
    planner_overrides: dict = raw.get("planner", {}) or {}

    # Run agent
    agent = IHCPAgent(output_dir=args.output_dir, llm_hooks=llm_hooks)
    summary = agent.run(
        config_path=args.config,
        observations_path=args.observations,
        planner_overrides=planner_overrides,
    )

    # Print summary to stdout
    print("\n" + "=" * 60)
    print(f"Run complete  |  Status: {summary.final_status.upper()}")
    print(f"Iterations   : {len(summary.traces)}")
    if summary.final_result.estimated_x:
        import numpy as np
        x = np.array(summary.final_result.estimated_x)
        print(f"Recovered flux range: [{x.min():.1f}, {x.max():.1f}] W/m²")
    print(f"Residual norm: {summary.final_result.residual_norm:.4f}")
    if summary.report_paths:
        print("\nReports:")
        for label, path in summary.report_paths.items():
            print(f"  {label}: {path}")
    print("=" * 60 + "\n")

    return 0 if summary.final_status in ("pass", "weak_pass") else 1


if __name__ == "__main__":
    sys.exit(main())
