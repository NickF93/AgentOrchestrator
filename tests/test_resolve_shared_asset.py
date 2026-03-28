from __future__ import annotations

from pathlib import Path

from conftest import run_python_script, run_shell_script


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
