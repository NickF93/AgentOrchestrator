# TODO — Personal Checklist

> Not normative. Not governance. Not for agents.
> Just a human-readable reminder of what's done and what's next.

---

## Control Plane Foundation (Level 0)

- [x] Workflow model, lifecycle, taxonomy, git policy
- [x] PLAN schema + validator + renderer
- [x] Governance hardening (authority model, DAG rules, automation policy)
- [x] Canonical consistency and tracking discipline
- [x] Planning model execution optimization
- [x] Commit hook enforcement and runtime alignment
- [x] Local quality gates (ruff, mypy, pytest, shellcheck)
- [x] Environment portability — AGENT_PYTHON env var, .env per workstation

## Runtime Portability

- [x] Runtime lifecycle tiers (experimental / supported / first-class)
- [x] Claude — first-class (adapter, profile, workspace template, sync)
- [x] Codex — first-class (adapter, profile, workspace template, sync)
- [x] Kilo — supported (profile-driven, uses AGENTS.md as entrypoint)
- [x] Copilot — supported (repo-local .github/copilot-instructions.md)
- [ ] Extend adapters for Kilo and Copilot (promote toward first-class when ready)

## Skills

- [x] plan-checkpoint-close — closing C items with validations and commit closure
- [ ] gitflow-pr-only — procedural PR-based git flow (strongest candidate)
- [ ] repo-bootstrap — wrapper around bootstrap-repo.sh + post-bootstrap checks
- [ ] workspace-sync — regenerate Level-1 files, report provenance drift
- [ ] plan-validate-render — validate + render + interpret failures/warnings
- [ ] repo-map-refresh — refresh REPO_MAP.md on triggers
- [ ] checker-reviewer-delegation — delegation contract (needs design first)

## Git Flow

- [ ] Define and document the git branching/PR workflow
- [ ] Implement gitflow-pr-only skill

## Shared Asset Distribution

- [x] Registry, prompts, profiles, protocols model
- [x] Two-root consumption (control_plane_root / repo_root)
- [x] materialize-shared-asset.sh for vendoring into repos
- [ ] Ensure sharing works end-to-end across Layer 0 and Layer 2

## Layer 1 — Workspace Runtime

- [x] sync-workspace.sh renders AGENTS.md, CLAUDE.md, .codex
- [x] Workspace templates with {{CONTROL_PLANE_ROOT}} placeholders
- [ ] Harden Layer-1 lifecycle (drift detection, staleness checks)
- [ ] Evaluate workspace template needs for Kilo and Copilot

## Layer 2 — Repository-Local Governance

- [x] bootstrap-repo.sh scaffolds AGENTS.md, PLAN.yaml, commit hook, copilot-instructions
- [ ] End-to-end bootstrap + governance validation in a real downstream repo
- [ ] Verify Layer-2 repos can consume shared assets cleanly

## Multi-Agent / Sub-Agent

- [ ] Coordination layer design (protocol-ready at adapter layer, not implemented)
- [ ] Delegation contract between checker/reviewer agents
- [ ] Sub-agent orchestration model

## RFC — Request for Comments / Future Considerations

- [ ] RFC normative review pass (ensure no stale or conflicting normative content)
