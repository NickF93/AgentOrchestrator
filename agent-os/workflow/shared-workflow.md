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
	`<type>(<scope>): [item ID] <description>`

Optional body and footer sections are strongly suggested, especially for medium or large commits.

## Automation Staging
- Phase A: branch naming, local commits, plan updates, view rendering
- Phase B: push, draft PR, develop alignment
- Phase C: controlled merge automation
- Phase D: hygiene automation
