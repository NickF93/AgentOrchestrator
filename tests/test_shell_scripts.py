from __future__ import annotations

from pathlib import Path

from conftest import run_shell_script


def test_bootstrap_repo_dry_run_reports_creates(
    repo_root: Path,
    tmp_path: Path,
    script_env: dict[str, str],
) -> None:
    target_repo = tmp_path / "BootRepo"
    result = run_shell_script(
        repo_root / "agent-os" / "scripts" / "bootstrap-repo.sh",
        "--dry-run",
        "--owner",
        "tester",
        "--ref",
        "main",
        str(target_repo),
        env=script_env,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "DRY-RUN: create" in result.stdout
    assert not target_repo.exists()


def test_bootstrap_repo_creates_expected_files(
    repo_root: Path,
    tmp_path: Path,
    script_env: dict[str, str],
) -> None:
    target_repo = tmp_path / "BootRepo"
    result = run_shell_script(
        repo_root / "agent-os" / "scripts" / "bootstrap-repo.sh",
        "--owner",
        "tester",
        "--ref",
        "main",
        str(target_repo),
        env=script_env,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert (target_repo / "AGENTS.md").exists()
    assert (target_repo / "PLAN.yaml").exists()
    assert (target_repo / ".githooks" / "commit-msg").exists()


def test_sync_workspace_stamps_control_plane_root(
    repo_root: Path,
    tmp_path: Path,
    script_env: dict[str, str],
) -> None:
    workspace_root = tmp_path / "workspace"
    result = run_shell_script(
        repo_root / "agent-os" / "scripts" / "sync-workspace.sh",
        str(workspace_root),
        env=script_env,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    workspace_agents = (workspace_root / "AGENTS.md").read_text(encoding="utf-8")
    assert "CONTROL_PLANE_ROOT:" in workspace_agents
    assert str(repo_root) in workspace_agents


def test_materialize_shared_asset_writes_snapshot_and_provenance(
    repo_root: Path,
    tmp_path: Path,
    script_env: dict[str, str],
) -> None:
    target_repo = tmp_path / "standalone-repo"
    target_repo.mkdir()

    result = run_shell_script(
        repo_root / "agent-os" / "scripts" / "materialize-shared-asset.sh",
        "--control-plane-root",
        str(repo_root),
        "--repo-root",
        str(target_repo),
        "checkpoint-closure-review",
        env=script_env,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    vendored_file = (
        target_repo
        / ".agent-os"
        / "vendor"
        / "prompt"
        / "checkpoint-closure-review"
        / "checkpoint-closure-review.md"
    )
    provenance = (
        target_repo
        / ".agent-os"
        / "vendor"
        / "prompt"
        / "checkpoint-closure-review"
        / "provenance.yaml"
    )
    assert vendored_file.exists()
    assert provenance.exists()
    provenance_text = provenance.read_text(encoding="utf-8")
    assert "asset_id: checkpoint-closure-review" in provenance_text
    assert "vendored_file: checkpoint-closure-review.md" in provenance_text
