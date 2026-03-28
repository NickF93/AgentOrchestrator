# Portability Model

## Goal
Keep the shared model tool-neutral so it can map to multiple agent ecosystems.

## Neutral Core Fields
Use these abstract fields in planning/execution metadata:
- role
- effort
- triggers
- tools_profile

## Mapping Strategy
Shared model remains stable; adapters map it to vendor-specific primitives.

Examples:
- Codex: AGENTS hierarchy, directory scoping, parallel isolated tasks
- Claude: CLAUDE memory hierarchy, imports, subagent separation
- Copilot: repository/path instruction precedence and nearest-file priority
- Kilo: custom modes and specialized workflow configurations map to role/effort/triggers profile

## Non-Goals
- Do not encode vendor-only features in shared taxonomy.
- Do not make Level-0 dependent on one single client runtime.

## Compatibility Principle
If a feature cannot be represented neutrally, keep it in adapter layer
(workspace materialization or tool-specific profile), not in canonical taxonomy.

## Skill Packaging Contract

- Canonical skill package file: `SKILL.md`.
- Required frontmatter:
	- `id`: stable identifier for cross-repo reuse.
	- `description`: concise scope statement.
	- `owner`: accountable maintainer.
	- `version`: semantic version.
	- `compatibility`: list of runtime adapters (`codex`, `claude`, `copilot`, `kilo`).
- Body sections:
	- purpose,
	- required inputs,
	- expected outputs,
	- constraints,
	- failure handling.

## Adapter Boundary Rule

- Canonical skills define neutral behavior only.
- Runtime-specific tool calls live in adapter notes or adapter files.
- Adapters may extend execution details but must not change normative meaning.
