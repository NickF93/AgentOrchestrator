# Portability Model

## Goal
Keep the shared model tool-neutral so it can map to multiple agent ecosystems
without duplicating authority or making Layer-0 dependent on one client.

## Neutral Core Fields
Use these abstract fields in planning/execution metadata:

- role
- effort
- triggers — **DEFERRED**: adapter-level invocation hints; semantics TBD;
  non-normative in MVP. Included as a vocabulary placeholder for future
  adapter mappings. MUST NOT drive execution semantics until defined.
- tools_profile — **DEFERRED**: adapter-level capability/profile label;
  semantics TBD; non-normative in MVP. Same restrictions as triggers.

## First-Wave Runtime Support

Shared-asset consumption in v1 is supported for:

- `claude`
- `codex`

Other runtimes remain future adapter work. They MUST NOT be treated as active
shared-asset targets until their profiles and consumption rules are added to
Layer 0.

## Canonical Shared Asset Families

Stable cross-repo reusable assets live only in Layer 0:

- `agent-os/skills/<skill-id>/SKILL.md`
- `agent-os/prompts/<prompt-id>.md`
- `agent-os/profiles/<runtime>/<profile-id>.yaml`
- `agent-os/protocols/<protocol-id>.yaml`

The canonical registry is:

- `agent-os/registry/shared-assets.yaml`

Registry entries MUST include:

- `id`
- `kind` (`skill`, `prompt`, `profile`, `protocol`)
- `version`
- `path`
- `compatibility`
- `materializable`
- optional `depends_on_assets`

Asset kinds stay explicit in v1. A generic catch-all asset kind is not part of
the portability contract.

## Two-Root Consumption Model

Shared asset resolution uses two distinct roots:

- `control_plane_root` resolves shared assets, the registry, prompts, skills,
  profiles, protocols, and Layer-0 scripts.
- `repo_root` resolves repo-local execution data and code such as `PLAN.yaml`,
  repo tests, and source files.

Layer-2 default consumption mode is `workspace`:

- shared assets are resolved from `CONTROL_PLANE_ROOT`
- no Layer-2 copy becomes authoritative
- workspace discovery is preferred over duplication

Optional `vendored` mode is allowed only through explicit materialization:

- vendored assets live under `.agent-os/vendor/`
- vendored assets are read-only snapshots with provenance
- vendored assets are portability aids, not editable sources of truth
- bootstrap and workspace sync MUST NOT auto-vendor assets in v1

## Mapping Strategy

Shared contracts stay stable; runtime-specific behavior is layered on top by
profiles and adapter notes rather than leaking into the neutral taxonomy.

In v1:

- prompts and skills stay tool-neutral
- runtime-specific behavior belongs in profiles or adapter notes
- PLAN items reference shared assets by registry ID, not by runtime-specific
  knobs

## Non-Goals

- Do not encode vendor-only features in the shared taxonomy.
- Do not make Layer-0 dependent on one single client runtime.
- Do not make Layer-2 copies authoritative.
- Do not repurpose deferred `triggers` or `tools_profile` fields for shared
  asset resolution.

## Compatibility Principle

If a feature cannot be represented neutrally, keep it in the adapter layer
(profiles, workspace materialization, or tool-specific notes), not in the
canonical taxonomy, prompt, or skill.

## Adapter Boundary Rule

- Canonical prompts and skills define neutral behavior only.
- Runtime-specific tool calls and workflow tuning live in profiles or adapter
  notes.
- Adapters may extend execution details but must not change normative meaning.
