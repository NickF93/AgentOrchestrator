---
id: workspace-sync
description: >
  Regenerate Level-1 workspace runtime files from control-plane templates
  and report provenance drift. Use this skill whenever workspace runtime
  files need to be regenerated, when the operator asks to sync a workspace,
  when checking whether workspace files are stale or drifted from the
  control plane, or when verifying workspace provenance metadata.
  Adds pre-flight validation, provenance drift detection, and structured
  reporting around sync-workspace.sh.
owner: NickF93
version: "0.2.0"
compatibility:
  - claude
  - codex
  - gemini
  - cursor
  - kilo
  - copilot
---

# workspace-sync

## Purpose

Provide a repeatable, execution-layer procedure for regenerating Level-1
workspace runtime files and detecting provenance drift against the
control plane. This skill wraps the existing `sync-workspace.sh` script
with pre-flight validation, provenance drift detection, and structured
reporting. It does not define governance rules. It applies the
synchronization process already implemented in canonical tooling and
ensures the result meets governance expectations.

This skill operates between Layer 0 and Layer 1:

- **Layer 0 (source)**: the control-plane repo provides the sync
  script, workspace templates, and git metadata used for provenance
  stamps.
- **Layer 1 (target)**: the workspace directory receives the rendered
  runtime files and config (AGENTS.md, CLAUDE.md, .codex/config.toml).

This skill is procedural. All normative rules it enforces are defined in
the canonical tooling and templates. When a specific rule must be
verified, read the relevant file — do not invent or restate governance
rules from memory.

Canonical authorities (paths relative to `control_plane_root`):

- `agent-os/scripts/sync-workspace.sh` — the wrapped sync script
- `agent-os/templates/workspace-AGENTS.md.template`
- `agent-os/templates/workspace-CLAUDE.md.template`
- `agent-os/templates/workspace-codex-config.toml.template`
- `agent-os/workflow/shared-workflow.md` — three-layer model, workspace
  topology

## Two-Root Model

This skill operates with two distinct roots. Every path used in the
procedure belongs to exactly one of them.

| Root                  | What lives there                                        |
|-----------------------|---------------------------------------------------------|
| `workspace_root`      | The workspace directory receiving generated runtime     |
|                       | files/config: AGENTS.md, CLAUDE.md, .codex/config.toml  |
| `control_plane_root`  | The Level-0 checkout: sync script, workspace templates, |
|                       | git metadata for provenance stamps                      |

Unlike `repo-bootstrap` (where `repo_root` and `control_plane_root` are
always different sibling directories), `workspace-sync` operates on a
workspace that typically *contains* the control plane as a child
directory. The workspace root is the parent; the control-plane checkout
is a subdirectory within it.

### Resolving `control_plane_root`

Use the first match:

1. **Explicit input**: caller provides `control_plane_root` directly.
2. **Environment variable**: `CONTROL_PLANE_ROOT` is set in the
   environment.
3. **Self-detection**: if the skill is being invoked from within the
   control-plane repo itself, derive from the repo root (the directory
   containing `agent-os/scripts/sync-workspace.sh`).
4. **Fail**: "Cannot locate control-plane root. Provide
   control_plane_root explicitly or export CONTROL_PLANE_ROOT."

After resolution, verify that
`{control_plane_root}/agent-os/scripts/sync-workspace.sh` exists.
If it does not, fail — the control plane checkout may be stale or
missing.

### Shared tooling (from `control_plane_root`)

- `{control_plane_root}/agent-os/scripts/sync-workspace.sh`
- `{control_plane_root}/agent-os/templates/workspace-AGENTS.md.template`
- `{control_plane_root}/agent-os/templates/workspace-CLAUDE.md.template`
- `{control_plane_root}/agent-os/templates/workspace-codex-config.toml.template`

### Workspace data (from `workspace_root`)

After a successful sync, `workspace_root` will contain these files:

| Source template                         | Target path                    |
|-----------------------------------------|--------------------------------|
| `workspace-AGENTS.md.template`          | `{workspace_root}/AGENTS.md`  |
| `workspace-CLAUDE.md.template`          | `{workspace_root}/CLAUDE.md`  |
| `workspace-codex-config.toml.template`  | `{workspace_root}/.codex/config.toml` |

## Required Inputs

| Input                  | Type   | Default       | Description                                         |
|------------------------|--------|---------------|-----------------------------------------------------|
| `workspace_path`       | string | (required)    | Absolute or relative path to the workspace root     |
| `control_plane_root`   | string | (resolved)    | Root of the Level-0 control-plane checkout           |
| `dry_run`              | bool   | `false`       | If true, compare what would change without writing   |
| `check_drift`          | bool   | `true`        | If true, check provenance drift on existing files    |

## Expected Outputs

A structured sync report containing:

- pre-flight results (workspace validation, control plane resolution)
- provenance drift analysis (if existing files found and `check_drift`
  is true)
- sync outcome (script exit code, files generated)
- post-sync verification (file existence, provenance stamps)
- next-steps guidance for the operator

Output template (adapt to context):

```
verdict: pass | warn | fail | blocked
phase: pre-flight | drift-check | sync | verification
findings:
  - <finding or explicit none>
evidence:
  - control_plane_root: <path>
  - workspace_path: <path>
  - control_plane_ref: <ref>
  - control_plane_commit: <sha>
  - dry_run: <true|false>
provenance:
  current:
    ref: <existing stamped ref or none>
    commit: <existing stamped commit or none>
    date: <existing stamped date or none>
  new:
    ref: <current control plane ref>
    commit: <current control plane commit>
    date: <today>
  drift: true | false | N/A
files_generated:
  - AGENTS.md: created | updated | unchanged | skipped
  - CLAUDE.md: created | updated | unchanged | skipped
  - .codex: created | updated | unchanged | skipped
commands_run:
  - `bash <cp>/agent-os/scripts/sync-workspace.sh <workspace>` -> exit <code>
next_steps:
  - <optional guidance>
```

## Procedure

Execute these steps in order. Stop and report on the first blocking
failure unless all issues can be enumerated without side effects (in
which case, collect all failures before stopping).

### Step 0 — Resolve control plane root

1. Resolve `control_plane_root` using the resolution order above.
2. Verify `{control_plane_root}/agent-os/scripts/sync-workspace.sh`
   exists.
3. Verify `{control_plane_root}/agent-os/templates/` exists and contains
   the three workspace templates:
   - `workspace-AGENTS.md.template`
   - `workspace-CLAUDE.md.template`
   - `workspace-codex-config.toml.template`
4. Record `control_plane_root` in the report header.

This step must succeed before any other step runs. If the control plane
cannot be located or is incomplete, nothing else is meaningful.

### Step 1 — Pre-flight: validate workspace path

1. Check whether `workspace_path` resolves to a valid directory, or can
   be created. The sync script calls `mkdir -p`, so a non-existent path
   is acceptable — the script will create it.
2. Record the resolved absolute path of `workspace_path` as
   `workspace_root`.

### Step 2 — Pre-flight: check for existing workspace files

1. For each of the three target files (AGENTS.md, CLAUDE.md, .codex/config.toml),
   check whether it already exists at `workspace_root`.

2. **If no files exist** (first-time sync): record current provenance as
   N/A, set drift to N/A, and skip Step 3 entirely. Proceed directly to
   Step 4 — there is nothing to compare against.

3. **If files exist**: extract the provenance metadata stamped by the
   previous sync. The provenance lines appear in lines 5–9 of each
   file, always in this order:
   ```
   Generated on: <date>
   Control plane: <path>
   CONTROL_PLANE_ROOT: <path>
   Control plane ref: <ref>
   Control plane commit: <sha>
   ```
   Extract with grep:
   ```bash
   grep "^Generated on:"          "{workspace_root}/AGENTS.md"
   grep "^Control plane ref:"     "{workspace_root}/AGENTS.md"
   grep "^Control plane commit:"  "{workspace_root}/AGENTS.md"
   ```
   It is sufficient to read provenance from one file (AGENTS.md) since
   all three are stamped identically by the same sync run.

4. Record the extracted values as "current provenance" in the report.

### Step 3 — Provenance drift detection

Skip this step if `check_drift` is `false` or no existing files were
found in Step 2.

1. Read the live control plane state:
   ```bash
   git -C {control_plane_root} symbolic-ref --quiet --short HEAD
   git -C {control_plane_root} rev-parse --short HEAD
   ```
2. Compare the live ref and commit against the stamps extracted in
   Step 2.
3. Classify drift:
   - **commit drift**: control plane commit has advanced since last sync.
   - **ref drift**: control plane branch has changed since last sync.
   - **age drift**: date of last sync differs from today (advisory).
4. If any drift is detected, record it in the report. Drift is
   informational — it does not block the sync, but it tells the operator
   that workspace files are stale relative to the control plane.

### Step 4 — Execute sync

**If `dry_run` is `true`:**

Compute what the rendered output would be without writing anything.
The sync script performs four `sed` substitutions on each template:

| Placeholder              | Current value                  |
|--------------------------|--------------------------------|
| `{{DATE}}`               | today's date (YYYY-MM-DD)      |
| `{{CONTROL_PLANE_ROOT}}` | resolved `control_plane_root`  |
| `{{CONTROL_PLANE_REF}}`  | current git branch or "detached"|
| `{{CONTROL_PLANE_COMMIT}}`| current short commit SHA       |

To compute the dry-run diff:
1. Read each template from
   `{control_plane_root}/agent-os/templates/`.
2. Substitute the four placeholders with the current values.
3. Compare the rendered result against the existing workspace file
   (if it exists). Show a diff or a summary of what would change.
4. Report the diffs without writing any files.

If existing files have the same provenance stamps as the new values,
report "unchanged" for those files.

**If `dry_run` is `false`:**

1. Run the sync script:
   ```bash
   bash {control_plane_root}/agent-os/scripts/sync-workspace.sh {workspace_root}
   ```
2. Capture stdout, stderr, and exit code.
3. If the exit code is non-zero, fail with the stderr output. Record
   the failure in the report and stop.
4. Record the sync outcome in the report.

**If the script cannot be executed** (sandbox restrictions, missing
bash, permission errors on the workspace path): fall back to manual
rendering. Read each template, perform the four `sed` substitutions
above, and write the rendered content to the workspace files using
whatever file-write mechanism is available. This produces the same
result as the script. Record in the report that manual rendering was
used instead of the script.

### Step 5 — Post-sync: verify file existence and provenance

If `dry_run` is `true`, skip this step (report all verifications as
"skipped").

1. For each of the three target files (AGENTS.md, CLAUDE.md, .codex/config.toml),
   verify it exists at its expected path under `workspace_root`.
2. For each existing file, extract the provenance stamps and verify
   they match the current control plane state:
   - `Control plane ref` matches the current branch.
   - `Control plane commit` matches the current short SHA.
   - `Generated on` matches today's date.
3. If any stamp does not match, flag it as a verification failure.

### Step 6 — Assemble report and next-steps

1. Combine all results into the structured report format defined in
   Expected Outputs.

2. Determine the overall verdict:
   - **pass**: sync completed (or dry-run computed), all files verified,
     provenance stamps correct. No pre-sync drift detected.
   - **warn**: sync completed and verified, but pre-sync drift was
     detected (informational — the workspace *was* stale, now it is
     fresh). Also use for dry-run when drift is detected.
   - **fail**: sync script returned non-zero, manual rendering failed,
     or post-sync verification found missing files or mismatched
     provenance stamps. The sync was attempted but did not succeed.
   - **blocked**: pre-flight failed before sync could be attempted
     (workspace path invalid, control plane missing or incomplete,
     templates not found). No sync was run.

3. Include next-steps guidance (only for non-dry-run pass or warn
   verdicts):
   - "Shared assets resolve from CONTROL_PLANE_ROOT in workspace mode."
   - "Vendoring remains optional and explicit via
     materialize-shared-asset.sh."
   - "Layer-2 repos under this workspace inherit the stamped
     CONTROL_PLANE_ROOT for shared asset resolution."

## Common-Case Command Sequence

For syncing a workspace where the control plane is a subdirectory:

```bash
# Variables (resolve once)
CP="/path/to/workspace/AgentOrchestrator"   # control_plane_root
WS="/path/to/workspace"                     # workspace_root

# 1. Check current provenance (if files exist)
grep "Control plane ref:" "$WS/AGENTS.md" 2>/dev/null
grep "Control plane commit:" "$WS/AGENTS.md" 2>/dev/null

# 2. Check live control plane state
git -C "$CP" symbolic-ref --quiet --short HEAD
git -C "$CP" rev-parse --short HEAD

# 3. Run sync
bash "$CP/agent-os/scripts/sync-workspace.sh" "$WS"

# 4. Verify provenance stamps in generated files
grep "Control plane ref:" "$WS/AGENTS.md"
grep "Control plane commit:" "$WS/AGENTS.md"
grep "Generated on:" "$WS/AGENTS.md"
```

## Constraints

- **Procedural only**: this skill wraps existing sync tooling. It must
  not define, redefine, or silently alter any governance rule. The
  templates and script are the canonical authority for what gets
  rendered.
- **Two-root integrity**: the sync script and templates come from
  `control_plane_root`. Rendered files go to `workspace_root`. Never
  confuse which root a file belongs to.
- **No modification of control plane**: this skill never writes to
  `control_plane_root`. All writes go to `workspace_root`.
- **Overwrite by design**: unlike `repo-bootstrap` (which skips existing
  files), `sync-workspace.sh` always overwrites workspace files. They
  are generated artifacts, not authored content. This is the intended
  behavior — workspace files should always reflect the current control
  plane state.
- **No auto-commit**: the skill renders files but does not stage or
  commit them. Workspace runtime files are not typically tracked in
  version control.
- **No push**: the skill operates locally. It does not push to any
  remote.
- **No auto-vendor**: per the portability model, bootstrap and workspace
  sync do not auto-vendor shared assets in v1. Vendoring is an explicit
  operation via `materialize-shared-asset.sh`.

## Failure Handling

| Failure                                           | Behavior                                              |
|---------------------------------------------------|-------------------------------------------------------|
| Control plane root not resolvable                 | Fail with resolution instructions                     |
| sync-workspace.sh not found                       | Fail with "sync-workspace.sh not found at <path>"     |
| Templates directory incomplete (missing templates)| Fail with list of missing template files              |
| workspace_path not provided                       | Fail with usage instructions                          |
| workspace_path not writable                       | Fail with permission error                            |
| sync-workspace.sh non-zero exit                   | Fail with stderr output                               |
| Expected files missing after sync                 | Fail with list of missing files                       |
| Provenance stamps mismatch after sync             | Fail with mismatch details                            |
| git not available (for provenance extraction)     | Warn; skip drift detection; note in report            |
| Existing files unparseable for provenance stamps  | Warn; treat as first-time sync; note in report        |
| sync-workspace.sh blocked by sandbox/permissions  | Fall back to manual template rendering (see Step 4)   |

## Adapter Notes

### Claude

When invoked via Claude Code or Claude-based agents, this skill uses
`Bash` to run `sync-workspace.sh` and provenance extraction commands,
`Read` to verify file existence and content, and `Grep` to extract
provenance stamps from existing files. For control plane resolution,
check the environment for `CONTROL_PLANE_ROOT`, or detect the control
plane from the current repo root. The sync report is returned as direct
text output.

### Codex

When invoked via Codex agents, use the file system and shell tools
available in the sandbox. Both `workspace_root` and
`control_plane_root` must be accessible within the sandbox filesystem.
The workspace is typically the sandbox root with the control plane
mounted as a child directory. The same command sequences apply.

### Gemini

When invoked via Gemini CLI or Gemini-based agents, the skill is
referenced from the workspace `AGENTS.md` generated by a previous sync,
or from `GEMINI.md` in bootstrapped repos. Resolve `CONTROL_PLANE_ROOT`
from the workspace file or environment. The same shared sync tooling and
procedure apply.

### Cursor

When invoked via Cursor, the skill is referenced from
`.cursor/rules/governance.mdc` in bootstrapped repos or from the
workspace `AGENTS.md`. Resolve `CONTROL_PLANE_ROOT` from the workspace
file or environment. The same shared sync tooling and procedure apply.

### Kilo

When invoked via Kilo, the skill is referenced from
`.kilo/rules/governance.md` in bootstrapped repos or from the workspace
`AGENTS.md`. Resolve `CONTROL_PLANE_ROOT` from the workspace file or
environment. The same shared sync tooling and procedure apply.

### Copilot

When invoked via GitHub Copilot agents, the skill is referenced from
`.github/copilot-instructions.md` in bootstrapped repos or from the
workspace `AGENTS.md`. Control plane resolution uses the workspace
layout or explicit configuration. The same sync procedure applies.
