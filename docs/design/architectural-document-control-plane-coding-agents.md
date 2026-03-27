# Architectural Document — Portable and DAG-ready Setup for Coding Agents
## Shared control plane, local repo governance, machine-readable plan, and generated views

**Version:** 1.0  
**Status:** consolidated architectural proposal  
**Language:** English  
**Audience:** human owner/orchestrator, coding agents, technical reviewers  
**Purpose:** define a general, portable, and incremental model for using coding agents across multiple repositories with:
- shared and versioned workflow;
- local software constraints per repo;
- machine-readable execution plan;
- future capability for DAG-oriented and multi-agent execution;
- gradual growth of Git/GitHub automation without introducing an overly heavy system from the start.

---

## Index

1. [Executive summary](#1-executive-summary)
2. [Context, problem, and objectives](#2-context-problem-and-objectives)
3. [Authoritative sources and rationale for choices](#3-authoritative-sources-and-rationale-for-choices)
4. [Architectural decisions already made](#4-architectural-decisions-already-made)
5. [General 3-level architecture](#5-general-3-level-architecture)
6. [Authority model and canonical source rule](#6-authority-model-and-canonical-source-rule)
7. [Distribution of responsibilities across files and directories](#7-distribution-of-responsibilities-across-files-and-directories)
8. [Why `PLAN.yaml` as source of truth](#8-why-planyaml-as-source-of-truth)
9. [Why `PLAN.md` and `PLAN.dot` as generated views](#9-why-planmd-and-plandot-as-generated-views)
10. [Shared taxonomy: items, actions, states, roles, and effort](#10-shared-taxonomy-items-actions-states-roles-and-effort)
11. [DAG-ready execution model](#11-dag-ready-execution-model)
12. [Commit groups, development blocks, and closure](#12-commit-groups-development-blocks-and-closure)
13. [Subagents and cross-tool portability](#13-subagents-and-cross-tool-portability)
14. [Git/GitHub automation in phases](#14-gitgithub-automation-in-phases)
15. [Concrete structure of the 3 levels](#15-concrete-structure-of-the-3-levels)
16. [What goes in each level: files, authority, and non-goals](#16-what-goes-in-each-level-files-authority-and-non-goals)
17. [First repo-agnostic MVP to set up](#17-first-repo-agnostic-mvp-to-set-up)
18. [Instructions to give the agent to implement the setup](#18-instructions-to-give-the-agent-to-implement-the-setup)
19. [Growth roadmap: what to do first and what to defer](#19-growth-roadmap-what-to-do-first-and-what-to-defer)
20. [Mapping the approach to the DUCT case and other existing repos](#20-mapping-the-approach-to-the-duct-case-and-other-existing-repos)
21. [Final summary](#21-final-summary)
22. [Handoff package to continue the conversation elsewhere](#22-handoff-package-to-continue-the-conversation-elsewhere)
23. [References](#23-references)

---

## 1. Executive summary

The consolidated architectural proposal is as follows:

- **Level 0 — central control plane repository**  
  A dedicated repository, versioned and portable across machines, that contains the shared model:
  cross-repo workflow, taxonomy, templates, prompts, sync/render/validation scripts, and — in later phases — skills and supporting tooling.

- **Level 1 — workspace runtime layer**  
  A workspace root that contains the actual repositories and the shared files that agents genuinely need to read at runtime (`AGENTS.md`, `CLAUDE.md`, or equivalents). This level is not the source of truth for the control plane: it is its runtime materialization.

- **Level 2 — repo-local layer**  
  Each individual repository has its own thin local files: software constraints, repo map, local plan, optional ADRs, and local architectural documentation.

The central choices already fixed are:

1. **No shared global `PLAN` across repos.**  
   The work plan is always local to the repository/subproject.

2. **Yes to a shared taxonomy.**  
   What is shared is the operational vocabulary: item types, action taxonomy, lifecycle, roles, effort, and dependency rules.

3. **The source of truth for the plan is machine-readable.**  
   The recommended format is `PLAN.yaml`.  
   `PLAN.md` and `PLAN.dot` are generated views.

4. **The plan is written by an orchestrator/planner agent, not by the human manually.**  
   The human defines the mission, constraints, choices, and limits; the agent translates them into `PLAN.yaml`.

5. **Sequentiality remains human, no longer a global runtime rule.**  
   The human will continue to think in milestone/sprint/item.  
   The agent will execute items according to explicit dependencies and compatible groups.

6. **The subagent model must be neutral and portable.**  
   The shared concepts are role, effort, trigger, and tool profile; mapping to Codex, Claude, Copilot, and other tools happens downstream.

7. **Git/GitHub automation must be introduced in phases.**  
   First branch naming, commit groups, plan updates, and view rendering.  
   Only afterwards push, draft PR, merge with `develop`, and only later optional final auto-merge.

This architecture is the best option today, not because a single vendor has published it as a unique standard, but because it cleanly aligns the patterns documented by:
- OpenAI / Codex (hierarchical `AGENTS.md`, parallel tasks, isolated worktrees);
- Anthropic / Claude Code (hierarchical memories, separated subagents, modular imports);
- GitHub Copilot (repository-wide and path-specific instructions, nearest-file precedence);
- Kilo (custom modes / workflow specialization).

---

## 2. Context, problem, and objectives

### 2.1 Starting problem

Effective use of coding agents across multiple repositories tends to degrade into one of two extremes:

1. **Everything local to each repo**  
   Each repository has its own `AGENTS.md`, its own plan, its own rules, its own templates.  
   Result: duplication, drift, costly maintenance, low portability.

2. **Everything centralized in a single monstrous document**  
   A single file tries to govern workflow, software architecture, work plan, rationale, and tool-specific instructions.  
   Result: authority mixing, bloated context, conflicts, rigidity, poor readability.

The proposal formalized here avoids both extremes:
- centralizes the **shared model**;
- keeps **repo-specific content** local;
- separates workflow, architecture, tracking, and optional rationale.

### 2.2 Objectives

The objectives of the model are:

- **portability** across repositories;
- **portability** across coding agents and orchestrators;
- **stable and reusable context**;
- **reduction of document entropy**;
- **strict separation of authorities**;
- **preparation for a future DAG-oriented approach**;
- **incremental adoption**: no big bang.

### 2.3 Non-objectives

The following are not immediate objectives:

- building a real DAG runtime engine right away;
- introducing a fully automated merge/push/PR system right away;
- defining plugins or custom skills for every tool right away;
- converting every existing repo to the complete model in a single iteration;
- imposing a single software layout on all repositories.

---

## 3. Authoritative sources and rationale for choices

The decisions formalized here are supported by the following evidence/documentation:

### 3.1 OpenAI / Codex
OpenAI documents that:
- Codex can work on **many tasks in parallel**;
- each task runs in an **isolated environment**;
- `AGENTS.md` guides Codex on how to navigate the codebase, which commands to use, and which practices to follow;
- the file can live outside the repo and the semantics are **hierarchical by directory scope**.

**Architectural implication:** the workspace level with a shared `AGENTS.md` makes sense at runtime; the local repo level makes sense for overrides and local constraints.

### 3.2 Anthropic / Claude Code
Anthropic documents that:
- `CLAUDE.md` is a memory/instruction file in Markdown;
- files can be loaded hierarchically;
- `@import` enables modularity;
- subagents have separate context, their own tools, and are defined by Markdown + YAML frontmatter (`name`, `description`, `tools`);
- subagents help preserve the main context.

**Architectural implication:** the neutral role/effort model is useful; the shared layer can be imported in a modular way; the planner/orchestrator as single-writer of the plan is a good choice.

### 3.3 GitHub Copilot
GitHub documents that:
- there are repository-wide and path-specific instructions;
- `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md` can be used as agent instructions;
- files closer to the specific context have higher priority;
- overlapping or conflicting instructions can create non-deterministic behavior.

**Architectural implication:** the canonical source rule is indispensable; one file per concern is better than many redundant files.

### 3.4 OpenAI Structured Outputs and Prompt Caching
OpenAI documents that:
- Structured Outputs adheres to a schema and is more reliable than "free" JSON output;
- the key order follows the schema;
- Prompt Caching requires **exact prefix matches** and rewards stable, repeated content.

**Architectural implication:** `PLAN.yaml` as source of truth is a strong choice; shared files that are stable and change rarely are desirable.

### 3.5 GitHub branch protection, auto-merge, and merge queue
GitHub documents that:
- protected branches can prevent deletion, force-push, and unauthorized merges;
- auto-merge exists but requires appropriate checks/reviews;
- the standard merge on a PR produces merge commits consistent with the preference for preserving separate history;
- merge queue is not a realistic prerequisite for every basic setup.

**Architectural implication:** Git/GitHub automation must be introduced in phases, not all at once.

---

## 4. Architectural decisions already made

This section collects the decisions that have already emerged and are considered consolidated.

### 4.1 Consolidated decisions

1. **Three distinct levels**
   - level 0 = shared and versioned control plane;
   - level 1 = shared runtime materialization in the workspace root;
   - level 2 = local repositories.

2. **No global `PLAN`**
   - the plan is always local to the repo/subproject.

3. **Yes to a shared taxonomy**
   - item types, action taxonomy, lifecycle, roles, effort, and dependency semantics are shared.

4. **`PLAN.yaml` as source of truth**
   - `PLAN.md` and `PLAN.dot` are generated views.
   - `PLAN.svg` or similar are optional graphical renders.

5. **YAML is not written manually by the human**
   - the human provides intentions, constraints, and decisions;
   - a planner/orchestrator agent updates `PLAN.yaml`.

6. **Single-writer rule**
   - only one agent that owns the plan can write the canonical source of truth;
   - other agents may propose changes or produce evidence, but do not write directly to the canonical plan.

7. **Sequentiality is no longer a global runtime rule**
   - sequentiality remains human semantics of milestone/sprint/item;
   - execution is dependency-driven.

8. **Commit on verified blocks**
   - no longer necessarily "one item = one commit";
   - the natural boundary becomes the verified `commit_group`.

9. **Cross-agent portability as a requirement**
   - the shared model must be neutral;
   - adapters for the various agents come afterwards.

10. **Git automation in phases**
    - first branch naming and commit groups;
    - then push and draft PR;
    - only later merge/auto-merge.

### 4.2 Still-deferred decisions

These are not discarded, but postponed:

- auto-push;
- non-draft automatic PR opening;
- final auto-merge;
- automatic feature branch cleanup;
- merge queue;
- real per-tool subagents;
- full DAG runtime;
- custom skills per agent;
- fully autonomous end-to-end orchestration.

---

## 5. General 3-level architecture

## 5.1 Level 0 — Central Control Plane Repository

### Definition
A dedicated repository that contains the shared and versioned model of the agentic system.

### Purposes
- version the shared workflow;
- version taxonomies and plan schema;
- host templates and bootstrap/sync/render scripts;
- serve as a portable source of truth across multiple machines.

### Non-purposes
- does not host product repositories;
- does not replace the local files of each repo;
- does not directly govern the software architecture of each project.

### Typical content
- shared workflow;
- item/actions/states taxonomy;
- `PLAN.yaml` schema;
- `AGENTS.md`, `ARCHITECTURE.md`, `REPO_MAP.md` templates;
- `sync`, `render`, `validate`, `bootstrap` scripts;
- optional shared prompts;
- optional skills and supporting metadata.

---

## 5.2 Level 1 — Workspace Runtime Layer

### Definition
The filesystem root under which the actual repositories and the shared files that agents genuinely read at runtime live.

### Purposes
- give hierarchical scope to shared instructions;
- materialize `AGENTS.md` and other shared files in positions relevant to the tools;
- avoid duplicating the workflow in every repo.

### Non-purposes
- not the place to manually modify the shared model;
- not the place to define the plan for each project;
- not the place to maintain divergent versions of the same authorities.

### Typical content
- workspace-wide `AGENTS.md`;
- workspace-wide `CLAUDE.md` or equivalent files;
- actual repositories under the root.

---

## 5.3 Level 2 — Repo-local Layer

### Definition
The level of the individual repository or subproject.

### Purposes
- define local software constraints;
- define the project architecture;
- maintain the local work plan;
- keep the local repo map;
- host optional local ADRs.

### Non-purposes
- redefine the globally shared workflow;
- redefine the shared taxonomy;
- redefine the canonical source rule without an explicit decision.

### Typical content
- local `AGENTS.md` (local workflow/authority, entry point to other authorities);
- `ARCHITECTURE.md` or `docs/architecture/*`;
- `PLAN.yaml`;
- generated `PLAN.md` and `PLAN.dot`;
- `REPO_MAP.md`;
- optional `docs/adr/*`.

---

## 6. Authority model and canonical source rule

### 6.1 Basic principle

**Every concern must have a single canonical authority.**

This is the most important rule of the system.  
If it is not respected, everything else becomes fragile.

### 6.2 Main concerns

| Concern | Recommended canonical authority |
|---|---|
| Agentic operational workflow | `AGENTS.md` |
| Software constraints / boundaries / design | `ARCHITECTURE.md` or `docs/architecture/*` |
| Local execution tracking | `PLAN.yaml` |
| Textual plan view | `PLAN.md` (generated) |
| Graph plan view | `PLAN.dot` / `PLAN.svg` (generated) |
| Decision rationale | `docs/adr/*` |
| Practical codebase map | `REPO_MAP.md` |
| Shared templates and cross-repo policy | level 0 (`agent-os/`) |

### 6.3 Precedence rule

The recommended general precedence is:

1. explicit human decisions and instructions;
2. `AGENTS.md` for workflow and authority map;
3. `ARCHITECTURE.md` / `docs/architecture/*` for software constraints;
4. `PLAN.yaml` for active local work;
5. code, tests, config, and real artifacts as implementation evidence;
6. generated views (`PLAN.md`, `PLAN.dot`) as informative artifacts, not authoritative.

### 6.4 Non-duplication rule

- `AGENTS.md` **may reference** `ARCHITECTURE.md` but must not duplicate its detailed content.
- `PLAN.yaml` **may reference** architectural decisions but must not become a technical constitution again.
- `PLAN.md` and `PLAN.dot` must not contain material that is not derivable or not consistent with the source of truth.

---

## 7. Distribution of responsibilities across files and directories

## 7.1 `AGENTS.md`
### Role
Operational contract and authority map.

### Must contain
- purpose;
- authority map;
- canonical source rule;
- workflow rules;
- escalation / stop conditions;
- taxonomy referenced or pointer to the shared file;
- general commit/checkpoint rules;
- where to read `ARCHITECTURE`, `PLAN`, `REPO_MAP`, optional ADRs.

### Must not contain
- all detailed technical architecture;
- the full active plan;
- extended historical rationale;
- long operational plan tables.

---

## 7.2 `ARCHITECTURE.md` / `docs/architecture/*`
### Role
Normative source of software constraints, boundaries, contracts, and invariants of the project.

### Must contain
- package/module boundaries;
- subsystem ownership;
- public contracts;
- semantic invariants;
- authorized modification limits;
- allowed or prohibited patterns;
- interfaces and boundary rules.

### Must not contain
- operational work tracker;
- commit checklists;
- item chronology.

---

## 7.3 `PLAN.yaml`
### Role
Local source of truth for work tracking and orchestration.

### Must contain
- active mission/milestone;
- active sprint;
- taxonomy used;
- item list;
- states;
- dependencies;
- roles/effort;
- commit groups;
- optional artifact/checks/notes.

### Must not contain
- long architectural texts;
- general agentic workflow;
- verbose non-operational rationale.

---

## 7.4 `PLAN.md`
### Role
Human-readable view.

### Must contain
- readable rendering of mission/sprint/items;
- optional tables or clear sections for states and dependencies;
- notes understandable by a human reviewer.

### Must not be hand-edited
It is a generated view.

---

## 7.5 `PLAN.dot` / `PLAN.svg`
### Role
Graph view.

### Must show
- nodes;
- dependencies;
- clusters (by sprint or by commit group);
- optional state and type as visual attributes.

### Must not be hand-edited
It is a generated view.

---

## 7.6 `REPO_MAP.md`
### Role
Practical codebase map.

### Must contain
- entry points;
- main modules;
- test map;
- hot paths;
- fragile areas.

### Must not become
- a second normative architecture document;
- a second `AGENTS.md`.

---

## 7.7 `docs/adr/*`
### Role
Rationale and irreversible or structural decisions.

### Should be introduced when
- the project becomes stable enough to require decision memory;
- the distinction between "current rule" and "why it was chosen" becomes useful.

---

## 7.8 `SKILLS/`
### Role
Reusable automation, specialized operational instructions, workflow packaging.

### Recommended position
- at level 0 in the control plane;
- optionally with local adapters or shims only where necessary.

### Must not become
- the normative source of the software architecture of a repo, unless explicitly declared.

---

## 8. Why `PLAN.yaml` as source of truth

## 8.1 Main motivation
The plan is not just text: it is structure.

You have already decided that the plan must be able to contain:
- item types;
- actions;
- states;
- dependencies;
- roles;
- effort;
- commit groups.

These concepts are more natural in a data format than in free prose.

## 8.2 Why not `PLAN.md` as source of truth
Markdown is excellent for:
- human reading;
- review;
- discussion.

It is less excellent for:
- strong validation;
- explicit dependencies;
- grouping and parallelism;
- deterministic multiple rendering;
- single-writer orchestration.

## 8.3 Why not `.dot` as source of truth
DOT is good for representing the graph.  
It is not good as the sole source of the domain, because your plan contains more than just the graph:
- execution metadata;
- item semantics;
- roles/effort;
- commit groups;
- operational rationale.

For this reason the correct choice is:

- `PLAN.yaml` = data model
- `PLAN.dot` = graph view

---

## 9. Why `PLAN.md` and `PLAN.dot` as generated views

## 9.1 `PLAN.md`
Serves for:
- reading the plan;
- human review;
- discussing state, dependencies, and blockers;
- having a text-oriented view.

## 9.2 `PLAN.dot`
Serves for:
- visualizing the DAG;
- understanding parallelism and bottlenecks;
- viewing clusters by sprint or commit group;
- generating SVG/PDF/PNG.

## 9.3 Determinism rule
The translation:
- `PLAN.yaml -> PLAN.md`
- `PLAN.yaml -> PLAN.dot`

must be **deterministic** and done by tools/scripts, not by an LLM in free-form mode.

---

## 10. Shared taxonomy: items, actions, states, roles, and effort

## 10.1 Item types

### `X`
Milestone container.  
Not executable by default.  
Used to contain a macro objective.

### `S`
Sprint container.  
Not executable by default.  
Used to group a tranche of human work.

### `Q`
Blocking question / decision gate.  
Executable item.  
Used to halt the flow and require an explicit decision.

### `D`
Documentation / planning / governance item.  
Executable item.  
Used to modify or produce documentation, plan, governance, operational rationale.

### `M`
Implementation / integration / refactor item.  
Executable item.  
Used to modify code or integration.

### `F`
Fix / hotfix item.  
Executable item.  
Used to correct a specific problem or bug.

### `T`
Test / validation item.  
Executable item.  
Used to write, update, or run tests/gates.

### `C`
Checkpoint / review / closure gate item.  
Executable item.  
Used to produce a controlled closure of a work tranche.

---

## 10.2 Action taxonomy

Actions are orthogonal to item type.

### `audit`
Read, map, understand, characterize.

### `plan`
Create or update the work structure.

### `design`
Define a local solution within already authorized architecture.

### `implement`
Write or modify code.

### `refactor`
Restructure while preserving external semantics.

### `test`
Add or update tests.

### `verify`
Run validations, gates, and check the outcome.

### `document`
Update documentation or rationale.

### `review`
Critically re-read and perform qualitative assessment.

### `checkpoint`
Produce an intermediate closure with evidence.

### `decide`
Formalize a human decision or the response to a `Q`.

### `migrate`
Move ownership/boundary/flow without changing expected outputs.

---

## 10.3 Type/action coherence rules

Recommended rules:

- `Q` must have at least `review` or `decide`
- `D` tends to have `plan`, `document`, `review`, `checkpoint`
- `M` tends to have `design`, `implement`, `refactor`, `migrate`, `verify`
- `F` tends to have `implement`, `test`, `verify`
- `T` tends to have `test`, `verify`
- `C` tends to have `review`, `checkpoint`, `verify`

These rules are not a rigid type-checking system, but they serve to avoid meaningless combinations.

---

## 10.4 Lifecycle states

Recommended states:

- `planned`
- `ready`
- `in_progress`
- `blocked`
- `review`
- `verified`
- `done`

Semantics:

- `planned`: exists but is not yet ready;
- `ready`: all minimum dependencies are satisfied;
- `in_progress`: under active execution;
- `blocked`: halted by an obstacle or missing decision;
- `review`: technically complete but under assessment;
- `verified`: has passed the required gates;
- `done`: closed logically and administratively.

---

## 10.5 Abstract roles

Recommended shared roles:

- `orchestrator`
- `implementer`
- `tester`
- `reviewer`
- `documenter`
- `researcher`

These are not yet specific subagents for a tool.  
They are abstract, portable semantics.

---

## 10.6 Effort

Recommended shared effort:

- `low`
- `medium`
- `high`

Used to:
- estimate the weight of an item;
- optionally choose different models/subagents;
- decide whether an item can be in a group or needs to be isolated.

---

## 10.7 Execution metadata

Recommended fields:

- `depends_on`
- `role`
- `effort`
- `commit_group`
- `scope`
- `artifacts_in`
- `artifacts_out`
- `checks`
- `triggers`
- `tools_profile`
- `notes`

---

## 11. DAG-ready execution model

## 11.1 Fundamental rule

The human plans in:
- milestones
- sprints
- items

The agent executes in:
- dependencies
- compatible groups
- optional controlled parallelism

Therefore:

$$item_i \text{ is executable} \iff deps(item_i)\subseteq done\_or\_verified$$

## 11.2 Parallelism rule
Parallelism is allowed only if:
- dependencies are satisfied;
- scopes are compatible;
- there is no evident collision on files or boundaries;
- the resulting block has verifiable closure.

## 11.3 Grouping rule
The agent may group compatible items into a common `commit_group` if:
- the group is semantically coherent;
- the required gates are compatible;
- the reviewer can evaluate the block without losing traceability.

## 11.4 Collision rule
If two items:
- touch the same sensitive scope,
- require different human decisions,
- or produce incompatible evidence,

then they must not be grouped automatically.

## 11.5 Human sequentiality, not runtime
Sequentiality remains in the way the human thinks, speaks, and orders the plan.
It is no longer an absolute law of execution.

---

## 12. Commit groups, development blocks, and closure

## 12.1 Why "one item = one commit" is no longer a universal law
That rule is disciplined but too rigid for:
- coherent development blocks;
- controlled parallelism;
- future multi-agent scenarios;
- reducing overhead.

## 12.2 New rule
The natural boundary becomes the **verified commit group**.

### Rule
A `commit_group` can be closed with a commit only if:
- all items in the group are at least `review` or `verified`;
- the required checks for the group are green;
- the group is semantically readable;
- item -> evidence -> commit traceability remains clear.

## 12.3 Commit groups as clusters
A `commit_group` can also be visualized as a cluster in the DAG.

---

## 13. Subagents and cross-tool portability

## 13.1 General rule
The shared model must remain **neutral**.

It must not be written using proprietary primitives from a single tool.

## 13.2 Conceptual mapping

### Codex / OpenAI
- hierarchical `AGENTS.md`;
- directory scope;
- parallel tasks and isolated environments;
- good integration with an orchestrator that uses `PLAN.yaml` as control plane.

### Claude Code
- hierarchical `CLAUDE.md`;
- `@import`;
- subagents in `.claude/agents/`;
- separate contexts;
- good fit for roles/effort.

### GitHub Copilot
- repository-wide / path-specific instructions;
- `AGENTS.md` supported;
- precedence of nearest files;
- good fit for the instruction layer and local constraints.

### Kilo and others
- custom modes and specialized configurations;
- possible mapping from neutral roles/effort/triggers.

## 13.3 Recommended shared fields
For portability, in the plan and shared model use:

- `role`
- `effort`
- `triggers`
- `tools_profile`

and then map downstream.

---

## 14. Git/GitHub automation in phases

## 14.1 General principle
Automating everything at once is a mistake.  
Irreversible or potentially costly actions must be introduced later.

## 14.2 Already fixed strategic constraints
- `develop` must never be removed;
- before the final PR, alignment with `develop` must be verified;
- preference for **merge** rather than **rebase**;
- separate branch history must be preserved;
- final merge is not to be automated at the start.

## 14.3 Phases

### Phase A — foundation
Automatic:
- branch naming;
- `PLAN.yaml` updates;
- `PLAN.md` / `PLAN.dot` rendering;
- local commits per commit group.

Not automatic:
- push;
- PR;
- merge.

### Phase B — collaboration
Automatic:
- push of the feature branch;
- opening a draft PR;
- verifying `develop` state;
- merging `develop` into the feature branch before final checks.

Still not automatic:
- final merge.

### Phase C — controlled merge
Automatic:
- auto-merge of the PR when all required checks are green and required reviews are satisfied.

### Phase D — hygiene
Optional:
- feature branch cleanup after merge;
- never for `develop`.

---

## 15. Concrete structure of the 3 levels

## 15.1 Level 0 — central repo

```text
agent-os/
├── workflow/
│   ├── shared-workflow.md
│   ├── item-taxonomy.md
│   ├── lifecycle.md
│   ├── git-automation-policy.md
│   └── portability-model.md
├── schemas/
│   ├── plan.schema.json
│   └── ...
├── templates/
│   ├── repo-AGENTS.md.template
│   ├── repo-ARCHITECTURE.md.template
│   ├── repo-REPO_MAP.md.template
│   └── PLAN.yaml.template
├── scripts/
│   ├── sync-workspace.sh
│   ├── render-plan.py
│   ├── validate-plan.py
│   └── bootstrap-repo.sh
├── prompts/
│   ├── orchestrator.md
│   ├── reviewer.md
│   └── ...
└── skills/
```

## 15.2 Level 1 — workspace runtime

```text
work/
├── AGENTS.md
├── CLAUDE.md
├── repo-a/
├── repo-b/
└── repo-c/
```

## 15.3 Level 2 — local repo

```text
repo/
├── AGENTS.md
├── ARCHITECTURE.md
├── REPO_MAP.md
├── PLAN.yaml
├── PLAN.md          # generated
├── PLAN.dot         # generated
├── docs/
│   └── adr/
└── ...
```

---

## 16. What goes in each level: files, authority, and non-goals

## 16.1 Level 0
### Goes here
- shared workflow;
- taxonomy;
- schema;
- scripts;
- templates;
- shared skills.

### Does not go here
- active plan of a specific repo;
- software constraints specific to a specific project.

## 16.2 Level 1
### Goes here
- shared runtime files that agents must read for scope.

### Does not go here
- source of truth manually modified;
- content that must diverge from machine to machine without control.

## 16.3 Level 2
### Goes here
- local `AGENTS.md`;
- `ARCHITECTURE.md`;
- `PLAN.yaml`;
- `REPO_MAP.md`;
- local ADRs.

### Does not go here
- manual duplication of the shared workflow;
- complete copy of the control plane.

---

## 17. First repo-agnostic MVP to set up

## 17.1 Purpose of the MVP
Have a solid, minimal, and scalable foundation for:
- shared workflow;
- thin local repos;
- machine-readable plan;
- generated views;
- no dangerous Git automation yet active.

## 17.2 Minimum files of the MVP

### Level 0
- `workflow/shared-workflow.md`
- `workflow/item-taxonomy.md`
- `workflow/lifecycle.md`
- `templates/repo-AGENTS.md.template`
- `templates/repo-ARCHITECTURE.md.template`
- `templates/repo-REPO_MAP.md.template`
- `templates/PLAN.yaml.template`
- `scripts/sync-workspace.sh`
- `scripts/render-plan.py`
- `scripts/validate-plan.py`

### Level 1
- `AGENTS.md`
- `CLAUDE.md` (if using Claude)

### Level 2
- `AGENTS.md`
- `ARCHITECTURE.md`
- `REPO_MAP.md`
- `PLAN.yaml`

## 17.3 What NOT to put in the MVP
- real per-tool subagents;
- auto-push;
- auto-merge;
- merge queue;
- complete multi-agent orchestration;
- mandatory `ADR` everywhere;
- custom skill generators.

---

## 18. Instructions to give the agent to implement the setup

This section is designed for your specific case: **an agent will create everything**.  
You will not write `.md` or `.yaml` files by hand.

## 18.1 High-level prompt/instructions to the agent

### Objective
"Create a portable and versioned central control plane, a workspace root with shared runtime files, and a minimal bootstrap of local repositories with `AGENTS.md`, `ARCHITECTURE.md`, `REPO_MAP.md`, and `PLAN.yaml`, following the structure and authorities formalized in this document."

### Constraints
- do not introduce superfluous files;
- do not introduce irreversible Git automations;
- do not duplicate concerns across multiple files;
- respect the 3-level model;
- use `PLAN.yaml` as the source of truth for the plan;
- generate `PLAN.md` and `PLAN.dot` from deterministic scripts;
- keep the system repo-agnostic;
- do not impose specific software constraints unless in the local repo;
- set up the model for dependency-driven execution, not global sequentiality.

## 18.2 Work sequence to have the agent follow

### Phase 1 — create the central repo
1. create the `agent-os/` structure;
2. create shared workflow, taxonomy, lifecycle;
3. create minimal templates;
4. create sync/render/validate scripts.

### Phase 2 — create the workspace root runtime
1. create `work/AGENTS.md` from the shared workflow;
2. create `work/CLAUDE.md` or equivalent if needed;
3. verify that the files are on the correct path for the target agents.

### Phase 3 — bootstrap the first repo
1. create thin local `repo/AGENTS.md`;
2. create minimal `repo/ARCHITECTURE.md`;
3. create `repo/REPO_MAP.md`;
4. create initial `repo/PLAN.yaml`;
5. generate `repo/PLAN.md` and `repo/PLAN.dot`;
6. validate plan consistency and rendering.

### Phase 4 — validation
1. verify that authorities are unambiguous;
2. verify that `PLAN.yaml` is the sole source of truth for the plan;
3. verify that there are no improper duplications;
4. test the bootstrap on at least one real repo.

## 18.3 Strong instruction to give the agent about the plan
"Do not manually write `PLAN.md` or `PLAN.dot`; write only `PLAN.yaml` and generate all views with the rendering scripts."

## 18.4 Strong instruction to give the agent about governance
"`AGENTS.md` governs the workflow and authorities; `ARCHITECTURE.md` governs software constraints; `PLAN.yaml` governs local execution tracking. Do not mix the three concerns."

---

## 19. Growth roadmap: what to do first and what to defer

## 19.1 Phase 1 — foundation
Implement:
- central control plane;
- taxonomy;
- lifecycle;
- `PLAN.yaml`;
- deterministic rendering;
- minimal local files.

## 19.2 Phase 2 — DAG readiness
Implement:
- `depends_on`;
- `commit_group`;
- `role`;
- `effort`;
- `PLAN.dot` visualization;
- basic grouping logic.

## 19.3 Phase 3 — subagent portability
Implement:
- neutral roles;
- mapping to Claude/Codex/Copilot;
- optional `tools_profile`;
- optional templates for subagents or custom modes.

## 19.4 Phase 4 — Git automation foundations
Implement:
- branch policy;
- branch naming;
- commit groups -> real commits;
- optional controlled push;
- optional draft PR.

## 19.5 Phase 5 — advanced automation
Defer until stable:
- auto-merge;
- automatic branch cleanup;
- complete multi-agent orchestration;
- external queue/scheduler;
- advanced custom skills.

---

## 20. Mapping the approach to the DUCT case and other existing repos

This section serves to preserve the connection with the real case from which the work originated, without making the document DUCT-specific.

### 20.1 DUCT case
In the current DUCT root:
- the local authorities are `AGENTS.md` and `PLAN.md`;
- the agent cannot push;
- there is no active milestone;
- `X5` is already closed.

Therefore applying the abstract model to the DUCT case implies:
- new milestone (`X9`) for governance re-foundation;
- split between `AGENTS.md`, `ARCHITECTURE.md`, and `PLAN.yaml`;
- shift from sequential execution constitution to dependency-driven execution;
- preservation of user decision supremacy;
- no runtime changes in the first governance milestone.

### 20.2 SignalProcessing
This is the best existing example of the canonical source rule principle:
- `AGENTS.md` for operational behavior;
- `docs/architecture/*` for technical architecture;
- `docs/adr/*` for rationale;
- `PLAN.md` for chronology/tracking.

This repo confirms that the concern split is not only sensible but already practiced successfully.

### 20.3 SmartBox
This is a strong example of:
- planning-before-execution;
- atomicity;
- dual tracking;
- PASS/NON-PASS discipline.

From there it is worth preserving:
- the tracking discipline;
- the seriousness of checkpoints;
- the clear distinction between closure and simple work progress.

### 20.4 9_DNAIS
The 9_DNAIS case showed an anti-pattern to avoid: a non-authoritative root that references absolute local paths that are not portable.  
The 3-level model proposed here solves exactly that problem:
- portable source of truth;
- correct runtime materialization;
- clear local repos.

---

## 21. Final summary

### 21.1 Main thesis
The best solution today for a portable and scalable setup for coding agents is neither:
- "everything in every repo",
- nor "a single global file for everything".

It is:

$$\text{central control plane} + \text{workspace runtime layer} + \text{repo-local thin layer}$$

### 21.2 Main corollaries
- workflow is shared, plan is not;
- taxonomy is shared, software constraints are not;
- the plan is structured, then rendered in text and graph;
- the human decides, the orchestrator translates into the plan;
- workers execute, but are not owners of the plan;
- sequentiality remains human semantics, not an absolute runtime constraint;
- Git automation is introduced in layers, not all at once.

### 21.3 Final model formula
$$\text{human planning} = \text{milestone/sprint/item}$$

$$\text{machine execution} = \text{deps + roles + effort + commit groups}$$

$$\text{control plane} = \text{shared workflow + taxonomy + templates + tooling}$$

$$\text{repo governance} = \text{workflow authority + software constraints + local plan}$$

---

## 22. Handoff package to continue the conversation elsewhere

This section is designed specifically to allow resuming work in another chat, with another agent, or in another tool.

### 22.1 Current design state
- a 3-level architectural model has been defined;
- it has been decided that the shared workflow lives in the central control plane;
- it has been decided that the plan is local to the repo;
- it has been decided that the plan is machine-readable (`PLAN.yaml`);
- it has been decided that `PLAN.md` and `PLAN.dot` are generated views;
- a shared taxonomy of items and actions has been decided;
- it has been decided to let global runtime sequentiality decay in favor of explicit dependencies;
- it has been decided to use neutral roles/effort for cross-tool portability;
- it has been decided to introduce Git/GitHub automation in phases.

### 22.2 Recommended handoff prompt
You can paste something like this into another conversation:

> I am designing a portable setup for coding agents based on 3 levels:
> 1) versioned central control plane,  
> 2) shared workspace root runtime,  
> 3) local layer per repo.  
>  
> Decisions already made:
> - no shared global `PLAN`;
> - yes to shared taxonomy of items/actions/states/roles/effort;
> - `PLAN.yaml` as local source of truth;
> - `PLAN.md` and `PLAN.dot` as generated views;
> - a single orchestrator/planner agent owns the plan;
> - items are written in human sequence but executed dependency-driven;
> - commits on verified commit groups;
> - Git/GitHub automation introduced in phases, not all at once.  
>  
> I want to continue from here and transform the design into:
> - initial `PLAN.yaml` schema;
> - initial `AGENTS.md`, `ARCHITECTURE.md`, `REPO_MAP.md` templates;
> - `render-plan` and `validate-plan` scripts;
> - MVP operational plan.

### 22.3 Minimum context that must always be remembered
- one concern must have a single canonical authority;
- `AGENTS.md` must not become a monster that also contains all the architecture;
- `ARCHITECTURE.md` must not become a plan;
- `PLAN.yaml` must not become a second repo constitution;
- `PLAN.md` and `PLAN.dot` are not hand-edited;
- the human does not edit the source of truth for the plan: the orchestrator updates it from prompts/decisions.

---

## 23. References

### OpenAI / Codex
- Introducing Codex — OpenAI  
  https://openai.com/index/introducing-codex/
- Structured Outputs — OpenAI Platform  
  https://platform.openai.com/docs/guides/structured-outputs
- Prompt Caching — OpenAI Platform  
  https://platform.openai.com/docs/guides/prompt-caching
- Prompting / prompt objects / versioning — OpenAI Platform  
  https://platform.openai.com/docs/guides/prompting

### Anthropic / Claude Code
- Claude Code Memory  
  https://docs.anthropic.com/en/docs/claude-code/memory
- Claude Code Subagents  
  https://docs.anthropic.com/en/docs/claude-code/sub-agents

### GitHub Copilot / GitHub
- About customizing GitHub Copilot responses  
  https://docs.github.com/en/copilot/concepts/prompting/response-customization
- Adding repository custom instructions for GitHub Copilot  
  https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot
- About protected branches  
  https://docs.github.com/github/administering-a-repository/about-protected-branches
- Automatically merging a pull request  
  https://docs.github.com/github/collaborating-with-issues-and-pull-requests/automatically-merging-a-pull-request
- About pull request merges  
  https://docs.github.com/github/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges
- Merging a pull request with a merge queue  
  https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request-with-a-merge-queue

### Graphviz
- DOT language  
  https://graphviz.org/doc/info/lang.html
- Graphviz outputs  
  https://graphviz.org/docs/outputs/

### Kilo
- Custom Modes  
  https://kilo.ai/docs/features/custom-modes

### Repositories analyzed as internal precedents
- `NickF93/MH-PatchCore-Private`
- `nAIs-BO/SignalProcessing`
- `nAIs-BO/SmartBox`
- `nAIs-BO/9_DNAIS`
- `matt-k-wong/mkw-DAG-architect`

---

## Closing

This document formalizes the consolidated architectural model that has emerged so far.  
The next natural step is not to continue discussing at an abstract level, but to move to a concrete technical deliverable:

1. `PLAN.yaml` schema;  
2. `AGENTS.md` template;  
3. `ARCHITECTURE.md` template;  
4. `REPO_MAP.md` template;  
5. `render-plan` and `validate-plan` scripts;  
6. MVP bootstrap in the central control plane and in the workspace root.
