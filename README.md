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
| `agent-os/prompts/` | Shared prompt asset contracts and lifecycle guidance |
| `agent-os/skills/` | Reusable skill packaging contracts and compatibility guidance |
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

### Install runtime dependencies in `nn-2`

```bash
conda run -n nn-2 python -m pip install -r requirements.txt
```

### Install development and test tooling in `nn-2`

```bash
conda run -n nn-2 python -m pip install -r requirements-dev.txt
```

### Validate a plan

```bash
conda run -n nn-2 python agent-os/scripts/validate-plan.py PLAN.yaml --schema agent-os/schemas/plan.schema.json
```

### Render plan views

```bash
conda run -n nn-2 python agent-os/scripts/render-plan.py PLAN.yaml
```

### Run script tests

```bash
conda run -n nn-2 python -m pytest -q
```

### Run local quality gates

```bash
bash agent-os/scripts/run-gates.sh
```

### Bootstrap a new repository

```bash
bash agent-os/scripts/bootstrap-repo.sh --owner <name> --ref <branch|tag> <target-path>
```

The bootstrap also writes `.githooks/commit-msg` into the target repository.
Enable it with:

```bash
git -C <target-path> config core.hooksPath .githooks
chmod +x <target-path>/.githooks/commit-msg
```

### Sync workspace runtime files

```bash
bash agent-os/scripts/sync-workspace.sh <workspace-root-path>
```

## Testing and Gates

The canonical local verification environment for this repository is `nn-2`.

- Python tests: `conda run -n nn-2 python -m pytest -q`
- Gate runner: `bash agent-os/scripts/run-gates.sh`
- The gate runs Ruff, mypy, Python compile checks, pytest, and ShellCheck when
  ShellCheck is available on the local machine.
- `requirements.txt` stays runtime-only; development/test tooling lives in
  `requirements-dev.txt`.

`sync-workspace.sh` materializes runtime files from the current local
control-plane checkout. It does not pull from the remote automatically.
If you want the latest `origin/main` first, run:

```bash
git -C /path/to/AgentOrchestrator pull --ff-only origin main
bash agent-os/scripts/sync-workspace.sh <workspace-root-path>
```

### Enable local commit message guard

```bash
git config core.hooksPath .githooks
chmod +x .githooks/commit-msg
```

The local `commit-msg` hook enforces:

`<type>(<scope>): <description>`

and exactly one footer line of the form:

`Refs: <PLAN item IDs>, <commit_group ID>`

Regexes:

- `^([a-z]+)\(([a-z0-9._/-]+)\): .+$`
- item IDs: `[A-Z]+[1-9][0-9]*\.[1-9][0-9]*\.[1-9][0-9]*[a-z]?`
- commit groups: `cg[1-9][0-9]*`

You can test it quickly with:

```bash
printf "docs(workflow): valid title\n\nRefs: D1.1.1, cg1\n" > /tmp/good-msg.txt
.githooks/commit-msg /tmp/good-msg.txt

printf "docs(workflow): missing refs\n\n" > /tmp/bad-msg.txt
.githooks/commit-msg /tmp/bad-msg.txt
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
