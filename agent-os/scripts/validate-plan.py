#!/usr/bin/env python3
"""Validate the canonical plan entrypoint against schema and governance hard rules."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

from plan_loader import PlanLoadError, load_plan

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: pyyaml. Install tooling deps with: "
        "python3 -m pip install -r requirements.txt"
    ) from exc

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None


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
READY_QUERY_STATUSES = {"planned", "ready"}
RECOMMENDED_ACTIONS: dict[str, set[str]] = {
    "Q": {"review", "decide"},
    "D": {"plan", "document", "review", "checkpoint"},
    "M": {"design", "implement", "refactor", "migrate", "verify"},
    "F": {"implement", "test", "verify"},
    "T": {"test", "verify"},
    "C": {"review", "checkpoint", "verify"},
}
EXECUTABLE_ITEM_TYPES = set(RECOMMENDED_ACTIONS.keys())
SHARED_ASSET_KINDS = {"skill", "prompt", "profile", "protocol"}
SHARED_ASSET_FIELD_KIND = {
    "skill": "skill",
    "prompt": "prompt",
    "profile": "profile",
    "result_protocol": "protocol",
}
SHARED_ASSET_PATH_PREFIX = {
    "skill": "agent-os/skills/",
    "prompt": "agent-os/prompts/",
    "profile": "agent-os/profiles/",
    "protocol": "agent-os/protocols/",
}


_BLOCK_SCALAR_RE = re.compile(r"^[ \t]*[^\s#][^:]*:[ \t]+[|>]")


def _count_unescaped(line: str, quote: str) -> int:
    """Count unescaped occurrences of *quote* in *line*.

    For single-quote (``'``), YAML escapes via ``''`` (two consecutive).
    For double-quote (``"``), YAML escapes via ``\\"``.
    """
    count = 0
    i = 0
    while i < len(line):
        if line[i] == quote:
            if quote == "'" and i + 1 < len(line) and line[i + 1] == "'":
                i += 2  # escaped ''
                continue
            if quote == '"' and i > 0 and line[i - 1] == "\\":
                i += 1  # escaped \"
                continue
            count += 1
        i += 1
    return count


def _is_inside_quotes(line: str, pos: int) -> bool:
    """Return True if the character at *pos* is inside single or double quotes."""
    in_single = False
    in_double = False
    i = 0
    while i < pos:
        ch = line[i]
        if ch == "'" and not in_double:
            if in_single and i + 1 < len(line) and line[i + 1] == "'":
                i += 2  # escaped ''
                continue
            in_single = not in_single
        elif ch == '"' and not in_single:
            if in_double and i > 0 and line[i - 1] == "\\":
                i += 1
                continue
            in_double = not in_double
        i += 1
    return in_single or in_double


def lint_yaml_unquoted_hash(path: Path) -> list[str]:
    """Scan a YAML file for unquoted ``#`` in value positions.

    Returns a list of human-readable error strings, one per offending line.
    Correctly skips block scalars (``|``, ``>``) and multi-line quoted
    scalars (single or double).
    """
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    block_scalar_indent: int | None = None
    in_multiline_quote: str | None = None  # "'" or '"' when active

    for lineno_0, raw_line in enumerate(lines, start=1):
        stripped = raw_line.rstrip()

        # Determine current indentation level.
        content = stripped.lstrip()
        indent = len(stripped) - len(content)

        # --- Multi-line quoted scalar tracking ---
        if in_multiline_quote is not None:
            closes = _count_unescaped(stripped, in_multiline_quote)
            if closes > 0:
                in_multiline_quote = None
            continue

        if not stripped:
            continue

        # --- Block scalar tracking ---
        if block_scalar_indent is not None:
            if indent > block_scalar_indent or not content:
                continue
            block_scalar_indent = None

        if _BLOCK_SCALAR_RE.match(stripped):
            block_scalar_indent = indent
            continue

        # Skip full-line comments.
        if content.startswith("#"):
            continue

        # Detect multi-line quoted scalars that open but don't close on
        # this line.  Look for a value that starts with a quote character.
        for quote_char in ("'", '"'):
            # Match  key: 'value...  or  key: "value...
            marker = f": {quote_char}"
            idx = stripped.find(marker)
            if idx != -1:
                value_start = idx + len(marker)
                rest = stripped[value_start:]
                closes = _count_unescaped(rest, quote_char)
                if closes == 0:
                    in_multiline_quote = quote_char
                break

        if in_multiline_quote is not None:
            continue

        # Look for ` #` in the line outside of quoted spans.
        search_start = 0
        while True:
            pos = stripped.find(" #", search_start)
            if pos == -1:
                break
            if not _is_inside_quotes(stripped, pos + 1):
                errors.append(f"{path}:{lineno_0}: unquoted '#' in value: {stripped.strip()}")
                break
            search_start = pos + 2

    return errors


def lint_yaml_unquoted_hash_all(plan_path: Path) -> list[str]:
    """Collect all YAML files from a split-plan index and lint each one."""
    errors: list[str] = []

    # Lint the index file itself first.
    errors.extend(lint_yaml_unquoted_hash(plan_path))

    try:
        index = yaml.safe_load(plan_path.read_text(encoding="utf-8"))
    except Exception:
        return errors

    if not isinstance(index, dict) or "current_plan" not in index:
        return errors

    plan_dir = plan_path.parent
    current = plan_dir / index["current_plan"]
    if current.exists():
        errors.extend(lint_yaml_unquoted_hash(current))

    for entry in index.get("archives", []):
        archive = plan_dir / entry.get("path", "")
        if archive.exists():
            errors.extend(lint_yaml_unquoted_hash(archive))

    return errors


def default_shared_asset_registry_path() -> Path:
    return Path(__file__).resolve().parents[2] / "agent-os" / "registry" / "shared-assets.yaml"


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


def load_shared_asset_registry(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Shared asset registry must be a mapping")
    return data


def validate_shared_asset_registry(
    registry: dict, registry_path: Path
) -> tuple[dict[str, dict], list[str]]:
    errors: list[str] = []
    assets = registry.get("assets")
    if not isinstance(assets, list):
        return {}, ["shared asset registry must define an 'assets' list"]

    control_plane_root = registry_path.parent.parent.parent
    asset_map: dict[str, dict] = {}
    referenced_dependencies: list[tuple[str, str]] = []

    for idx, asset in enumerate(assets):
        prefix = f"shared asset registry entry #{idx + 1}"
        if not isinstance(asset, dict):
            errors.append(f"{prefix}: entry must be a mapping")
            continue

        asset_id = asset.get("id")
        kind = asset.get("kind")
        version = asset.get("version")
        path_text = asset.get("path")
        compatibility = asset.get("compatibility")
        materializable = asset.get("materializable")

        if not isinstance(asset_id, str) or not asset_id:
            errors.append(f"{prefix}: missing non-empty id")
            continue
        if asset_id in asset_map:
            errors.append(f"shared asset registry has duplicate id '{asset_id}'")
            continue
        if kind not in SHARED_ASSET_KINDS:
            errors.append(
                f"shared asset '{asset_id}' has invalid kind '{kind}' "
                f"(expected one of {sorted(SHARED_ASSET_KINDS)})"
            )
        if not isinstance(version, str) or not version:
            errors.append(f"shared asset '{asset_id}' has no non-empty version")
        if not isinstance(path_text, str) or not path_text:
            errors.append(f"shared asset '{asset_id}' has no non-empty path")
        if (
            not isinstance(compatibility, list)
            or not compatibility
            or not all(isinstance(entry, str) and entry for entry in compatibility)
        ):
            errors.append(f"shared asset '{asset_id}' must declare a non-empty compatibility list")
        if not isinstance(materializable, bool):
            errors.append(f"shared asset '{asset_id}' must declare materializable as true or false")

        asset_map[asset_id] = asset

        if isinstance(path_text, str) and isinstance(kind, str):
            expected_prefix = SHARED_ASSET_PATH_PREFIX.get(kind)
            if expected_prefix and not path_text.startswith(expected_prefix):
                errors.append(
                    f"shared asset '{asset_id}' kind '{kind}' must live under '{expected_prefix}' "
                    f"(got '{path_text}')"
                )
            asset_path = control_plane_root / path_text
            if not asset_path.exists():
                errors.append(f"shared asset '{asset_id}' path does not exist: {asset_path}")

        depends_on_assets = asset.get("depends_on_assets", []) or []
        if not isinstance(depends_on_assets, list):
            errors.append(f"shared asset '{asset_id}' has non-list depends_on_assets")
            continue
        for dep in depends_on_assets:
            if not isinstance(dep, str) or not dep:
                errors.append(
                    f"shared asset '{asset_id}' has invalid depends_on_assets entry '{dep}'"
                )
                continue
            referenced_dependencies.append((asset_id, dep))

    for asset_id, dep in referenced_dependencies:
        if dep not in asset_map:
            errors.append(
                f"shared asset '{asset_id}' depends_on_assets references unknown asset '{dep}'"
            )

    return asset_map, errors


def validate_shared_asset_refs(items: list[dict], asset_map: dict[str, dict]) -> list[str]:
    errors: list[str] = []

    for item in items:
        item_id = item.get("id", "<unknown>")
        shared_assets = item.get("shared_assets")
        if shared_assets is None:
            continue
        if not isinstance(shared_assets, dict):
            errors.append(f"{item_id}: shared_assets must be a mapping")
            continue

        for field, expected_kind in SHARED_ASSET_FIELD_KIND.items():
            asset_id = shared_assets.get(field)
            if asset_id is None:
                continue
            asset = asset_map.get(asset_id)
            if asset is None:
                errors.append(
                    f"{item_id}: shared_assets.{field} references unknown asset id '{asset_id}'"
                )
                continue
            actual_kind = asset.get("kind")
            if actual_kind != expected_kind:
                errors.append(
                    f"{item_id}: shared_assets.{field} references '{asset_id}' of kind "
                    f"'{actual_kind}', expected '{expected_kind}'"
                )

    return errors


def ensure_mapping(value: object, context: str, errors: list[str]) -> dict | None:
    if not isinstance(value, dict):
        errors.append(f"{context}: expected mapping")
        return None
    return value


def ensure_list(value: object, context: str, errors: list[str]) -> list | None:
    if not isinstance(value, list):
        errors.append(f"{context}: expected list")
        return None
    return value


def validate_plan_schema_subset(plan: dict) -> list[str]:
    """Fallback schema validation when jsonschema is unavailable."""
    errors: list[str] = []

    required_top_level = ["meta", "mission", "milestones", "sprints", "items", "commit_groups"]
    for field in required_top_level:
        if field not in plan:
            errors.append(f"missing required top-level field '{field}'")

    meta = ensure_mapping(plan.get("meta"), "meta", errors)
    if meta is not None:
        for field in ("repo", "owner", "version", "schema_version", "last_updated"):
            if not isinstance(meta.get(field), str) or not meta.get(field):
                errors.append(f"meta.{field}: expected non-empty string")

    mission = plan.get("mission")
    if not isinstance(mission, str) or not mission.strip():
        errors.append("mission: expected non-empty string")

    milestones = ensure_list(plan.get("milestones"), "milestones", errors) or []
    for idx, milestone in enumerate(milestones):
        context = f"milestones[{idx}]"
        milestone_map = ensure_mapping(milestone, context, errors)
        if milestone_map is None:
            continue
        if not isinstance(milestone_map.get("id"), str) or not MILESTONE_ID_RE.fullmatch(
            milestone_map["id"]
        ):
            errors.append(f"{context}.id: expected milestone id like X1")
        if milestone_map.get("type") != "X":
            errors.append(f"{context}.type: expected 'X'")
        if not isinstance(milestone_map.get("title"), str) or not milestone_map.get("title"):
            errors.append(f"{context}.title: expected non-empty string")
        if milestone_map.get("status") not in ALLOWED_STATE_TRANSITIONS:
            errors.append(f"{context}.status: invalid status '{milestone_map.get('status')}'")

    sprints = ensure_list(plan.get("sprints"), "sprints", errors) or []
    for idx, sprint in enumerate(sprints):
        context = f"sprints[{idx}]"
        sprint_map = ensure_mapping(sprint, context, errors)
        if sprint_map is None:
            continue
        if not isinstance(sprint_map.get("id"), str) or not SPRINT_ID_RE.fullmatch(
            sprint_map["id"]
        ):
            errors.append(f"{context}.id: expected sprint id like S1.1")
        if sprint_map.get("type") != "S":
            errors.append(f"{context}.type: expected 'S'")
        if not isinstance(sprint_map.get("parent"), str) or not MILESTONE_ID_RE.fullmatch(
            sprint_map["parent"]
        ):
            errors.append(f"{context}.parent: expected milestone id like X1")
        if not isinstance(sprint_map.get("title"), str) or not sprint_map.get("title"):
            errors.append(f"{context}.title: expected non-empty string")
        if sprint_map.get("status") not in ALLOWED_STATE_TRANSITIONS:
            errors.append(f"{context}.status: invalid status '{sprint_map.get('status')}'")

    items = ensure_list(plan.get("items"), "items", errors) or []
    action_enum = {
        "audit",
        "plan",
        "design",
        "implement",
        "refactor",
        "test",
        "verify",
        "document",
        "review",
        "checkpoint",
        "decide",
        "migrate",
    }
    role_enum = {"orchestrator", "implementer", "tester", "reviewer", "documenter", "researcher"}
    effort_enum = {"low", "medium", "high"}
    shared_asset_fields = {
        "skill",
        "prompt",
        "profile",
        "result_protocol",
        "context_policy",
        "resolution_mode",
    }

    for idx, item in enumerate(items):
        context = f"items[{idx}]"
        item_map = ensure_mapping(item, context, errors)
        if item_map is None:
            continue

        for field in (
            "id",
            "parent",
            "type",
            "title",
            "status",
            "role",
            "effort",
            "actions",
            "commit_group",
        ):
            if field not in item_map:
                errors.append(f"{context}: missing required field '{field}'")

        item_id = item_map.get("id")
        if not isinstance(item_id, str) or not ITEM_ID_RE.fullmatch(item_id):
            errors.append(f"{context}.id: expected item id like M1.1.1")
        parent = item_map.get("parent")
        if not isinstance(parent, str) or not SPRINT_ID_RE.fullmatch(parent):
            errors.append(f"{context}.parent: expected sprint id like S1.1")
        item_type = item_map.get("type")
        if item_type not in EXECUTABLE_ITEM_TYPES:
            errors.append(f"{context}.type: invalid item type '{item_type}'")
        if not isinstance(item_map.get("title"), str) or not item_map.get("title"):
            errors.append(f"{context}.title: expected non-empty string")
        if item_map.get("status") not in ALLOWED_STATE_TRANSITIONS:
            errors.append(f"{context}.status: invalid status '{item_map.get('status')}'")
        if item_map.get("role") not in role_enum:
            errors.append(f"{context}.role: invalid role '{item_map.get('role')}'")
        if item_map.get("effort") not in effort_enum:
            errors.append(f"{context}.effort: invalid effort '{item_map.get('effort')}'")

        actions = item_map.get("actions")
        if not isinstance(actions, list) or not actions:
            errors.append(f"{context}.actions: expected non-empty list")
        else:
            for action in actions:
                if action not in action_enum:
                    errors.append(f"{context}.actions: invalid action '{action}'")

        commit_group = item_map.get("commit_group")
        if not isinstance(commit_group, str) or not re.fullmatch(r"^cg[0-9]+$", commit_group):
            errors.append(f"{context}.commit_group: expected value like cg1")

        depends_on = item_map.get("depends_on")
        if depends_on is not None and not isinstance(depends_on, list):
            errors.append(f"{context}.depends_on: expected list")

        scope = item_map.get("scope")
        if scope is not None and (
            not isinstance(scope, str) or not re.fullmatch(r"^(\.|[A-Za-z0-9._/-]+)$", scope)
        ):
            errors.append(f"{context}.scope: invalid scope '{scope}'")

        checks = item_map.get("checks")
        if checks is not None and (
            not isinstance(checks, list) or any(not isinstance(check, str) for check in checks)
        ):
            errors.append(f"{context}.checks: expected list of strings")

        artifacts_in = item_map.get("artifacts_in")
        if artifacts_in is not None and (
            not isinstance(artifacts_in, list)
            or any(not isinstance(path, str) for path in artifacts_in)
        ):
            errors.append(f"{context}.artifacts_in: expected list of strings")

        artifacts_out = item_map.get("artifacts_out")
        if artifacts_out is not None and (
            not isinstance(artifacts_out, list)
            or any(not isinstance(path, str) for path in artifacts_out)
        ):
            errors.append(f"{context}.artifacts_out: expected list of strings")

        decision = item_map.get("decision")
        if decision is not None and not isinstance(decision, str):
            errors.append(f"{context}.decision: expected string")
        if item_type != "Q" and "decision" in item_map:
            errors.append(f"{context}.decision: non-Q items must not declare decision")

        triggers = item_map.get("triggers")
        if triggers is not None and (
            not isinstance(triggers, list) or any(not isinstance(entry, str) for entry in triggers)
        ):
            errors.append(f"{context}.triggers: expected list of strings")

        tools_profile = item_map.get("tools_profile")
        if tools_profile is not None and not isinstance(tools_profile, str):
            errors.append(f"{context}.tools_profile: expected string")

        requires_phase = item_map.get("requires_phase")
        if requires_phase is not None and requires_phase not in {"A", "B", "C", "D"}:
            errors.append(f"{context}.requires_phase: invalid value '{requires_phase}'")

        approval_ref = item_map.get("approval_ref")
        if approval_ref is not None and (not isinstance(approval_ref, str) or not approval_ref):
            errors.append(f"{context}.approval_ref: expected non-empty string")

        shared_assets = item_map.get("shared_assets")
        if shared_assets is not None:
            shared_assets_map = ensure_mapping(shared_assets, f"{context}.shared_assets", errors)
            if shared_assets_map is not None:
                unexpected = sorted(set(shared_assets_map.keys()) - shared_asset_fields)
                if unexpected:
                    errors.append(
                        f"{context}.shared_assets: unexpected field(s): {', '.join(unexpected)}"
                    )
                for field in ("skill", "prompt", "profile", "result_protocol"):
                    value = shared_assets_map.get(field)
                    if value is not None and (
                        not isinstance(value, str)
                        or not re.fullmatch(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$", value)
                    ):
                        errors.append(
                            f"{context}.shared_assets.{field}: invalid asset id '{value}'"
                        )
                context_policy = shared_assets_map.get("context_policy")
                if context_policy is not None and context_policy not in {
                    "focused",
                    "diff_only",
                    "repo_full",
                }:
                    errors.append(
                        f"{context}.shared_assets.context_policy: invalid value '{context_policy}'"
                    )
                resolution_mode = shared_assets_map.get("resolution_mode")
                if resolution_mode is not None and resolution_mode not in {"workspace", "vendored"}:
                    errors.append(
                        f"{context}.shared_assets.resolution_mode: invalid value '{resolution_mode}'"
                    )

    commit_groups = ensure_list(plan.get("commit_groups"), "commit_groups", errors) or []
    for idx, commit_group in enumerate(commit_groups):
        context = f"commit_groups[{idx}]"
        cg_map = ensure_mapping(commit_group, context, errors)
        if cg_map is None:
            continue
        if not isinstance(cg_map.get("id"), str) or not re.fullmatch(r"^cg[0-9]+$", cg_map["id"]):
            errors.append(f"{context}.id: expected commit group id like cg1")
        if not isinstance(cg_map.get("title"), str) or not cg_map.get("title"):
            errors.append(f"{context}.title: expected non-empty string")
        cg_items = cg_map.get("items")
        if not isinstance(cg_items, list) or not cg_items:
            errors.append(f"{context}.items: expected non-empty list")
        elif any(
            not isinstance(item_id, str) or not ITEM_ID_RE.fullmatch(item_id)
            for item_id in cg_items
        ):
            errors.append(f"{context}.items: expected item IDs")

    return errors


def validate_plan_schema(plan: dict, schema: dict) -> tuple[list[str], str]:
    """Validate the plan schema via jsonschema or the built-in subset fallback."""
    if jsonschema is None:
        return validate_plan_schema_subset(plan), "subset"

    try:
        jsonschema.validate(instance=plan, schema=schema)
    except jsonschema.ValidationError as exc:
        return [
            f"path: {'/'.join(str(p) for p in exc.path)}",
            f"message: {exc.message}",
        ], "jsonschema"

    return [], "jsonschema"


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


def unresolved_dependencies(item: dict, id_to_status: dict[str, str]) -> list[str]:
    """Return unresolved dependency IDs for a single executable item."""
    unresolved: list[str] = []
    for dep in item.get("depends_on", []) or []:
        if id_to_status.get(dep, "") not in DEPENDENCY_READY_STATES:
            unresolved.append(dep)
    return unresolved


def compute_ready_items(plan: dict) -> list[dict[str, object]]:
    """Return executable items that are ready to run now.

    The ready-set is intentionally read-only and conservative:
    - executable item types only,
    - current item status must be ``planned`` or ``ready``,
    - every declared dependency must already be ``verified`` or ``done``.
    """
    id_to_status = collect_statuses(plan)
    ready_items: list[dict[str, object]] = []

    for item in sorted(plan.get("items", []) or [], key=lambda entry: entry.get("id", "")):
        item_type = item.get("type", "")
        item_status = item.get("status", "")
        if item_type not in EXECUTABLE_ITEM_TYPES:
            continue
        if item_status not in READY_QUERY_STATUSES:
            continue

        unresolved = unresolved_dependencies(item, id_to_status)
        if unresolved:
            continue

        ready_items.append(
            {
                "id": item.get("id", ""),
                "type": item_type,
                "status": item_status,
                "commit_group": item.get("commit_group", ""),
                "unresolved_dependencies": unresolved,
                "unresolved_dependencies_count": len(unresolved),
            }
        )

    return ready_items


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
    return [f"dependency cycle detected among items: {', '.join(cycle_participants)}"]


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
                errors.append(f"commit_group '{cg_id}' references unknown item '{member}'")

    # Reverse check: every item.commit_group must reference an existing commit_group
    for item_id, cg in item_to_cg.items():
        if cg not in cg_ids:
            errors.append(f"item '{item_id}' references unknown commit_group '{cg}'")

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


def validate_custom_rules(plan: dict, asset_map: dict[str, dict]) -> tuple[list[str], list[str]]:
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
            errors.append(f"milestone id '{mid}' is invalid; expected format X<number> (e.g. X1)")

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
            if (
                left_scope == right_scope
                or left_scope.startswith(right_scope)
                or right_scope.startswith(left_scope)
            ):
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

    # Hard-fail: shared_assets references must resolve through the canonical registry.
    errors.extend(validate_shared_asset_refs(items, asset_map))

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


def check_repo_map_freshness(plan: dict, repo_root: Path) -> list[str]:
    """Hard-fail if REPO_MAP.md is stale when checkpoint items are active."""
    errors: list[str] = []
    items = plan.get("items", []) or []
    active_checkpoints = [
        i for i in items if i.get("type") == "C" and i.get("status") in {"review", "verified"}
    ]
    if not active_checkpoints:
        return errors

    repo_map_path = repo_root / "REPO_MAP.md"
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


def print_split_plan_report(metadata: dict) -> None:
    current_fragment = metadata.get("current_fragment", {})
    archive_details = metadata.get("archives", []) or []

    print("ACTIVE:")
    print(f"  - current_plan: {metadata['current_path']}")
    print(f"  - milestones: {len(current_fragment.get('milestones', []) or [])}")
    print(f"  - sprints: {len(current_fragment.get('sprints', []) or [])}")
    print(f"  - items: {len(current_fragment.get('items', []) or [])}")
    print(f"  - commit_groups: {len(current_fragment.get('commit_groups', []) or [])}")

    print("ARCHIVED:")
    print(f"  - archive_root: {metadata['archive_root']}")
    print(f"  - fragments: {len(archive_details)}")
    print(
        f"  - milestones: {sum(len(detail['fragment'].get('milestones', []) or []) for detail in archive_details)}"
    )
    print(
        f"  - sprints: {sum(len(detail['fragment'].get('sprints', []) or []) for detail in archive_details)}"
    )
    print(
        f"  - items: {sum(len(detail['fragment'].get('items', []) or []) for detail in archive_details)}"
    )
    print(
        "  - commit_groups: "
        f"{sum(len(detail['fragment'].get('commit_groups', []) or []) for detail in archive_details)}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the canonical plan entrypoint")
    parser.add_argument(
        "plan",
        nargs="?",
        default="plan/PLAN-index.yaml",
        help="Path to the canonical split-plan entrypoint (plan/PLAN-index.yaml)",
    )
    parser.add_argument(
        "--schema",
        default="agent-os/schemas/plan.schema.json",
        help="Path to plan schema JSON",
    )
    parser.add_argument(
        "--previous-plan",
        default="",
        help="Optional previous plan entrypoint to enforce lifecycle transition rules",
    )
    parser.add_argument(
        "--check-freshness",
        action="store_true",
        help="Check REPO_MAP.md freshness when checkpoint items are active",
    )
    parser.add_argument(
        "--shared-asset-registry",
        default=str(default_shared_asset_registry_path()),
        help="Path to the shared asset registry YAML",
    )
    parser.add_argument(
        "--compute-ready",
        action="store_true",
        help="Emit deterministic JSON describing the current ready-set",
    )
    args = parser.parse_args()

    plan_path = Path(args.plan)
    schema_path = Path(args.schema)
    registry_path = Path(args.shared_asset_registry)

    if not plan_path.exists():
        print(f"ERROR: Plan file not found: {plan_path}", file=sys.stderr)
        return 2
    if not schema_path.exists():
        print(f"ERROR: Schema file not found: {schema_path}", file=sys.stderr)
        return 2
    if not registry_path.exists():
        print(f"ERROR: Shared asset registry not found: {registry_path}", file=sys.stderr)
        return 2

    lint_errors = lint_yaml_unquoted_hash_all(plan_path)
    if lint_errors:
        for err in lint_errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    try:
        plan, plan_metadata = load_plan(plan_path)
    except PlanLoadError as exc:
        print(f"ERROR: Failed to load plan: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"ERROR: Failed to load plan: {exc}", file=sys.stderr)
        return 2

    try:
        schema = load_schema(schema_path)
    except Exception as exc:
        print(f"ERROR: Failed to load schema JSON: {exc}", file=sys.stderr)
        return 2

    try:
        registry = load_shared_asset_registry(registry_path)
    except Exception as exc:
        print(f"ERROR: Failed to load shared asset registry YAML: {exc}", file=sys.stderr)
        return 2

    schema_errors, schema_validator = validate_plan_schema(plan, schema)
    if schema_errors:
        if schema_validator == "subset":
            print(
                "ERROR: Schema validation failed "
                "(jsonschema unavailable; using built-in subset validator)",
                file=sys.stderr,
            )
            for err in schema_errors:
                print(f"  - {err}", file=sys.stderr)
        else:
            print("ERROR: Schema validation failed", file=sys.stderr)
            for err in schema_errors:
                print(f"  {err}", file=sys.stderr)
        return 1

    if args.previous_plan:
        prev_path = Path(args.previous_plan)
        if not prev_path.exists():
            print(f"ERROR: Previous plan file not found: {prev_path}", file=sys.stderr)
            return 2
        try:
            previous, _ = load_plan(prev_path)
        except PlanLoadError as exc:
            print(f"ERROR: Failed to load previous plan: {exc}", file=sys.stderr)
            return 1
        except Exception as exc:
            print(f"ERROR: Failed to load previous plan: {exc}", file=sys.stderr)
            return 2

        transition_errors = validate_transitions(plan, previous)
        if transition_errors:
            print("ERROR: Lifecycle transition checks failed", file=sys.stderr)
            for err in transition_errors:
                print(f"  - {err}", file=sys.stderr)
            return 1

    asset_map, registry_errors = validate_shared_asset_registry(registry, registry_path)
    errors, warnings = validate_custom_rules(plan, asset_map)
    errors.extend(registry_errors)

    if args.check_freshness:
        repo_root = (
            plan_metadata["index_path"].parent.parent
            if plan_metadata.get("format") == "split"
            else plan_path.parent
        )
        errors.extend(check_repo_map_freshness(plan, repo_root))

    if plan_metadata.get("format") == "split" and not args.compute_ready:
        print_split_plan_report(plan_metadata)

    if args.compute_ready:
        if errors:
            print("ERROR: Governance checks failed", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)
            return 1
        payload = {
            "ready_items": compute_ready_items(plan),
            "warnings": warnings,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

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
