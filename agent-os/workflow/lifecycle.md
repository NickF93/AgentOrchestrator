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

- REPO_MAP freshness must be checked at release/checkpoint closure.
- Freshness fails when `last_validated_on` exceeds `freshness_window_days`.
- Stale REPO_MAP status blocks `verified -> done` for related checkpoint items.

## ADR State Flow

Recommended ADR transitions:
- proposed -> accepted
- accepted -> superseded
- accepted -> deprecated

Each ADR transition should reference the PLAN item that triggered it.
