# X51 Shared Asset L0 to L2 Validation Evidence

Date: 2026-05-26

Issue: <https://github.com/NickF93/AgentOrchestrator/issues/17>

Control-plane PR: <https://github.com/NickF93/AgentOrchestrator/pull/41>

This document is non-authoritative validation evidence. Governance authority
remains in `AGENTS.md`, `ARCHITECTURE.md`, and `agent-os/workflow/*`.

## Verdict

Pass.

Shared asset consumption was validated through both a hermetic automated test
and a disposable local clone of `AgentOrchestrator-Test`. The validation covered
workspace-mode discovery from Layer 2, explicit vendoring into `.agent-os/vendor/`,
and vendored-mode resolution from the materialized snapshot.

No target-repo PR was opened. No changes were made to the real
`AgentOrchestrator-Test` checkout.

## Environment

- `control_plane_root`: `/home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator`
- Feature branch: `feature/X51-shared-assets-l0-l2-validation`
- Control-plane commit used for validation: `f435ec4`
- Source downstream checkout: `/home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator-Test`
- Disposable workspace: `/tmp/ao-x51-real-validation.cQ1LNR`
- Disposable repo clone: `/tmp/ao-x51-real-validation.cQ1LNR/AgentOrchestrator-Test`

## Hermetic Test

Command:

```bash
python3 -m pytest -q tests/test_shared_asset_e2e.py
```

Result:

```text
.                                                                        [100%]
```

The test performs the following flow in a temporary workspace:

- run `sync-workspace.sh`
- bootstrap a temporary Layer-2 repo with `bootstrap-repo.sh`
- verify Layer-2 runtime entrypoints delegate to `AGENTS.md`
- resolve `plan-checkpoint-close` in workspace mode without explicit
  `--control-plane-root`
- materialize `plan-checkpoint-close` into `.agent-os/vendor/`
- resolve the vendored snapshot in `vendored` mode

## Disposable Real-Repo Transcript

Clone the existing downstream repo into a disposable workspace:

```bash
git clone /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator-Test \
  /tmp/ao-x51-real-validation.cQ1LNR/AgentOrchestrator-Test
```

Result:

```text
Cloning into '/tmp/ao-x51-real-validation.cQ1LNR/AgentOrchestrator-Test'...
done.
```

Sync workspace runtime files:

```bash
bash agent-os/scripts/sync-workspace.sh /tmp/ao-x51-real-validation.cQ1LNR
```

Result summary:

```text
INFO:   root: /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator
INFO:   ref: feature/X51-shared-assets-l0-l2-validation
INFO:   commit: f435ec4
OK: generated /tmp/ao-x51-real-validation.cQ1LNR/AGENTS.md
OK: generated /tmp/ao-x51-real-validation.cQ1LNR/CLAUDE.md
OK: generated /tmp/ao-x51-real-validation.cQ1LNR/.codex/config.toml
INFO: shared assets resolve from CONTROL_PLANE_ROOT in workspace mode
INFO: vendoring remains optional and explicit via materialize-shared-asset.sh
```

Resolve a shared skill from the disposable Layer-2 clone in workspace mode:

```bash
python3 agent-os/scripts/resolve-shared-asset.py plan-checkpoint-close \
  --repo-root /tmp/ao-x51-real-validation.cQ1LNR/AgentOrchestrator-Test \
  --format json
```

Result summary:

```text
asset_id: plan-checkpoint-close
kind: skill
resolution_mode: workspace
control_plane_root: /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator
path: /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator/agent-os/skills/plan-checkpoint-close/SKILL.md
```

Materialize the same skill into the disposable Layer-2 clone:

```bash
bash agent-os/scripts/materialize-shared-asset.sh \
  --repo-root /tmp/ao-x51-real-validation.cQ1LNR/AgentOrchestrator-Test \
  plan-checkpoint-close
```

Result:

```text
OK: materialized plan-checkpoint-close to /tmp/ao-x51-real-validation.cQ1LNR/AgentOrchestrator-Test/.agent-os/vendor/skill/plan-checkpoint-close
OK: wrote provenance /tmp/ao-x51-real-validation.cQ1LNR/AgentOrchestrator-Test/.agent-os/vendor/skill/plan-checkpoint-close/provenance.yaml
```

Resolve the materialized snapshot in vendored mode:

```bash
python3 agent-os/scripts/resolve-shared-asset.py plan-checkpoint-close \
  --repo-root /tmp/ao-x51-real-validation.cQ1LNR/AgentOrchestrator-Test \
  --resolution-mode vendored \
  --format json
```

Result summary:

```text
asset_id: plan-checkpoint-close
kind: skill
resolution_mode: vendored
control_plane_root: /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator
path: /tmp/ao-x51-real-validation.cQ1LNR/AgentOrchestrator-Test/.agent-os/vendor/skill/plan-checkpoint-close/SKILL.md
```

Working-tree checks:

```text
Disposable clone status after materialization: ?? .agent-os/
Real AgentOrchestrator-Test checkout status: ## main...origin/main
```

## Findings

- Workspace-mode shared asset resolution works from a Layer-2 repo through
  the workspace `CONTROL_PLANE_ROOT` stamp.
- Explicit materialization writes the expected `.agent-os/vendor/skill/<id>/`
  snapshot and provenance file.
- Vendored-mode resolution reads the materialized snapshot and retains source
  control-plane provenance.
- Runtime-entrypoint consumption remains thin: Layer-2 `CLAUDE.md` points back
  to `AGENTS.md`, and `AGENTS.md` declares shared-asset resolution rules.
- No root-cause remediation was needed for #17.
