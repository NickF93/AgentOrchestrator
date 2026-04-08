from __future__ import annotations

import subprocess
from pathlib import Path

from conftest import run_shell_script

ZERO_OID = "0000000000000000000000000000000000000000"


def run_hook(
    script_path: Path,
    *args: str,
    cwd: Path | None = None,
    stdin: str = "",
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(script_path), *args],
        cwd=cwd,
        input=stdin,
        text=True,
        capture_output=True,
        check=False,
    )


def git_ok(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout.strip()


def init_hook_repo(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "hook-repo"
    repo.mkdir(parents=True)
    git_ok(repo, "init")
    git_ok(repo, "config", "user.name", "Tester")
    git_ok(repo, "config", "user.email", "tester@example.com")
    git_ok(repo, "checkout", "-b", "feature/test")
    (repo / "README.md").write_text("initial\n", encoding="utf-8")
    git_ok(repo, "add", "README.md")
    git_ok(repo, "commit", "-m", "docs(repo): initial commit", "-m", "Refs: D1.1.1, cg1")
    return repo, git_ok(repo, "rev-parse", "HEAD")


def commit_file(repo: Path, relative_path: str, content: str, title: str, body: str) -> str:
    path = repo / relative_path
    path.write_text(content, encoding="utf-8")
    git_ok(repo, "add", relative_path)
    git_ok(repo, "commit", "-m", title, "-m", body)
    return git_ok(repo, "rev-parse", "HEAD")


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
    assert "plan/PLAN-index.yaml" in result.stdout
    assert "plan/archive" in result.stdout
    assert ".githooks/pre-push" in result.stdout
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
    assert (target_repo / "plan" / "PLAN-index.yaml").exists()
    assert (target_repo / "plan" / "PLAN-current.yaml").exists()
    assert (target_repo / "plan" / "archive").is_dir()
    assert not (target_repo / "PLAN.yaml").exists()
    assert (target_repo / ".githooks" / "commit-msg").exists()
    assert (target_repo / ".githooks" / "pre-push").exists()
    assert (target_repo / ".githooks" / "commit-msg").stat().st_mode & 0o111
    assert (target_repo / ".githooks" / "pre-push").stat().st_mode & 0o111

    readme_text = (target_repo / "README.md").read_text(encoding="utf-8")
    assert ".githooks/commit-msg" in readme_text
    assert ".githooks/pre-push" in readme_text
    assert "AGENT_PYTHON" in readme_text

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
    assert "plan/PLAN-index.yaml" in claude_text
    assert "## Adapter Overrides" in claude_text

    codex_file = target_repo / ".codex"
    assert codex_file.exists()
    codex_text = codex_file.read_text(encoding="utf-8")
    assert "thin runtime entrypoint for Codex" in codex_text
    assert "AGENTS.md" in codex_text
    assert "AGENT_PYTHON" in codex_text
    assert "plan/PLAN-index.yaml" in codex_text
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

    kilo_rules = target_repo / ".kilo" / "rules" / "governance.md"
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
    assert not (workspace_root / ".kilo").exists()
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


def test_commit_msg_hook_allows_human_coauthor_and_rejects_ai_markers(
    repo_root: Path, tmp_path: Path
) -> None:
    hook = repo_root / ".githooks" / "commit-msg"

    valid_msg = tmp_path / "valid-msg.txt"
    valid_msg.write_text(
        "docs(repo): valid message\n\n"
        "Co-authored-by: Jane Example <jane@example.com>\n"
        "Refs: D1.1.1, cg1\n",
        encoding="utf-8",
    )
    valid_result = run_hook(hook, str(valid_msg), cwd=repo_root)
    assert valid_result.returncode == 0, valid_result.stdout + valid_result.stderr

    ai_coauthor_msg = tmp_path / "ai-coauthor-msg.txt"
    ai_coauthor_msg.write_text(
        "docs(repo): invalid message\n\n"
        "Co-Authored-By: Claude Opus 4.1 <noreply@anthropic.com>\n"
        "Refs: D1.1.1, cg1\n",
        encoding="utf-8",
    )
    ai_coauthor_result = run_hook(hook, str(ai_coauthor_msg), cwd=repo_root)
    assert ai_coauthor_result.returncode == 1
    assert "forbidden AI/codegen attribution markers" in ai_coauthor_result.stderr

    generated_msg = tmp_path / "generated-msg.txt"
    generated_msg.write_text(
        "docs(repo): invalid message\n\nGenerated by ChatGPT\nRefs: D1.1.1, cg1\n",
        encoding="utf-8",
    )
    generated_result = run_hook(hook, str(generated_msg), cwd=repo_root)
    assert generated_result.returncode == 1
    assert "forbidden AI/codegen attribution markers" in generated_result.stderr


def test_pre_push_hook_rejects_direct_push_to_protected_branch(
    repo_root: Path, tmp_path: Path
) -> None:
    hook = repo_root / ".githooks" / "pre-push"
    repo, initial_sha = init_hook_repo(tmp_path)

    result = run_hook(
        hook,
        "origin",
        "https://example.invalid/repo.git",
        cwd=repo,
        stdin=f"refs/heads/main {initial_sha} refs/heads/main {ZERO_OID}\n",
    )
    assert result.returncode == 1
    assert "Direct pushes to main and develop are forbidden" in result.stderr


def test_pre_push_hook_rejects_ai_markers_and_allows_clean_topic_push(
    repo_root: Path, tmp_path: Path
) -> None:
    hook = repo_root / ".githooks" / "pre-push"

    clean_repo, clean_base = init_hook_repo(tmp_path / "clean")
    clean_sha = commit_file(
        clean_repo,
        "notes.txt",
        "clean text\n",
        "docs(repo): add notes",
        "Refs: D1.1.2, cg1",
    )
    clean_result = run_hook(
        hook,
        "origin",
        "https://example.invalid/repo.git",
        cwd=clean_repo,
        stdin=(f"refs/heads/feature/test {clean_sha} refs/heads/feature/test {clean_base}\n"),
    )
    assert clean_result.returncode == 0, clean_result.stdout + clean_result.stderr

    message_repo, message_base = init_hook_repo(tmp_path / "message")
    message_sha = commit_file(
        message_repo,
        "notes.txt",
        "clean text\n",
        "docs(repo): add notes",
        "Co-Authored-By: Claude Opus 4.1 <noreply@anthropic.com>\n\nRefs: D1.1.2, cg1",
    )
    message_result = run_hook(
        hook,
        "origin",
        "https://example.invalid/repo.git",
        cwd=message_repo,
        stdin=(f"refs/heads/feature/test {message_sha} refs/heads/feature/test {message_base}\n"),
    )
    assert message_result.returncode == 1
    assert "Commit message in" in message_result.stderr

    added_repo, added_base = init_hook_repo(tmp_path / "added")
    added_sha = commit_file(
        added_repo,
        "notes.txt",
        "# Generated by ChatGPT\n",
        "docs(repo): add notes",
        "Refs: D1.1.2, cg1",
    )
    added_result = run_hook(
        hook,
        "origin",
        "https://example.invalid/repo.git",
        cwd=added_repo,
        stdin=(f"refs/heads/feature/test {added_sha} refs/heads/feature/test {added_base}\n"),
    )
    assert added_result.returncode == 1
    assert "Added lines in" in added_result.stderr
