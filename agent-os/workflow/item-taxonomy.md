# Item Taxonomy

## Item Types
- X: milestone container (non-executable)
- S: sprint container (non-executable)
- Q: decision gate / blocking question
- D: documentation or governance work
- M: implementation, integration, refactor
- F: fix or hotfix
- T: test or validation
- C: checkpoint, review, closure gate

## Action Taxonomy
- audit
- plan
- design
- implement
- refactor
- test
- verify
- document
- review
- checkpoint
- decide
- migrate

## Recommended Type/Action Coherence

This table is advisory. Violations produce warnings, not hard failures.

- Q: review, decide
- D: plan, document, review, checkpoint
- M: design, implement, refactor, migrate, verify
- F: implement, test, verify
- T: test, verify
- C: review, checkpoint, verify

## Lifecycle States
- planned
- ready
- in_progress
- blocked
- review
- verified
- done

State flow:
- planned -> ready -> in_progress -> review -> verified -> done
- blocked is a side-state reachable from active states

## Roles
- orchestrator
- implementer
- tester
- reviewer
- documenter
- researcher

## Effort Levels
- low
- medium
- high

## Required Item Fields

Every executable item (Q, D, M, F, T, C) must declare:

- id
- type
- title
- status
- role
- effort
- actions (at least one action verb from the action taxonomy)
- parent (sprint ID under which the item belongs)
- commit_group (commit group ID for commit boundary)

## Optional Metadata Fields

- depends_on — list of dependency target IDs (sprint or item IDs; milestone IDs
  are not valid dependency targets)
- scope — a file or directory path prefix (e.g. `agent-os/scripts/`, `AGENTS.md`).
  Used for collision detection between concurrent items. Must match
  `^(\.|[A-Za-z0-9._/-]+)$`.
- artifacts_in
- artifacts_out
- checks — an array of human-readable check descriptions (e.g.
  `validate-plan.py exits 0`, `render idempotent`). Verification is manual or
  scripted outside the schema.
- decision (Q items only — schema enforces this restriction; non-Q items MUST NOT
  declare a decision field)
- triggers
- tools_profile
- notes

## Identifier Grammar
- Milestone IDs: `X<number>` (example: `X1`)
- Sprint IDs: `S<milestone>.<sprint>` (example: `S1.1`)
- Item IDs: `<TYPE><milestone>.<sprint>.<sequence><optional suffix>`

Where:
- `<TYPE>` is one or more uppercase letters, usually one of `M`, `F`, `D`, `T`, `C`, `Q`
- `<sequence>` is the numeric item number inside the sprint
- `<optional suffix>` is a single lowercase letter (`a`, `b`, `c`, ...)

Rules:
- Bracketed suffixes are invalid (`M1.1.1[a]` is invalid)
- Suffixes are variant/continuation labels assigned in derivation/plan order.
  They MUST form a contiguous lowercase sequence (`a`, `b`, `c`, ...) with no
  gaps. `a` is the first derived variant, `b` the next, etc. Execution order
  is represented by `depends_on`, not suffixes.

Valid examples:
- `M1.1.1`
- `M1.1.1a`
- `T1.1.1b`
- `D1.1.1c`
