# skills/

Reusable skill packages for cross-repo and cross-agent workflows.

## Canonical Package Format

- Primary file: `SKILL.md`.
- Required YAML frontmatter fields:
  - `id`
  - `description`
  - `owner`
  - `version`
  - `compatibility`

## Supported Runtimes in v1

Shared-asset support is currently defined for:

- `claude`
- `codex`
- `kilo`
- `copilot`

Runtime lifecycle tiers (experimental, supported, first-class) are defined in
`agent-os/workflow/portability-model.md`.

## Required Body Sections

- purpose
- required inputs
- expected outputs
- constraints
- failure handling

## Compatibility Boundary

- Skill semantics must stay tool-neutral in the canonical package.
- Runtime-specific execution details belong to profiles or adapter notes.
- Skills may reference shared prompt and protocol IDs, but they must not embed
  runtime-specific tool behavior directly.
- Adapters may extend execution strategy but must not alter normative intent.
