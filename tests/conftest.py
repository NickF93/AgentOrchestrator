from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "agent-os" / "scripts"
SCHEMA_PATH = REPO_ROOT / "agent-os" / "schemas" / "plan.schema.json"
PLAN_PATH = REPO_ROOT / "plan" / "PLAN-index.yaml"


@pytest.fixture
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture
def scripts_dir() -> Path:
    return SCRIPTS_DIR


@pytest.fixture
def python_bin() -> str:
    return sys.executable


@pytest.fixture
def script_env(python_bin: str) -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHON_BIN"] = python_bin
    env["PATH"] = f"{Path(python_bin).parent}{os.pathsep}{env.get('PATH', '')}"
    return env


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def copy_split_plan(tmp_path: Path) -> Path:
    shutil.copytree(REPO_ROOT / "plan", tmp_path / "plan")
    return tmp_path / "plan" / "PLAN-index.yaml"


def run_python_script(
    script_path: Path, *args: str, cwd: Path | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script_path), *args],
        cwd=cwd or REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def run_shell_script(
    script_path: Path,
    *args: str,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(script_path), *args],
        cwd=cwd or REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )
