from __future__ import annotations

import importlib.util
import runpy
import sys
from pathlib import Path
from typing import Any

import pytest
from conftest import copy_split_plan, load_yaml, run_python_script, write_yaml


def load_module(module_name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
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
    archive_entry = next(
        entry for entry in updated_index["archives"] if entry["milestone"] == "X31"
    )
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


def test_archive_plan_main_handles_missing_plan_index(
    repo_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = load_module(
        "archive_plan_module", repo_root / "agent-os" / "scripts" / "archive-plan.py"
    )
    missing_path = tmp_path / "missing-index.yaml"

    monkeypatch.setattr(
        sys, "argv", ["archive-plan.py", "--plan", str(missing_path), "--milestone", "X31"]
    )

    assert module.main() == 2
    assert "Plan index not found" in capsys.readouterr().out


def test_archive_plan_main_rejects_missing_current_milestone(
    repo_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = load_module(
        "archive_plan_module", repo_root / "agent-os" / "scripts" / "archive-plan.py"
    )
    index_path = copy_split_plan(tmp_path)

    monkeypatch.setattr(
        sys, "argv", ["archive-plan.py", "--plan", str(index_path), "--milestone", "X999"]
    )

    assert module.main() == 1
    assert "milestone is not present in the current fragment" in capsys.readouterr().out


def test_archive_plan_main_succeeds_in_process(
    repo_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = load_module(
        "archive_plan_module", repo_root / "agent-os" / "scripts" / "archive-plan.py"
    )
    index_path = copy_split_plan(tmp_path)
    current_path = index_path.parent / "PLAN-current.yaml"
    mark_current_fragment_done(current_path)
    md_path = tmp_path / "PLAN.md"
    dot_path = tmp_path / "PLAN.dot"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "archive-plan.py",
            "--plan",
            str(index_path),
            "--milestone",
            "X31",
            "--md",
            str(md_path),
            "--dot",
            str(dot_path),
        ],
    )

    assert module.main() == 0
    stdout = capsys.readouterr().out
    assert "OK: archived X31" in stdout
    assert md_path.exists()
    assert dot_path.exists()
    assert (tmp_path / "plan" / "archive" / "PLAN-X31.yaml").exists()
    assert load_yaml(index_path)["meta"]["last_updated"]


def test_archive_plan_main_rejects_existing_archive_target_in_process(
    repo_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = load_module(
        "archive_plan_module", repo_root / "agent-os" / "scripts" / "archive-plan.py"
    )
    index_path = copy_split_plan(tmp_path)
    current_path = index_path.parent / "PLAN-current.yaml"
    mark_current_fragment_done(current_path)
    archive_path = tmp_path / "plan" / "archive" / "PLAN-X31.yaml"
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    archive_path.write_text("already there\n", encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        ["archive-plan.py", "--plan", str(index_path), "--milestone", "X31"],
    )

    assert module.main() == 1
    assert "archive target already exists" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("status_updates", "message"),
    [
        ({"milestones": "review"}, "milestone must be status 'done' before archival"),
        ({"sprints": "review"}, "sprints must be done before archival"),
        ({"items": "review"}, "items must be done before archival"),
    ],
)
def test_ensure_fragment_is_closed_rejects_open_elements(
    repo_root: Path, status_updates: dict[str, str], message: str
) -> None:
    module = load_module(
        "archive_plan_module", repo_root / "agent-os" / "scripts" / "archive-plan.py"
    )
    fragment = {
        "milestones": [{"id": "X1", "status": "done"}],
        "sprints": [{"id": "S1.1", "status": "done"}],
        "items": [{"id": "D1.1.1", "status": "done"}],
        "commit_groups": [],
    }
    for section, status in status_updates.items():
        fragment[section][0]["status"] = status

    with pytest.raises(module.PlanLoadError, match=message):
        module.ensure_fragment_is_closed(fragment, "X1")


def test_archive_plan_main_handles_unexpected_render_failure(
    repo_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = load_module(
        "archive_plan_module", repo_root / "agent-os" / "scripts" / "archive-plan.py"
    )
    index_path = copy_split_plan(tmp_path)
    current_path = index_path.parent / "PLAN-current.yaml"
    mark_current_fragment_done(current_path)

    def fail_render(_script_dir: Path) -> Any:
        raise RuntimeError("render failure")

    monkeypatch.setattr(module, "load_render_module", fail_render)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "archive-plan.py",
            "--plan",
            str(index_path),
            "--milestone",
            "X31",
            "--md",
            str(tmp_path / "PLAN.md"),
            "--dot",
            str(tmp_path / "PLAN.dot"),
        ],
    )

    assert module.main() == 2
    assert "render failure" in capsys.readouterr().out


def test_archive_plan_load_render_module_rejects_unloadable_script(
    repo_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = load_module(
        "archive_plan_module", repo_root / "agent-os" / "scripts" / "archive-plan.py"
    )
    monkeypatch.setattr(
        module.importlib.util, "spec_from_file_location", lambda *_args, **_kwargs: None
    )

    with pytest.raises(module.PlanLoadError, match="Unable to load render helper"):
        module.load_render_module(repo_root / "agent-os" / "scripts")


def test_archive_plan_script_entrypoint_runs(
    repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    index_path = copy_split_plan(tmp_path)
    current_path = index_path.parent / "PLAN-current.yaml"
    mark_current_fragment_done(current_path)

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "archive-plan.py",
            "--plan",
            str(index_path),
            "--milestone",
            "X31",
            "--md",
            str(tmp_path / "PLAN.md"),
            "--dot",
            str(tmp_path / "PLAN.dot"),
        ],
    )

    with pytest.raises(SystemExit) as exc:
        runpy.run_path(
            str(repo_root / "agent-os" / "scripts" / "archive-plan.py"), run_name="__main__"
        )

    assert exc.value.code == 0
