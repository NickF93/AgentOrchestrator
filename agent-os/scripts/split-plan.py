#!/usr/bin/env python3
"""Split a legacy aggregate PLAN.yaml into plan/ current and archive fragments."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from typing import Any

from plan_loader import (
    PlanLoadError,
    build_split_layout,
    load_legacy_plan,
    load_split_plan,
    write_yaml,
)


def load_render_module(script_dir: Path) -> Any:
    render_path = script_dir / "render-plan.py"
    spec = importlib.util.spec_from_file_location("render_plan_module", render_path)
    if spec is None or spec.loader is None:
        raise PlanLoadError(f"Unable to load render helper from {render_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser(description="Split a legacy PLAN.yaml into plan/ fragments")
    parser.add_argument(
        "plan", nargs="?", default="PLAN.yaml", help="Path to the legacy aggregate PLAN.yaml"
    )
    parser.add_argument(
        "--index",
        default="plan/PLAN-index.yaml",
        help="Output path for the split-plan index",
    )
    parser.add_argument("--md", default="PLAN.md", help="Output markdown path")
    parser.add_argument("--dot", default="PLAN.dot", help="Output dot path")
    parser.add_argument(
        "--remove-source",
        action="store_true",
        help="Remove the legacy aggregate source plan after a successful split",
    )
    args = parser.parse_args()

    plan_path = Path(args.plan)
    index_path = Path(args.index)

    if not plan_path.exists():
        print(f"ERROR: Plan file not found: {plan_path}")
        return 2

    try:
        aggregate_plan = load_legacy_plan(plan_path)
    except Exception as exc:
        print(f"ERROR: Failed to load plan: {exc}")
        return 2

    try:
        index, current_fragment, archive_fragments = build_split_layout(aggregate_plan)
        write_yaml(index_path, index)
        write_yaml(index_path.parent / index["current_plan"], current_fragment)
        for rel_path, fragment in archive_fragments.items():
            write_yaml(index_path.parent / rel_path, fragment)

        split_plan, split_metadata = load_split_plan(index_path)
        if split_plan != aggregate_plan:
            raise PlanLoadError("split aggregate plan does not match the legacy source plan")

        render_module = load_render_module(Path(__file__).resolve().parent)
        legacy_md = render_module.render_markdown(aggregate_plan)
        legacy_dot = render_module.render_dot(aggregate_plan)
        split_md = render_module.render_markdown(split_plan)
        split_dot = render_module.render_dot(split_plan)
        if legacy_md != split_md or legacy_dot != split_dot:
            raise PlanLoadError("rendered aggregate outputs changed across the split migration")

        Path(args.md).write_text(split_md, encoding="utf-8")
        Path(args.dot).write_text(split_dot, encoding="utf-8")

        if args.remove_source:
            plan_path.unlink()

        print(f"OK: wrote {index_path}")
        print(f"OK: wrote {split_metadata['current_path']}")
        for archive in split_metadata["archives"]:
            print(f"OK: wrote {archive['path']}")
        print(f"OK: wrote {args.md}")
        print(f"OK: wrote {args.dot}")
        if args.remove_source:
            print(f"OK: removed legacy source {plan_path}")
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
