#!/usr/bin/env python3
"""Render deterministic archive digest summaries from the split plan index."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Any

from plan_loader import PlanLoadError, generated_source_label, load_split_plan


def markdown_escape(value: Any) -> str:
    text = " ".join(str(value or "").strip().split())
    return text.replace("\\", "\\\\").replace("|", "\\|")


def code_list(values: list[str]) -> str:
    if not values:
        return "(none)"
    return ", ".join(f"`{markdown_escape(value)}`" for value in values)


def summarize_item_types(items: list[dict[str, Any]]) -> str:
    counts = Counter(str(item.get("type", "")) for item in items if item.get("type"))
    if not counts:
        return "(none)"
    return ", ".join(f"{kind}:{counts[kind]}" for kind in sorted(counts))


def summarize_scopes(items: list[dict[str, Any]]) -> str:
    scopes = sorted({str(item.get("scope", "")) for item in items if item.get("scope")})
    return code_list(scopes)


def render_archive_digest(
    metadata: dict[str, Any], source_label: str = "plan/PLAN-index.yaml"
) -> str:
    archive_details = list(metadata.get("archives", []) or [])

    lines: list[str] = []
    lines.append("# Archive Digest")
    lines.append("")
    lines.append(f"AUTO-GENERATED from {source_label}. Do not edit manually.")
    lines.append("")
    lines.append(
        "This digest is a non-authoritative lookup aid. "
        "Canonical history remains in `plan/PLAN-index.yaml` and the indexed archive fragments."
    )
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Archived milestones: {len(archive_details)}")
    lines.append(
        f"- Archived items: {sum(len(detail['fragment'].get('items', []) or []) for detail in archive_details)}"
    )
    lines.append(
        "- Archived commit groups: "
        f"{sum(len(detail['fragment'].get('commit_groups', []) or []) for detail in archive_details)}"
    )
    lines.append("")
    lines.append("## Milestones")
    lines.append("")

    if not archive_details:
        lines.append("No archived milestones.")
        lines.append("")
        return "\n".join(lines)

    lines.append(
        "| Milestone | Title | Archive | Digest | Sprints | Items | Commit groups | Item types | Scope prefixes |"
    )
    lines.append("|---|---|---|---|---:|---:|---:|---|---|")

    for detail in archive_details:
        entry = detail["entry"]
        fragment = detail["fragment"]
        sprints = fragment.get("sprints", []) or []
        items = fragment.get("items", []) or []
        commit_groups = fragment.get("commit_groups", []) or []
        lines.append(
            "| "
            f"`{markdown_escape(entry.get('milestone', ''))}` | "
            f"{markdown_escape(entry.get('title', ''))} | "
            f"`{markdown_escape(entry.get('path', ''))}` | "
            f"`{markdown_escape(entry.get('digest', ''))}` | "
            f"{len(sprints)} | "
            f"{len(items)} | "
            f"{len(commit_groups)} | "
            f"{markdown_escape(summarize_item_types(items))} | "
            f"{summarize_scopes(items)} |"
        )

    lines.append("")
    return "\n".join(lines)


def default_digest_path(metadata: dict[str, Any]) -> Path:
    return Path(metadata["archive_root"]) / "DIGEST.md"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render archive digest summaries from the canonical split-plan entrypoint"
    )
    parser.add_argument(
        "plan",
        nargs="?",
        default="plan/PLAN-index.yaml",
        help="Path to the canonical split-plan entrypoint",
    )
    parser.add_argument(
        "--output",
        help="Output markdown path; defaults to <archive_root>/DIGEST.md",
    )
    args = parser.parse_args()

    plan_path = Path(args.plan)
    if not plan_path.exists():
        print(f"ERROR: Plan file not found: {plan_path}")
        return 2

    try:
        _plan, metadata = load_split_plan(plan_path)
        digest_text = render_archive_digest(metadata, source_label=generated_source_label(plan_path))
        output_path = Path(args.output) if args.output else default_digest_path(metadata)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(digest_text, encoding="utf-8")
        print(f"OK: wrote {output_path}")
    except PlanLoadError as exc:
        print(f"ERROR: Failed to load plan: {exc}")
        return 1
    except Exception as exc:
        print(f"ERROR: Failed to render archive digest: {exc}")
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
