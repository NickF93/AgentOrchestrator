# quick-fix · evals

Test prompts and objective assertions for the `quick-fix` skill,
authored using the
[`skill-creator`](https://github.com/anthropics) eval format.

## Why this folder exists

`SKILL.md` documents the skill's procedure. This folder documents how
we will *check* that the procedure actually fires, refuses, and
produces the right artefacts when an operator phrases a request the way
operators actually phrase requests — not the way the skill is written.

The five sibling skills in this repository (`plan-checkpoint-close`,
`gitflow-pr-only`, `repo-bootstrap`, `plan-validate-render`,
`workspace-sync`) currently rely on the local quality gates
(`validate-plan.py`, `run-gates.sh`, `pytest`) for correctness checks.
Adding `evals/` for `quick-fix` does not break that convention — it
extends it for skills whose value lives partly in triggering behaviour
(refusing on `develop`, refusing after a dirty edit), which the gates
do not exercise.

## Layout

```
evals/
├── README.md   — this file
└── evals.json  — prompts + objective assertions (no runs yet)
```

## What is in `evals.json`

Three test prompts that together exercise the most important triggering
and refusal paths:

1. **`happy-path-typo-fix-on-topic-branch`** — operator on a topic
   branch with a clean working tree asks for a tiny typo fix.
   Expectation: the skill scaffolds the F-item and the
   `commit_group`, runs the validator, prepares the closure commit
   message, and does **not** edit the in-scope file itself.
2. **`refuses-on-develop-points-to-gitflow`** — operator on `develop`
   asks for a one-line patch. Expectation: the skill refuses and
   points to `gitflow-pr-only` (`action: start`). `plan/PLAN-current.yaml`
   stays untouched.
3. **`refuses-retroactive-tracking-when-scope-already-dirty`** —
   operator already edited the in-scope file before asking for
   tracking. Expectation: the skill refuses and explains the
   plan-first ordering. The dirty file stays dirty; the skill does
   not stash or revert on the operator's behalf.

Each prompt carries a list of assertions with descriptive names
(`plan_current_yaml_gains_F_item`, `skill_verdict_is_blocked_or_fail`,
`no_ai_attribution_in_proposed_commit_message`, …). Assertions are
objective and binary; they read clearly in a benchmark viewer so a
glance tells you exactly which behaviour was checked.

## What is **not** in here (yet)

- **No subagent runs.** Running the full `skill-creator` eval loop
  (with-skill vs. baseline subagents in parallel, graded outputs,
  benchmark.json, eval viewer) is intentionally deferred. The schema is
  in place so that loop can be wired up later without changing the
  prompts or assertions.
- **No `benchmark.json` / `grading.json`.** These are produced by the
  run/grade tooling; they do not live in source.
- **No assertions for refinements not in scope.** Trigger-accuracy
  evals (the `skill-creator` description-optimisation loop) are
  separate and are not represented here.

## How to run later (sketch, not normative)

When the eval loop is wired up, the expected invocation will look
roughly like:

```bash
# from a skill-creator workspace, not this repo:
python -m scripts.aggregate_benchmark \
  /tmp/quick-fix-workspace/iteration-1 \
  --skill-name quick-fix

nohup python <skill-creator-path>/eval-viewer/generate_review.py \
  /tmp/quick-fix-workspace/iteration-1 \
  --skill-name quick-fix \
  --benchmark /tmp/quick-fix-workspace/iteration-1/benchmark.json \
  --static /tmp/quick-fix-eval-review.html \
  > /dev/null 2>&1 &
```

Until then, the prompts and assertions in `evals.json` serve as a
written specification of "what `quick-fix` should do when invoked",
independent of any particular runtime.
