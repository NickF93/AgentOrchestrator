# prompts/

Shared prompt assets for orchestrator/reviewer flows.

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

## Boundaries

- Prompt assets may not redefine canonical taxonomy, lifecycle, or authority rules.
- Prompt assets must reference canonical governance docs for normative rules.
