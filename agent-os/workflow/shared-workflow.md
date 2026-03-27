# Shared Workflow

## Purpose
Define the cross-repository operating workflow for coding agents with strict
separation between governance concerns.

## Three-Layer Model
1. Level 0: central control plane repository (this repository)
2. Level 1: workspace runtime materialization
3. Level 2: repository-local governance and execution files

## Canonical Concern Split
- Workflow authority: AGENTS
- Software constraints: ARCHITECTURE
- Execution tracking: PLAN.yaml
- Readable/graph views: generated from PLAN.yaml

## Planning and Execution
- Human planning model: milestone -> sprint -> item
- Runtime execution model: dependency-driven and scope-aware
- Single-writer rule: one orchestrator writes canonical PLAN source

Execution predicate:
- Item is executable when all dependencies are in verified or done state

## Parallelism Rules
Parallel execution is allowed only when:
- dependencies are satisfied,
- scopes are compatible,
- there is no boundary conflict,
- resulting commit groups remain reviewable.

## Commit and Checkpoint Policy
- Use commit_group as natural commit boundary.
- Close a commit_group only when its items satisfy required checks.
- Keep traceability from item -> evidence -> commit.
- Enforce commit message format on all repositories governed by Layer-0:
	`<type>(<scope>): [item ID] <description>`

Optional body and footer lines are allowed after the title line.

## Automation Staging
- Phase A: branch naming, local commits, plan updates, view rendering
- Phase B: push, draft PR, develop alignment
- Phase C: controlled merge automation
- Phase D: hygiene automation
