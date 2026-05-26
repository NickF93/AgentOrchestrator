from __future__ import annotations

import json
from pathlib import Path

from conftest import run_python_script, run_shell_script


def test_shared_asset_l0_to_l2_workspace_and_vendored_flow(
    repo_root: Path,
    tmp_path: Path,
    script_env: dict[str, str],
) -> None:
    workspace_root = tmp_path / "workspace"
    layer2_repo = workspace_root / "Layer2Repo"

    sync = run_shell_script(
        repo_root / "agent-os" / "scripts" / "sync-workspace.sh",
        str(workspace_root),
        env=script_env,
    )
    assert sync.returncode == 0, sync.stdout + sync.stderr

    workspace_agents = (workspace_root / "AGENTS.md").read_text(encoding="utf-8")
    assert f"CONTROL_PLANE_ROOT: {repo_root}" in workspace_agents
    assert "materialize-shared-asset.sh" in workspace_agents

    bootstrap = run_shell_script(
        repo_root / "agent-os" / "scripts" / "bootstrap-repo.sh",
        "--owner",
        "tester",
        "--ref",
        "test-ref",
        str(layer2_repo),
        env=script_env,
    )
    assert bootstrap.returncode == 0, bootstrap.stdout + bootstrap.stderr

    assert (layer2_repo / "plan" / "archive" / ".gitkeep").exists()
    assert (layer2_repo / ".codex" / "config.toml").exists()

    layer2_agents = (layer2_repo / "AGENTS.md").read_text(encoding="utf-8")
    assert "Operational skills are resolved as shared assets" in layer2_agents
    assert "Layer-2 copies of shared assets are never authoritative" in layer2_agents

    claude_entrypoint = (layer2_repo / "CLAUDE.md").read_text(encoding="utf-8")
    assert "thin runtime entrypoint" in claude_entrypoint
    assert "AGENTS.md" in claude_entrypoint

    workspace_resolution = run_python_script(
        repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py",
        "plan-checkpoint-close",
        "--repo-root",
        str(layer2_repo),
        "--format",
        "json",
    )
    assert workspace_resolution.returncode == 0, (
        workspace_resolution.stdout + workspace_resolution.stderr
    )
    workspace_result = json.loads(workspace_resolution.stdout)
    assert workspace_result["asset_id"] == "plan-checkpoint-close"
    assert workspace_result["kind"] == "skill"
    assert workspace_result["resolution_mode"] == "workspace"
    assert workspace_result["control_plane_root"] == str(repo_root)
    assert workspace_result["repo_root"] == str(layer2_repo.resolve())
    assert workspace_result["path"].endswith("agent-os/skills/plan-checkpoint-close/SKILL.md")

    materialize = run_shell_script(
        repo_root / "agent-os" / "scripts" / "materialize-shared-asset.sh",
        "--repo-root",
        str(layer2_repo),
        "plan-checkpoint-close",
        env=script_env,
    )
    assert materialize.returncode == 0, materialize.stdout + materialize.stderr

    vendored_asset = (
        layer2_repo / ".agent-os" / "vendor" / "skill" / "plan-checkpoint-close" / "SKILL.md"
    )
    provenance = vendored_asset.with_name("provenance.yaml")
    assert vendored_asset.exists()
    assert provenance.exists()

    provenance_text = provenance.read_text(encoding="utf-8")
    assert "asset_id: plan-checkpoint-close" in provenance_text
    assert "kind: skill" in provenance_text
    assert f"source_control_plane_root: {repo_root}" in provenance_text

    vendored_resolution = run_python_script(
        repo_root / "agent-os" / "scripts" / "resolve-shared-asset.py",
        "plan-checkpoint-close",
        "--repo-root",
        str(layer2_repo),
        "--resolution-mode",
        "vendored",
        "--format",
        "json",
    )
    assert vendored_resolution.returncode == 0, (
        vendored_resolution.stdout + vendored_resolution.stderr
    )
    vendored_result = json.loads(vendored_resolution.stdout)
    assert vendored_result["asset_id"] == "plan-checkpoint-close"
    assert vendored_result["resolution_mode"] == "vendored"
    assert vendored_result["path"] == str(vendored_asset.resolve())
    assert vendored_result["control_plane_root"] == str(repo_root)
