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
| `plan/PLAN-index.yaml` | Canonical plan entrypoint (source of truth) |
| `plan/PLAN-current.yaml` | Active execution fragment |
| `plan/archive/PLAN-XNN.yaml` | Closed milestone archive fragments |
| `PLAN.md` | Human-readable plan view (generated) |
| `PLAN.dot` | Graph plan view (generated) |

## Quick Start

### Configure the Python environment

Copy `.env.example` to `.env` and set `AGENT_PYTHON` for your workstation:

```bash
cp .env.example .env
# Edit .env — set AGENT_PYTHON to your local Python command, e.g.:
#   AGENT_PYTHON="python3"
#   AGENT_PYTHON="conda run -n myenv python"
#   AGENT_PYTHON="/path/to/venv/bin/python"
```

`.env` is gitignored and never committed. Scripts source it automatically.
`run-gates.sh` resolves Python with this precedence: exported
`AGENT_PYTHON`, then `.env`, then `python3`. For manual commands, source
`.env` first or export `AGENT_PYTHON` explicitly.

### Install runtime dependencies

```bash
$AGENT_PYTHON -m pip install -r requirements.txt
```

### Install development and test tooling

```bash
$AGENT_PYTHON -m pip install -r requirements-dev.txt
```

### Validate a plan

```bash
$AGENT_PYTHON agent-os/scripts/validate-plan.py plan/PLAN-index.yaml --schema agent-os/schemas/plan.schema.json
```

### Query the current ready-set

```bash
$AGENT_PYTHON agent-os/scripts/validate-plan.py plan/PLAN-index.yaml --schema agent-os/schemas/plan.schema.json --compute-ready
```

This emits deterministic JSON with a `ready_items` array. Each entry includes
`id`, `type`, `status`, `commit_group`, and unresolved dependency metadata.

### Render plan views

```bash
$AGENT_PYTHON agent-os/scripts/render-plan.py plan/PLAN-index.yaml
```

### Run script tests

```bash
$AGENT_PYTHON -m pytest -q
```

### Run local quality gates

```bash
bash agent-os/scripts/run-gates.sh
```

### Bootstrap a new repository

```bash
bash agent-os/scripts/bootstrap-repo.sh --owner <name> --ref <branch|tag> <target-path>
```

The bootstrap also writes both local hooks into the target repository:

- `.githooks/commit-msg`
- `.githooks/pre-push`

It also writes thin repo-local runtime entrypoints for:

- `CLAUDE.md`
- `GEMINI.md`
- `.cursor/rules/governance.mdc`
- `.github/copilot-instructions.md`
- `.kilo/rules/governance.md`

It also writes Codex repo-local configuration to `.codex/config.toml`.
Codex instructions remain in `AGENTS.md`; the TOML file is config-only.

Canonical governance still lives in `AGENTS.md`, `ARCHITECTURE.md`, and
`plan/PLAN-index.yaml`.
Enable them with:

```bash
git -C <target-path> config core.hooksPath .githooks
chmod +x <target-path>/.githooks/commit-msg <target-path>/.githooks/pre-push
```

### Sync workspace runtime files

```bash
bash agent-os/scripts/sync-workspace.sh <workspace-root-path>
```

## Testing and Gates

Repo-tracked Python commands use `AGENT_PYTHON`. `run-gates.sh` resolves it
with this precedence: exported `AGENT_PYTHON`, then `.env`, then `python3`.

- Python tests: `$AGENT_PYTHON -m pytest -q`
- Gate runner: `bash agent-os/scripts/run-gates.sh` (sources `.env` automatically)
- The gate runs Ruff, mypy, Python compile checks, pytest, and ShellCheck when
  ShellCheck is available on the local machine.
- `requirements.txt` stays runtime-only; development/test tooling lives in
  `requirements-dev.txt`.

`sync-workspace.sh` materializes runtime files from the current local
control-plane checkout. It does not pull from the remote automatically.
It currently renders only the workspace-scoped runtime entrypoints
(`AGENTS.md`, `CLAUDE.md`) and Codex workspace config
(`.codex/config.toml`).
If you want the latest `origin/main` first, run:

```bash
git -C /path/to/AgentOrchestrator pull --ff-only origin main
bash agent-os/scripts/sync-workspace.sh <workspace-root-path>
```

### Enable local hooks

```bash
git config core.hooksPath .githooks
chmod +x .githooks/commit-msg .githooks/pre-push
```

The local `commit-msg` hook enforces:

`<type>(<scope>): <description>`

and exactly one footer line of the form:

`Refs: <PLAN item IDs>, <commit_group ID>`

Regexes:

- `^([a-z]+)\(([a-z0-9._/-]+)\): .+$`
- item IDs: `[A-Z]+[1-9][0-9]*\.[1-9][0-9]*\.[1-9][0-9]*[a-z]?`
- commit groups: `cg[1-9][0-9]*`

It also rejects AI/codegen attribution markers such as
`Co-Authored-By: Claude Opus ...` or `Generated by ChatGPT`.

The local `pre-push` hook:

- blocks direct pushes to `main` and `develop`
- rejects pushed commit messages containing banned AI/codegen attribution markers
- rejects added text lines containing the same banned markers

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
  templates by `sync-workspace.sh` for workspace-scoped runtimes
- **Level 2**: repository-local governance — bootstrapped from Level-0
  templates by `bootstrap-repo.sh`

Runtime entrypoint artifacts remain thin pointers only. In this repository:

- `CLAUDE.md` is a workspace/runtime entrypoint
- `.codex/config.toml` is Codex workspace/repo configuration; `AGENTS.md`
  remains the Codex instruction authority
- `CLAUDE.md`, `GEMINI.md`, `.cursor/rules/governance.mdc`,
  `.github/copilot-instructions.md`, and `.kilo/rules/governance.md`
  are bootstrapped repo-level runtime entrypoints

## License

See [LICENSE](LICENSE).
