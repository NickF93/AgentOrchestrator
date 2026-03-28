#!/usr/bin/env python3
"""Render PLAN.yaml into PLAN.md and PLAN.dot deterministically."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: pyyaml. Install tooling deps with: "
        "python3 -m pip install -r requirements.txt"
    ) from exc


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Top-level YAML document must be a mapping")
    return data


def source_order(items: list[dict] | None) -> list[dict]:
    return list(items or [])


def normalize_text(value: str) -> str:
    return " ".join((value or "").strip().split())


def markdown_inline_list(values: list[str]) -> str:
    return ", ".join(f"`{value}`" for value in values)


def format_shared_assets(item: dict) -> str:
    shared_assets = item.get("shared_assets")
    if not isinstance(shared_assets, dict) or not shared_assets:
        return ""

    item_type = item.get("type", "")
    context_policy = shared_assets.get("context_policy")
    if not context_policy and item_type in {"T", "C"}:
        context_policy = "focused"
    resolution_mode = shared_assets.get("resolution_mode") or "workspace"

    ordered_fields = [
        ("skill", shared_assets.get("skill")),
        ("prompt", shared_assets.get("prompt")),
        ("profile", shared_assets.get("profile")),
        ("result_protocol", shared_assets.get("result_protocol")),
        ("context_policy", context_policy),
        ("resolution_mode", resolution_mode),
    ]
    present = [f"{name}={value}" for name, value in ordered_fields if value]
    return ", ".join(present)


def render_markdown(plan: dict) -> str:
    milestones = source_order(plan.get("milestones"))
    sprints = source_order(plan.get("sprints"))
    items = source_order(plan.get("items"))
    commit_groups = source_order(plan.get("commit_groups"))

    sprints_by_milestone: dict[str, list[dict]] = {}
    for sprint in sprints:
        sprints_by_milestone.setdefault(sprint.get("parent", ""), []).append(sprint)

    items_by_sprint: dict[str, list[dict]] = {}
    for item in items:
        items_by_sprint.setdefault(item.get("parent", ""), []).append(item)

    lines: list[str] = []
    lines.append("# PLAN.md")
    lines.append("")
    lines.append("AUTO-GENERATED from PLAN.yaml. Do not edit manually.")
    lines.append("")
    lines.append(f"- Repository: {plan.get('meta', {}).get('repo', '')}")
    lines.append(f"- Owner: {plan.get('meta', {}).get('owner', '')}")
    lines.append(f"- Version: {plan.get('meta', {}).get('version', '')}")
    lines.append(f"- Last updated: {plan.get('meta', {}).get('last_updated', '')}")
    lines.append("")
    lines.append("## Mission")
    lines.append("")
    lines.append((plan.get("mission") or "").strip())
    lines.append("")

    lines.append("## Milestones")
    lines.append("")
    lines.append("| ID | Type | Title | Status |")
    lines.append("|---|---|---|---|")
    for obj in milestones:
        lines.append(
            f"| {obj.get('id','')} | {obj.get('type','')} | {obj.get('title','')} | {obj.get('status','')} |"
        )
    lines.append("")

    lines.append("## Plan")
    lines.append("")
    for milestone in milestones:
        milestone_id = milestone.get("id", "")
        lines.append(f"### {milestone_id}")
        lines.append("")
        lines.append(f"- ID: `{milestone_id}`")
        lines.append(f"- Title: {milestone.get('title', '')}")
        lines.append(f"- Status: {milestone.get('status', '')}")
        milestone_note = normalize_text(milestone.get("note", ""))
        if milestone_note:
            lines.append(f"- Note: {milestone_note}")
        lines.append("")

        milestone_sprints = sprints_by_milestone.get(milestone_id, [])
        if not milestone_sprints:
            continue

        for sprint in milestone_sprints:
            sprint_id = sprint.get("id", "")
            sprint_items = items_by_sprint.get(sprint_id, [])
            lines.append(f"#### {sprint_id} Items")
            lines.append("")
            lines.append(f"Sprint: {sprint.get('title', '')}")
            lines.append(f"Status: {sprint.get('status', '')}")
            lines.append("")
            lines.append("| ID | Type | Description | Status | Notes |")
            lines.append("| --- | --- | --- | --- | --- |")
            for item in sprint_items:
                notes = normalize_text(item.get("notes", ""))
                lines.append(
                    f"| `{item.get('id', '')}` | `{item.get('type', '')}` | {item.get('title', '')} | {item.get('status', '')} | {notes} |"
                )
            lines.append("")

    lines.append("## Commit Groups")
    lines.append("")
    lines.append("| ID | Title | Items |")
    lines.append("|---|---|---|")
    for cg in commit_groups:
        cg_items = markdown_inline_list(cg.get("items", []) or [])
        lines.append(f"| {cg.get('id','')} | {cg.get('title','')} | {cg_items} |")

    lines.append("")
    lines.append("## Item Details")
    lines.append("")
    for obj in items:
        item_id = obj.get("id", "")
        title = obj.get("title", "")
        lines.append(f"### {item_id}: {title}")
        lines.append("")
        lines.append(f"- **Type**: {obj.get('type', '')} | **Status**: {obj.get('status', '')} | **Role**: {obj.get('role', '')} | **Effort**: {obj.get('effort', '')}")
        parent = obj.get("parent", "")
        if parent:
            lines.append(f"- **Sprint**: `{parent}`")
        actions = obj.get("actions", []) or []
        if actions:
            lines.append(f"- **Actions**: {', '.join(actions)}")
        deps = obj.get("depends_on", []) or []
        if deps:
            lines.append(f"- **Depends on**: {markdown_inline_list(deps)}")
        commit_group = obj.get("commit_group", "")
        if commit_group:
            lines.append(f"- **Commit group**: `{commit_group}`")
        shared_assets = format_shared_assets(obj)
        if shared_assets:
            lines.append(f"- **Shared assets**: {shared_assets}")
        artifacts = obj.get("artifacts_out", []) or []
        if artifacts:
            lines.append(f"- **Artifacts**: {', '.join(artifacts)}")
        decision = normalize_text(obj.get("decision", ""))
        if decision:
            lines.append(f"- **Decision**: {decision}")
        checks = obj.get("checks", []) or []
        if checks:
            lines.append("- **Checks**:")
            for check in checks:
                lines.append(f"  - {check}")
        notes = normalize_text(obj.get("notes", ""))
        if notes:
            lines.append(f"- **Notes**: {notes}")
        lines.append("")

    return "\n".join(lines)


STATUS_COLORS: dict[str, str] = {
    "planned": "lightgray",
    "ready": "lightyellow",
    "in_progress": "lightblue",
    "blocked": "salmon",
    "review": "orange",
    "verified": "lightgreen",
    "done": "darkseagreen1",
}

TYPE_SHAPES: dict[str, str] = {
    "X": "box3d",
    "S": "tab",
    "Q": "diamond",
    "D": "note",
    "M": "box",
    "F": "octagon",
    "T": "ellipse",
    "C": "doubleoctagon",
}


def dot_escape(text: str) -> str:
    return text.replace('"', '\\"')


def node_dot(obj: dict) -> str:
    node_id = obj.get("id", "")
    obj_type = obj.get("type", "")
    obj_status = obj.get("status", "")
    label = f"{node_id} | {obj_type} | {obj_status}"
    shape = TYPE_SHAPES.get(obj_type, "box")
    color = STATUS_COLORS.get(obj_status, "white")
    return f'  "{dot_escape(node_id)}" [label="{dot_escape(label)}", shape={shape}, style="filled,rounded", fillcolor={color}];'


def render_dot(plan: dict) -> str:
    lines: list[str] = []
    lines.append("digraph PLAN {")
    lines.append("  rankdir=LR;")
    lines.append("  node [shape=box, style=\"filled,rounded\", fillcolor=white];")

    nodes: list[dict] = []
    nodes.extend(source_order(plan.get("milestones")))
    nodes.extend(source_order(plan.get("sprints")))
    nodes.extend(source_order(plan.get("items")))

    milestones = source_order(plan.get("milestones"))
    sprints = source_order(plan.get("sprints"))
    items = source_order(plan.get("items"))

    # Milestones and sprints are always rendered as top-level nodes.
    for obj in milestones:
        lines.append(node_dot(obj))
    for obj in sprints:
        lines.append(node_dot(obj))

    # Render items clustered by commit_group when available.
    item_by_id = {item.get("id", ""): item for item in items}
    rendered_item_ids: set[str] = set()
    for cg in source_order(plan.get("commit_groups")):
        cg_id = cg.get("id", "")
        cg_items = [item_by_id[i] for i in cg.get("items", []) or [] if i in item_by_id]
        if not cg_items:
            continue
        lines.append(f'  subgraph "cluster_{dot_escape(cg_id)}" {{')
        lines.append('    style="rounded,dashed";')
        lines.append(f'    label="{dot_escape(cg_id)}: {dot_escape(cg.get("title", ""))}";')
        for item in cg_items:
            lines.append("  " + node_dot(item).strip())
            rendered_item_ids.add(item.get("id", ""))
        lines.append("  }")

    # Render items that are not listed in commit_groups.
    for item in items:
        item_id = item.get("id", "")
        if item_id in rendered_item_ids:
            continue
        lines.append(node_dot(item))

    # Parent edges
    for obj in nodes:
        parent = obj.get("parent")
        if parent:
            lines.append(f'  "{dot_escape(parent)}" -> "{dot_escape(obj.get("id", ""))}" [style=dashed];')

    # Dependency edges
    for item in items:
        item_id = item.get("id", "")
        for dep in item.get("depends_on", []) or []:
            lines.append(f'  "{dot_escape(dep)}" -> "{dot_escape(item_id)}";')

    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render PLAN.yaml to PLAN.md and PLAN.dot")
    parser.add_argument("plan", nargs="?", default="PLAN.yaml", help="Path to PLAN.yaml")
    parser.add_argument("--md", default="PLAN.md", help="Output markdown path")
    parser.add_argument("--dot", default="PLAN.dot", help="Output dot path")
    args = parser.parse_args()

    plan_path = Path(args.plan)
    if not plan_path.exists():
        print(f"ERROR: Plan file not found: {plan_path}")
        return 2

    try:
        plan = load_yaml(plan_path)
    except Exception as exc:
        print(f"ERROR: Failed to read YAML: {exc}")
        return 2

    md_text = render_markdown(plan)
    dot_text = render_dot(plan)

    Path(args.md).write_text(md_text, encoding="utf-8")
    Path(args.dot).write_text(dot_text, encoding="utf-8")

    print(f"OK: wrote {args.md}")
    print(f"OK: wrote {args.dot}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
