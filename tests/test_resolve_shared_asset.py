from __future__ import annotations

import importlib.util
import json
import runpy
import sys
from pathlib import Path
from typing import Any

import pytest
from conftest import run_python_script, run_shell_script


def load_module(module_name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    spec.loader.exec_module(module)
    return module


def test_resolve_workspace_asset_with_explicit_root(repo_root: Path, tmp_path: Path) -> None:
    repo_clone = tmp_path / "repo"
    repo_clone.mkdir()

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py",
        "plan-checkpoint-close",
        "--control-plane-root",
        str(repo_root),
        "--repo-root",
        str(repo_clone),
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert '"asset_id": "plan-checkpoint-close"' in result.stdout
    assert '"resolution_mode": "workspace"' in result.stdout


def test_resolve_workspace_asset_from_stamped_workspace_metadata(
    repo_root: Path,
    tmp_path: Path,
) -> None:
    workspace_root = tmp_path / "workspace"
    workspace_root.mkdir()
    layer2_repo = workspace_root / "Layer2Repo"
    layer2_repo.mkdir()
    (workspace_root / "AGENTS.md").write_text(
        f"Workspace AGENTS\nCONTROL_PLANE_ROOT: {repo_root}\n",
        encoding="utf-8",
    )

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py",
        "checkpoint-closure-review",
        "--repo-root",
        str(layer2_repo),
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert '"asset_id": "checkpoint-closure-review"' in result.stdout


def test_resolve_vendored_asset_after_materialization(
    repo_root: Path,
    tmp_path: Path,
    script_env: dict[str, str],
) -> None:
    repo_clone = tmp_path / "standalone-repo"
    repo_clone.mkdir()

    materialize = run_shell_script(
        repo_root / "agent-os" / "scripts" / "materialize-shared-asset.sh",
        "--control-plane-root",
        str(repo_root),
        "--repo-root",
        str(repo_clone),
        "plan-checkpoint-close",
        env=script_env,
    )
    assert materialize.returncode == 0, materialize.stdout + materialize.stderr

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py",
        "plan-checkpoint-close",
        "--repo-root",
        str(repo_clone),
        "--resolution-mode",
        "vendored",
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert '"resolution_mode": "vendored"' in result.stdout
    assert str(repo_clone / ".agent-os" / "vendor") in result.stdout


def test_resolve_vendored_asset_fails_when_manifest_is_missing(
    repo_root: Path, tmp_path: Path
) -> None:
    repo_clone = tmp_path / "standalone-repo"
    repo_clone.mkdir()

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py",
        "plan-checkpoint-close",
        "--repo-root",
        str(repo_clone),
        "--resolution-mode",
        "vendored",
        "--format",
        "json",
    )

    assert result.returncode == 1
    assert "Vendored asset root not found" in result.stderr


def test_resolve_unknown_asset_fails_clearly(repo_root: Path, tmp_path: Path) -> None:
    repo_clone = tmp_path / "repo"
    repo_clone.mkdir()

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py",
        "not-a-real-asset",
        "--control-plane-root",
        str(repo_root),
        "--repo-root",
        str(repo_clone),
    )

    assert result.returncode == 1
    assert "Unknown shared asset id" in result.stderr


def test_load_yaml_rejects_non_mapping(repo_root: Path, tmp_path: Path) -> None:
    module = load_module(
        "resolve_shared_asset", repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py"
    )
    path = tmp_path / "list.yaml"
    path.write_text("- bad\n", encoding="utf-8")

    with pytest.raises(ValueError, match="YAML file must be a mapping"):
        module.load_yaml(path)


def test_discover_control_plane_root_prefers_env(repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_module(
        "resolve_shared_asset", repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py"
    )
    repo_clone = tmp_path / "repo"
    repo_clone.mkdir()
    env_root = tmp_path / "env-root"
    env_root.mkdir()
    monkeypatch.setenv("CONTROL_PLANE_ROOT", str(env_root))

    assert module.discover_control_plane_root(repo_clone, None) == env_root.resolve()


def test_discover_control_plane_root_handles_explicit_local_and_missing(
    repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = load_module(
        "resolve_shared_asset", repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py"
    )
    repo_clone = tmp_path / "repo"
    repo_clone.mkdir()
    monkeypatch.delenv("CONTROL_PLANE_ROOT", raising=False)

    explicit_root = tmp_path / "explicit-root"
    explicit_root.mkdir()
    assert module.discover_control_plane_root(repo_clone, str(explicit_root)) == explicit_root.resolve()

    local_registry = repo_clone / "agent-os" / "registry"
    local_registry.mkdir(parents=True)
    (local_registry / "shared-assets.yaml").write_text("assets: []\n", encoding="utf-8")
    assert module.discover_control_plane_root(repo_clone, None) == repo_clone.resolve()

    (local_registry / "shared-assets.yaml").unlink()
    with pytest.raises(FileNotFoundError, match="Cannot locate control-plane root"):
        module.discover_control_plane_root(repo_clone, None)


def test_discover_control_plane_root_uses_stamped_workspace(repo_root: Path, tmp_path: Path) -> None:
    module = load_module(
        "resolve_shared_asset", repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py"
    )
    workspace_root = tmp_path / "workspace"
    workspace_root.mkdir()
    repo_clone = workspace_root / "repo"
    repo_clone.mkdir()
    (workspace_root / "CLAUDE.md").write_text(f"CONTROL_PLANE_ROOT: {repo_root}\n", encoding="utf-8")

    assert module.discover_control_plane_root(repo_clone, None) == repo_root.resolve()


def test_parse_workspace_control_plane_root_reads_codex_marker(repo_root: Path, tmp_path: Path) -> None:
    module = load_module(
        "resolve_shared_asset", repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py"
    )
    workspace_root = tmp_path / "workspace"
    workspace_root.mkdir()
    repo_clone = workspace_root / "repo"
    repo_clone.mkdir()
    (workspace_root / ".codex").write_text(f"Control plane: {repo_root}\n", encoding="utf-8")

    assert module.parse_workspace_control_plane_root(repo_clone) == repo_root.resolve()


def test_find_registry_asset_rejects_non_mapping_entries(repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_module(
        "resolve_shared_asset", repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py"
    )
    monkeypatch.setattr(module, "load_registry", lambda _root: {"assets": ["bad"]})

    with pytest.raises(ValueError, match="Registry entry for 'plan-checkpoint-close' is not a mapping"):
        module.find_registry_asset("plan-checkpoint-close", tmp_path)


def test_load_registry_rejects_missing_registry(repo_root: Path, tmp_path: Path) -> None:
    module = load_module(
        "resolve_shared_asset", repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py"
    )

    with pytest.raises(FileNotFoundError, match="Shared asset registry not found"):
        module.load_registry(tmp_path)


def test_find_registry_asset_rejects_unknown_id(repo_root: Path, tmp_path: Path) -> None:
    module = load_module(
        "resolve_shared_asset", repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py"
    )
    control_plane_root = tmp_path / "control"
    registry_dir = control_plane_root / "agent-os" / "registry"
    registry_dir.mkdir(parents=True)
    (registry_dir / "shared-assets.yaml").write_text("assets: []\n", encoding="utf-8")

    with pytest.raises(KeyError, match="Unknown shared asset id"):
        module.find_registry_asset("missing-asset", control_plane_root)


def test_resolve_workspace_asset_rejects_missing_registry_path(
    repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = load_module(
        "resolve_shared_asset", repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py"
    )
    repo_clone = tmp_path / "repo"
    repo_clone.mkdir()
    monkeypatch.setattr(
        module,
        "find_registry_asset",
        lambda _asset_id, _root: {
            "id": "plan-checkpoint-close",
            "kind": "skill",
            "version": "1.0.0",
            "compatibility": ["codex"],
            "materializable": True,
            "depends_on_assets": [],
            "path": "agent-os/skills/missing/SKILL.md",
        },
    )

    with pytest.raises(FileNotFoundError, match="Resolved asset path does not exist"):
        module.resolve_workspace_asset("plan-checkpoint-close", repo_clone, str(repo_root))


def test_resolve_workspace_asset_rejects_invalid_registry_path_field(
    repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = load_module(
        "resolve_shared_asset", repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py"
    )
    repo_clone = tmp_path / "repo"
    repo_clone.mkdir()
    monkeypatch.setattr(
        module,
        "find_registry_asset",
        lambda _asset_id, _root: {
            "id": "plan-checkpoint-close",
            "kind": "skill",
            "version": "1.0.0",
            "compatibility": ["codex"],
            "materializable": True,
            "depends_on_assets": [],
            "path": "",
        },
    )

    with pytest.raises(ValueError, match="has no valid path"):
        module.resolve_workspace_asset("plan-checkpoint-close", repo_clone, str(repo_root))


def test_resolve_vendored_asset_rejects_missing_vendored_file(
    repo_root: Path, tmp_path: Path
) -> None:
    module = load_module(
        "resolve_shared_asset", repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py"
    )
    repo_clone = tmp_path / "repo"
    manifest_dir = repo_clone / ".agent-os" / "vendor" / "skill" / "plan-checkpoint-close"
    manifest_dir.mkdir(parents=True)
    (manifest_dir / "provenance.yaml").write_text(
        "asset_id: plan-checkpoint-close\nkind: skill\nversion: 1\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="missing vendored_file"):
        module.resolve_vendored_asset("plan-checkpoint-close", repo_clone, "skill")


def test_resolve_vendored_asset_scans_manifests_and_rejects_missing_payload(
    repo_root: Path, tmp_path: Path
) -> None:
    module = load_module(
        "resolve_shared_asset", repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py"
    )
    repo_clone = tmp_path / "repo"
    wrong_dir = repo_clone / ".agent-os" / "vendor" / "skill" / "wrong-asset"
    wrong_dir.mkdir(parents=True)
    (wrong_dir / "provenance.yaml").write_text(
        "asset_id: wrong-asset\nkind: skill\nvendored_file: SKILL.md\n",
        encoding="utf-8",
    )
    target_dir = repo_clone / ".agent-os" / "vendor" / "skill" / "plan-checkpoint-close"
    target_dir.mkdir(parents=True)
    (target_dir / "provenance.yaml").write_text(
        "asset_id: plan-checkpoint-close\nkind: skill\nvendored_file: missing.md\n",
        encoding="utf-8",
    )

    with pytest.raises(FileNotFoundError, match="Vendored asset path does not exist"):
        module.resolve_vendored_asset("plan-checkpoint-close", repo_clone, None)


def test_resolve_vendored_asset_rejects_missing_vendor_root_directly(
    repo_root: Path, tmp_path: Path
) -> None:
    module = load_module(
        "resolve_shared_asset", repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py"
    )

    with pytest.raises(FileNotFoundError, match="Vendored asset root not found"):
        module.resolve_vendored_asset("plan-checkpoint-close", tmp_path / "repo", None)


def test_resolve_vendored_asset_skips_kind_mismatch(repo_root: Path, tmp_path: Path) -> None:
    module = load_module(
        "resolve_shared_asset", repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py"
    )
    repo_clone = tmp_path / "repo"
    manifest_dir = repo_clone / ".agent-os" / "vendor" / "skill" / "plan-checkpoint-close"
    manifest_dir.mkdir(parents=True)
    (manifest_dir / "provenance.yaml").write_text(
        "asset_id: plan-checkpoint-close\nkind: prompt\nvendored_file: payload.txt\n",
        encoding="utf-8",
    )
    (manifest_dir / "payload.txt").write_text("payload\n", encoding="utf-8")

    with pytest.raises(FileNotFoundError, match="was not found"):
        module.resolve_vendored_asset("plan-checkpoint-close", repo_clone, "skill")


def test_resolve_vendored_asset_returns_manifest_data(repo_root: Path, tmp_path: Path) -> None:
    module = load_module(
        "resolve_shared_asset", repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py"
    )
    repo_clone = tmp_path / "repo"
    manifest_dir = repo_clone / ".agent-os" / "vendor" / "skill" / "plan-checkpoint-close"
    manifest_dir.mkdir(parents=True)
    (manifest_dir / "payload.txt").write_text("payload\n", encoding="utf-8")
    (manifest_dir / "provenance.yaml").write_text(
        "\n".join(
            [
                "asset_id: plan-checkpoint-close",
                "kind: skill",
                "version: '1.0.0'",
                "compatibility: [codex]",
                "depends_on_assets: [other]",
                "vendored_file: payload.txt",
                "source_registry_path: agent-os/skills/plan-checkpoint-close/SKILL.md",
                "source_registry_file: /tmp/registry.yaml",
                "source_control_plane_root: /tmp/control",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    result = module.resolve_vendored_asset("plan-checkpoint-close", repo_clone, "skill")

    assert result["asset_id"] == "plan-checkpoint-close"
    assert result["resolution_mode"] == "vendored"
    assert result["path"].endswith("payload.txt")


def test_emit_supports_shell_and_json_formats(repo_root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    module = load_module(
        "resolve_shared_asset", repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py"
    )
    result = {
        "asset_id": "plan-checkpoint-close",
        "kind": "skill",
        "version": "1",
        "path": "/tmp/asset",
        "registry_relative_path": "agent-os/skills/plan-checkpoint-close/SKILL.md",
        "registry_path": "/tmp/registry.yaml",
        "control_plane_root": "/tmp/control",
        "repo_root": "/tmp/repo",
        "resolution_mode": "workspace",
        "compatibility": ["codex", "claude"],
        "depends_on_assets": ["other"],
    }

    module.emit(result, "json")
    assert json.loads(capsys.readouterr().out)["asset_id"] == "plan-checkpoint-close"

    module.emit(result, "shell")
    shell_out = capsys.readouterr().out
    assert "ASSET_ID=plan-checkpoint-close" in shell_out
    assert "ASSET_COMPATIBILITY=codex,claude" in shell_out


def test_emit_supports_path_format(repo_root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    module = load_module(
        "resolve_shared_asset", repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py"
    )
    module.emit({"path": "/tmp/asset"}, "path")
    assert capsys.readouterr().out.strip() == "/tmp/asset"


def test_resolve_shared_asset_main_succeeds_in_process(
    repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    module = load_module(
        "resolve_shared_asset", repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py"
    )
    repo_clone = tmp_path / "repo"
    repo_clone.mkdir()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "resolve-shared-asset.py",
            "plan-checkpoint-close",
            "--control-plane-root",
            str(repo_root),
            "--repo-root",
            str(repo_clone),
            "--format",
            "path",
        ],
    )

    assert module.main() == 0
    assert "plan-checkpoint-close" in capsys.readouterr().out


def test_resolve_shared_asset_main_handles_missing_repo_root(
    repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    module = load_module(
        "resolve_shared_asset", repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py"
    )
    missing_root = tmp_path / "missing"
    monkeypatch.setattr(
        sys,
        "argv",
        ["resolve-shared-asset.py", "plan-checkpoint-close", "--repo-root", str(missing_root)],
    )

    assert module.main() == 2
    assert "repo_root not found" in capsys.readouterr().err


def test_resolve_shared_asset_main_handles_resolution_failure(
    repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    module = load_module(
        "resolve_shared_asset", repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py"
    )
    repo_clone = tmp_path / "repo"
    repo_clone.mkdir()
    monkeypatch.setattr(
        module,
        "resolve_vendored_asset",
        lambda *_args: (_ for _ in ()).throw(FileNotFoundError("vendored failure")),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "resolve-shared-asset.py",
            "plan-checkpoint-close",
            "--repo-root",
            str(repo_clone),
            "--resolution-mode",
            "vendored",
        ],
    )

    assert module.main() == 1
    assert "ERROR: vendored failure" in capsys.readouterr().err


def test_resolve_shared_asset_script_entrypoint_runs(
    repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_clone = tmp_path / "repo"
    repo_clone.mkdir()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "resolve-shared-asset.py",
            "plan-checkpoint-close",
            "--control-plane-root",
            str(repo_root),
            "--repo-root",
            str(repo_clone),
        ],
    )

    with pytest.raises(SystemExit) as exc:
        runpy.run_path(
            str(repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py"),
            run_name="__main__",
        )

    assert exc.value.code == 0
