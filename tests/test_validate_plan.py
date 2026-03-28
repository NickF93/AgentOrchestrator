from __future__ import annotations

from pathlib import Path

import yaml
from conftest import PLAN_PATH, SCHEMA_PATH, run_python_script


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
