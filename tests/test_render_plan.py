from __future__ import annotations

from pathlib import Path

import yaml
from conftest import run_python_script


def test_render_plan_generates_outputs(repo_root: Path, tmp_path: Path) -> None:
    plan = yaml.safe_load((repo_root / "PLAN.yaml").read_text(encoding="utf-8"))
    fixture_plan = tmp_path / "PLAN.yaml"
    fixture_plan.write_text(yaml.safe_dump(plan, sort_keys=False), encoding="utf-8")

    md_path = tmp_path / "PLAN.md"
    dot_path = tmp_path / "PLAN.dot"
    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "render-plan.py",
        str(fixture_plan),
        "--md",
        str(md_path),
        "--dot",
        str(dot_path),
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert md_path.exists()
    assert dot_path.exists()
    assert "Shared assets" in md_path.read_text(encoding="utf-8")
    assert "cluster_cg27" in dot_path.read_text(encoding="utf-8")


def test_render_plan_handles_missing_input(repo_root: Path, tmp_path: Path) -> None:
    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "render-plan.py",
        str(tmp_path / "missing.yaml"),
    )

    assert result.returncode == 2
    assert "Plan file not found" in result.stdout
