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

## Commit Group Semantics

- `commit_group` is a plan-time declaration, not an ad-hoc commit label.
- All items in the same `commit_group` are intended to land in one git commit.
- A git commit closes exactly one `commit_group`.
- The commit message footer MUST reference the closed item IDs and exactly one
  `commit_group` ID.
- File modifications are expected to be attributable to the item's declared
  `scope` and/or explicit artifact list.

## Optional Metadata Fields

- depends_on — list of dependency target IDs (sprint or item IDs; milestone IDs
  are not valid dependency targets)
- scope — a file or directory path prefix (e.g. `agent-os/scripts/`, `AGENTS.md`).
  Used for collision detection between concurrent items. Must match
  `^(\.|[A-Za-z0-9._/-]+)$`.
- artifacts_in
- artifacts_out
- checks — an array of prose check descriptions or structured check metadata.
  Prose checks remain human-readable strings (e.g. `validate-plan.py exits 0`,
  `render idempotent`). Structured checks use `command`, `expected_exit`, and
  `timeout` fields so closure tooling can identify programmatic checks without
  parsing prose. `validate-plan.py` validates structured check shape but does
  not execute check commands.
- shared_assets — optional object for executable items that consume Layer-0
  shared assets. Supported fields:
  - `skill`
  - `prompt`
  - `profile`
  - `result_protocol`
  - `context_policy` (`focused`, `diff_only`, `repo_full`)
  - `resolution_mode` (`workspace`, `vendored`)
  Referenced asset IDs MUST exist in `agent-os/registry/shared-assets.yaml`.
  Default `resolution_mode` is `workspace`. Default `context_policy` for
  checker/reviewer/test tasks is `focused`. Runtime-specific knobs MUST NOT be
  added directly to PLAN items; they belong in profiles.
- decision (Q items only — schema enforces this restriction; non-Q items MUST NOT
  declare a decision field)
- triggers — **DEFERRED**: adapter-level invocation hints; semantics TBD;
  non-normative in MVP. Reserved for future adapter mappings; MUST NOT drive
  execution semantics or be required by validation logic until the adapter
  model is implemented.
- tools_profile — **DEFERRED**: adapter-level capability/profile label;
  semantics TBD; non-normative in MVP. Reserved for future adapter mappings;
  same restrictions as triggers.
- notes
- requires_phase — automation phase gate (enum: `A`, `B`, `C`, `D`). When set,
  the item is declaring that it touches deferred automation and requires the
  specified phase to be unlocked. Validator enforces that `approval_ref` is
  present when this item is in ready/in_progress/review.
- approval_ref — human sign-off reference (e.g. ADR ID, decision item ID).
  Required when `requires_phase` is set and item is active. Documents the
  authorization for implementing deferred automation.

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
