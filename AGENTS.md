# AGENTS.md

## Scope
This repository is the Level-0 control-plane OS for coding-agent governance.
It does not host product code. It hosts shared workflow, taxonomy, templates,
schemas, and scripts used to bootstrap and coordinate other repositories.

## Authority Map
- Workflow and governance model: `agent-os/workflow/*`
- Plan schema contract: `agent-os/schemas/plan.schema.json`
- Repo bootstrap templates: `agent-os/templates/*`
- Operational tooling: `agent-os/scripts/*`
- Active execution tracking for this repository: `PLAN.yaml`
- Design/background references (non-authoritative): `docs/design/*`
- Structural constraints for this repository: `ARCHITECTURE.md`

## Canonical Source Rule
One concern must have one canonical authority. Do not duplicate normative content
across files.

Priority order:
1. Explicit human instructions
2. This file for workflow authority and operating rules
3. `ARCHITECTURE.md` for structural and boundary constraints
4. `PLAN.yaml` for active execution tracking
5. Code and tests as implementation evidence
6. Generated plan views (`PLAN.md`, `PLAN.dot`) as non-authoritative outputs

## Working Rules
- Treat `PLAN.yaml` as source of truth for planning status and dependencies.
- Before modifying any non-generated repository file, create or update the
  owning `PLAN.yaml` item first. The item MUST already declare the intended
  `commit_group`, relevant `scope`, and expected artifacts. Untracked edits are
  forbidden.
- Do not invent or reshuffle `commit_group` boundaries during commit creation.
  `commit_group` membership is declared in `PLAN.yaml` before implementation
  starts and is the mandatory git commit boundary.
- Keep startup/design documents in `docs/design/`; do not use them as runtime authority.
- Do not hand-edit generated artifacts (`PLAN.md`, `PLAN.dot`) once render scripts exist.
- Preserve determinism in generated outputs and script behavior.
- Prefer additive, minimal changes with explicit checkpoints.
- **Mandatory commit rule**: every `commit_group` MUST be committed to git
  immediately upon completion. Do NOT proceed to the next commit_group
  without committing the current one. This is a hard gate.

## Skills

Operational skills are in `agent-os/skills/`. When a skill's trigger
conditions match the current task, read the relevant `SKILL.md` and follow
its procedure. Skills are procedural — they apply existing governance rules
and must not override or redefine them.

### Available Skills

| Skill ID | Path | Triggers on |
|----------|------|-------------|
| `plan-checkpoint-close` | `agent-os/skills/plan-checkpoint-close/SKILL.md` | Closing a checkpoint, finalizing a commit_group, verifying closure readiness |
| `gitflow-pr-only` | `agent-os/skills/gitflow-pr-only/SKILL.md` | Starting a branch (feature, bugfix, hotfix, release, support), synchronizing a topic branch, merging a PR, tagging a release/hotfix, performing a back-merge |
| `repo-bootstrap` | `agent-os/skills/repo-bootstrap/SKILL.md` | Bootstrapping a new repo, scaffolding governance files, checking if a repo is already bootstrapped |
| `plan-validate-render` | `agent-os/skills/plan-validate-render/SKILL.md` | Validating a plan, rendering plan views, checking for plan drift, interpreting validation warnings or errors, verifying generated plan artifacts are up to date |

## Commit Message Contract
All commits MUST use this format:

`<type>(<scope>): <description>`

Tracked work MUST include a `Refs:` footer that lists the PLAN item IDs closed
by the commit and exactly one `commit_group` ID.

Canonical format:

`Refs: D5.1.1, D5.1.2, C5.1.3, cg20`

Body sections SHOULD be included, especially for medium or large
commits. Recommended structure:

Body (SHOULD):

- Summary: what changed and why
- Scope: affected canonical areas/files
- Items: referenced PLAN item IDs
- Validation: checks run / outcomes

Footer (SHOULD):

- Refs: PLAN item IDs and exactly one commit_group ID
- ADR: linked ADR if relevant
- Follow-up: deferred work if applicable

Valid examples:
- `docs(workflow): split shared workflow into canonical files`
- `feat(scripts): add deterministic PLAN renderer`
- `chore(repo): move startup docs under docs/design`

## Escalation and Stop Conditions
Stop and ask the human owner when:
- A change would alter authority boundaries,
- A conflict exists between `ARCHITECTURE.md` and `PLAN.yaml`,
- A canonical-authority conflict cannot be resolved by regeneration from source,
- A schema change would invalidate existing plan data,
- A workflow policy implies irreversible Git automation beyond current phase.

## Layer-0 Build Context
Current implementation focus is Layer-0 foundation:
- `agent-os/workflow/`
- `agent-os/schemas/`
- `agent-os/templates/`
- `agent-os/scripts/`
- `agent-os/prompts/` and `agent-os/skills/` contracts/scaffolds
