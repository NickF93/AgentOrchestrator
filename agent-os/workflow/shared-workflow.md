# Shared Workflow

## Purpose
Define the cross-repository operating workflow for coding agents with strict
separation between governance concerns.

## Three-Layer Model
1. Level 0: central control plane repository (this repository)
2. Level 1: workspace runtime materialization
3. Level 2: repository-local governance and execution files

## Canonical Concern Split

One concern must have exactly one canonical authority. Duplication is forbidden.

| Concern | Canonical Authority |
|---|---|
| Agentic workflow and operating rules | `AGENTS.md` |
| Software constraints, boundaries, and design invariants | `ARCHITECTURE.md` or `docs/architecture/*` |
| Active execution tracking | `PLAN.yaml` |
| Human-readable plan view | `PLAN.md` (generated) |
| Graph plan view | `PLAN.dot` / `PLAN.svg` (generated) |
| Decision rationale | `docs/adr/*` |
| Practical codebase map | `REPO_MAP.md` |
| Shared templates, schemas, and cross-repo policy | Level-0 (`agent-os/`) |

## Authority Precedence

Priority order for conflict resolution:
1. Explicit human instructions
2. `AGENTS.md` — workflow authority and operating rules
3. `ARCHITECTURE.md` / `docs/architecture/*` — software constraints
4. `PLAN.yaml` — active execution tracking
5. Code, tests, and real artifacts — implementation evidence
6. Generated views (`PLAN.md`, `PLAN.dot`) — informative, not authoritative

## Non-Duplication Rule

- `AGENTS.md` may reference `ARCHITECTURE.md` but must not duplicate its detailed content.
- `PLAN.yaml` may reference architectural decisions but must not become a technical constitution.
- `PLAN.md` and `PLAN.dot` must contain only content derivable from `PLAN.yaml`.
- Each concern lives in exactly one authority; cross-referencing is allowed, copying is not.

## Planning and Execution
- Human planning model: milestone -> sprint -> item
- Runtime execution model: dependency-driven and scope-aware
- Single-writer rule: one orchestrator agent owns and writes the canonical PLAN source;
  other agents may propose changes or produce evidence but must not write directly to the canonical PLAN.

Execution predicate:
- Item is executable when all dependencies are in verified or done state

## Parallelism Rules
Parallel execution is allowed only when:
- dependencies are satisfied,
- scopes are compatible,
- there is no boundary conflict,
- resulting commit groups remain reviewable.

## Grouping Rule

An agent may group compatible items into a shared commit_group if:
- the group is semantically coherent,
- required checks for all items are compatible,
- a reviewer can evaluate the group without losing item-level traceability.

## Collision Rule

Items must NOT be grouped together if:
- they touch the same sensitive scope with conflicting intent,
- they require separate human decisions,
- they produce incompatible evidence.

## Commit and Checkpoint Policy
- Use commit_group as natural commit boundary.
- Close a commit_group only when its items satisfy required checks.
- Keep traceability from item -> evidence -> commit.
- Enforce commit message format on all repositories governed by Layer-0:
	`<type>(<scope>): <description>`

Optional body and footer sections are strongly suggested, especially for medium or large commits.

## Automation Staging
- Phase A: branch naming, local commits, plan updates, view rendering
- Phase B: push, draft PR, develop alignment
- Phase C: controlled merge automation
- Phase D: hygiene automation

## Governance Asset Lifecycles

### prompts/
- Canonical format: Markdown with YAML frontmatter.
- Required frontmatter fields: `id`, `role`, `purpose`, `owner`, `version`, `status`.
- Allowed `status` values: `draft`, `active`, `deprecated`, `superseded`.
- Versioning: semantic (`major.minor.patch`) and incremented on normative behavior changes.
- Update triggers: workflow policy change, taxonomy/lifecycle change, or tool-adapter contract change.

### skills/
- Canonical package format: `SKILL.md` with YAML frontmatter + markdown body.
- Required frontmatter fields: `id`, `description`, `owner`, `version`, `compatibility`.
- `compatibility` must declare neutral-core support and optional adapter notes.
- Skills must not redefine canonical taxonomy or authority boundaries.

### REPO_MAP.md freshness
- Ownership: orchestrator maintains freshness; implementers/reviewers may propose deltas.
- Required metadata: `last_validated_on`, `validated_by`, `freshness_window_days`.
- Refresh triggers: module/entry-point changes, boundary changes, test topology changes,
  and each release checkpoint.

### ADR lifecycle
- Numbering: `ADR-0001`, `ADR-0002`, ... (zero-padded incremental sequence).
- States: `proposed`, `accepted`, `superseded`, `deprecated`.
- ADRs must link to relevant PLAN decision or implementation items.

## Design Document Governance

- `docs/design/` is non-authoritative reference material. Files in this
  directory capture brainstorming, reviews, and background reasoning.
- If a design document introduces a normative rule (a constraint, policy,
  or procedure that agents must follow), that rule MUST be migrated to the
  appropriate canonical authority (`AGENTS.md`, `ARCHITECTURE.md`,
  `agent-os/workflow/*`, or `agent-os/schemas/*`) before it is considered
  binding.
- A design document that has not been migrated carries no governance weight.
  Agents should not treat design docs as executable instructions.
- When migrating a rule, add a note in the design doc indicating the rule
  has been superseded by the canonical authority reference.

## Canonical-Authority Conflict Recovery

Conflict examples:
- non-canonical edits made to generated files (`PLAN.md`, `PLAN.dot`),
- workflow policy edits made outside canonical authority,
- divergent duplicated normative rules across authorities.

Required recovery procedure:
1. Detect conflict (validator checks, render drift, or review finding).
2. Quarantine non-canonical edits (do not merge; preserve for inspection only).
3. Restore canonical state from source authority and regenerate derived artifacts.
4. Record incident in PLAN notes/checkpoint context.
5. Escalate to human owner if authority boundaries are ambiguous.

## Phase B Safety Gate

Before enabling Phase B automation, all conditions below MUST be true:
- canonical-authority conflict recovery procedure is documented and active,
- no unresolved authority conflicts exist in working state,
- generated artifacts are fully reproducible from canonical sources,
- escalation path for boundary conflicts is tested.
