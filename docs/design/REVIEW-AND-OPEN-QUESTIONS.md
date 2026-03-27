# Architecture Review & Open Questions
## AgentOrchestrator — Control Plane OS Repository

**Based on:** `documento-architetturale-control-plane-coding-agents.md` v1.0  
**Review date:** 2026-03-27  
**Reviewer:** GitHub Copilot (claude-sonnet-4.6)  
**Status:** working document — answers to open questions become decisions in PLAN.yaml

---

## 1. What is already strong — confirmed decisions

These parts of the architecture are coherent and should be locked as-is:

| Decision | Rationale | Where defined |
|---|---|---|
| 3-level model (control plane / workspace runtime / repo local) | Clean separation of shared model vs. runtime materialization vs. local specifics | §5 |
| One authority per concern (canonical source rule) | Foundation of the whole system; without it everything degrades | §6 |
| Workflow shared, plan local | Scales across repos without global plan coupling | §1, §21 |
| Taxonomy shared, software constraints local | Vocabulary unifies across tools; constraints stay bounded per-repo | §10 |
| `PLAN.yaml` as source of truth, `PLAN.md` / `PLAN.dot` as generated views | Right split: structured data for tooling, readable for humans, graph for DAG; rendering must be deterministic | §8, §9 |
| Planner/orchestrator = single writer of the plan | Avoids conflicting concurrent writes; worker agents propose, orchestrator commits | §4.1.6 |
| Human plans in milestone/sprint/item; machine executes dependency-driven | Sequentiality is a human semantic, not a runtime constraint | §11 |
| Commit groups as the natural commit boundary | More flexible than "one item = one commit", still traceable | §12 |
| Git automation in phases (A→B→C→D) | Correct order of risk; irreversible actions introduced only after stability is proven | §14 |
| Tool-neutral model (role/effort/triggers/tools_profile) | Portability across Codex, Claude, Copilot, Kilo without rewriting the model | §13 |
| `gitflow_pr_only_terminal_workflow.md` already in repo | Git discipline for developers and agents is already documented; feeds directly into Phase A/B automation | — |

---

## 2. Open questions — decisions required before implementation

These must be answered (items `Q1`–`Q5` in `PLAN.yaml`) before writing the schema, templates, and scripts.

### Q1 — PLAN.yaml schema contract (HARD BLOCKER for M2, M4)

**Problem:** The document defines fields at §10.7 but does not specify:
- Which fields are required vs. optional per item type
- Legal state transitions (e.g., can an item go from `planned` to `verified` directly?)
- Whether container items (`X`, `S`) may appear in `depends_on` of executable items
- The exact operational difference between `verified` and `done`
- Whether `commit_group` is required on all executable items or advisory

**Decision needed:** A formal, minimal state machine + required field table.

**Why it matters:** Without this, `validate-plan.py` cannot fail deterministically. The schema becomes a suggestion, not a contract.

---

### Q2 — Runtime materialization strategy for Level-1 files (HARD BLOCKER for M3, M5)

**Problem:** Level-1 (`AGENTS.md`, `CLAUDE.md`, tool-specific files) are described as a "materialization" of Level-0, but the mechanism is undefined:
- Option A: Script-generated from Level-0 templates on each `sync-workspace` run (fully deterministic, read-only at Level-1)
- Option B: Hand-maintained thin adapters that import/reference Level-0 (flexible, drift-prone)
- Option C: Hybrid — generated shell files that `@import` or include canonical blocks from Level-0

**Decision needed:** Pick one. Commit to it.

**Why it matters:** If Level-1 files are edited by hand, they will drift from Level-0. If they are generated, they need a stable generation contract and must not be committed alongside uncommitted Level-0 changes.

---

### Q3 — Control-plane release/consumption model (SOFT BLOCKER for M5)

**Problem:** Downstream repos need to know how they consume this control plane:
- Option A: Straight from `main` (always latest, no pinning)
- Option B: Tagged releases (e.g., `v0.1.0`) — downstream pin to a tag
- Option C: Pinned commit SHA in a lockfile inside each downstream repo

**Decision needed:** Pick the model for the MVP. Note: for a first MVP where you are the only consumer, `main` is fine. It becomes a real concern when multiple people or machines use this.

**Why it matters:** The `sync-workspace.sh` script must know whether to pull from a branch or a tag. The `bootstrap-repo.sh` must know whether to record a locked version.

---

### Q4 — Scope definition for collision detection (SOFT BLOCKER for M2)

**Problem:** §11.4 says parallel items must not have "colliding scope", but `scope` is a free text field in §10.7. The document gives examples (`agent-os/workflow`, `agent-os/scripts`) but does not define:
- Whether scope is a path glob, a named module, or both
- Who validates scope exclusivity (the schema validator, the orchestrator, or neither)
- What happens when an item legitimately touches multiple scopes

**Decision needed:** Define the `scope` field format and whether the validator checks it.

**Why it matters:** Scope collision detection is the main safety mechanism for DAG parallelism. Leaving it undefined means the orchestrator can never enforce it.

---

### Q5 — Failure semantics for tooling (SOFT BLOCKER for M4)

**Problem:** §18.3 says "generate only, never hand-edit," but it does not define:
- What `validate-plan.py` exits non-zero on (schema errors? state transition violations? dangling depends_on?)
- Whether `render-plan.py` is idempotent (i.e., regenerating the same input always produces the same output)
- Whether generated artifacts (`PLAN.md`, `PLAN.dot`) must be committed in the same commit as the source `PLAN.yaml` change
- Whether validation runs pre-commit (hook) or only on CI

**Decision needed:** Define the hard-fail conditions for validate, the idempotency contract for render, and the commit hygiene rule for generated artifacts.

**Why it matters:** Agents that update `PLAN.yaml` must know whether they are responsible for also regenerating and committing the views, or whether a separate step handles that.

---

## 3. Specification gaps — not blockers but should be resolved before Phase B

These are not blockers for the Level-0 MVP but will become problems at Phase B (push / draft PR automation) or when a second person/machine joins.

### G1 — `prompts/` directory is mentioned but not specified
§15.1 lists `prompts/orchestrator.md` and `prompts/reviewer.md`. No format, no required fields, no lifecycle for these is defined.

### G2 — `skills/` directory is mentioned but empty in the MVP
§7.8 and §15.1 mention a `skills/` directory. The VS Code Copilot agent-customization skill format is known (YAML frontmatter + markdown body). Whether the same format applies here, or a different packaging, must be decided before the directory is populated.

### G3 — How `REPO_MAP.md` stays current is undefined
§7.6 says it must contain entry points, hot paths, fragile areas. Nothing says who updates it, when, or via what trigger. It risks becoming stale silently.

### G4 — ADR lifecycle is undefined
§7.7 says ADRs go in `docs/adr/`. No template, no numbering convention, no state machine (proposed / accepted / superseded / deprecated) is given.

### G5 — No failure mode for the 3-level authority hierarchy
The canonical source rule says "one concern, one authority." But in practice agents will sometimes write to non-canonical files. Nothing in the model defines a recovery/correction procedure for that.

---

## 4. Priority order for next actions

```
Q1 → M2 (schema) → M4 (scripts: validate + render)
Q2 → M3 (templates) → M5 (scripts: bootstrap + sync)
Q3 → M5 (sync-workspace)
Q4 → M2 (schema: scope field)
Q5 → M4 (scripts: failure contracts)
M1 (workflow docs) can proceed after Q1+Q2+Q3 are answered
```

In PLAN.yaml terms, the dependency DAG for Sprint 1 is:

```
D1 (this doc) ──► Q1 ──► M2 ──► M4 ──► T1 ──► C1
              └──► Q2 ──► M3 ──► M5 ──► T2 ──┘
              └──► Q3 ──► M5
              └──► Q1+Q2+Q3 ──► M1 ──► M3
```

---

## 5. Suggested answers (proposals — not decisions until the user confirms)

| Q# | Proposed answer |
|---|---|
| Q1 | Define a minimal required-field table: `id`, `type`, `title`, `status`, `role`, `effort` required on all executable items. State machine: `planned → ready → in_progress → review → verified → done`; `blocked` can be entered from any active state. Containers (`X`, `S`) may not appear in `depends_on`. `verified` = all checks pass; `done` = also committed and optionally pushed. |
| Q2 | Option A for the MVP (script-generated, Level-1 files are read-only outputs). Generated files get a header comment: `# AUTO-GENERATED by sync-workspace.sh from agent-os/templates/. Do not edit manually.` |
| Q3 | For MVP: straight from `main`. When first external consumer joins, introduce tags. |
| Q4 | `scope` is a path prefix relative to repo root (e.g., `agent-os/workflow`). Validator checks that no two simultaneously `in_progress` items share an identical scope prefix. Multiple scopes on one item: comma-separated list. |
| Q5 | `validate-plan.py` exits non-zero on: missing required fields, unknown state values, `depends_on` referencing unknown IDs, container types in `depends_on`, and state transitions that skip required stages. `render-plan.py` is idempotent. Generated artifacts must be committed in the same commit as `PLAN.yaml`. Validation runs as a pre-commit hook AND is callable standalone. |

These proposals become binding only when confirmed by the human owner and recorded as `decide` actions on the `Q` items in `PLAN.yaml`.
