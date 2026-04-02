#!/usr/bin/env python3
"""Archive a completed current milestone into plan/archive/."""

from __future__ import annotations

import argparse
import importlib.util
from datetime import date
from pathlib import Path
from typing import Any

from plan_loader import (
    PlanLoadError,
    compute_fragment_digest,
    extract_fragment,
    load_split_plan,
    load_yaml_mapping,
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


def ensure_fragment_is_closed(fragment: dict, milestone_id: str) -> None:
    if fragment["milestones"][0].get("status") != "done":
        raise PlanLoadError(f"{milestone_id}: milestone must be status 'done' before archival")

    open_sprints = [obj["id"] for obj in fragment.get("sprints", []) if obj.get("status") != "done"]
    if open_sprints:
        raise PlanLoadError(f"{milestone_id}: sprints must be done before archival: {open_sprints}")

    open_items = [obj["id"] for obj in fragment.get("items", []) if obj.get("status") != "done"]
    if open_items:
        raise PlanLoadError(f"{milestone_id}: items must be done before archival: {open_items}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Archive a completed current milestone")
    parser.add_argument(
        "--plan",
        default="plan/PLAN-index.yaml",
        help="Path to plan/PLAN-index.yaml",
    )
    parser.add_argument(
        "--milestone", required=True, help="Milestone ID to archive (for example X31)"
    )
    parser.add_argument("--md", default="PLAN.md", help="Output markdown path")
    parser.add_argument("--dot", default="PLAN.dot", help="Output dot path")
    args = parser.parse_args()

    index_path = Path(args.plan)
    if not index_path.exists():
        print(f"ERROR: Plan index not found: {index_path}")
        return 2

    try:
        aggregate_plan, metadata = load_split_plan(index_path)
        index = load_yaml_mapping(index_path)
        current_fragment = metadata["current_fragment"]
        milestone_id = args.milestone

        current_milestones = {
            str(obj.get("id", "")): obj for obj in current_fragment.get("milestones", []) or []
        }
        if milestone_id not in current_milestones:
            raise PlanLoadError(f"{milestone_id}: milestone is not present in the current fragment")

        archive_root_rel = Path(str(index.get("archive_root", "")))
        archive_rel_path = (archive_root_rel / f"PLAN-{milestone_id}.yaml").as_posix()
        archive_abs_path = index_path.parent / archive_rel_path
        if archive_abs_path.exists():
            raise PlanLoadError(
                f"{milestone_id}: archive target already exists at {archive_abs_path}"
            )

        existing_entries = index.get("archives", []) or []

        archived_fragment = extract_fragment(current_fragment, {milestone_id})
        ensure_fragment_is_closed(archived_fragment, milestone_id)

        remaining_milestone_ids = {
            str(obj.get("id", ""))
            for obj in current_fragment.get("milestones", []) or []
            if str(obj.get("id", "")) != milestone_id
        }
        remaining_current = extract_fragment(current_fragment, remaining_milestone_ids)

        archived_milestone = archived_fragment["milestones"][0]
        updated_archives = list(existing_entries)
        updated_archives.append(
            {
                "milestone": milestone_id,
                "title": str(archived_milestone.get("title", "")),
                "path": archive_rel_path,
                "digest": compute_fragment_digest(archived_fragment),
            }
        )
        updated_archives.sort(key=lambda entry: int(str(entry["milestone"])[1:]))

        index["archives"] = updated_archives
        index["meta"]["last_updated"] = date.today().isoformat()

        write_yaml(archive_abs_path, archived_fragment)
        write_yaml(metadata["current_path"], remaining_current)
        write_yaml(index_path, index)

        split_plan, _ = load_split_plan(index_path)
        render_module = load_render_module(Path(__file__).resolve().parent)
        Path(args.md).write_text(
            render_module.render_markdown(split_plan, source_label=str(index_path)),
            encoding="utf-8",
        )
        Path(args.dot).write_text(render_module.render_dot(split_plan), encoding="utf-8")

        print(f"OK: archived {milestone_id} to {archive_abs_path}")
        print(f"OK: updated {metadata['current_path']}")
        print(f"OK: updated {index_path}")
        print(f"OK: wrote {args.md}")
        print(f"OK: wrote {args.dot}")
    except PlanLoadError as exc:
        print(f"ERROR: {exc}")
        return 1
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
