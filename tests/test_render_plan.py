from __future__ import annotations

import importlib.util
import re
from pathlib import Path

from conftest import copy_split_plan, run_python_script, write_yaml


def load_module(module_name: str, path: Path) -> object:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
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
    legacy_plan, _ = loader.load_plan(index_path)
    legacy_path = tmp_path / "PLAN-legacy.yaml"
    write_yaml(legacy_path, legacy_plan)

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
    legacy_md = tmp_path / "PLAN-legacy.md"
    legacy_dot = tmp_path / "PLAN-legacy.dot"
    legacy_result = run_python_script(
        repo_root / "agent-os" / "scripts" / "render-plan.py",
        str(legacy_path),
        "--md",
        str(legacy_md),
        "--dot",
        str(legacy_dot),
    )

    assert split_result.returncode == 0, split_result.stdout + split_result.stderr
    assert legacy_result.returncode == 0, legacy_result.stdout + legacy_result.stderr
    assert split_md.exists()
    assert split_dot.exists()
    assert legacy_md.exists()
    assert legacy_dot.exists()
    assert normalize_generated_markdown(split_md.read_text(encoding="utf-8")) == normalize_generated_markdown(
        legacy_md.read_text(encoding="utf-8")
    )
    assert split_dot.read_text(encoding="utf-8") == legacy_dot.read_text(encoding="utf-8")
    assert "Shared assets" in split_md.read_text(encoding="utf-8")
    assert "cluster_cg27" in split_dot.read_text(encoding="utf-8")


def test_render_plan_handles_missing_input(repo_root: Path, tmp_path: Path) -> None:
    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "render-plan.py",
        str(tmp_path / "missing.yaml"),
    )

    assert result.returncode == 2
    assert "Plan file not found" in result.stdout
