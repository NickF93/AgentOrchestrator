# TODO — Personal Checklist

> Not normative. Not governance. Not for agents.
> Just a human-readable reminder of what's done and what's next.

---

## Control Plane Foundation (Level 0) — Priority: P0 (done)

- [x] Workflow model, lifecycle, taxonomy, git policy
- [x] PLAN schema + validator + renderer
- [x] Governance hardening (authority model, DAG rules, automation policy)
- [x] Canonical consistency and tracking discipline
- [x] Planning model execution optimization
- [x] Commit hook enforcement and runtime alignment
- [x] Local quality gates (ruff, mypy, pytest, shellcheck)
- [x] Environment portability — `AGENT_PYTHON` env var, `.env` per workstation

## Runtime Portability — Priority: P0 (done)

- [x] Runtime lifecycle tiers (experimental / supported / first-class)
- [x] Claude — first-class (adapter, profile, workspace template, sync)
- [x] Codex — first-class (adapter, profile, workspace template, sync)
- [x] Gemini — first-class (repo-local `GEMINI.md`, bootstrap template)
- [x] Cursor — first-class (repo-local `.cursor/rules/governance.mdc`, bootstrap template)
- [x] Copilot — first-class (repo-local `.github/copilot-instructions.md`, bootstrap template)
- [x] Kilo — first-class (repo-local `.kilo/rules/governance.md`, bootstrap template)
- [x] Extend adapters for all runtimes (all six promoted to first-class)

## Skills — Priority: P1

- [x] `plan-checkpoint-close` — closing C items with validations and commit closure
- [x] `gitflow-pr-only` — procedural PR-based git flow
- [x] Skill discovery table in `AGENTS.md` and repo template
- [x] `repo-bootstrap` — wrapper around `bootstrap-repo.sh` + post-bootstrap checks
- [x] `plan-validate-render` — validate + render + interpret failures/warnings
- [ ] `workspace-sync` — regenerate Level-1 files, report provenance drift
- [ ] `repo-map-refresh` — refresh `REPO_MAP.md` on triggers
- [ ] `checker-reviewer-delegation` — delegation contract once runtime roles settle
- [ ] `quick-fix` — scaffold F-type item + commit_group in one step, reducing tracking-first friction without weakening the invariant (ref: issue #8)

## Git Flow — Priority: P0 (done)

- [x] Define and document the git branching/PR workflow
- [x] Implement `gitflow-pr-only` skill
- [x] Planning-to-git mapping and branch naming convention
- [x] Register `gitflow-pr-only` as a portable shared asset

## Shared Asset Distribution — Priority: P1

- [x] Registry, prompts, profiles, protocols model
- [x] Two-root consumption (`control_plane_root` / `repo_root`)
- [x] `materialize-shared-asset.sh` for vendoring into repos
- [ ] Ensure sharing works end-to-end across Layer 0 and Layer 2

## Layer 1 — Workspace Runtime — Priority: P2

- [x] `sync-workspace.sh` renders `AGENTS.md`, `CLAUDE.md`, `.codex`
- [x] Workspace templates with `{{CONTROL_PLANE_ROOT}}` placeholders
- [ ] Harden Layer-1 lifecycle (drift detection, staleness checks)
- [x] Evaluate workspace template boundaries — repo-scoped runtimes (Gemini, Cursor, Kilo, Copilot) use bootstrap templates, not workspace templates

## Layer 2 — Repository-Local Governance — Priority: P1

- [x] `bootstrap-repo.sh` scaffolds `AGENTS.md`, `PLAN.yaml`, commit hook, and thin runtime entrypoints for Claude, Codex, Gemini, Cursor, Copilot, and Kilo
- [ ] End-to-end bootstrap + governance validation in a real downstream repo
- [ ] Verify Layer-2 repos can consume shared assets cleanly

## Plan Scaling / Archival — Priority: P1

- [x] Evolve beyond one ever-growing active `PLAN.yaml` without losing the current execution shape
- [x] Separate the active plan surface from archived plan fragments
- [x] Add an archive index that makes closed milestones and old fragments easy to find
- [x] Extend validator and renderer loading to work cleanly across multiple plan files
- [x] Keep execution focused on the active surface while still supporting historical lookup
- [ ] Add digest-style historical summaries so old work can be consulted without loading everything
- [x] Think through append-only archive habits so plan history stays easy to trust and inspect

## Execution Gap Closure — Priority: P1

> Items derived from issue #8 review analysis. These close the gap between
> governance rules and runtime evaluation without building a full engine.

- [ ] Add `--compute-ready` flag to `validate-plan.py` — read-only query that evaluates the dependency predicate and outputs ready items as JSON
- [ ] Add `on_fail` optional metadata field to item schema — declarative failure policy per item (enum: `retry:<N>`, `escalate`, `pivot:<item_id>`, `block`)
- [ ] Add structured `checks` format alongside prose checks — `{command, expected_exit, timeout}` for programmatic verification
- [ ] Add `scope_exclusive` field for smarter scope collision handling — default `true` (current behavior), `false` allows overlapping prefixes

## Runtime Execution Layer — Priority: P1

- [ ] Sketch the runtime layer that sits below the control plane and above worker execution
- [ ] Clarify the orchestrator role as the runtime writer/coordinator at a conceptual level
- [ ] Model persistent worker identities separately from ephemeral sessions
- [ ] Define minimal runtime state storage for active sessions, retries, leases, and resumability
- [ ] Define task dispatch shape across orchestrator, workers, and validation loops
- [ ] Decide what runtime isolation is needed between concurrent workers and repos
- [ ] Add timeout, retry, cancel, and failure semantics that are simple enough for an MVP
- [ ] Keep durable execution minimal at first: enough to survive interruptions without building a full engine

## Work Units / Live Tracking — Priority: P2

- [ ] Separate runtime work units from canonical PLAN items so live execution does not distort planning structure
- [ ] Define convoy or work-batch concepts for grouped runtime dispatch
- [ ] Design a task-packet shape for worker handoff, narrow context loading, and evidence return
- [ ] Add a runtime event ledger for packet state changes, stalls, retries, and completions
- [ ] Define blocked-work escalation objects instead of hiding runtime stalls inside plan notes
- [ ] Carry budget, token, and cost metadata with runtime packets and work batches
- [ ] Generate runtime packets with dependency awareness instead of flat item fan-out

## Session Continuity / Handoff — Priority: P2

- [ ] Design a session handoff protocol that works across interrupted or time-sliced execution
- [ ] Define a compact session-summary structure for successor pickup
- [ ] Support interrupted-work recovery without turning repo governance files into runtime memory
- [ ] Explore predecessor continuity patterns such as lightweight “ask previous session” retrieval
- [ ] Keep minimal persisted memory per worker identity instead of rebuilding all context every time
- [ ] Inject runtime context from summaries and ledgers rather than stuffing it into repo authorities

## Worker Roles and Effort Routing — Priority: P2

- [ ] Formalize the runtime role set: orchestrator, implementer, verifier, documenter
- [ ] Map work type to default worker role instead of routing everything through one generic lane
- [ ] Define sensible default effort policies for `D` / `T` / `C` / `Q` work versus `M` / `F` work
- [ ] Reserve expensive escalation for difficult implementation and fix paths, not routine traffic
- [ ] Define runtime profile mapping for `low`, `medium`, `high`, and `xhigh` effort
- [ ] Add file-sensitivity and scope-risk weighting so risky paths escalate earlier than safe ones

## Multi-Agent / Sub-Agent — Priority: P2

- [ ] Design the coordination layer instead of leaving multi-agent as an adapter-side placeholder
- [ ] Define the delegation contract between orchestrator-owned planning state and worker-owned execution state
- [ ] Model sub-agent orchestration explicitly rather than treating delegation as a one-off special case
- [ ] Treat `1 orchestrator + 1 implementer + 1 verifier/doc` as the primary operating shape to validate first
- [ ] Make the “do not split” criteria explicit for tiny work, tightly coupled edits, or narrow scopes
- [ ] Define the review boundary between orchestrator-owned state, worker outputs, and integrated repo changes
- [ ] Add cross-model review advisory for C-type items — prefer different runtime for reviewer vs implementer (ref: issue #8, IBM Lessons Learned)

## Merge / Integration Flow — Priority: P2

- [ ] Separate worker completion from integration acceptance so “done working” is not the same as “accepted”
- [ ] Define the path from runtime completion to validation to commit-group closure
- [ ] Add a minimal refinery/finalizer step for cleanup, coherence, and evidence assembly before integration
- [ ] Clarify merge gates for integrated work without duplicating the canonical Git flow text
- [ ] Leave room for an optional PR or merge-queue path after the simpler path works
- [ ] Define a conflict, restack, and revalidation strategy for multi-worker integration pressure

## Observability / Ops — Priority: P3

- [ ] Add a runtime event stream that is actually useful for live execution visibility
- [ ] Build a status view for active packets, queued work, retries, and blocked work
- [ ] Add lightweight watchdog logic for stalled or abandoned workers
- [ ] Standardize structured telemetry across duration, retries, failures, and outcome classes
- [ ] Account for cost, token spend, and retry churn at packet and convoy level
- [ ] Report drift or mismatch between runtime state and control-plane expectations

## Issue Intake — Priority: P3

- [ ] Treat issue tracker integration as intake and translation, not as the planning model itself
- [ ] Define how upstream issues map into milestone, sprint, and item structures
- [ ] Link imported planning work back to upstream issue IDs for traceability
- [ ] Decompose large issues into smaller planning units instead of mirroring issue granularity blindly
- [ ] Decide how much status sync back to the issue tracker is actually useful
- [ ] Keep a clear human override path when imported issue structure is wrong or incomplete

## Downstream Validation Matrix — Priority: P1

- [ ] Validate the full model in a tiny toy repo with almost no legacy complexity
- [ ] Validate in a medium real repo with normal code churn and real review pressure
- [ ] Validate in a more complex repo with broader topology and heavier cross-cutting change risk
- [ ] Validate issue-intake flow against a real backlog source instead of synthetic examples only
- [ ] Validate runtime portability across the supported runtime entrypoints
- [ ] Validate low-context worker execution to see where the current startup burden is still too high

## Documentation Compression / Context Economy — Priority: P1

- [ ] Separate always-load governance (taxonomy, lifecycle, commit contract) from on-demand content (freshness rules, portability model, skill definitions) (ref: issue #8, Tessl "What Survives")
- [ ] Generate compact context digests for workers instead of replaying the same authorities in full
- [ ] Reduce mandatory startup context for routine work
- [ ] Move repetitive operational context into generated packets and runtime summaries
- [ ] Keep normative authority centralized while shrinking runtime prompt load
- [ ] Review `TODO`, `AGENTS`, and workflow docs periodically for duplication drift and prompt bloat

## RFC — Request for Comments / Future Considerations — Priority: P3

- [ ] RFC normative review pass (ensure no stale or conflicting normative content)
- [ ] Evaluate optional external workflow engines or durable runtime backends only if the lightweight model starts to hurt
- [ ] Explore merge queue or batch verification only when the simpler integration flow proves insufficient
- [ ] Add richer supervisor or specialist roles only if the base orchestrator/implementer/verifier/doc split saturates
