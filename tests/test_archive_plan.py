from __future__ import annotations

import importlib.util
from pathlib import Path

from conftest import copy_split_plan, load_yaml, run_python_script, write_yaml


def load_module(module_name: str, path: Path) -> object:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def mark_current_fragment_done(current_path: Path) -> None:
    current_fragment = load_yaml(current_path)
    for section in ("milestones", "sprints", "items"):
        for obj in current_fragment[section]:
            obj["status"] = "done"
    write_yaml(current_path, current_fragment)


def test_archive_plan_moves_done_milestone_and_updates_index(
    repo_root: Path, tmp_path: Path
) -> None:
    index_path = copy_split_plan(tmp_path)
    current_path = index_path.parent / "PLAN-current.yaml"
    mark_current_fragment_done(current_path)
    md_path = tmp_path / "PLAN.md"
    dot_path = tmp_path / "PLAN.dot"

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "archive-plan.py",
        "--plan",
        str(index_path),
        "--milestone",
        "X31",
        "--md",
        str(md_path),
        "--dot",
        str(dot_path),
    )

    assert result.returncode == 0, result.stdout + result.stderr
    archive_path = tmp_path / "plan" / "archive" / "PLAN-X31.yaml"
    assert archive_path.exists()
    assert md_path.exists()
    assert dot_path.exists()

    updated_current = load_yaml(current_path)
    assert updated_current == {"milestones": [], "sprints": [], "items": [], "commit_groups": []}

    updated_index = load_yaml(index_path)
    archive_entry = next(entry for entry in updated_index["archives"] if entry["milestone"] == "X31")
    loader = load_module("plan_loader", repo_root / "agent-os" / "scripts" / "plan_loader.py")
    archived_fragment = load_yaml(archive_path)
    assert archive_entry["digest"] == loader.compute_fragment_digest(archived_fragment)

    rerun = run_python_script(
        repo_root / "agent-os" / "scripts" / "archive-plan.py",
        "--plan",
        str(index_path),
        "--milestone",
        "X31",
        "--md",
        str(md_path),
        "--dot",
        str(dot_path),
    )
    assert rerun.returncode == 1
    assert "milestone is not present in the current fragment" in f"{rerun.stdout}\n{rerun.stderr}"


def test_archive_plan_rejects_open_milestone(repo_root: Path, tmp_path: Path) -> None:
    index_path = copy_split_plan(tmp_path)

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "archive-plan.py",
        "--plan",
        str(index_path),
        "--milestone",
        "X31",
    )

    assert result.returncode == 1
    assert "milestone must be status 'done' before archival" in f"{result.stdout}\n{result.stderr}"
