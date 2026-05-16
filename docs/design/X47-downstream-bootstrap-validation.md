# X47 Downstream Bootstrap Validation Evidence

Date: 2026-05-16

Issue: <https://github.com/NickF93/AgentOrchestrator/issues/18>

Target repository: <https://github.com/NickF93/AgentOrchestrator-Test>

Control-plane PR: <https://github.com/NickF93/AgentOrchestrator/pull/37>

This document is non-authoritative validation evidence. Governance authority
remains in `AGENTS.md`, `ARCHITECTURE.md`, and `agent-os/workflow/*`.

## Verdict

Pass with one follow-up issue.

The Level-0 bootstrap path was validated end-to-end against the public
`AgentOrchestrator-Test` downstream repository. The target bootstrap branch was
pushed, opened as a PR, marked ready, and merged with a merge commit.

Follow-up created: <https://github.com/NickF93/AgentOrchestrator/issues/38>

## Environment

- `control_plane_root`: `/home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator`
- `repo_root`: `/home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator-Test`
- Control-plane ref used by bootstrap: `2234505`
- Target branch: `feature/X47-governance-bootstrap`
- Target PR: <https://github.com/NickF93/AgentOrchestrator-Test/pull/1>
- Target merge commit: `cd7847160eb3aa91c5108c472dfd898deaedceec`

## Transcript

Target clone and branch setup:

```bash
git clone https://github.com/NickF93/AgentOrchestrator-Test.git /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator-Test
git -C /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator-Test checkout -b feature/X47-governance-bootstrap
```

Result:

```text
Cloning into '/home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator-Test'...
Switched to a new branch 'feature/X47-governance-bootstrap'
```

Bootstrap:

```bash
PYTHON_BIN=/home/niccolo/miniconda3/envs/nn-4/bin/python \
  bash /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator/agent-os/scripts/bootstrap-repo.sh \
  --owner NickF93 \
  --ref 2234505 \
  /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator-Test
```

Result summary:

```text
OK: created AGENTS.md
OK: created ARCHITECTURE.md
OK: created REPO_MAP.md
OK: created plan/PLAN-index.yaml
OK: created plan/PLAN-current.yaml
OK: created README.md
OK: created docs/adr/ADR-0001.md
OK: created .githooks/commit-msg
OK: created .githooks/pre-push
OK: created .github/copilot-instructions.md
OK: created CLAUDE.md
OK: created .codex
OK: created GEMINI.md
OK: created .cursor/rules/governance.mdc
OK: created .kilo/rules/governance.md
OK: created plan/archive
OK: marked executable .githooks/commit-msg
OK: marked executable .githooks/pre-push
OK: Post-bootstrap validation passed
Done.
```

Hook enablement:

```bash
git -C /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator-Test config core.hooksPath .githooks
git -C /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator-Test config --get core.hooksPath
```

Result:

```text
.githooks
```

Independent target plan validation:

```bash
/home/niccolo/miniconda3/envs/nn-4/bin/python \
  /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator/agent-os/scripts/validate-plan.py \
  /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator-Test/plan/PLAN-index.yaml \
  --schema /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator/agent-os/schemas/plan.schema.json
```

Result:

```text
ACTIVE:
  - current_plan: /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator-Test/plan/PLAN-current.yaml
  - milestones: 1
  - sprints: 1
  - items: 1
  - commit_groups: 1
ARCHIVED:
  - archive_root: /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator-Test/plan/archive
  - fragments: 0
  - milestones: 0
  - sprints: 0
  - items: 0
  - commit_groups: 0
OK: plan/PLAN-index.yaml is valid against plan.schema.json
```

Target plan render:

```bash
/home/niccolo/miniconda3/envs/nn-4/bin/python \
  /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator/agent-os/scripts/render-plan.py \
  /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator-Test/plan/PLAN-index.yaml \
  --md /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator-Test/PLAN.md \
  --dot /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator-Test/PLAN.dot
```

Result:

```text
OK: wrote PLAN.md
OK: wrote PLAN.dot
```

Hook smoke checks:

```text
commit-msg valid fixture: exit 0
commit-msg invalid title fixture: exit 1, "Invalid commit title format"
commit-msg attribution-marker fixture: exit 1, "forbidden AI/codegen attribution markers"
pre-push simulated direct main push: exit 1, "Direct pushes to main and develop are forbidden"
pre-push simulated clean topic push: exit 0
```

Target commit:

```bash
git -C /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator-Test add \
  .codex \
  .cursor/rules/governance.mdc \
  .githooks/commit-msg \
  .githooks/pre-push \
  .github/copilot-instructions.md \
  .kilo/rules/governance.md \
  AGENTS.md \
  ARCHITECTURE.md \
  CLAUDE.md \
  GEMINI.md \
  PLAN.dot \
  PLAN.md \
  README.md \
  REPO_MAP.md \
  docs/adr/ADR-0001.md \
  plan/PLAN-current.yaml \
  plan/PLAN-index.yaml
```

Commit result:

```text
[feature/X47-governance-bootstrap 9d062ce] chore(governance): bootstrap repository governance
17 files changed, 780 insertions(+)
```

Target PR flow:

```bash
git -C /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator-Test push -u origin feature/X47-governance-bootstrap
gh pr create --repo NickF93/AgentOrchestrator-Test --base main --head feature/X47-governance-bootstrap --draft
gh pr checks 1 --repo NickF93/AgentOrchestrator-Test
gh pr ready 1 --repo NickF93/AgentOrchestrator-Test
gh pr merge 1 --repo NickF93/AgentOrchestrator-Test --merge
git -C /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator-Test checkout main
git -C /home/niccolo/PRGM/1-git-prj/github/AgentOrchestrator-Test pull --ff-only origin main
```

Result:

```text
PR #1 merged at 2026-05-16T16:09:18Z
Merge commit: cd7847160eb3aa91c5108c472dfd898deaedceec
Local main fast-forwarded to origin/main
Feature branch preserved locally and remotely
```

## Findings

- Bootstrap created the expected governance files, runtime entrypoints, hooks,
  split-plan files, README, ADR seed, and generated plan views.
- Repo-local hooks were executable and enforced the commit-message and protected
  branch push checks.
- Target plan validation and rendering worked from the Level-0 scripts against
  Layer-2 data.
- The downstream publication path used branch + PR + merge commit; no direct
  commit was made on the target `main` branch.
- Initial bootstrap used `main` as the target PR base because the test repo was
  a new main-only repository before governance was installed.
- Gap: `plan/archive/` is created by bootstrap but is empty, so Git does not
  preserve it after commit and merge. Follow-up: issue #38.
