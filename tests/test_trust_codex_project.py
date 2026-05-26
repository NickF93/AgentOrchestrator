from __future__ import annotations

import importlib.util
import runpy
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest


def load_module(repo_root: Path) -> Any:
    script_path = repo_root / "agent-os" / "scripts" / "trust-codex-project.py"
    spec = importlib.util.spec_from_file_location("trust_codex_project", script_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
    module = load_module(repo_root)
    project = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    project.mkdir()
    config = codex_home / "config.toml"

    changed = module.trust_project(config, project.resolve(), dry_run=True)

    assert changed is True
    assert not config.exists()


def test_trust_codex_project_creates_missing_config(repo_root: Path, tmp_path: Path) -> None:
    module = load_module(repo_root)
    project = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    project.mkdir()

    changed = module.trust_project(codex_home / "config.toml", project.resolve(), dry_run=False)

    assert changed is True
    config = codex_home / "config.toml"
    assert config.exists()
    assert not (codex_home / "config.toml.bak").exists()
    content = config.read_text(encoding="utf-8")
    assert f'[projects."{project.resolve().as_posix()}"]' in content
    assert 'trust_level = "trusted"' in content


def test_trust_codex_project_is_idempotent_when_already_trusted(
    repo_root: Path, tmp_path: Path
) -> None:
    module = load_module(repo_root)
    project = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    config = codex_home / "config.toml"
    project.mkdir()
    codex_home.mkdir()
    content = f'[projects."{project.resolve().as_posix()}"]\ntrust_level = "trusted"\n'
    config.write_text(content, encoding="utf-8")

    changed = module.trust_project(config, project.resolve(), dry_run=False)

    assert changed is False
    assert config.read_text(encoding="utf-8") == content
    assert not (codex_home / "config.toml.bak").exists()


def test_trust_codex_project_updates_existing_entry_and_backs_up(
    repo_root: Path, tmp_path: Path
) -> None:
    module = load_module(repo_root)
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

    changed = module.trust_project(config, project.resolve(), dry_run=False)

    assert changed is True
    assert (codex_home / "config.toml.bak").read_text(encoding="utf-8") == original
    content = config.read_text(encoding="utf-8")
    assert 'model = "gpt-5.5"' in content
    assert 'trust_level = "trusted"' in content
    assert 'trust_level = "untrusted"' not in content


def test_trust_codex_project_normalizes_project_path(repo_root: Path, tmp_path: Path) -> None:
    module = load_module(repo_root)
    project = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    project.mkdir()
    config = codex_home / "config.toml"

    project_path = (tmp_path / "repo" / ".." / "repo").resolve()
    changed = module.trust_project(config, project_path, dry_run=False)

    assert changed is True
    content = config.read_text(encoding="utf-8")
    assert f'[projects."{project.resolve().as_posix()}"]' in content


def test_trust_codex_project_appends_to_existing_config_without_project_table(
    repo_root: Path, tmp_path: Path
) -> None:
    module = load_module(repo_root)
    project = tmp_path / "repo"
    config = tmp_path / "codex-home" / "config.toml"
    project.mkdir()
    config.parent.mkdir()
    original = 'model = "gpt-5.5"\n'
    config.write_text(original, encoding="utf-8")

    changed = module.trust_project(config, project.resolve(), dry_run=False)

    assert changed is True
    assert (config.parent / "config.toml.bak").read_text(encoding="utf-8") == original
    assert (
        f'model = "gpt-5.5"\n\n[projects."{project.resolve().as_posix()}"]\n'
        'trust_level = "trusted"\n'
    ) == config.read_text(encoding="utf-8")


def test_trust_codex_project_inserts_missing_trust_line(repo_root: Path, tmp_path: Path) -> None:
    module = load_module(repo_root)
    project = tmp_path / "repo"
    config = tmp_path / "codex-home" / "config.toml"
    project.mkdir()
    config.parent.mkdir()
    config.write_text(
        f'[projects."{project.resolve().as_posix()}"]\nmodel = "gpt-5.5"\n', encoding="utf-8"
    )

    changed = module.trust_project(config, project.resolve(), dry_run=False)

    assert changed is True
    content = config.read_text(encoding="utf-8")
    assert (
        f'[projects."{project.resolve().as_posix()}"]\ntrust_level = "trusted"\nmodel = "gpt-5.5"'
        in content
    )


def test_trust_codex_project_appends_before_next_table(repo_root: Path, tmp_path: Path) -> None:
    module = load_module(repo_root)
    project = tmp_path / "repo"
    other = tmp_path / "other"
    config = tmp_path / "codex-home" / "config.toml"
    project.mkdir()
    other.mkdir()
    config.parent.mkdir()
    config.write_text(
        f'[projects."{project.resolve().as_posix()}"]\n'
        f'[projects."{other.resolve().as_posix()}"]\n'
        'trust_level = "trusted"\n',
        encoding="utf-8",
    )

    changed = module.trust_project(config, project.resolve(), dry_run=False)

    assert changed is True
    assert (
        f'[projects."{project.resolve().as_posix()}"]\n'
        'trust_level = "trusted"\n'
        f'[projects."{other.resolve().as_posix()}"]'
    ) in config.read_text(encoding="utf-8")


def test_trust_codex_project_resolves_config_precedence(
    repo_root: Path, tmp_path: Path, monkeypatch
) -> None:
    module = load_module(repo_root)
    explicit = tmp_path / "explicit" / "config.toml"
    codex_home = tmp_path / "codex-home"
    env_home = tmp_path / "env-home"
    monkeypatch.setenv("CODEX_HOME", str(env_home))

    assert (
        module.resolve_config_path(
            SimpleNamespace(config=str(explicit), codex_home=str(codex_home))
        )
        == explicit
    )
    assert (
        module.resolve_config_path(SimpleNamespace(config="", codex_home=str(codex_home)))
        == (codex_home / "config.toml").resolve()
    )
    assert (
        module.resolve_config_path(SimpleNamespace(config="", codex_home=""))
        == (env_home / "config.toml").resolve()
    )


def test_trust_codex_project_main_uses_cli_arguments(
    repo_root: Path, tmp_path: Path, monkeypatch
) -> None:
    module = load_module(repo_root)
    project = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    project.mkdir()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "trust-codex-project.py",
            "--codex-home",
            str(codex_home),
            str(project),
        ],
    )

    assert module.main() == 0
    assert (codex_home / "config.toml").exists()


def test_trust_codex_project_main_guard(repo_root: Path, tmp_path: Path, monkeypatch) -> None:
    script_path = repo_root / "agent-os" / "scripts" / "trust-codex-project.py"
    project = tmp_path / "repo"
    codex_home = tmp_path / "codex-home"
    project.mkdir()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "trust-codex-project.py",
            "--codex-home",
            str(codex_home),
            str(project),
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_path(str(script_path), run_name="__main__")

    assert exc_info.value.code == 0
    assert (codex_home / "config.toml").exists()
