#!/usr/bin/env python3
"""Render PLAN.yaml into PLAN.md and PLAN.dot deterministically."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: pyyaml. Install with: pip install pyyaml") from exc


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Top-level YAML document must be a mapping")
    return data


def sorted_by_id(items: list[dict]) -> list[dict]:
    return sorted(items, key=lambda x: x.get("id", ""))


def render_markdown(plan: dict) -> str:
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
    for obj in sorted_by_id(plan.get("milestones", []) or []):
        lines.append(
            f"| {obj.get('id','')} | {obj.get('type','')} | {obj.get('title','')} | {obj.get('status','')} |"
        )
    lines.append("")

    lines.append("## Sprints")
    lines.append("")
    lines.append("| ID | Parent | Type | Title | Status |")
    lines.append("|---|---|---|---|---|")
    for obj in sorted_by_id(plan.get("sprints", []) or []):
        lines.append(
            f"| {obj.get('id','')} | {obj.get('parent','')} | {obj.get('type','')} | {obj.get('title','')} | {obj.get('status','')} |"
        )
    lines.append("")

    lines.append("## Items")
    lines.append("")
    lines.append("| ID | Parent | Type | Status | Role | Effort | Commit Group | Depends On |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for obj in sorted_by_id(plan.get("items", []) or []):
        deps = ", ".join(obj.get("depends_on", []) or [])
        lines.append(
            f"| {obj.get('id','')} | {obj.get('parent','')} | {obj.get('type','')} | {obj.get('status','')} | {obj.get('role','')} | {obj.get('effort','')} | {obj.get('commit_group','')} | {deps} |"
        )

    lines.append("")
    lines.append("## Commit Groups")
    lines.append("")
    lines.append("| ID | Title | Items |")
    lines.append("|---|---|---|")
    for cg in sorted_by_id(plan.get("commit_groups", []) or []):
        items = ", ".join(cg.get("items", []) or [])
        lines.append(f"| {cg.get('id','')} | {cg.get('title','')} | {items} |")

    lines.append("")
    return "\n".join(lines)


def dot_escape(text: str) -> str:
    return text.replace('"', '\\"')


def render_dot(plan: dict) -> str:
    lines: list[str] = []
    lines.append("digraph PLAN {")
    lines.append("  rankdir=LR;")
    lines.append("  node [shape=box, style=rounded];")

    nodes: list[dict] = []
    nodes.extend(plan.get("milestones", []) or [])
    nodes.extend(plan.get("sprints", []) or [])
    nodes.extend(plan.get("items", []) or [])

    for obj in sorted_by_id(nodes):
        node_id = obj.get("id", "")
        label = f"{node_id} | {obj.get('type','')} | {obj.get('status','')}"
        lines.append(f'  "{dot_escape(node_id)}" [label="{dot_escape(label)}"];')

    # Parent edges
    for obj in sorted_by_id(nodes):
        parent = obj.get("parent")
        if parent:
            lines.append(f'  "{dot_escape(parent)}" -> "{dot_escape(obj.get("id", ""))}" [style=dashed];')

    # Dependency edges
    for item in sorted_by_id(plan.get("items", []) or []):
        item_id = item.get("id", "")
        for dep in sorted(item.get("depends_on", []) or []):
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
