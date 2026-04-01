from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from conftest import run_python_script


def load_module(module_name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    spec.loader.exec_module(module)
    return module


def normalize_generated_markdown(text: str) -> str:
    return re.sub(
        r"^AUTO-GENERATED from .+\. Do not edit manually\.$",
        "AUTO-GENERATED from <source>. Do not edit manually.",
        text,
        count=1,
        flags=re.MULTILINE,
    )


def test_split_plan_preserves_aggregate_content_and_outputs(
    repo_root: Path, tmp_path: Path
) -> None:
    render_module = load_module(
        "render_plan", repo_root / "agent-os" / "scripts" / "render-plan.py"
    )
    legacy_plan = {
        "meta": {
            "repo": "fixture",
            "owner": "tester",
            "version": "1",
            "schema_version": "1",
            "last_updated": "2026-04-02",
        },
        "mission": "Fixture mission",
        "milestones": [
            {"id": "X1", "type": "X", "title": "Archived milestone", "status": "done"},
            {"id": "X2", "type": "X", "title": "Active milestone", "status": "in_progress"},
        ],
        "sprints": [
            {
                "id": "S1.1",
                "type": "S",
                "parent": "X1",
                "title": "Archived sprint",
                "status": "done",
            },
            {
                "id": "S2.1",
                "type": "S",
                "parent": "X2",
                "title": "Active sprint",
                "status": "in_progress",
            },
        ],
        "items": [
            {
                "id": "D1.1.1",
                "parent": "S1.1",
                "type": "D",
                "title": "Archived item",
                "actions": ["document"],
                "status": "done",
                "role": "documenter",
                "effort": "low",
                "commit_group": "cg1",
                "scope": ".",
            },
            {
                "id": "M2.1.1",
                "parent": "S2.1",
                "type": "M",
                "title": "Active item",
                "actions": ["implement"],
                "status": "in_progress",
                "role": "implementer",
                "effort": "medium",
                "commit_group": "cg2",
                "scope": ".",
            },
        ],
        "commit_groups": [
            {"id": "cg1", "title": "Archived work", "items": ["D1.1.1"]},
            {"id": "cg2", "title": "Active work", "items": ["M2.1.1"]},
        ],
    }

    legacy_path = tmp_path / "PLAN.yaml"
    legacy_path.write_text(yaml.safe_dump(legacy_plan, sort_keys=False), encoding="utf-8")
    index_path = tmp_path / "plan" / "PLAN-index.yaml"
    md_path = tmp_path / "PLAN.md"
    dot_path = tmp_path / "PLAN.dot"

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "split-plan.py",
        str(legacy_path),
        "--index",
        str(index_path),
        "--md",
        str(md_path),
        "--dot",
        str(dot_path),
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert index_path.exists()
    assert (tmp_path / "plan" / "PLAN-current.yaml").exists()
    assert (tmp_path / "plan" / "archive" / "PLAN-X1.yaml").exists()
    assert md_path.exists()
    assert dot_path.exists()

    loader = load_module("plan_loader", repo_root / "agent-os" / "scripts" / "plan_loader.py")
    aggregate, metadata = loader.load_split_plan(index_path)

    assert metadata["format"] == "split"
    assert aggregate == loader.sort_aggregate_plan(legacy_plan)
    expected_md = render_module.render_markdown(loader.sort_aggregate_plan(legacy_plan))
    expected_dot = render_module.render_dot(loader.sort_aggregate_plan(legacy_plan))
    assert normalize_generated_markdown(
        md_path.read_text(encoding="utf-8")
    ) == normalize_generated_markdown(expected_md)
    assert dot_path.read_text(encoding="utf-8") == expected_dot
    assert "### X1" in md_path.read_text(encoding="utf-8")
    assert '"cluster_cg1"' in dot_path.read_text(encoding="utf-8")


def test_split_plan_can_remove_legacy_source(repo_root: Path, tmp_path: Path) -> None:
    legacy_plan = {
        "meta": {
            "repo": "fixture",
            "owner": "tester",
            "version": "1",
            "schema_version": "1",
            "last_updated": "2026-04-02",
        },
        "mission": "Fixture mission",
        "milestones": [{"id": "X1", "type": "X", "title": "Only milestone", "status": "done"}],
        "sprints": [
            {"id": "S1.1", "type": "S", "parent": "X1", "title": "Only sprint", "status": "done"}
        ],
        "items": [
            {
                "id": "D1.1.1",
                "parent": "S1.1",
                "type": "D",
                "title": "Only item",
                "actions": ["document"],
                "status": "done",
                "role": "documenter",
                "effort": "low",
                "commit_group": "cg1",
                "scope": ".",
            }
        ],
        "commit_groups": [{"id": "cg1", "title": "Only work", "items": ["D1.1.1"]}],
    }

    legacy_path = tmp_path / "PLAN.yaml"
    legacy_path.write_text(yaml.safe_dump(legacy_plan, sort_keys=False), encoding="utf-8")

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "split-plan.py",
        str(legacy_path),
        "--index",
        str(tmp_path / "plan" / "PLAN-index.yaml"),
        "--remove-source",
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert not legacy_path.exists()
