from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "agent-os" / "scripts"
SCHEMA_PATH = REPO_ROOT / "agent-os" / "schemas" / "plan.schema.json"
PLAN_PATH = REPO_ROOT / "PLAN.yaml"


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
