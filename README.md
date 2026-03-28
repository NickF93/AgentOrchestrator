# AgentOrchestrator

Level-0 control-plane OS for coding-agent governance.

## Purpose

This repository defines the shared governance model, schemas, templates, and
tooling used to bootstrap and coordinate coding-agent workflows across multiple
repositories. It does not host product code.

## Directory Structure

| Directory | Purpose |
|---|---|
| `agent-os/workflow/` | Authoritative workflow model, lifecycle, taxonomy, portability, Git policy |
| `agent-os/schemas/` | Machine-readable contracts (PLAN schema) |
| `agent-os/templates/` | Canonical templates for repo-local and workspace governance files |
| `agent-os/scripts/` | Deterministic tooling: validation, rendering, bootstrap, sync |
| `agent-os/prompts/` | Shared prompt assets (placeholder) |
| `agent-os/skills/` | Reusable skill packages (placeholder) |
| `docs/design/` | Non-authoritative design and reference material |

## Governance Files

| File | Role |
|---|---|
| `AGENTS.md` | Workflow authority and operating rules |
| `ARCHITECTURE.md` | Structural constraints and boundary rules |
| `PLAN.yaml` | Active execution tracking (source of truth) |
| `PLAN.md` | Human-readable plan view (generated) |
| `PLAN.dot` | Graph plan view (generated) |

## Quick Start

### Validate a plan

```bash
python agent-os/scripts/validate-plan.py PLAN.yaml
```

### Render plan views

```bash
python agent-os/scripts/render-plan.py PLAN.yaml
```

### Bootstrap a new repository

```bash
bash agent-os/scripts/bootstrap-repo.sh --owner <name> --ref <branch|tag> <target-path>
```

### Sync workspace runtime files

```bash
bash agent-os/scripts/sync-workspace.sh <workspace-root-path>
```

## Three-Layer Model

- **Level 0** (this repository): central control plane — shared workflow,
  schemas, templates, scripts
- **Level 1**: workspace runtime materialization — generated from Level-0
  templates by `sync-workspace.sh`
- **Level 2**: repository-local governance — bootstrapped from Level-0
  templates by `bootstrap-repo.sh`

## License

See [LICENSE](LICENSE).
