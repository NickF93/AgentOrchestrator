# ARCHITECTURE.md

## Repository Role
This repository is the Level-0 central control plane for coding-agent operations.
Its purpose is to define shared governance and tooling that can be materialized
in workspaces and reused by multiple repositories.

## Directory Ownership
- `agent-os/workflow/`: authoritative workflow model, lifecycle, taxonomy,
  portability model, and Git automation policy.
- `agent-os/schemas/`: machine-readable contracts (starting with PLAN schema).
- `agent-os/templates/`: canonical templates for repo-local governance files.
- `agent-os/scripts/`: deterministic tooling for validation, rendering,
  bootstrap, and sync.
- `agent-os/prompts/`: placeholder area for future prompt assets.
- `agent-os/skills/`: placeholder area for future skill packaging.
- `docs/design/`: non-authoritative brainstorming and source material.

## Invariants
- Scripts in `agent-os/scripts/` must be deterministic and idempotent.
- Templates must include canonical source and authority guidance where relevant.
- Workflow documents must be split by concern and avoid cross-duplication.
- `docs/design/` is reference-only and must not become runtime authority.
- `PLAN.yaml` is the only authoritative execution-tracking file for this repo.

## Boundary Rules
- Changes that alter item taxonomy, lifecycle states, or dependency semantics
  require corresponding updates in both schema and validation logic.
- Changes to `agent-os/schemas/` should be backward-aware or include migration notes.
- Generated plan views are downstream artifacts and should never be used as source.
- Root governance files (`AGENTS.md`, `ARCHITECTURE.md`) are authoritative for this
  repository; they are not generated from templates.

## Explicit Exception
This repository has no parent control plane. Therefore, root governance files are
maintained locally by design. This does not violate the generation strategy used
for downstream Level-1 and Level-2 targets.
