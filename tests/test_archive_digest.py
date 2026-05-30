from __future__ import annotations

import importlib.util
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


def test_render_archive_digest_writes_default_output(repo_root: Path, tmp_path: Path) -> None:
    index_path = copy_split_plan(tmp_path)
    digest_path = tmp_path / "plan" / "archive" / "DIGEST.md"

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "render-archive-digest.py",
        str(index_path),
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert digest_path.exists()
    digest = digest_path.read_text(encoding="utf-8")
    assert digest.startswith("# Archive Digest")
    assert "AUTO-GENERATED from" in digest
    assert "`X52`" in digest
    assert "`archive/PLAN-X52.yaml`" in digest
    assert "Canonical history remains in `plan/PLAN-index.yaml`" in digest


def test_render_archive_digest_is_deterministic(repo_root: Path, tmp_path: Path) -> None:
    index_path = copy_split_plan(tmp_path)
    first_path = tmp_path / "first.md"
    second_path = tmp_path / "second.md"

    first = run_python_script(
        repo_root / "agent-os" / "scripts" / "render-archive-digest.py",
        str(index_path),
        "--output",
        str(first_path),
    )
    second = run_python_script(
        repo_root / "agent-os" / "scripts" / "render-archive-digest.py",
        str(index_path),
        "--output",
        str(second_path),
    )

    assert first.returncode == 0, first.stdout + first.stderr
    assert second.returncode == 0, second.stdout + second.stderr
    assert first_path.read_text(encoding="utf-8") == second_path.read_text(encoding="utf-8")


def test_render_archive_digest_handles_empty_archives(repo_root: Path, tmp_path: Path) -> None:
    plan_dir = tmp_path / "plan"
    archive_dir = plan_dir / "archive"
    archive_dir.mkdir(parents=True)
    write_yaml(
        plan_dir / "PLAN-current.yaml",
        {"milestones": [], "sprints": [], "items": [], "commit_groups": []},
    )
    write_yaml(
        plan_dir / "PLAN-index.yaml",
        {
            "meta": {
                "repo": "fixture",
                "owner": "tester",
                "version": "1",
                "schema_version": "1",
                "last_updated": "2026-05-30",
            },
            "mission": "Fixture mission",
            "current_plan": "PLAN-current.yaml",
            "archive_root": "archive",
            "archives": [],
        },
    )

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "render-archive-digest.py",
        str(plan_dir / "PLAN-index.yaml"),
    )

    assert result.returncode == 0, result.stdout + result.stderr
    digest = (archive_dir / "DIGEST.md").read_text(encoding="utf-8")
    assert "- Archived milestones: 0" in digest
    assert "No archived milestones." in digest


def test_render_archive_digest_handles_missing_plan(repo_root: Path, tmp_path: Path) -> None:
    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "render-archive-digest.py",
        str(tmp_path / "missing.yaml"),
    )

    assert result.returncode == 2
    assert "Plan file not found" in result.stdout


def test_render_archive_digest_escapes_markdown_table_cells(repo_root: Path) -> None:
    module = load_module(
        "render_archive_digest", repo_root / "agent-os" / "scripts" / "render-archive-digest.py"
    )

    rendered = module.render_archive_digest(
        {
            "archives": [
                {
                    "entry": {
                        "milestone": "X1",
                        "title": "Title | with pipe",
                        "path": "archive/PLAN-X1.yaml",
                        "digest": "sha256:abcdef123456",
                    },
                    "fragment": {
                        "milestones": [],
                        "sprints": [{"id": "S1.1"}],
                        "items": [
                            {"id": "D1.1.1", "type": "D", "scope": "docs|workflow"},
                            {"id": "M1.1.2", "type": "M", "scope": "agent-os/scripts/"},
                        ],
                        "commit_groups": [{"id": "cg1"}],
                    },
                }
            ],
            "archive_root": Path("plan/archive"),
        }
    )

    assert "Title \\| with pipe" in rendered
    assert "`docs\\|workflow`" in rendered
    assert "D:1, M:1" in rendered
