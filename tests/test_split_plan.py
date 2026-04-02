from __future__ import annotations

import importlib.util
import re
import runpy
import sys
from pathlib import Path
from typing import Any

import pytest
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
    md_path = tmp_path / "PLAN.md"
    dot_path = tmp_path / "PLAN.dot"

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "split-plan.py",
        str(legacy_path),
        "--index",
        str(tmp_path / "plan" / "PLAN-index.yaml"),
        "--md",
        str(md_path),
        "--dot",
        str(dot_path),
        "--remove-source",
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert not legacy_path.exists()
    assert md_path.exists()
    assert dot_path.exists()


def test_split_plan_main_handles_missing_source(
    repo_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = load_module("split_plan_module", repo_root / "agent-os" / "scripts" / "split-plan.py")

    monkeypatch.setattr(sys, "argv", ["split-plan.py", str(tmp_path / "missing.yaml")])

    assert module.main() == 2
    assert "Plan file not found" in capsys.readouterr().out


def test_split_plan_main_rejects_split_index_input(
    repo_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = load_module("split_plan_module", repo_root / "agent-os" / "scripts" / "split-plan.py")
    index_path = tmp_path / "plan" / "PLAN-index.yaml"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(
        yaml.safe_dump(
            {
                "meta": {"repo": "fixture"},
                "mission": "Fixture mission",
                "current_plan": "PLAN-current.yaml",
                "archive_root": "archive",
                "archives": [],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(sys, "argv", ["split-plan.py", str(index_path)])

    assert module.main() == 2
    assert "not a legacy aggregate plan" in capsys.readouterr().out


def test_split_plan_main_succeeds_in_process(
    repo_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = load_module("split_plan_module", repo_root / "agent-os" / "scripts" / "split-plan.py")
    legacy_path = tmp_path / "PLAN.yaml"
    legacy_path.write_text(
        yaml.safe_dump(
            {
                "meta": {
                    "repo": "fixture",
                    "owner": "tester",
                    "version": "1",
                    "schema_version": "1",
                    "last_updated": "2026-04-02",
                },
                "mission": "Fixture mission",
                "milestones": [
                    {"id": "X1", "type": "X", "title": "Only milestone", "status": "done"}
                ],
                "sprints": [
                    {
                        "id": "S1.1",
                        "type": "S",
                        "parent": "X1",
                        "title": "Only sprint",
                        "status": "done",
                    }
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
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    index_path = tmp_path / "plan" / "PLAN-index.yaml"
    md_path = tmp_path / "PLAN.md"
    dot_path = tmp_path / "PLAN.dot"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "split-plan.py",
            str(legacy_path),
            "--index",
            str(index_path),
            "--md",
            str(md_path),
            "--dot",
            str(dot_path),
            "--remove-source",
        ],
    )

    assert module.main() == 0
    stdout = capsys.readouterr().out
    assert f"OK: wrote {index_path}" in stdout
    assert f"OK: removed legacy source {legacy_path}" in stdout
    assert index_path.exists()
    assert md_path.exists()
    assert dot_path.exists()
    assert not legacy_path.exists()


def test_split_plan_main_succeeds_without_remove_source(
    repo_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = load_module("split_plan_module", repo_root / "agent-os" / "scripts" / "split-plan.py")
    legacy_path = tmp_path / "PLAN.yaml"
    legacy_path.write_text(
        yaml.safe_dump(
            {
                "meta": {
                    "repo": "fixture",
                    "owner": "tester",
                    "version": "1",
                    "schema_version": "1",
                    "last_updated": "2026-04-02",
                },
                "mission": "Fixture mission",
                "milestones": [
                    {"id": "X1", "type": "X", "title": "Only milestone", "status": "done"}
                ],
                "sprints": [
                    {
                        "id": "S1.1",
                        "type": "S",
                        "parent": "X1",
                        "title": "Only sprint",
                        "status": "done",
                    }
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
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "split-plan.py",
            str(legacy_path),
            "--index",
            str(tmp_path / "plan" / "PLAN-index.yaml"),
            "--md",
            str(tmp_path / "PLAN.md"),
            "--dot",
            str(tmp_path / "PLAN.dot"),
        ],
    )

    assert module.main() == 0
    assert f"OK: removed legacy source {legacy_path}" not in capsys.readouterr().out
    assert legacy_path.exists()


def test_split_plan_main_detects_render_drift(
    repo_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = load_module("split_plan_module", repo_root / "agent-os" / "scripts" / "split-plan.py")
    legacy_path = tmp_path / "PLAN.yaml"
    legacy_path.write_text(
        yaml.safe_dump(
            {
                "meta": {
                    "repo": "fixture",
                    "owner": "tester",
                    "version": "1",
                    "schema_version": "1",
                    "last_updated": "2026-04-02",
                },
                "mission": "Fixture mission",
                "milestones": [
                    {"id": "X1", "type": "X", "title": "Only milestone", "status": "done"}
                ],
                "sprints": [
                    {
                        "id": "S1.1",
                        "type": "S",
                        "parent": "X1",
                        "title": "Only sprint",
                        "status": "done",
                    }
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
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    class DriftRenderModule:
        def __init__(self) -> None:
            self.calls = 0

        def render_markdown(self, _plan: dict) -> str:
            self.calls += 1
            return f"markdown-{self.calls}"

        def render_dot(self, _plan: dict) -> str:
            self.calls += 1
            return f"dot-{self.calls}"

    monkeypatch.setattr(module, "load_render_module", lambda _script_dir: DriftRenderModule())
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "split-plan.py",
            str(legacy_path),
            "--index",
            str(tmp_path / "plan" / "PLAN-index.yaml"),
            "--md",
            str(tmp_path / "PLAN.md"),
            "--dot",
            str(tmp_path / "PLAN.dot"),
        ],
    )

    assert module.main() == 1
    assert (
        "rendered aggregate outputs changed across the split migration" in capsys.readouterr().out
    )


def test_split_plan_main_detects_split_mismatch(
    repo_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = load_module("split_plan_module", repo_root / "agent-os" / "scripts" / "split-plan.py")
    legacy_path = tmp_path / "PLAN.yaml"
    legacy_path.write_text(
        yaml.safe_dump(
            {
                "meta": {
                    "repo": "fixture",
                    "owner": "tester",
                    "version": "1",
                    "schema_version": "1",
                    "last_updated": "2026-04-02",
                },
                "mission": "Fixture mission",
                "milestones": [
                    {"id": "X1", "type": "X", "title": "Only milestone", "status": "done"}
                ],
                "sprints": [
                    {
                        "id": "S1.1",
                        "type": "S",
                        "parent": "X1",
                        "title": "Only sprint",
                        "status": "done",
                    }
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
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    original_load_split_plan = module.load_split_plan

    def mismatched_load_split_plan(index_path: Path) -> tuple[dict, dict]:
        split_plan, metadata = original_load_split_plan(index_path)
        split_plan["mission"] = "changed"
        return split_plan, metadata

    monkeypatch.setattr(module, "load_split_plan", mismatched_load_split_plan)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "split-plan.py",
            str(legacy_path),
            "--index",
            str(tmp_path / "plan" / "PLAN-index.yaml"),
            "--md",
            str(tmp_path / "PLAN.md"),
            "--dot",
            str(tmp_path / "PLAN.dot"),
        ],
    )

    assert module.main() == 1
    assert "split aggregate plan does not match the legacy source plan" in capsys.readouterr().out


def test_split_plan_load_render_module_rejects_unloadable_script(
    repo_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = load_module("split_plan_module", repo_root / "agent-os" / "scripts" / "split-plan.py")
    monkeypatch.setattr(
        module.importlib.util, "spec_from_file_location", lambda *_args, **_kwargs: None
    )

    with pytest.raises(module.PlanLoadError, match="Unable to load render helper"):
        module.load_render_module(repo_root / "agent-os" / "scripts")


def test_split_plan_script_entrypoint_runs(
    repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    legacy_path = tmp_path / "PLAN.yaml"
    legacy_path.write_text(
        yaml.safe_dump(
            {
                "meta": {
                    "repo": "fixture",
                    "owner": "tester",
                    "version": "1",
                    "schema_version": "1",
                    "last_updated": "2026-04-02",
                },
                "mission": "Fixture mission",
                "milestones": [
                    {"id": "X1", "type": "X", "title": "Only milestone", "status": "done"}
                ],
                "sprints": [
                    {
                        "id": "S1.1",
                        "type": "S",
                        "parent": "X1",
                        "title": "Only sprint",
                        "status": "done",
                    }
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
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "split-plan.py",
            str(legacy_path),
            "--index",
            str(tmp_path / "plan" / "PLAN-index.yaml"),
            "--md",
            str(tmp_path / "PLAN.md"),
            "--dot",
            str(tmp_path / "PLAN.dot"),
        ],
    )

    with pytest.raises(SystemExit) as exc:
        runpy.run_path(
            str(repo_root / "agent-os" / "scripts" / "split-plan.py"), run_name="__main__"
        )

    assert exc.value.code == 0
