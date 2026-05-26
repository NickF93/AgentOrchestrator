from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run_trust_script(
    repo_root: Path,
    project_path: Path | str,
    *args: str,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(repo_root / "agent-os" / "scripts" / "trust-codex-project.py"),
            *args,
            str(project_path),
        ],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


def test_trust_codex_project_dry_run_performs_no_writes(repo_root: Path, tmp_path: Path) -> None:
    project = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    project.mkdir()

    result = run_trust_script(repo_root, project, "--dry-run", "--codex-home", str(codex_home))

    assert result.returncode == 0, result.stdout + result.stderr
    assert "DRY-RUN: would trust" in result.stdout
    assert not (codex_home / "config.toml").exists()


def test_trust_codex_project_creates_missing_config(repo_root: Path, tmp_path: Path) -> None:
    project = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    project.mkdir()

    result = run_trust_script(repo_root, project, "--codex-home", str(codex_home))

    assert result.returncode == 0, result.stdout + result.stderr
    config = codex_home / "config.toml"
    assert config.exists()
    assert not (codex_home / "config.toml.bak").exists()
    content = config.read_text(encoding="utf-8")
    assert f'[projects."{project.resolve().as_posix()}"]' in content
    assert 'trust_level = "trusted"' in content


def test_trust_codex_project_is_idempotent_when_already_trusted(
    repo_root: Path, tmp_path: Path
) -> None:
    project = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    config = codex_home / "config.toml"
    project.mkdir()
    codex_home.mkdir()
    content = f'[projects."{project.resolve().as_posix()}"]\ntrust_level = "trusted"\n'
    config.write_text(content, encoding="utf-8")

    result = run_trust_script(repo_root, project, "--codex-home", str(codex_home))

    assert result.returncode == 0, result.stdout + result.stderr
    assert "OK: already trusted" in result.stdout
    assert config.read_text(encoding="utf-8") == content
    assert not (codex_home / "config.toml.bak").exists()


def test_trust_codex_project_updates_existing_entry_and_backs_up(
    repo_root: Path, tmp_path: Path
) -> None:
    project = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    config = codex_home / "config.toml"
    project.mkdir()
    codex_home.mkdir()
    original = (
        'model = "gpt-5.5"\n\n'
        f'[projects."{project.resolve().as_posix()}"]\n'
        'trust_level = "untrusted"\n'
    )
    config.write_text(original, encoding="utf-8")

    result = run_trust_script(repo_root, project, "--codex-home", str(codex_home))

    assert result.returncode == 0, result.stdout + result.stderr
    assert (codex_home / "config.toml.bak").read_text(encoding="utf-8") == original
    content = config.read_text(encoding="utf-8")
    assert 'model = "gpt-5.5"' in content
    assert 'trust_level = "trusted"' in content
    assert 'trust_level = "untrusted"' not in content


def test_trust_codex_project_normalizes_project_path(repo_root: Path, tmp_path: Path) -> None:
    project = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    project.mkdir()

    result = run_trust_script(
        repo_root,
        Path("repo") / ".." / "repo",
        "--codex-home",
        str(codex_home),
        cwd=tmp_path,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    content = (codex_home / "config.toml").read_text(encoding="utf-8")
    assert f'[projects."{project.resolve().as_posix()}"]' in content
