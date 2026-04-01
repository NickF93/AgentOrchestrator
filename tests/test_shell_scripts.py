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
    copilot_instructions = target_repo / ".github" / "copilot-instructions.md"
    assert copilot_instructions.exists()
    copilot_text = copilot_instructions.read_text(encoding="utf-8")
    assert "thin runtime entrypoint" in copilot_text
    assert "AGENTS.md" in copilot_text
    assert "## Adapter Overrides" in copilot_text

    claude_md = target_repo / "CLAUDE.md"
    assert claude_md.exists()
    claude_text = claude_md.read_text(encoding="utf-8")
    assert "thin runtime entrypoint" in claude_text
    assert "AGENTS.md" in claude_text
    assert "## Adapter Overrides" in claude_text

    codex_file = target_repo / ".codex"
    assert codex_file.exists()
    codex_text = codex_file.read_text(encoding="utf-8")
    assert "thin runtime entrypoint for Codex" in codex_text
    assert "AGENTS.md" in codex_text
    assert "AGENT_PYTHON" in codex_text
    assert "Canonical authority is bounded in" in codex_text

    gemini_file = target_repo / "GEMINI.md"
    assert gemini_file.exists()
    gemini_text = gemini_file.read_text(encoding="utf-8")
    assert "thin runtime entrypoint" in gemini_text
    assert "AGENTS.md" in gemini_text
    assert "## Adapter Overrides" in gemini_text

    cursor_rules = target_repo / ".cursor" / "rules" / "governance.mdc"
    assert cursor_rules.exists()
    cursor_text = cursor_rules.read_text(encoding="utf-8")
    assert "thin runtime entrypoint" in cursor_text
    assert "AGENTS.md" in cursor_text
    assert "## Adapter Overrides" in cursor_text

    kilo_rules = target_repo / ".kilocode" / "rules" / "governance.md"
    assert kilo_rules.exists()
    kilo_text = kilo_rules.read_text(encoding="utf-8")
    assert "thin runtime entrypoint" in kilo_text
    assert "AGENTS.md" in kilo_text
    assert "## Adapter Overrides" in kilo_text


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

    workspace_claude = (workspace_root / "CLAUDE.md").read_text(encoding="utf-8")
    assert "CONTROL_PLANE_ROOT:" in workspace_claude
    assert str(repo_root) in workspace_claude
    assert "## Adapter Overrides" in workspace_claude

    workspace_codex = (workspace_root / ".codex").read_text(encoding="utf-8")
    assert "CONTROL_PLANE_ROOT:" in workspace_codex
    assert str(repo_root) in workspace_codex
    assert "thin workspace runtime entrypoint for Codex" in workspace_codex
    assert "AGENT_PYTHON" in workspace_codex

    assert not (workspace_root / "GEMINI.md").exists()
    assert not (workspace_root / ".cursor").exists()
    assert not (workspace_root / ".github").exists()
    assert not (workspace_root / ".kilocode").exists()
    assert not (workspace_root / "KILO.md").exists()


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
