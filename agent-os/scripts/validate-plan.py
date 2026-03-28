#!/usr/bin/env python3
"""Validate PLAN.yaml against schema and governance hard rules."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
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
ALLOWED_STATE_TRANSITIONS = {
    "planned": {"planned", "ready"},
    "ready": {"ready", "in_progress", "blocked"},
    "in_progress": {"in_progress", "review", "blocked"},
    "review": {"review", "verified", "blocked"},
    "verified": {"verified", "done"},
    "done": {"done"},
    "blocked": {"blocked", "ready"},
}
DEPENDENCY_READY_STATES = {"verified", "done"}
RECOMMENDED_ACTIONS: dict[str, set[str]] = {
    "Q": {"review", "decide"},
    "D": {"plan", "document", "review", "checkpoint"},
    "M": {"design", "implement", "refactor", "migrate", "verify"},
    "F": {"implement", "test", "verify"},
    "T": {"test", "verify"},
    "C": {"review", "checkpoint", "verify"},
}
EXECUTABLE_ITEM_TYPES = set(RECOMMENDED_ACTIONS.keys())


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


def collect_statuses(plan: dict) -> dict[str, str]:
    id_to_status: dict[str, str] = {}
    for section in ("milestones", "sprints", "items"):
        for obj in plan.get(section, []) or []:
            obj_id = obj.get("id")
            obj_status = obj.get("status")
            if obj_id and obj_status:
                id_to_status[obj_id] = obj_status
    return id_to_status


def validate_transitions(current: dict, previous: dict) -> list[str]:
    errors: list[str] = []
    prev_status = collect_statuses(previous)
    curr_status = collect_statuses(current)

    for obj_id, now in curr_status.items():
        before = prev_status.get(obj_id)
        if before is None:
            continue
        allowed = ALLOWED_STATE_TRANSITIONS.get(before)
        if not allowed:
            continue
        if now not in allowed:
            errors.append(
                f"{obj_id}: invalid status transition {before} -> {now}; allowed: {sorted(allowed)}"
            )
    return errors


def detect_cycles(items: list[dict]) -> list[str]:
    """Detect cycles in depends_on using Kahn's algorithm. Returns error messages."""
    # Build adjacency list and in-degree map for items only
    item_ids = {item.get("id", "") for item in items}
    adj: dict[str, list[str]] = {item.get("id", ""): [] for item in items}
    in_degree: dict[str, int] = {item.get("id", ""): 0 for item in items}

    for item in items:
        item_id = item.get("id", "")
        for dep in item.get("depends_on", []) or []:
            if dep in item_ids:
                adj[dep].append(item_id)
                in_degree[item_id] += 1

    # Kahn's algorithm
    queue = [nid for nid, deg in in_degree.items() if deg == 0]
    processed = 0
    while queue:
        node = queue.pop(0)
        processed += 1
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if processed == len(item_ids):
        return []

    cycle_participants = sorted(nid for nid, deg in in_degree.items() if deg > 0)
    return [
        f"dependency cycle detected among items: {', '.join(cycle_participants)}"
    ]


def validate_commit_group_coherence(plan: dict) -> list[str]:
    """Validate bidirectional consistency between commit_groups and items."""
    errors: list[str] = []
    items = plan.get("items", []) or []
    commit_groups = plan.get("commit_groups", []) or []

    item_ids = {item.get("id", "") for item in items}
    cg_ids = {cg.get("id", "") for cg in commit_groups}

    # Build maps
    item_to_cg: dict[str, str] = {}
    for item in items:
        item_id = item.get("id", "")
        item_type = item.get("type", "")
        cg = item.get("commit_group", "")
        if item_type in EXECUTABLE_ITEM_TYPES and not cg:
            errors.append(
                f"item '{item_id}' is executable (type {item_type}) but has no commit_group"
            )
        if cg:
            item_to_cg[item_id] = cg

    cg_to_items: dict[str, list[str]] = {}
    for cg in commit_groups:
        cg_id = cg.get("id", "")
        cg_to_items[cg_id] = list(cg.get("items", []) or [])

    # Forward check: every commit_group.items[] must resolve to an existing item
    for cg_id, members in cg_to_items.items():
        for member in members:
            if member not in item_ids:
                errors.append(
                    f"commit_group '{cg_id}' references unknown item '{member}'"
                )

    # Reverse check: every item.commit_group must reference an existing commit_group
    for item_id, cg in item_to_cg.items():
        if cg not in cg_ids:
            errors.append(
                f"item '{item_id}' references unknown commit_group '{cg}'"
            )

    # Membership coherence: bidirectional match
    for item_id, cg in item_to_cg.items():
        if cg in cg_to_items and item_id not in cg_to_items[cg]:
            errors.append(
                f"item '{item_id}' declares commit_group '{cg}' but is not listed in that commit_group's items"
            )

    for cg_id, members in cg_to_items.items():
        for member in members:
            if member in item_to_cg and item_to_cg[member] != cg_id:
                errors.append(
                    f"commit_group '{cg_id}' lists item '{member}' but that item declares commit_group '{item_to_cg[member]}'"
                )

    return errors


def validate_type_action_coherence(items: list[dict]) -> list[str]:
    """Warn when item actions are outside the recommended set for its type."""
    warnings: list[str] = []
    for item in items:
        item_id = item.get("id", "<unknown>")
        item_type = item.get("type", "")
        actions = item.get("actions", []) or []
        recommended = RECOMMENDED_ACTIONS.get(item_type)
        if recommended is None:
            continue
        for action in actions:
            if action not in recommended:
                warnings.append(
                    f"{item_id}: action '{action}' is not in recommended set for type {item_type} "
                    f"(recommended: {sorted(recommended)})"
                )
    return warnings


def validate_custom_rules(plan: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    id_to_type = collect_ids(plan)
    id_to_status = collect_statuses(plan)
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
        item_status = item.get("status", "")
        depends_on = item.get("depends_on", []) or []
        for dep in depends_on:
            if dep not in id_to_type:
                errors.append(f"{item_id}: depends_on references unknown id '{dep}'")
                continue
            if id_to_type[dep] in CONTAINER_TYPES:
                errors.append(
                    f"{item_id}: depends_on references container id '{dep}' of type {id_to_type[dep]}"
                )
                continue

            if item_status in {"ready", "in_progress", "review", "verified", "done"}:
                dep_status = id_to_status.get(dep, "")
                if dep_status not in DEPENDENCY_READY_STATES:
                    errors.append(
                        f"{item_id}: dependency '{dep}' is {dep_status}, required one of {sorted(DEPENDENCY_READY_STATES)} for item status {item_status}"
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

    # Hard-fail: DAG cycle detection in depends_on relationships.
    errors.extend(detect_cycles(items))

    # Hard-fail: bidirectional commit_group/item consistency.
    errors.extend(validate_commit_group_coherence(plan))

    # Warning-only: type/action coherence.
    warnings.extend(validate_type_action_coherence(items))

    # Phase-gate enforcement: requires_phase items need approval_ref.
    pg_errors, pg_warnings = validate_phase_gates(items)
    errors.extend(pg_errors)
    warnings.extend(pg_warnings)

    return errors, warnings


def validate_phase_gates(items: list[dict]) -> tuple[list[str], list[str]]:
    """Enforce phase-gate rules for items with requires_phase."""
    errors: list[str] = []
    warnings: list[str] = []
    active_statuses = {"ready", "in_progress", "review"}

    for item in items:
        item_id = item.get("id", "<unknown>")
        requires_phase = item.get("requires_phase")
        approval_ref = item.get("approval_ref")
        status = item.get("status", "")

        if requires_phase and status in active_statuses and not approval_ref:
            errors.append(
                f"{item_id}: has requires_phase={requires_phase} and status={status} "
                f"but no approval_ref — phase-gate items MUST have approval_ref "
                f"before entering active status"
            )

    return errors, warnings


def check_repo_map_freshness(plan: dict, plan_path: Path) -> list[str]:
    """Hard-fail if REPO_MAP.md is stale when checkpoint items are active."""
    errors: list[str] = []
    items = plan.get("items", []) or []
    active_checkpoints = [
        i for i in items
        if i.get("type") == "C" and i.get("status") in {"review", "verified"}
    ]
    if not active_checkpoints:
        return errors

    repo_map_path = plan_path.parent / "REPO_MAP.md"
    if not repo_map_path.exists():
        return errors

    # Parse freshness metadata from REPO_MAP.md header
    last_validated = None
    window_days = 30
    for line in repo_map_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("last_validated_on:"):
            val = stripped.split(":", 1)[1].strip()
            if val:
                try:
                    last_validated = datetime.strptime(val, "%Y-%m-%d").date()
                except ValueError:
                    pass
        elif stripped.startswith("freshness_window_days:"):
            val = stripped.split(":", 1)[1].strip()
            if val:
                try:
                    window_days = int(val)
                except ValueError:
                    pass

    if last_validated is None:
        checkpoint_ids = ", ".join(i.get("id", "") for i in active_checkpoints)
        errors.append(
            f"REPO_MAP.md has no last_validated_on date; "
            f"active checkpoint(s) {checkpoint_ids} cannot close without freshness verification"
        )
        return errors

    age = (date.today() - last_validated).days
    if age > window_days:
        checkpoint_ids = ", ".join(i.get("id", "") for i in active_checkpoints)
        errors.append(
            f"REPO_MAP.md is stale ({age} days old, window is {window_days} days); "
            f"active checkpoint(s) {checkpoint_ids} cannot close until map is refreshed"
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate PLAN.yaml")
    parser.add_argument("plan", nargs="?", default="PLAN.yaml", help="Path to PLAN.yaml")
    parser.add_argument(
        "--schema",
        default="agent-os/schemas/plan.schema.json",
        help="Path to plan schema JSON",
    )
    parser.add_argument(
        "--previous-plan",
        default="",
        help="Optional previous PLAN.yaml to enforce lifecycle transition rules",
    )
    parser.add_argument(
        "--check-freshness",
        action="store_true",
        help="Check REPO_MAP.md freshness when checkpoint items are active",
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

    if args.previous_plan:
        prev_path = Path(args.previous_plan)
        if not prev_path.exists():
            print(f"ERROR: Previous plan file not found: {prev_path}", file=sys.stderr)
            return 2
        try:
            previous = load_yaml(prev_path)
        except Exception as exc:
            print(f"ERROR: Failed to load previous plan YAML: {exc}", file=sys.stderr)
            return 2

        transition_errors = validate_transitions(plan, previous)
        if transition_errors:
            print("ERROR: Lifecycle transition checks failed", file=sys.stderr)
            for err in transition_errors:
                print(f"  - {err}", file=sys.stderr)
            return 1

    errors, warnings = validate_custom_rules(plan)

    if args.check_freshness:
        errors.extend(check_repo_map_freshness(plan, plan_path))

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
