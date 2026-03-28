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
- `compatibility` lists supported adapters from:
	- `codex`
	- `claude`
	- `copilot`
	- `kilo`

## Required Body Sections

- purpose
- required inputs
- expected outputs
- constraints
- failure handling

## Compatibility Boundary

- Skill semantics must stay tool-neutral in the canonical package.
- Tool-specific execution details belong to adapter notes/files.
- Adapters may extend execution strategy but must not alter normative intent.
