from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from conftest import PLAN_PATH, SCHEMA_PATH, copy_split_plan, load_yaml, run_python_script, write_yaml


def run_validate_plan_without_jsonschema(
    repo_root: Path, plan_path: Path, schema_path: Path, temp_path: Path
) -> subprocess.CompletedProcess[str]:
    blocker = temp_path / "sitecustomize.py"
    blocker.write_text(
        "import builtins\n"
        "_original_import = builtins.__import__\n"
        "def _guarded_import(name, globals=None, locals=None, fromlist=(), level=0):\n"
        "    if name == 'jsonschema':\n"
        "        raise ImportError('blocked for test')\n"
        "    return _original_import(name, globals, locals, fromlist, level)\n"
        "builtins.__import__ = _guarded_import\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        f"{temp_path}{os.pathsep}{existing_pythonpath}" if existing_pythonpath else str(temp_path)
    )
    return subprocess.run(
        [
            sys.executable,
            str(repo_root / "agent-os" / "scripts" / "validate-plan.py"),
            str(plan_path),
            "--schema",
            str(schema_path),
        ],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )


def test_validate_plan_accepts_current_plan(repo_root: Path) -> None:
    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "validate-plan.py",
        str(PLAN_PATH),
        "--schema",
        str(SCHEMA_PATH),
    )
    assert result.returncode == 0, result.stderr
    assert "ACTIVE:" in result.stdout
    assert "ARCHIVED:" in result.stdout
    assert "OK:" in result.stdout


def test_validate_plan_rejects_unknown_shared_asset(repo_root: Path, tmp_path: Path) -> None:
    index_path = copy_split_plan(tmp_path)
    current_path = index_path.parent / "PLAN-current.yaml"
    current_plan = load_yaml(current_path)
    target_item = next(item for item in current_plan["items"] if item["id"] == "C31.2.6")
    target_item["shared_assets"]["prompt"] = "does-not-exist"
    write_yaml(current_path, current_plan)

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "validate-plan.py",
        str(index_path),
        "--schema",
        str(SCHEMA_PATH),
    )
    assert result.returncode == 1
    combined = f"{result.stdout}\n{result.stderr}"
    assert "unknown asset id 'does-not-exist'" in combined


def test_validate_plan_rejects_missing_required_field(repo_root: Path, tmp_path: Path) -> None:
    index_path = copy_split_plan(tmp_path)
    index = load_yaml(index_path)
    del index["meta"]["repo"]
    write_yaml(index_path, index)

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "validate-plan.py",
        str(index_path),
        "--schema",
        str(SCHEMA_PATH),
    )
    assert result.returncode == 1
    combined = f"{result.stdout}\n{result.stderr}"
    assert "Schema validation failed" in combined or "meta.repo" in combined


def test_validate_plan_accepts_current_plan_without_jsonschema(
    repo_root: Path, tmp_path: Path
) -> None:
    index_path = copy_split_plan(tmp_path)
    result = run_validate_plan_without_jsonschema(repo_root, index_path, SCHEMA_PATH, tmp_path)
    assert result.returncode == 0, f"{result.stdout}\n{result.stderr}"
    assert "ACTIVE:" in result.stdout
    assert "ARCHIVED:" in result.stdout
    assert "OK:" in result.stdout


def test_validate_plan_rejects_missing_required_field_without_jsonschema(
    repo_root: Path, tmp_path: Path
) -> None:
    index_path = copy_split_plan(tmp_path)
    index = load_yaml(index_path)
    del index["meta"]["repo"]
    write_yaml(index_path, index)

    result = run_validate_plan_without_jsonschema(repo_root, index_path, SCHEMA_PATH, tmp_path)
    assert result.returncode == 1
    combined = f"{result.stdout}\n{result.stderr}"
    assert "Schema validation failed" in combined
    assert "meta.repo: expected non-empty string" in combined
    assert "AttributeError" not in combined


def test_validate_plan_rejects_archive_digest_mismatch(repo_root: Path, tmp_path: Path) -> None:
    index_path = copy_split_plan(tmp_path)
    index = load_yaml(index_path)
    archive_path = index_path.parent / index["archives"][0]["path"]
    archive_fragment = load_yaml(archive_path)
    archive_fragment["items"][0]["title"] = "tampered archived item"
    write_yaml(archive_path, archive_fragment)

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "validate-plan.py",
        str(index_path),
        "--schema",
        str(SCHEMA_PATH),
    )

    assert result.returncode == 1
    combined = f"{result.stdout}\n{result.stderr}"
    assert "archive digest mismatch" in combined


def test_validate_plan_rejects_cross_fragment_archive_structure(
    repo_root: Path, tmp_path: Path
) -> None:
    index_path = copy_split_plan(tmp_path)
    index = load_yaml(index_path)
    archive_path = index_path.parent / index["archives"][0]["path"]
    archive_fragment = load_yaml(archive_path)
    archive_fragment["sprints"][0]["parent"] = "X999"
    write_yaml(archive_path, archive_fragment)

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "validate-plan.py",
        str(index_path),
        "--schema",
        str(SCHEMA_PATH),
    )

    assert result.returncode == 1
    combined = f"{result.stdout}\n{result.stderr}"
    assert "outside its fragment" in combined
