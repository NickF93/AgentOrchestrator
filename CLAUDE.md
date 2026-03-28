# CLAUDE.md — Adapter Layer for Claude Code

This file is a thin adapter layer. It does not define governance rules.
All normative rules live in the canonical authorities listed below.

## Canonical Authorities

Read these files before starting work. They are your operating rules:

- `AGENTS.md` — workflow authority, commit message contract, escalation
- `ARCHITECTURE.md` — structural constraints and boundary rules
- `PLAN.yaml` — active execution tracking (source of truth)
- `agent-os/workflow/shared-workflow.md` — cross-repo workflow, three-layer
  model, commit-group closure, tracking-first rule
- `agent-os/workflow/lifecycle.md` — status transitions, dependency rules,
  freshness checks
- `agent-os/workflow/git-automation-policy.md` — automation phases, mandatory
  commit rule, phase gates
- `agent-os/workflow/item-taxonomy.md` — item types, actions, required fields,
  commit-group semantics

## Adapter Overrides

The following override Claude Code defaults that conflict with this
repository's governance:

### Mandatory commit rule

This repository requires every `commit_group` to be committed to git
immediately upon completion. Do not ask for permission to commit when
closing a commit_group — the governance rules already mandate it. Stage
the relevant files, build the commit message per `AGENTS.md`, and commit.
Do not push (Phase A only) unless explicitly told to.

### Tracking-first execution

Before modifying any non-generated file, the owning `PLAN.yaml` item must
exist with a declared `commit_group`. If no item exists, create one first.
Do not start implementation without tracking.

### Autonomous plan execution

When working through `PLAN.yaml`, advance items through the lifecycle
automatically: implement, update statuses, run checks, validate, render,
and commit each `commit_group` as it completes. Do not stop to ask between
commit_groups unless an escalation condition from `AGENTS.md` is triggered.

## Tooling

The Python command is configured per workstation via `AGENT_PYTHON` in `.env`
(see `.env.example`). Use `$AGENT_PYTHON` to run scripts:

```
$AGENT_PYTHON agent-os/scripts/validate-plan.py PLAN.yaml --schema agent-os/schemas/plan.schema.json
$AGENT_PYTHON agent-os/scripts/render-plan.py PLAN.yaml
$AGENT_PYTHON -m pytest -q
bash agent-os/scripts/run-gates.sh
```

`run-gates.sh` sources `.env` automatically. For manual commands, either
source `.env` first or substitute the value directly.
