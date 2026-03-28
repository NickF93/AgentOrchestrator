# PLAN.md

AUTO-GENERATED from PLAN.yaml. Do not edit manually.

- Repository: AgentOrchestrator
- Owner: NickF93
- Version: 0.1
- Last updated: 2026-03-28

## Mission

Build the minimal viable Level-0 central control plane (agent-os/) inside this repository. Level-0 provides: shared workflow documentation, plan schema, templates for repo-local files, and render/validate scripts. This repository IS the control-plane OS (Level-0). Level-1 (workspace runtime) and Level-2 (repo-local bootstrap) come after.

## Milestones

| ID | Type | Title | Status |
|---|---|---|---|
| X1 | X | Level-0 MVP — Control Plane Foundation | done |
| X2 | X | Layer-0 Governance Hardening | done |
| X3 | X | Control-Plane Hardening | done |

## Sprints

| ID | Parent | Type | Title | Status |
|---|---|---|---|---|
| S1.1 | X1 | S | Sprint 1 — Decisions, scaffold, schema, workflow docs, templates, scripts | done |
| S2.1 | X2 | S | Sprint 1 — Propagate missing architectural rules to governance files | done |
| S3.1 | X3 | S | Sprint 1 — Source-of-truth integrity and schema hardening | done |
| S3.2 | X3 | S | Sprint 2 — Validation tooling hardening | done |
| S3.3 | X3 | S | Sprint 3 — Rendering, bootstrap, and workspace improvements | done |
| S3.4 | X3 | S | Sprint 4 — Documentation, operational guardrails, and closure | done |

## Items

| ID | Parent | Type | Status | Role | Effort | Commit Group | Depends On |
|---|---|---|---|---|---|---|---|
| C1.1.1 | S1.1 | C | done | reviewer | low | cg5 | T1.1.1, T1.1.2, T1.1.3 |
| C2.1.1 | S2.1 | C | done | reviewer | low | cg8 | D2.1.4, D2.1.5, D2.1.6, D2.1.7, D2.1.8 |
| C3.2.5 | S3.2 | C | done | reviewer | low | cg10 | T3.2.4 |
| C3.4.6 | S3.4 | C | done | reviewer | low | cg12 | T3.3.6, T3.4.5 |
| D1.1.1 | S1.1 | D | done | orchestrator | low | cg0 |  |
| D1.1.2 | S1.1 | D | done | orchestrator | low | cg1 |  |
| D1.1.3 | S1.1 | D | done | orchestrator | low | cg6 |  |
| D1.1.4 | S1.1 | D | done | orchestrator | low | cg6 |  |
| D2.1.1 | S2.1 | D | done | orchestrator | medium | cg7 |  |
| D2.1.2 | S2.1 | D | done | orchestrator | medium | cg7 |  |
| D2.1.3 | S2.1 | D | done | orchestrator | low | cg7 |  |
| D2.1.4 | S2.1 | D | done | orchestrator | medium | cg8 |  |
| D2.1.5 | S2.1 | D | done | orchestrator | medium | cg8 |  |
| D2.1.6 | S2.1 | D | done | orchestrator | low | cg8 |  |
| D2.1.7 | S2.1 | D | done | orchestrator | medium | cg8 |  |
| D2.1.8 | S2.1 | D | done | orchestrator | high | cg8 |  |
| D3.1.3 | S3.1 | D | done | documenter | low | cg9 | M3.1.2 |
| D3.4.1 | S3.4 | D | done | documenter | medium | cg12 |  |
| D3.4.2 | S3.4 | D | done | orchestrator | medium | cg12 | C3.2.5 |
| D3.4.3 | S3.4 | D | done | orchestrator | low | cg12 |  |
| F3.1.1 | S3.1 | F | done | implementer | low | cg9 |  |
| M1.1.1 | S1.1 | M | done | implementer | medium | cg3 | Q1.1.1, Q1.1.2, Q1.1.3 |
| M1.1.2 | S1.1 | M | done | implementer | medium | cg3 | Q1.1.1, Q1.1.4 |
| M1.1.3 | S1.1 | M | done | implementer | medium | cg3 | Q1.1.2, M1.1.1 |
| M1.1.4 | S1.1 | M | done | implementer | high | cg4 | M1.1.2, Q1.1.5 |
| M1.1.5 | S1.1 | M | done | implementer | medium | cg4 | M1.1.3, Q1.1.3 |
| M1.1.6 | S1.1 | M | done | implementer | medium | cg3 | Q1.1.1, Q1.1.2, Q1.1.3 |
| M3.1.2 | S3.1 | M | done | implementer | medium | cg9 | F3.1.1 |
| M3.2.1 | S3.2 | M | done | implementer | high | cg10 | T3.1.4 |
| M3.2.2 | S3.2 | M | done | implementer | medium | cg10 | T3.1.4 |
| M3.2.3 | S3.2 | M | done | implementer | medium | cg10 | T3.1.4 |
| M3.3.1 | S3.3 | M | done | implementer | medium | cg11 | T3.1.4 |
| M3.3.2 | S3.3 | M | done | implementer | medium | cg11 | T3.1.4 |
| M3.3.3 | S3.3 | M | done | implementer | medium | cg11 | T3.1.4, M3.3.4 |
| M3.3.4 | S3.3 | M | done | implementer | low | cg11 |  |
| M3.3.5 | S3.3 | M | done | implementer | medium | cg11 | T3.1.4 |
| M3.4.4 | S3.4 | M | done | implementer | medium | cg12 | D3.4.2, C3.2.5 |
| Q1.1.1 | S1.1 | Q | done | orchestrator | low | cg2 | D1.1.2 |
| Q1.1.2 | S1.1 | Q | done | orchestrator | low | cg2 | D1.1.2 |
| Q1.1.3 | S1.1 | Q | done | orchestrator | low | cg2 | D1.1.2 |
| Q1.1.4 | S1.1 | Q | done | orchestrator | low | cg2 | D1.1.2 |
| Q1.1.5 | S1.1 | Q | done | orchestrator | low | cg2 | D1.1.2 |
| T1.1.1 | S1.1 | T | done | tester | low | cg5 | M1.1.2, M1.1.4 |
| T1.1.2 | S1.1 | T | done | tester | low | cg5 | M1.1.5 |
| T1.1.3 | S1.1 | T | done | tester | low | cg5 | M1.1.4 |
| T3.1.4 | S3.1 | T | done | tester | low | cg9 | M3.1.2, F3.1.1 |
| T3.2.4 | S3.2 | T | done | tester | low | cg10 | M3.2.1, M3.2.2, M3.2.3 |
| T3.3.6 | S3.3 | T | done | tester | low | cg11 | M3.3.1, M3.3.2, M3.3.3, M3.3.4, M3.3.5 |
| T3.4.5 | S3.4 | T | done | tester | low | cg12 | D3.4.1, D3.4.2, D3.4.3, M3.4.4 |

## Commit Groups

| ID | Title | Items |
|---|---|---|
| cg0 | Repository bootstrap hygiene | D1.1.1 |
| cg1 | Review and planning artifacts | D1.1.2 |
| cg10 | Validation tooling hardening — cycle detection, commit group coherence, type/action warnings | M3.2.1, M3.2.2, M3.2.3, T3.2.4, C3.2.5 |
| cg11 | Rendering, bootstrap, and workspace template improvements | M3.3.1, M3.3.2, M3.3.3, M3.3.4, M3.3.5, T3.3.6 |
| cg12 | Documentation, operational guardrails, and milestone closure | D3.4.1, D3.4.2, D3.4.3, M3.4.4, T3.4.5, C3.4.6 |
| cg2 | Decision gates — Q1.1.1 through Q1.1.5 answers recorded | Q1.1.1, Q1.1.2, Q1.1.3, Q1.1.4, Q1.1.5 |
| cg3 | Scaffold — workflow docs, schema, templates | M1.1.1, M1.1.2, M1.1.3, M1.1.6 |
| cg4 | Scripts — render, validate, bootstrap, sync | M1.1.4, M1.1.5 |
| cg5 | Sprint 1 closure — tests and checkpoint | T1.1.1, T1.1.2, T1.1.3, C1.1.1 |
| cg6 | Governance hardening updates | D1.1.3, D1.1.4 |
| cg7 | Governance compliance — propagate architectural rules to workflow docs | D2.1.1, D2.1.2, D2.1.3 |
| cg8 | Architecture finalization — close specification gaps G1-G5 | D2.1.4, D2.1.5, D2.1.6, D2.1.7, D2.1.8, C2.1.1 |
| cg9 | Source-of-truth integrity and schema hardening | F3.1.1, M3.1.2, D3.1.3, T3.1.4 |

## Item Details

### C1.1.1: Sprint 1 checkpoint — Level-0 scaffold complete and self-validating

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Actions**: review, checkpoint, verify
- **Depends on**: T1.1.1, T1.1.2, T1.1.3
- **Checks**:
  - All S1.1 items are status: verified or done
  - PLAN.md and PLAN.dot are committed and match PLAN.yaml
  - No concern duplication detected (AGENTS vs ARCHITECTURE vs PLAN)
  - agent-os/ directory structure matches §15.1 of architecture doc
  - Each template file includes canonical source rule header
  - Commit messages follow: <type>(<scope>): <description>
  - validate-plan.py passes on this PLAN.yaml
- **Notes**: After this checkpoint, the control plane is operational and able to bootstrap its first real target repo (Level-2) as Sprint 2 work.

### C2.1.1: Architecture finalization checkpoint — close review gaps G1-G5

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Actions**: review, checkpoint, verify
- **Depends on**: D2.1.4, D2.1.5, D2.1.6, D2.1.7, D2.1.8
- **Checks**:
  - Open gaps G1-G5 are resolved or explicitly governed with final policy
  - REVIEW-AND-OPEN-QUESTIONS.md is updated from working status to closure status
  - Prompt, skill, ADR, and REPO_MAP policies are defined in canonical authorities
  - Phase B automation includes explicit safety gate for authority-conflict recovery
  - validate-plan.py passes on this PLAN.yaml
  - render-plan.py regenerates PLAN.md and PLAN.dot deterministically
- **Notes**: Marks architecture baseline as finalized for Level-0 governance, with unresolved work shifted from open questions into explicit governed policy.

### C3.2.5: Sprint S3.2 checkpoint — validation hardening complete

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Actions**: review, checkpoint, verify
- **Depends on**: T3.2.4
- **Checks**:
  - All S3.2 items are verified or done
  - Cycle detection produces hard-fail on circular depends_on
  - Commit group coherence produces hard-fail on mismatches
  - Type/action coherence produces warnings on non-recommended combinations
  - validate-plan.py passes on current PLAN.yaml
  - render-plan.py regenerates PLAN.md and PLAN.dot deterministically
- **Notes**: Marks validation tooling as hardened for control-plane-grade enforcement.

### C3.4.6: Milestone X3 closure checkpoint — control-plane hardening complete

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Actions**: review, checkpoint, verify
- **Depends on**: T3.3.6, T3.4.5
- **Checks**:
  - All S3.1, S3.2, S3.3, S3.4 items are verified or done
  - PLAN.yaml has no duplicate keys
  - Schema requires actions/parent/commit_group
  - validate-plan.py has cycle detection, commit group coherence, type/action warnings
  - DOT rendering uses visual differentiation
  - Markdown rendering has per-item detail sections
  - bootstrap-repo.sh accepts --owner/--ref, runs post-validation, creates ADR/README
  - Workspace templates contain operational content
  - README.md exists at repo root
  - REPO_MAP freshness mechanism is specified and partially implemented
  - Design-doc discipline guardrail is documented
  - PLAN.md and PLAN.dot are regenerated and committed
- **Notes**: Marks the control plane as hardened per the 149-point review findings.

### D1.1.1: Create non-authoritative docs directory and initialize .gitignore

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Actions**: document
- **Artifacts**: .gitignore, docs/design/documento-architetturale-control-plane-coding-agents.md, docs/design/gitflow_pr_only_terminal_workflow.md, docs/design/REVIEW-AND-OPEN-QUESTIONS.md
- **Notes**: Moved startup documentation to docs/design/ as non-authoritative reference material and added baseline ignore rules for local/editor/runtime artifacts.

### D1.1.2: Create architecture review and open-questions document

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Actions**: document
- **Artifacts**: docs/design/REVIEW-AND-OPEN-QUESTIONS.md
- **Notes**: Captures what is confirmed, what is ambiguous, and five open questions (Q1.1.1–Q1.1.5) that must be decided before schema and scripts can be written.

### D1.1.3: Enforce commit message contract in Layer-0 governance

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Actions**: document, checkpoint
- **Artifacts**: AGENTS.md, agent-os/workflow/shared-workflow.md, agent-os/workflow/git-automation-policy.md, agent-os/templates/repo-AGENTS.md.template
- **Notes**: Added mandatory commit title contract: <type>(<scope>): <description> with optional body/footer sections. This is a Layer-0 global rule.

### D1.1.4: Strengthen and align commit body/footer recommendation wording

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Actions**: document
- **Artifacts**: AGENTS.md, agent-os/workflow/shared-workflow.md, agent-os/workflow/git-automation-policy.md, agent-os/templates/repo-AGENTS.md.template
- **Notes**: Standardized wording to: "Optional body and footer sections are strongly suggested, especially for medium or large commits." across all authoritative governance surfaces.

### D2.1.1: Enforce missing architectural doc rules in workflow governance files

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: medium
- **Actions**: document, review
- **Artifacts**: agent-os/workflow/shared-workflow.md, agent-os/workflow/git-automation-policy.md, agent-os/workflow/portability-model.md
- **Notes**: Close compliance gaps between the architecture doc (§6.2–6.4, §11.3–11.4, §4.2, §13.2) and the authoritative workflow files. Adds: full authority concern table, precedence rule, non-duplication rule, single-writer rule detail, grouping and collision rules, deferred automation list, and Kilo portability mapping example.

### D2.1.2: Create English translation of the Italian architectural document

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: medium
- **Actions**: document
- **Artifacts**: docs/design/architectural-document-control-plane-coding-agents.md
- **Notes**: 1:1 English translation of docs/design/documento-architetturale-control-plane-coding-agents.md, placed in the same directory. Structural fidelity to the original is required: all sections, tables, code blocks, and math equations must be preserved verbatim in structure.

### D2.1.3: Simplify commit title contract by removing item ID from header

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Actions**: document
- **Artifacts**: AGENTS.md, agent-os/workflow/shared-workflow.md, agent-os/workflow/git-automation-policy.md, agent-os/templates/repo-AGENTS.md.template, PLAN.yaml
- **Notes**: Updated commit title contract everywhere from the item-ID-inclusive format to <type>(<scope>): <description> while keeping body/footer recommendation unchanged.

### D2.1.4: Define prompts directory contract and lifecycle

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: medium
- **Actions**: design, document
- **Artifacts**: agent-os/prompts/README.md, agent-os/workflow/shared-workflow.md
- **Notes**: Closes G1 by specifying prompt file format, required metadata, versioning, and lifecycle triggers in authoritative workflow guidance.

### D2.1.5: Define skills packaging contract and compatibility mapping

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: medium
- **Actions**: design, document
- **Artifacts**: agent-os/skills/README.md, agent-os/workflow/portability-model.md, agent-os/workflow/shared-workflow.md
- **Notes**: Closes G2 by defining a neutral skill package format and adapter mapping expectations across agent runtimes.

### D2.1.6: Define REPO_MAP freshness policy and update triggers

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Actions**: design, document
- **Artifacts**: agent-os/templates/repo-REPO_MAP.md.template, agent-os/workflow/shared-workflow.md, agent-os/workflow/lifecycle.md
- **Notes**: Closes G3 by defining ownership, refresh triggers, and freshness metadata for REPO_MAP.md so map staleness is detectable and reviewable.

### D2.1.7: Define ADR template, numbering, and lifecycle states

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: medium
- **Actions**: design, document
- **Artifacts**: agent-os/templates/repo-ADR.md.template, agent-os/workflow/shared-workflow.md, agent-os/templates/repo-ARCHITECTURE.md.template
- **Notes**: Closes G4 by introducing a canonical ADR template with lifecycle states and linkage guidance to PLAN decision items.

### D2.1.8: Define canonical-authority conflict detection and recovery procedure

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: high
- **Actions**: design, document, review
- **Artifacts**: agent-os/workflow/shared-workflow.md, ARCHITECTURE.md, AGENTS.md
- **Notes**: Closes G5 by defining conflict detection, recovery actions, escalation, and a safety gate before Phase B automation.

### D3.1.3: Document new required fields in item-taxonomy.md

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: low
- **Actions**: document
- **Depends on**: M3.1.2
- **Artifacts**: agent-os/workflow/item-taxonomy.md
- **Notes**: Split Metadata Fields section into Required Item Fields and Optional Metadata Fields. Documents that actions, parent, and commit_group are now mandatory for all executable items.

### D3.4.1: Create root README.md for this repository

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: medium
- **Actions**: document
- **Artifacts**: README.md
- **Notes**: Hand-maintained README (not template-generated) for the AgentOrchestrator repo itself. Contains: purpose, directory structure, quickstart, governance file links, license reference.

### D3.4.2: Define REPO_MAP freshness operational mechanism

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: medium
- **Actions**: design, document
- **Depends on**: C3.2.5
- **Artifacts**: agent-os/workflow/lifecycle.md, agent-os/templates/repo-REPO_MAP.md.template
- **Notes**: Define freshness computation (today - last_validated_on > freshness_window_days), update triggers, and checkpoint consumption rules. Close the gap between concept and operational mechanism.

### D3.4.3: Add design-doc discipline guardrail

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Actions**: design, document, review
- **Artifacts**: agent-os/workflow/shared-workflow.md, ARCHITECTURE.md
- **Notes**: Add Design Document Governance section to shared-workflow.md: docs/design is non-authoritative, normative rules must migrate to canonical authority. Reinforce in ARCHITECTURE.md invariants.

### F3.1.1: Fix duplicate note key in PLAN.yaml X2 milestone

- **Type**: F | **Status**: done | **Role**: implementer | **Effort**: low
- **Actions**: implement, verify
- **Artifacts**: PLAN.yaml
- **Notes**: PLAN.yaml had two note: keys on milestone X2 (lines 35-41). YAML parsers silently override earlier values; PyYAML keeps the last. Merged both notes into a single field to preserve all content.

### M1.1.1: Create agent-os/workflow/ documentation files

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Actions**: implement, document
- **Depends on**: Q1.1.1, Q1.1.2, Q1.1.3
- **Artifacts**: agent-os/workflow/shared-workflow.md, agent-os/workflow/item-taxonomy.md, agent-os/workflow/lifecycle.md, agent-os/workflow/git-automation-policy.md, agent-os/workflow/portability-model.md
- **Notes**: Content sourced from docs/design/documento-architetturale-control-plane-coding-agents.md and docs/design/gitflow_pr_only_terminal_workflow.md. Do NOT duplicate content; these files are the canonical split of the monolithic architecture doc.

### M1.1.2: Create agent-os/schemas/plan.schema.json

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Actions**: design, implement
- **Depends on**: Q1.1.1, Q1.1.4
- **Artifacts**: agent-os/schemas/plan.schema.json
- **Notes**: JSON Schema (draft-2020-12) for PLAN.yaml. Must encode required fields, enum values for type/status/role/effort/actions, and scope field format as decided in Q1.1.1 and Q1.1.4. Must be self-consistent so that this PLAN.yaml passes validation once M1.1.4 is done.

### M1.1.3: Create agent-os/templates/ (AGENTS, ARCHITECTURE, REPO_MAP, PLAN)

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Actions**: design, implement
- **Depends on**: Q1.1.2, M1.1.1
- **Artifacts**: agent-os/templates/repo-AGENTS.md.template, agent-os/templates/repo-ARCHITECTURE.md.template, agent-os/templates/repo-REPO_MAP.md.template, agent-os/templates/PLAN.yaml.template
- **Notes**: Templates use {{REPO_NAME}}, {{DATE}}, {{OWNER}} placeholders. Level-1 files are generated from these templates by sync-workspace.sh (per Q1.1.2 decision). Each template must include the canonical source rule and authority map header so generated files self-document their origin.

### M1.1.4: Create agent-os/scripts/render-plan.py and validate-plan.py

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: high
- **Actions**: implement
- **Depends on**: M1.1.2, Q1.1.5
- **Artifacts**: agent-os/scripts/render-plan.py, agent-os/scripts/validate-plan.py
- **Notes**: validate-plan.py: validates PLAN.yaml against plan.schema.json; checks state transition legality, dangling depends_on, container items in depends_on, required fields. Exits non-zero on any hard-fail. render-plan.py: deterministic PLAN.yaml → PLAN.md + PLAN.yaml → PLAN.dot. Both scripts must be idempotent and callable standalone.

### M1.1.5: Create agent-os/scripts/bootstrap-repo.sh and sync-workspace.sh

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Actions**: implement
- **Depends on**: M1.1.3, Q1.1.3
- **Artifacts**: agent-os/scripts/bootstrap-repo.sh, agent-os/scripts/sync-workspace.sh
- **Notes**: bootstrap-repo.sh: instantiates a new repo-local layer (Level-2) from templates. Supports --dry-run. Emits a PLAN.yaml seed from the template. sync-workspace.sh: pulls latest from control plane (per Q1.1.3 decision) and regenerates Level-1 runtime files from Level-0 templates (per Q1.1.2 decision).

### M1.1.6: Create root governance files for this Level-0 repository

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Actions**: design, implement, document
- **Depends on**: Q1.1.1, Q1.1.2, Q1.1.3
- **Artifacts**: AGENTS.md, ARCHITECTURE.md
- **Notes**: This repository is itself the Level-0 control-plane OS. Root AGENTS.md and ARCHITECTURE.md define local authority mapping and structural constraints for building and evolving agent-os/.

### M3.1.2: Add actions, parent, commit_group to schema required fields for items

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Actions**: design, implement
- **Depends on**: F3.1.1
- **Artifacts**: agent-os/schemas/plan.schema.json
- **Notes**: Changed item required from [id, type, title, status, role, effort] to [id, type, title, status, role, effort, actions, parent, commit_group]. Safe: all 28 existing items already have these fields.

### M3.2.1: Implement DAG cycle detection in validate-plan.py

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: high
- **Actions**: design, implement
- **Depends on**: T3.1.4
- **Artifacts**: agent-os/scripts/validate-plan.py
- **Notes**: Add detect_cycles() using Kahn's algorithm (topological sort). If remaining nodes after BFS, report cycle. Hard-fail on any cycle in depends_on relationships.

### M3.2.2: Implement bidirectional commit_group/item consistency check

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Actions**: design, implement
- **Depends on**: T3.1.4
- **Artifacts**: agent-os/scripts/validate-plan.py
- **Notes**: Three checks: (1) every commit_group.items[] resolves to existing item, (2) every item.commit_group references existing commit_group, (3) bidirectional membership is coherent. All hard-fail.

### M3.2.3: Implement type/action coherence warnings

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Actions**: design, implement
- **Depends on**: T3.1.4
- **Artifacts**: agent-os/scripts/validate-plan.py
- **Notes**: Encode recommended type/action coherence table from item-taxonomy.md. Warning-only, not hard-fail, since taxonomy says "recommended" not "mandatory".

### M3.3.1: Add status/type visual styling to DOT rendering

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Actions**: design, implement
- **Depends on**: T3.1.4
- **Artifacts**: agent-os/scripts/render-plan.py
- **Notes**: Color nodes by status (done=green, blocked=red, in_progress=blue, etc.) and shape by type (Q=diamond, C=doubleoctagon, T=ellipse, etc.).

### M3.3.2: Add per-item detail sections to markdown rendering

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Actions**: design, implement
- **Depends on**: T3.1.4
- **Artifacts**: agent-os/scripts/render-plan.py
- **Notes**: After items table, add Item Details section with per-item subsections showing notes, checks, decision, artifacts_out, and depends_on.

### M3.3.3: Harden bootstrap-repo.sh with --owner, --ref, post-validation, ADR/README scaffolds

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Actions**: design, implement
- **Depends on**: T3.1.4, M3.3.4
- **Artifacts**: agent-os/scripts/bootstrap-repo.sh
- **Notes**: Add --owner/--ref flags, run validate-plan.py post-bootstrap, create docs/adr/ADR-0001.md and README.md scaffolds from templates.

### M3.3.4: Create repo-README.md.template

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: low
- **Actions**: design, implement
- **Artifacts**: agent-os/templates/repo-README.md.template
- **Notes**: New template for bootstrap-generated README.md in target repos. Uses existing {{REPO_NAME}}, {{OWNER}}, {{DATE}}, {{CONTROL_PLANE_REF}} placeholders.

### M3.3.5: Enrich workspace templates with operational content

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Actions**: design, implement, document
- **Depends on**: T3.1.4
- **Artifacts**: agent-os/templates/workspace-AGENTS.md.template, agent-os/templates/workspace-CLAUDE.md.template
- **Notes**: Add precedence rules, workflow summary, authority split reminder, commit contract, and links to runtime-relevant files. Workspace templates must be useful runtime references, not just stubs.

### M3.4.4: Add REPO_MAP staleness warning to validate-plan.py

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Actions**: implement
- **Depends on**: D3.4.2, C3.2.5
- **Artifacts**: agent-os/scripts/validate-plan.py
- **Notes**: Add --check-freshness flag. Parse REPO_MAP.md metadata, warn if stale when checkpoint items exist in review/verified state. Warning-only.

### Q1.1.1: Decide: PLAN.yaml required fields and state transition rules

- **Type**: Q | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Actions**: decide
- **Depends on**: D1.1.2
- **Decision**: Required executable fields are id, type, title, status, role, effort. State machine is planned -> ready -> in_progress -> review -> verified -> done, with blocked as a side-state reachable from active states. Container items (X, S) must not appear in depends_on. verified means all required checks pass; done means verified plus repository bookkeeping closure (committed, optionally pushed).
- **Notes**: Decision recorded from interactive governance alignment.

### Q1.1.2: Decide: Level-1 runtime materialization strategy

- **Type**: Q | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Actions**: decide
- **Depends on**: D1.1.2
- **Decision**: Level-1 runtime files are fully generated by sync-workspace.sh from Level-0 templates. Generated files are read-only outputs and must include an AUTO-GENERATED header.
- **Notes**: Decision recorded from interactive governance alignment.

### Q1.1.3: Decide: control-plane release and consumption model

- **Type**: Q | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Actions**: decide
- **Depends on**: D1.1.2
- **Decision**: MVP consumption tracks the control-plane main branch. Tag-based pinning will be introduced when a second external consumer is onboarded.
- **Notes**: Decision recorded from interactive governance alignment.

### Q1.1.4: Decide: scope field format and collision-detection semantics

- **Type**: Q | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Actions**: decide
- **Depends on**: D1.1.2
- **Decision**: scope is a repository-relative path prefix. validate-plan.py emits a warning (not hard-fail) when two in_progress items share a scope prefix.
- **Notes**: Decision recorded from interactive governance alignment.

### Q1.1.5: Decide: tooling failure semantics and commit hygiene rules

- **Type**: Q | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Actions**: decide
- **Depends on**: D1.1.2
- **Decision**: validate-plan.py hard-fails on missing required fields, unknown enum values, dangling depends_on references, and container types (X, S) in depends_on. Other policy checks can be warnings.
- **Notes**: Decision recorded from interactive governance alignment.

### T1.1.1: Validate this PLAN.yaml against plan.schema.json

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Actions**: test, verify
- **Depends on**: M1.1.2, M1.1.4
- **Checks**:
  - python agent-os/scripts/validate-plan.py PLAN.yaml exits 0
  - no required fields missing
  - no dangling depends_on references
- **Notes**: This is the self-validation gate: the control plane must validate its own plan before it can claim to be a working control plane.

### T1.1.2: Dry-run bootstrap-repo.sh on a temp path

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Actions**: test, verify
- **Depends on**: M1.1.5
- **Checks**:
  - bash agent-os/scripts/bootstrap-repo.sh --dry-run /tmp/test-repo exits 0
  - expected output files listed without being created
- **Notes**: Must confirm bootstrap is idempotent and does not write to disk in dry-run mode. A second run on the same target must produce identical output.

### T1.1.3: Generate PLAN.md and PLAN.dot from this PLAN.yaml

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Actions**: test, verify
- **Depends on**: M1.1.4
- **Checks**:
  - python agent-os/scripts/render-plan.py PLAN.yaml produces PLAN.md
  - python agent-os/scripts/render-plan.py PLAN.yaml produces PLAN.dot
  - running render a second time produces identical output (idempotency)
- **Notes**: PLAN.md and PLAN.dot are committed in the same commit as this PLAN.yaml update, not as separate commits (per Q1.1.5 decision).

### T3.1.4: Validate PLAN.yaml against hardened schema

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Actions**: test, verify
- **Depends on**: M3.1.2, F3.1.1
- **Checks**:
  - python agent-os/scripts/validate-plan.py PLAN.yaml exits 0
  - No schema validation errors for any existing item
  - Duplicate note key is resolved
- **Notes**: Gate for Sprint S3.1: the hardened schema must validate the current PLAN.yaml without errors.

### T3.2.4: Validate all new validation checks against current PLAN.yaml

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Actions**: test, verify
- **Depends on**: M3.2.1, M3.2.2, M3.2.3
- **Checks**:
  - python agent-os/scripts/validate-plan.py PLAN.yaml exits 0
  - No false-positive warnings from type/action coherence
  - No cycle detection false positives on the existing acyclic plan
  - Commit group coherence passes for all existing commit groups
- **Notes**: Gate for Sprint S3.2: all new validation checks must pass on the current PLAN.yaml without false positives.

### T3.3.6: Validate rendering and bootstrap improvements

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Actions**: test, verify
- **Depends on**: M3.3.1, M3.3.2, M3.3.3, M3.3.4, M3.3.5
- **Checks**:
  - render-plan.py produces enriched PLAN.md with item details
  - render-plan.py produces DOT with color/shape styling
  - Rendering is idempotent (second run produces identical output)
  - bootstrap-repo.sh --dry-run /tmp/test-X3 exits 0 and lists ADR + README
  - Workspace templates contain operational content
- **Notes**: Gate for Sprint S3.3: rendering, bootstrap, and workspace improvements must all work correctly.

### T3.4.5: Validate S3.4 documentation and operational mechanisms

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Actions**: test, verify
- **Depends on**: D3.4.1, D3.4.2, D3.4.3, M3.4.4
- **Checks**:
  - README.md exists and renders correctly
  - lifecycle.md freshness mechanism is fully specified
  - shared-workflow.md contains design-doc guardrail
  - validate-plan.py REPO_MAP staleness warning works
  - Full validate-plan.py run passes on PLAN.yaml
  - render-plan.py regenerates views deterministically
- **Notes**: Gate for Sprint S3.4: all documentation, guardrails, and operational mechanisms must be in place.
