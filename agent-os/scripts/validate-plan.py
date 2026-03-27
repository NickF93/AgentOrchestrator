#!/usr/bin/env python3
"""Validate PLAN.yaml against schema and governance hard rules."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: pyyaml. Install with: pip install pyyaml") from exc

try:
    import jsonschema
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: jsonschema. Install with: pip install jsonschema"
    ) from exc


CONTAINER_TYPES = {"X", "S"}
MILESTONE_ID_RE = re.compile(r"^X[1-9][0-9]*$")
SPRINT_ID_RE = re.compile(r"^S[1-9][0-9]*\.[1-9][0-9]*$")
ITEM_ID_RE = re.compile(r"^([A-Z]+)([1-9][0-9]*)\.([1-9][0-9]*)\.([1-9][0-9]*)([a-z]?)$")


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Top-level YAML document must be a mapping")
    return data


def load_schema(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Schema must be a JSON object")
    return data


def collect_ids(plan: dict) -> dict[str, str]:
    id_to_type: dict[str, str] = {}
    for section in ("milestones", "sprints", "items"):
        for obj in plan.get(section, []) or []:
            obj_id = obj.get("id")
            obj_type = obj.get("type")
            if obj_id:
                id_to_type[obj_id] = obj_type
    return id_to_type


def validate_custom_rules(plan: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    id_to_type = collect_ids(plan)
    milestones = plan.get("milestones", []) or []
    sprints = plan.get("sprints", []) or []
    items = plan.get("items", []) or []

    # Hard-fail: identifier grammar for milestone/sprint/item IDs.
    for milestone in milestones:
        mid = milestone.get("id", "")
        if not MILESTONE_ID_RE.fullmatch(mid):
            errors.append(
                f"milestone id '{mid}' is invalid; expected format X<number> (e.g. X1)"
            )

    for sprint in sprints:
        sid = sprint.get("id", "")
        if not SPRINT_ID_RE.fullmatch(sid):
            errors.append(
                f"sprint id '{sid}' is invalid; expected format S<milestone>.<sprint> (e.g. S1.1)"
            )

    suffixes_by_base: dict[str, list[str]] = {}
    for item in items:
        iid = item.get("id", "")
        m = ITEM_ID_RE.fullmatch(iid)
        if not m:
            errors.append(
                f"item id '{iid}' is invalid; expected format <TYPE><m>.<s>.<n><optional lowercase suffix> (e.g. M1.1.1, M1.1.1a)"
            )
            continue
        base = f"{m.group(1)}{m.group(2)}.{m.group(3)}.{m.group(4)}"
        suffix = m.group(5)
        suffixes_by_base.setdefault(base, []).append(suffix)

    # Hard-fail: suffix uniqueness and chronology within same base item.
    for base, suffixes in suffixes_by_base.items():
        letter_suffixes = [s for s in suffixes if s]
        if len(letter_suffixes) != len(set(letter_suffixes)):
            errors.append(f"{base}: duplicate suffix detected; suffixes must be unique")
        if letter_suffixes:
            ordered_unique = sorted(set(letter_suffixes))
            expected = [chr(c) for c in range(ord("a"), ord("a") + len(ordered_unique))]
            if ordered_unique != expected:
                errors.append(
                    f"{base}: suffixes must be chronological from 'a' without gaps (found: {', '.join(ordered_unique)})"
                )

    # Hard-fail: dangling depends_on and container usage in depends_on.
    for item in items:
        item_id = item.get("id", "<unknown>")
        depends_on = item.get("depends_on", []) or []
        for dep in depends_on:
            if dep not in id_to_type:
                errors.append(f"{item_id}: depends_on references unknown id '{dep}'")
                continue
            if id_to_type[dep] in CONTAINER_TYPES:
                errors.append(
                    f"{item_id}: depends_on references container id '{dep}' of type {id_to_type[dep]}"
                )

    # Warning-only: scope collisions among in_progress items.
    in_progress = [i for i in items if i.get("status") == "in_progress"]
    for idx, left in enumerate(in_progress):
        left_scope = (left.get("scope") or "").strip()
        if not left_scope:
            continue
        for right in in_progress[idx + 1 :]:
            right_scope = (right.get("scope") or "").strip()
            if not right_scope:
                continue
            if left_scope == right_scope or left_scope.startswith(right_scope) or right_scope.startswith(left_scope):
                warnings.append(
                    "scope collision warning: "
                    f"{left.get('id', '<unknown>')} ({left_scope}) <-> "
                    f"{right.get('id', '<unknown>')} ({right_scope})"
                )

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate PLAN.yaml")
    parser.add_argument("plan", nargs="?", default="PLAN.yaml", help="Path to PLAN.yaml")
    parser.add_argument(
        "--schema",
        default="agent-os/schemas/plan.schema.json",
        help="Path to plan schema JSON",
    )
    args = parser.parse_args()

    plan_path = Path(args.plan)
    schema_path = Path(args.schema)

    if not plan_path.exists():
        print(f"ERROR: Plan file not found: {plan_path}", file=sys.stderr)
        return 2
    if not schema_path.exists():
        print(f"ERROR: Schema file not found: {schema_path}", file=sys.stderr)
        return 2

    try:
        plan = load_yaml(plan_path)
    except Exception as exc:
        print(f"ERROR: Failed to load plan YAML: {exc}", file=sys.stderr)
        return 2

    try:
        schema = load_schema(schema_path)
    except Exception as exc:
        print(f"ERROR: Failed to load schema JSON: {exc}", file=sys.stderr)
        return 2

    try:
        jsonschema.validate(instance=plan, schema=schema)
    except jsonschema.ValidationError as exc:
        print("ERROR: Schema validation failed", file=sys.stderr)
        print(f"  path: {'/'.join(str(p) for p in exc.path)}", file=sys.stderr)
        print(f"  message: {exc.message}", file=sys.stderr)
        return 1

    errors, warnings = validate_custom_rules(plan)

    for warning in warnings:
        print(f"WARNING: {warning}")

    if errors:
        print("ERROR: Governance checks failed", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"OK: {plan_path} is valid against {schema_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
