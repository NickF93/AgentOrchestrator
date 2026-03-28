---
id: checkpoint-closure-review
role: reviewer
purpose: >
  Review checkpoint, verification, and closure-ready work with a compact,
  evidence-backed result that can drive commit-group closure decisions.
owner: NickF93
version: "1.0.0"
status: active
---

# checkpoint-closure-review

Use this prompt for review, check, and verification tasks where the operator
needs a compact closure-oriented assessment.

## Inputs

- target item or checkpoint ID
- relevant diffs, files, tests, and plan context
- any declared shared profile and protocol IDs from the active PLAN item

## Procedure

1. Read the canonical governance files before evaluating closure readiness.
2. Focus on behavior, regressions, missing validation, and evidence quality.
3. Treat prompts and skills as tool-neutral contracts.
4. Leave runtime-specific execution details to the active profile.

## Output Contract

Return results using `check-result-v1`.

- `verdict`
- `findings`
- `evidence`
- `commands_run`
- `ready_to_close`
- optional `proposed_commit_message`
- optional `follow_up`

## Constraints

- Do not restate or override canonical governance rules.
- Do not put runtime-specific tool behavior in this prompt.
- When evidence is incomplete, record that explicitly in `findings` or `follow_up`.
