# AGENTS.md

## Scope
This repository is the Level-0 control-plane OS for coding-agent governance.
It does not host product code. It hosts shared workflow, taxonomy, templates,
schemas, and scripts used to bootstrap and coordinate other repositories.

## Authority Map
- Workflow and governance model: `agent-os/workflow/*`
- Plan schema contract: `agent-os/schemas/plan.schema.json`
- Repo bootstrap templates: `agent-os/templates/*`
- Operational tooling: `agent-os/scripts/*`
- Active execution tracking for this repository: `PLAN.yaml`
- Design/background references (non-authoritative): `docs/design/*`
- Structural constraints for this repository: `ARCHITECTURE.md`

## Canonical Source Rule
One concern must have one canonical authority. Do not duplicate normative content
across files.

Priority order:
1. Explicit human instructions
2. This file for workflow authority and operating rules
3. `ARCHITECTURE.md` for structural and boundary constraints
4. `PLAN.yaml` for active execution tracking
5. Code and tests as implementation evidence
6. Generated plan views (`PLAN.md`, `PLAN.dot`) as non-authoritative outputs

## Working Rules
- Treat `PLAN.yaml` as source of truth for planning status and dependencies.
- Keep startup/design documents in `docs/design/`; do not use them as runtime authority.
- Do not hand-edit generated artifacts (`PLAN.md`, `PLAN.dot`) once render scripts exist.
- Preserve determinism in generated outputs and script behavior.
- Prefer additive, minimal changes with explicit checkpoints.

## Escalation and Stop Conditions
Stop and ask the human owner when:
- A change would alter authority boundaries,
- A conflict exists between `ARCHITECTURE.md` and `PLAN.yaml`,
- A schema change would invalidate existing plan data,
- A workflow policy implies irreversible Git automation beyond current phase.

## Layer-0 Build Context
Current implementation focus is Layer-0 foundation:
- `agent-os/workflow/`
- `agent-os/schemas/`
- `agent-os/templates/`
- `agent-os/scripts/`
- `agent-os/prompts/` and `agent-os/skills/` placeholders
