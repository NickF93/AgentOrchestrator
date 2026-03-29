# Git Flow Policy

## Objective

Define the branching model, merge rules, and operational constraints for
repositories governed by the PR-only Git Flow workflow.

This is a canonical workflow authority. The non-authoritative design
reference is `docs/design/gitflow-pr-only-terminal-workflow.md`.

## Branch Model

### Long-lived branches

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready code. Every commit is a merge from a PR. |
| `develop` | Integration branch. Receives features, bugfixes, and back-merges from hotfix/release. |

### Topic branch families

| Family | Created from | PR target | PR count | Tagging |
|--------|-------------|-----------|----------|---------|
| `feature/*` | `develop` | `develop` | 1 | No |
| `bugfix/*` | `develop` | `develop` | 1 | No |
| `hotfix/*` | `main` | `main` + back-merge | 2 | Yes (annotated) |
| `release/*` | `develop` | `main` + back-merge | 2 | Yes (annotated) |
| `support/*` | `main` or tag | child branch targets `support/*` | 1 (child branch) | No |

Branch creation uses `git flow ... start` (AVH Edition) for all families
except `support/*` child branches, which use normal `git checkout -b`.

## Workflow Invariants

These rules apply to all branch types without exception:

1. **Immediate push.** Every newly created branch MUST be pushed to origin
   immediately after creation (`git push -u origin <branch>`).
2. **Immediate draft PR.** A draft PR MUST be opened immediately after the
   branch is pushed, for every branch type. Do not predict whether work
   will be long or short.
3. **Micro-commits and frequent pushes.** Commit early, push at least by
   end of day.
4. **Explicit staging only.** Stage files by name (`git add <file> ...`).
   Never use `git add -A` or `git add .`.
5. **No rebase.** Never rebase a topic branch. History is preserved as-is.
6. **Merge-only synchronization.** Always merge the base branch into the
   topic branch (`git merge <base>`). Never rebase onto the base.
7. **Terminal-only PR merge.** Merge PRs exclusively from the terminal
   using `gh pr merge --merge`. No squash, no rebase merge.
8. **Agents never delete branches.** Neither local nor remote, neither
   topic nor long-lived. The human operator may prune manually.
9. **Base update uses fast-forward only.** When updating a long-lived
   branch, always use `git pull --ff-only origin <branch>`.

## Forbidden Operations

The following commands MUST NOT be used in this workflow:

| Command | Reason |
|---------|--------|
| `git flow ... finish` | Performs local merges and branch deletion; conflicts with PR-only model. |
| `gh pr merge --delete-branch` | Deletes the branch after merge; conflicts with branch retention. |
| `git add -A` / `git add .` | Blanket staging risks committing secrets, editor files, or binaries. |
| `git rebase` (on topic branches) | Rewrites history; conflicts with merge-only model. |
| `git push --force` (on `main`/`develop`) | Destroys shared history. |

## Synchronization Rule

Before a PR can be merged, the topic branch MUST incorporate the latest
state of its base branch:

1. `git checkout <base> && git pull --ff-only origin <base>`
2. `git checkout <topic-branch>`
3. `git merge <base>`
4. Resolve conflicts if any (see Conflict Resolution below).
5. `git push`

The PR merge MUST be conflict-free. If the base moved between push and
merge, repeat the synchronization.

## PR Topology

### Single-PR flows (feature, bugfix)

One PR from the topic branch toward `develop`. After merge, update local
`develop` with `git pull --ff-only`.

### Two-PR flows (hotfix, release)

1. **PR1** from the topic branch toward `main`. After merge:
   - update local `main` (`git pull --ff-only`),
   - create an annotated tag on `main`,
   - push the tag.
2. **PR2** (back-merge) from the topic branch toward the back-merge target.

### Back-merge target selection

- If a `release/*` branch currently exists, the back-merge targets that
  release branch instead of `develop`. The release branch will carry the
  changes into `develop` when it is itself merged.
- If no release branch exists, the back-merge targets `develop`.

### Support flow

`support/*` branches are long-lived. Work happens on child branches
(e.g., `fix/3.2.x-BUG-789`) created with normal `git checkout -b`.
The child branch opens a single PR toward the `support/*` parent.

## Tagging Policy

- Hotfix and release branches receive an annotated tag after PR1 (toward
  `main`) is merged.
- Tags are created on `main` after `git pull --ff-only`.
- Format: `git tag -a <version> -m "<type> <version>"`.
- Tags are pushed individually: `git push origin <version>`.

## Conflict Resolution

### Where conflicts surface

Conflicts can only occur during the synchronization merge (step 3 of the
synchronization rule). They MUST be resolved on the topic branch before
the PR merge, which MUST always be conflict-free.

### Conflict classification

| Classification | Definition | Who resolves |
|---------------|------------|--------------|
| **Trivial** | Only one side has semantic changes (the other is whitespace, formatting, or context drift). Also: conflicts in generated files that will be regenerated. | Agent resolves |
| **Non-trivial** | Both sides modified the same logical block, or the conflict is in governance/authority files, or the agent is not confident. | Agent escalates to human |

### Resolution rules

- **Trivial:** agent resolves, commits the merge, and documents the
  resolution in the PR description (files affected, hunks, strategy).
- **Non-trivial:** agent aborts the merge (`git merge --abort`), reports
  the conflicting files and hunks to the human, and waits for human
  resolution.
- Every conflict resolution MUST be reported in the PR description or as
  a PR comment, regardless of who resolved it.

### Two-PR flow conflicts

PR2 (back-merge) follows the same synchronization and conflict resolution
rules as PR1. The agent merges the back-merge target into the topic
branch, resolves trivial conflicts, and escalates non-trivial ones.

The tag created between PR1 and PR2 is unaffected by PR2 conflicts — it
points to the `main` commit, which is already safe.

## Branch Protection Enforcement

GitHub server-side branch protection requires a paid plan for private
repositories. This workflow enforces protection through two layers.

### Layer 1 — Local git hooks

A `pre-push` hook in `.githooks/pre-push` prevents direct pushes to
`main` and `develop`. Installation: `git config core.hooksPath .githooks`.

This SHOULD be part of the repository bootstrap script.

Limitation: local hooks are client-side and can be bypassed with
`--no-verify`. In a small disciplined team this prevents accidents,
not malice.

### Layer 2 — Agent governance

Agents follow the rules in this file, `AGENTS.md`, and the `gitflow-pr-only`
skill. Agents MUST NOT push directly to `main` or `develop` under any
circumstances.

### Deferred — GitHub Actions enforcement

Server-side detection and alerting via GitHub Actions is deferred to a
future milestone. When implemented, it will provide:
- detection and alerting on direct pushes to protected branches,
- PR validation (branch naming, target correctness),
- status check enforcement.

### Branch protection principles

- `main` and `develop` MUST require PR-based merging (no direct push).
- Rebase merging and squash merging SHOULD be disabled at the repository
  level when the GitHub plan allows it.
- Auto-delete head branches MUST be disabled.
- Force push MUST NOT be used on `main` and `develop`.
- Topic branches require no protection.

### GitHub repository settings

| Setting | Value |
|---------|-------|
| Allow merge commits | Yes |
| Allow squash merging | No |
| Allow rebase merging | No |
| Automatically delete head branches | No |

## Relationship to Automation Phases

This workflow operates at Phase B minimum (push + PR creation). Final PR
merge placement depends on Phase C authorization per
`git-automation-policy.md`.

- **Phase A:** branch creation, local commits, plan updates, view
  rendering — all permitted.
- **Phase B:** push, draft PR creation, synchronization merge — requires
  Phase B unlock.
- **Phase C:** `gh pr merge` — requires Phase C authorization.

## Design Reference

The non-authoritative design reference with installation guides, Mermaid
diagrams, detailed rationale, command-by-command explanations, and
footnotes is:

`docs/design/gitflow-pr-only-terminal-workflow.md`

The design document is not executable. Normative rules live in this file.
