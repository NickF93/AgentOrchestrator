from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from typing import Any

from conftest import copy_split_plan, run_python_script, write_yaml


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


def test_render_plan_generates_outputs(repo_root: Path, tmp_path: Path) -> None:
    index_path = copy_split_plan(tmp_path)
    loader = load_module("plan_loader", repo_root / "agent-os" / "scripts" / "plan_loader.py")
    render_module = load_module(
        "render_plan", repo_root / "agent-os" / "scripts" / "render-plan.py"
    )
    aggregate_plan, _ = loader.load_plan(index_path)

    split_md = tmp_path / "PLAN-split.md"
    split_dot = tmp_path / "PLAN-split.dot"
    split_result = run_python_script(
        repo_root / "agent-os" / "scripts" / "render-plan.py",
        str(index_path),
        "--md",
        str(split_md),
        "--dot",
        str(split_dot),
    )

    assert split_result.returncode == 0, split_result.stdout + split_result.stderr
    assert split_md.exists()
    assert split_dot.exists()
    expected_md = render_module.render_markdown(aggregate_plan, source_label=str(index_path))
    expected_dot = render_module.render_dot(aggregate_plan)
    assert normalize_generated_markdown(
        split_md.read_text(encoding="utf-8")
    ) == normalize_generated_markdown(expected_md)
    assert split_dot.read_text(encoding="utf-8") == expected_dot
    assert "Shared assets" in split_md.read_text(encoding="utf-8")
    assert "cluster_cg27" in split_dot.read_text(encoding="utf-8")


def test_render_plan_rejects_legacy_aggregate_input(repo_root: Path, tmp_path: Path) -> None:
    legacy_path = tmp_path / "PLAN.yaml"
    write_yaml(
        legacy_path,
        {
            "meta": {
                "repo": "fixture",
                "owner": "tester",
                "version": "1",
                "schema_version": "1",
                "last_updated": "2026-04-02",
            },
            "mission": "Fixture mission",
            "milestones": [],
            "sprints": [],
            "items": [],
            "commit_groups": [],
        },
    )

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "render-plan.py",
        str(legacy_path),
    )

    assert result.returncode == 1
    assert "split plan index" in result.stdout


def test_render_plan_handles_missing_input(repo_root: Path, tmp_path: Path) -> None:
    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "render-plan.py",
        str(tmp_path / "missing.yaml"),
    )

    assert result.returncode == 2
    assert "Plan file not found" in result.stdout
