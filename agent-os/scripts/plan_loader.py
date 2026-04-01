#!/usr/bin/env python3
"""Shared loader and normalizer for legacy and split plan layouts."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: pyyaml. Install tooling deps with: "
        "python3 -m pip install -r requirements.txt"
    ) from exc


AGGREGATE_PLAN_KEYS = ("meta", "mission", "milestones", "sprints", "items", "commit_groups")
FRAGMENT_KEYS = ("milestones", "sprints", "items", "commit_groups")
INDEX_KEYS = ("meta", "mission", "current_plan", "archive_root", "archives")

MILESTONE_ID_RE = re.compile(r"^X([1-9][0-9]*)$")
SPRINT_ID_RE = re.compile(r"^S([1-9][0-9]*)\.([1-9][0-9]*)$")
ITEM_ID_RE = re.compile(r"^([A-Z]+)([1-9][0-9]*)\.([1-9][0-9]*)\.([1-9][0-9]*)([a-z]?)$")
COMMIT_GROUP_ID_RE = re.compile(r"^cg([0-9]+)$")


class PlanLoadError(ValueError):
    """Raised when a plan file or split-plan layout is invalid."""


def load_yaml_mapping(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise PlanLoadError(f"{path}: top-level YAML document must be a mapping")
    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def is_aggregate_plan(data: dict[str, Any]) -> bool:
    return all(key in data for key in AGGREGATE_PLAN_KEYS)


def is_plan_index(data: dict[str, Any]) -> bool:
    return all(key in data for key in INDEX_KEYS)


def _ensure_list_of_mappings(value: Any, field: str, path: Path) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise PlanLoadError(f"{path}: '{field}' must be a list")
    result: list[dict[str, Any]] = []
    for idx, entry in enumerate(value):
        if not isinstance(entry, dict):
            raise PlanLoadError(f"{path}: '{field}[{idx}]' must be a mapping")
        result.append(entry)
    return result


def _milestone_sort_key(obj: dict[str, Any]) -> tuple[int]:
    milestone_id = str(obj.get("id", ""))
    match = MILESTONE_ID_RE.fullmatch(milestone_id)
    if not match:
        raise PlanLoadError(f"Invalid milestone ID: {milestone_id}")
    return (int(match.group(1)),)


def _sprint_sort_key(obj: dict[str, Any]) -> tuple[int, int]:
    sprint_id = str(obj.get("id", ""))
    match = SPRINT_ID_RE.fullmatch(sprint_id)
    if not match:
        raise PlanLoadError(f"Invalid sprint ID: {sprint_id}")
    return (int(match.group(1)), int(match.group(2)))


def _item_sort_key(obj: dict[str, Any]) -> tuple[int, int, int, str, str]:
    item_id = str(obj.get("id", ""))
    match = ITEM_ID_RE.fullmatch(item_id)
    if not match:
        raise PlanLoadError(f"Invalid item ID: {item_id}")
    suffix = match.group(5) or ""
    return (
        int(match.group(2)),
        int(match.group(3)),
        int(match.group(4)),
        suffix,
        match.group(1),
    )


def _commit_group_sort_key(obj: dict[str, Any]) -> tuple[int]:
    commit_group_id = str(obj.get("id", ""))
    match = COMMIT_GROUP_ID_RE.fullmatch(commit_group_id)
    if not match:
        raise PlanLoadError(f"Invalid commit group ID: {commit_group_id}")
    return (int(match.group(1)),)


def sort_fragment(fragment: dict[str, Any]) -> dict[str, Any]:
    return {
        "milestones": [dict(obj) for obj in sorted(fragment.get("milestones", []) or [], key=_milestone_sort_key)],
        "sprints": [dict(obj) for obj in sorted(fragment.get("sprints", []) or [], key=_sprint_sort_key)],
        "items": [dict(obj) for obj in sorted(fragment.get("items", []) or [], key=_item_sort_key)],
        "commit_groups": [
            dict(obj) for obj in sorted(fragment.get("commit_groups", []) or [], key=_commit_group_sort_key)
        ],
    }


def sort_aggregate_plan(plan: dict[str, Any]) -> dict[str, Any]:
    normalized = {
        "meta": dict(plan.get("meta", {})),
        "mission": str(plan.get("mission", "")),
    }
    normalized.update(sort_fragment(plan))
    return normalized


def compute_fragment_digest(fragment: dict[str, Any]) -> str:
    normalized = sort_fragment(fragment)
    payload = json.dumps(normalized, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]
    return f"sha256:{digest}"


def _resolve_relative_path(base_dir: Path, relative_path: Any, label: str) -> Path:
    if not isinstance(relative_path, str) or not relative_path:
        raise PlanLoadError(f"{base_dir}: '{label}' must be a non-empty relative path")
    rel_path = Path(relative_path)
    if rel_path.is_absolute():
        raise PlanLoadError(f"{base_dir}: '{label}' must be relative, got '{relative_path}'")
    return (base_dir / rel_path).resolve()


def _validate_fragment_structure(
    fragment: dict[str, Any],
    *,
    path: Path,
    kind: str,
    expected_milestone: str | None = None,
) -> list[str]:
    errors: list[str] = []

    milestones = _ensure_list_of_mappings(fragment.get("milestones"), "milestones", path)
    sprints = _ensure_list_of_mappings(fragment.get("sprints"), "sprints", path)
    items = _ensure_list_of_mappings(fragment.get("items"), "items", path)
    commit_groups = _ensure_list_of_mappings(fragment.get("commit_groups"), "commit_groups", path)

    milestone_ids = [str(obj.get("id", "")) for obj in milestones]
    milestone_set = set(milestone_ids)

    if kind == "archive":
        if len(milestones) != 1:
            errors.append(f"{path}: archive fragment must contain exactly one milestone")
        if expected_milestone and milestone_ids != [expected_milestone]:
            errors.append(
                f"{path}: archive fragment milestone mismatch (expected {expected_milestone}, got {milestone_ids})"
            )
        if milestones and str(milestones[0].get("status", "")) != "done":
            errors.append(f"{path}: archived milestone must have status 'done'")
    elif kind == "current":
        done_milestones = [mid for mid, obj in zip(milestone_ids, milestones) if obj.get("status") == "done"]
        if done_milestones:
            errors.append(f"{path}: current fragment must not contain done milestones: {done_milestones}")

    sprint_ids: set[str] = set()
    for sprint in sprints:
        sprint_id = str(sprint.get("id", ""))
        sprint_ids.add(sprint_id)
        if str(sprint.get("parent", "")) not in milestone_set:
            errors.append(f"{path}: sprint '{sprint_id}' has parent outside its fragment")

    item_ids: set[str] = set()
    for item in items:
        item_id = str(item.get("id", ""))
        item_ids.add(item_id)
        if str(item.get("parent", "")) not in sprint_ids:
            errors.append(f"{path}: item '{item_id}' has parent sprint outside its fragment")

    for commit_group in commit_groups:
        commit_group_id = str(commit_group.get("id", ""))
        members = commit_group.get("items")
        if not isinstance(members, list) or not members:
            errors.append(f"{path}: commit group '{commit_group_id}' must declare a non-empty items list")
            continue
        invalid_members = [str(item_id) for item_id in members if str(item_id) not in item_ids]
        if invalid_members:
            errors.append(
                f"{path}: commit group '{commit_group_id}' references items outside its fragment: {invalid_members}"
            )

    return errors


def _detect_duplicate_ids(objects: list[dict[str, Any]], field: str, label: str) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for obj in objects:
        obj_id = str(obj.get(field, ""))
        if obj_id in seen:
            duplicates.append(obj_id)
        else:
            seen.add(obj_id)
    return [f"duplicate {label} id '{obj_id}'" for obj_id in duplicates]


def load_fragment(path: Path, *, kind: str, expected_milestone: str | None = None) -> dict[str, Any]:
    fragment = load_yaml_mapping(path)
    if any(key not in fragment for key in FRAGMENT_KEYS):
        missing = [key for key in FRAGMENT_KEYS if key not in fragment]
        raise PlanLoadError(f"{path}: fragment is missing required keys {missing}")
    errors = _validate_fragment_structure(
        fragment,
        path=path,
        kind=kind,
        expected_milestone=expected_milestone,
    )
    if errors:
        raise PlanLoadError("\n".join(errors))
    return sort_fragment(fragment)


def load_split_plan(index_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    index = load_yaml_mapping(index_path)
    if not is_plan_index(index):
        raise PlanLoadError(f"{index_path}: not a split plan index")

    base_dir = index_path.parent.resolve()
    current_path = _resolve_relative_path(base_dir, index.get("current_plan"), "current_plan")
    archive_root = _resolve_relative_path(base_dir, index.get("archive_root"), "archive_root")

    meta = index.get("meta")
    mission = index.get("mission")
    archives = index.get("archives")
    if not isinstance(meta, dict):
        raise PlanLoadError(f"{index_path}: 'meta' must be a mapping")
    if not isinstance(mission, str) or not mission:
        raise PlanLoadError(f"{index_path}: 'mission' must be a non-empty string")
    if not isinstance(archives, list):
        raise PlanLoadError(f"{index_path}: 'archives' must be a list")

    current_fragment = load_fragment(current_path, kind="current")
    archive_details: list[dict[str, Any]] = []
    seen_milestones = {str(obj.get("id", "")) for obj in current_fragment.get("milestones", [])}
    seen_paths = {current_path.resolve()}
    errors: list[str] = []

    for idx, entry in enumerate(archives):
        if not isinstance(entry, dict):
            errors.append(f"{index_path}: archives[{idx}] must be a mapping")
            continue
        milestone_id = entry.get("milestone")
        title = entry.get("title")
        digest = entry.get("digest")
        if not isinstance(milestone_id, str) or not milestone_id:
            errors.append(f"{index_path}: archives[{idx}].milestone must be a non-empty string")
            continue
        if not isinstance(title, str) or not title:
            errors.append(f"{index_path}: archives[{idx}].title must be a non-empty string")
            continue
        if not isinstance(digest, str) or not digest:
            errors.append(f"{index_path}: archives[{idx}].digest must be a non-empty string")
            continue

        archive_path = _resolve_relative_path(base_dir, entry.get("path"), f"archives[{idx}].path")
        if archive_path in seen_paths:
            errors.append(f"{index_path}: duplicate split-plan fragment path '{archive_path}'")
            continue
        seen_paths.add(archive_path)
        if not archive_path.is_relative_to(archive_root):
            errors.append(f"{index_path}: archive fragment '{archive_path}' must live under '{archive_root}'")
            continue
        if milestone_id in seen_milestones:
            errors.append(f"{index_path}: duplicate archived milestone '{milestone_id}'")
            continue
        seen_milestones.add(milestone_id)

        try:
            fragment = load_fragment(archive_path, kind="archive", expected_milestone=milestone_id)
        except PlanLoadError as exc:
            errors.append(str(exc))
            continue

        fragment_milestone = fragment["milestones"][0]
        if str(fragment_milestone.get("title", "")) != title:
            errors.append(
                f"{index_path}: archive title mismatch for {milestone_id} "
                f"(index='{title}', fragment='{fragment_milestone.get('title', '')}')"
            )

        actual_digest = compute_fragment_digest(fragment)
        if actual_digest != digest:
            errors.append(
                f"{index_path}: archive digest mismatch for {milestone_id} "
                f"(index='{digest}', fragment='{actual_digest}')"
            )

        archive_details.append(
            {
                "entry": dict(entry),
                "path": archive_path,
                "fragment": fragment,
            }
        )

    if errors:
        raise PlanLoadError("\n".join(errors))

    aggregate = {
        "meta": dict(meta),
        "mission": mission,
        "milestones": list(current_fragment["milestones"]),
        "sprints": list(current_fragment["sprints"]),
        "items": list(current_fragment["items"]),
        "commit_groups": list(current_fragment["commit_groups"]),
    }

    for detail in archive_details:
        fragment = detail["fragment"]
        aggregate["milestones"].extend(fragment["milestones"])
        aggregate["sprints"].extend(fragment["sprints"])
        aggregate["items"].extend(fragment["items"])
        aggregate["commit_groups"].extend(fragment["commit_groups"])

    aggregate = sort_aggregate_plan(aggregate)

    duplicate_errors: list[str] = []
    duplicate_errors.extend(_detect_duplicate_ids(aggregate["milestones"], "id", "milestone"))
    duplicate_errors.extend(_detect_duplicate_ids(aggregate["sprints"], "id", "sprint"))
    duplicate_errors.extend(_detect_duplicate_ids(aggregate["items"], "id", "item"))
    duplicate_errors.extend(_detect_duplicate_ids(aggregate["commit_groups"], "id", "commit group"))
    if duplicate_errors:
        raise PlanLoadError("\n".join(duplicate_errors))

    metadata = {
        "format": "split",
        "index_path": index_path.resolve(),
        "current_path": current_path,
        "current_fragment": current_fragment,
        "archive_root": archive_root,
        "archives": archive_details,
    }
    return aggregate, metadata


def load_plan(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    raw = load_yaml_mapping(path)
    if is_plan_index(raw):
        return load_split_plan(path)
    if not is_aggregate_plan(raw):
        raise PlanLoadError(f"{path}: unsupported plan format")
    return sort_aggregate_plan(raw), {"format": "legacy", "source_path": path.resolve()}


def extract_fragment(plan: dict[str, Any], milestone_ids: set[str]) -> dict[str, Any]:
    sorted_plan = sort_aggregate_plan(plan)
    milestones = [obj for obj in sorted_plan["milestones"] if str(obj.get("id", "")) in milestone_ids]
    sprint_ids = {
        str(obj.get("id", ""))
        for obj in sorted_plan["sprints"]
        if str(obj.get("parent", "")) in milestone_ids
    }
    sprints = [obj for obj in sorted_plan["sprints"] if str(obj.get("id", "")) in sprint_ids]
    item_ids = {
        str(obj.get("id", ""))
        for obj in sorted_plan["items"]
        if str(obj.get("parent", "")) in sprint_ids
    }
    items = [obj for obj in sorted_plan["items"] if str(obj.get("id", "")) in item_ids]

    commit_groups: list[dict[str, Any]] = []
    for commit_group in sorted_plan["commit_groups"]:
        members = [str(item_id) for item_id in commit_group.get("items", []) or []]
        matching = [item_id for item_id in members if item_id in item_ids]
        if not matching:
            continue
        if len(matching) != len(members):
            raise PlanLoadError(
                f"commit group '{commit_group.get('id', '')}' spans multiple milestone fragments"
            )
        commit_groups.append(commit_group)

    return sort_fragment(
        {
            "milestones": milestones,
            "sprints": sprints,
            "items": items,
            "commit_groups": commit_groups,
        }
    )


def build_split_layout(
    plan: dict[str, Any],
    *,
    current_plan_name: str = "PLAN-current.yaml",
    archive_root_name: str = "archive",
) -> tuple[dict[str, Any], dict[str, Any], dict[str, dict[str, Any]]]:
    sorted_plan = sort_aggregate_plan(plan)
    active_milestone_ids = {
        str(obj.get("id", ""))
        for obj in sorted_plan["milestones"]
        if str(obj.get("status", "")) != "done"
    }
    archived_milestones = [
        obj for obj in sorted_plan["milestones"] if str(obj.get("status", "")) == "done"
    ]

    current_fragment = extract_fragment(sorted_plan, active_milestone_ids)
    archive_fragments: dict[str, dict[str, Any]] = {}
    archives_index: list[dict[str, str]] = []

    for milestone in archived_milestones:
        milestone_id = str(milestone.get("id", ""))
        rel_path = Path(archive_root_name) / f"PLAN-{milestone_id}.yaml"
        fragment = extract_fragment(sorted_plan, {milestone_id})
        archive_fragments[rel_path.as_posix()] = fragment
        archives_index.append(
            {
                "milestone": milestone_id,
                "title": str(milestone.get("title", "")),
                "path": rel_path.as_posix(),
                "digest": compute_fragment_digest(fragment),
            }
        )

    index = {
        "meta": dict(sorted_plan["meta"]),
        "mission": sorted_plan["mission"],
        "current_plan": current_plan_name,
        "archive_root": archive_root_name,
        "archives": sorted(
            archives_index,
            key=lambda entry: _milestone_sort_key({"id": entry["milestone"]}),
        ),
    }
    return index, current_fragment, archive_fragments
