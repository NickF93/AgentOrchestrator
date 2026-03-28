# Lifecycle Model

## Objective
Define consistent status semantics and transition rules for plan items.

## Status Semantics
- planned: item exists but is not ready to run
- ready: dependencies and prerequisites are satisfied
- in_progress: active execution
- blocked: temporarily halted by external dependency or decision gate
- review: implementation complete, pending assessment
- verified: all required checks passed
- done: closed administratively after verification

## Transition Rules
Primary forward transitions:
- planned -> ready
- ready -> in_progress
- in_progress -> review
- review -> verified
- verified -> done

Blocked side-state:
- ready -> blocked
- in_progress -> blocked
- review -> blocked
- blocked -> ready

## Dependency Rule
An item can move to ready only if all items listed in depends_on are in
verified or done state.

## Container Rule
Container types (X, S) are non-executable and must not be used as dependency
targets for executable items.

## Scope Collision Guidance
Scope is a repository-relative path prefix.
If two in_progress items share a prefix, emit a warning and require explicit
orchestrator confirmation before parallel execution.

## Commit Group Closure
A commit group can close when:
- all included items are review, verified, or done,
- required checks are green,
- resulting diff is semantically coherent and reviewable.

## Governance Freshness Checks

### REPO_MAP Freshness Mechanism

REPO_MAP.md includes three metadata fields for freshness tracking:

- `last_validated_on`: ISO date when the map was last confirmed accurate.
- `validated_by`: identifier of the agent or person who validated.
- `freshness_window_days`: maximum allowed age in days before the map is stale.

**Freshness computation**: the map is stale when
`today - last_validated_on > freshness_window_days`.

**Refresh triggers** (any of these requires a freshness update):

- Any change to entry points, module boundaries, or critical interfaces.
- Any test topology change (unit/integration/e2e layout).
- Release and checkpoint closure.
- Major refactor impacting hot paths or fragile areas.

**Checkpoint consumption**: when closing a C-type (checkpoint) item, the
orchestrator must:

1. Check whether `REPO_MAP.md` exists in the target repository.
2. If it exists, verify that `last_validated_on` is within `freshness_window_days`.
3. If stale, the checkpoint cannot transition from `verified` to `done` until
   the map is refreshed and `last_validated_on` is updated to the current date.
4. Record the freshness check result in the checkpoint's notes or commit message.

**Automation**: `validate-plan.py --check-freshness` MUST detect staleness
and emit a warning when checkpoint items are in `review` or `verified`
state.

## ADR State Flow

Recommended ADR transitions:
- proposed -> accepted
- accepted -> superseded
- accepted -> deprecated

Each ADR transition should reference the PLAN item that triggered it.
