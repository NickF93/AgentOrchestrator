from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import yaml
from conftest import PLAN_PATH, SCHEMA_PATH, run_python_script


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
    assert "OK:" in result.stdout


def test_validate_plan_rejects_unknown_shared_asset(repo_root: Path, tmp_path: Path) -> None:
    plan = yaml.safe_load(PLAN_PATH.read_text(encoding="utf-8"))
    target_item = next(item for item in plan["items"] if item["id"] == "T9.1.4")
    target_item["shared_assets"]["prompt"] = "does-not-exist"

    invalid_plan = tmp_path / "PLAN-invalid-shared.yaml"
    invalid_plan.write_text(yaml.safe_dump(plan, sort_keys=False), encoding="utf-8")

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "validate-plan.py",
        str(invalid_plan),
        "--schema",
        str(SCHEMA_PATH),
    )
    assert result.returncode == 1
    combined = f"{result.stdout}\n{result.stderr}"
    assert "unknown asset id 'does-not-exist'" in combined


def test_validate_plan_rejects_missing_required_field(repo_root: Path, tmp_path: Path) -> None:
    plan = yaml.safe_load(PLAN_PATH.read_text(encoding="utf-8"))
    del plan["meta"]["repo"]

    invalid_plan = tmp_path / "PLAN-invalid-required.yaml"
    invalid_plan.write_text(yaml.safe_dump(plan, sort_keys=False), encoding="utf-8")

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "validate-plan.py",
        str(invalid_plan),
        "--schema",
        str(SCHEMA_PATH),
    )
    assert result.returncode == 1
    combined = f"{result.stdout}\n{result.stderr}"
    assert "Schema validation failed" in combined or "meta.repo" in combined


def test_validate_plan_accepts_current_plan_without_jsonschema(
    repo_root: Path, tmp_path: Path
) -> None:
    result = run_validate_plan_without_jsonschema(repo_root, PLAN_PATH, SCHEMA_PATH, tmp_path)
    assert result.returncode == 0, f"{result.stdout}\n{result.stderr}"
    assert "OK:" in result.stdout


def test_validate_plan_rejects_missing_required_field_without_jsonschema(
    repo_root: Path, tmp_path: Path
) -> None:
    plan = yaml.safe_load(PLAN_PATH.read_text(encoding="utf-8"))
    del plan["meta"]["repo"]

    invalid_plan = tmp_path / "PLAN-invalid-required-fallback.yaml"
    invalid_plan.write_text(yaml.safe_dump(plan, sort_keys=False), encoding="utf-8")

    result = run_validate_plan_without_jsonschema(repo_root, invalid_plan, SCHEMA_PATH, tmp_path)
    assert result.returncode == 1
    combined = f"{result.stdout}\n{result.stderr}"
    assert "Schema validation failed" in combined
    assert "meta.repo: expected non-empty string" in combined
    assert "AttributeError" not in combined
