# prompts/

Shared prompt assets for orchestrator, reviewer, and verification flows.

## Canonical Format

- File format: Markdown (`.md`) with YAML frontmatter.
- Required frontmatter fields:
  - `id`
  - `role`
  - `purpose`
  - `owner`
  - `version`
  - `status`
- Allowed `status` values: `draft`, `active`, `deprecated`, `superseded`.

## Lifecycle

- Create in `draft` state.
- Promote to `active` only after workflow review.
- Mark as `superseded` when replaced by newer prompt version.
- Mark as `deprecated` when intentionally retired.

## Versioning

- Use semantic versioning (`major.minor.patch`).
- Increment `major` for normative behavior changes.
- Increment `minor` for additive guidance.
- Increment `patch` for clarifications without behavior changes.

## Runtime Boundary

- Prompt assets stay tool-neutral.
- Runtime-specific behavior belongs in Layer-0 profiles or adapter notes.
- Shared-asset consumption in v1 is defined for `claude`, `codex`,
  `gemini`, `cursor`, `kilo`, and `copilot`. Runtime lifecycle tiers
  (experimental, supported,
  first-class) are defined in `agent-os/workflow/portability-model.md`.
- Prompt assets may reference canonical protocols and skills, but they must not
  redefine taxonomy, lifecycle, or authority rules.
