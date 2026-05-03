# PLAN.md

AUTO-GENERATED from plan/PLAN-index.yaml. Do not edit manually.

- Repository: AgentOrchestrator
- Owner: NickF93
- Version: 0.1
- Last updated: 2026-05-03

## Mission

Build the minimal viable Level-0 central control plane (agent-os/) inside this repository. Level-0 provides: shared workflow documentation, plan schema, templates for repo-local files, and render/validate scripts. This repository IS the control-plane OS (Level-0). Level-1 (workspace runtime) and Level-2 (repo-local bootstrap) come after. The plan is not only a progress tracker. It is the canonical execution graph for agent orchestration, optimized for decomposition into independently executable items, safe aggregation into reviewable commit groups, and controlled parallel execution under explicit dependency, scope, and policy constraints.

## Milestones

| ID | Type | Title | Status |
|---|---|---|---|
| X1 | X | Level-0 MVP — Control Plane Foundation | done |
| X2 | X | Layer-0 Governance Hardening | done |
| X3 | X | Control-Plane Hardening | done |
| X4 | X | Governance Baseline Hardening | done |
| X5 | X | Tracking Discipline and Canonical Consistency Hardening | done |
| X6 | X | Planning Model Execution Optimization Clarification | done |
| X7 | X | Skill Packaging and Cross-Layer Execution | done |
| X8 | X | Adapter Layer Configuration and Repo Hygiene | done |
| X9 | X | Shared Layer-0 Asset Distribution and Two-Root Consumption | done |
| X10 | X | Script Test Suite and Local Quality Gates | done |
| X11 | X | Runtime Portability Expansion | done |
| X12 | X | Promote Codex to First-Class Runtime | done |
| X13 | X | Workspace Template Parity and Test Coverage Repair | done |
| X14 | X | Portability Milestone Completion — Copilot Support and Kilo Realignment | done |
| X15 | X | Environment Portability — Remove Hardcoded Conda Environment | done |
| X16 | X | Human-Readable TODO Checklist | done |
| X17 | X | Git Flow Design Doc English Translation | done |
| X18 | X | Git Flow Conflict Resolution and Operational Refinements | done |
| X19 | X | Git Flow Governance Extraction | done |
| X20 | X | Git Flow PR-Only Skill | done |
| X21 | X | Skill Discovery Table in AGENTS.md | done |
| X22 | X | Planning-to-Git Mapping and Branch Naming Convention | done |
| X23 | X | Git Flow Skill Portability Repairs | done |
| X24 | X | TODO Checklist Refresh After Git Flow Rollout | done |
| X25 | X | Full Runtime Parity and First-Class Promotion | done |
| X26 | X | Gemini and Cursor First-Class Portability | done |
| X27 | X | Repo Bootstrap Skill Packaging | done |
| X28 | X | Plan Validate-Render Skill Packaging | done |
| X29 | X | Portability and Governance Enforcement Bugfixes | done |
| X30 | X | TODO Roadmap Expansion | done |
| X31 | X | PLAN Splitting and Archival Foundation | done |
| X33 | X | Issue #8 Review Response and TODO Roadmap Integration | done |
| X34 | X | Make plan tests independent from active PLAN-current state | done |
| X35 | X | YAML hash-quoting guard and data repair | done |
| X36 | X | Add compute-ready readiness query to validate-plan.py | done |
| X37 | X | X36 gate repair and archival | done |
| X38 | X | Kilo Entrypoint Migration (.kilocode → .kilo) | done |
| X39 | X | Workspace Sync Skill Packaging | done |
| X40 | X | Structured Checks for Programmatic Verification | done |
| X41 | X | Issue and TODO Reconciliation Cleanup | done |
| X42 | X | Declarative on_fail Policy Metadata | done |
| X43 | X | Dangling on_fail Pivot Warning | in_progress |

## Plan

### X1

- ID: `X1`
- Title: Level-0 MVP — Control Plane Foundation
- Status: done

#### S1.1 Items

Sprint: Sprint 1 — Decisions, scaffold, schema, workflow docs, templates, scripts
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `C1.1.1` | `C` | Sprint 1 checkpoint — Level-0 scaffold complete and self-validating | done | After this checkpoint, the control plane is operational and able to bootstrap its first real target repo (Level-2) as Sprint 2 work. |
| `D1.1.1` | `D` | Create non-authoritative docs directory and initialize .gitignore | done | Moved startup documentation to docs/design/ as non-authoritative reference material and added baseline ignore rules for local/editor/runtime artifacts. |
| `M1.1.1` | `M` | Create agent-os/workflow/ documentation files | done | Content sourced from docs/design/documento-architetturale-control-plane-coding-agents.md and docs/design/gitflow_pr_only_terminal_workflow.md. Do NOT duplicate content; these files are the canonical split of the monolithic architecture doc. |
| `Q1.1.1` | `Q` | Decide: PLAN.yaml required fields and state transition rules | done | Decision recorded from interactive governance alignment. |
| `T1.1.1` | `T` | Validate this PLAN.yaml against plan.schema.json | done | This is the self-validation gate: the control plane must validate its own plan before it can claim to be a working control plane. |
| `D1.1.2` | `D` | Create architecture review and open-questions document | done | Captures what is confirmed, what is ambiguous, and five open questions (Q1.1.1–Q1.1.5) that must be decided before schema and scripts can be written. |
| `M1.1.2` | `M` | Create agent-os/schemas/plan.schema.json | done | JSON Schema (draft-2020-12) for PLAN.yaml. Must encode required fields, enum values for type/status/role/effort/actions, and scope field format as decided in Q1.1.1 and Q1.1.4. Must be self-consistent so that this PLAN.yaml passes validation once M1.1.4 is done. |
| `Q1.1.2` | `Q` | Decide: Level-1 runtime materialization strategy | done | Decision recorded from interactive governance alignment. |
| `T1.1.2` | `T` | Dry-run bootstrap-repo.sh on a temp path | done | Must confirm bootstrap is idempotent and does not write to disk in dry-run mode. A second run on the same target must produce identical output. |
| `D1.1.3` | `D` | Enforce commit message contract in Layer-0 governance | done | Added mandatory commit title contract: <type>(<scope>): <description> with optional body/footer sections. This is a Layer-0 global rule. |
| `M1.1.3` | `M` | Create agent-os/templates/ (AGENTS, ARCHITECTURE, REPO_MAP, PLAN) | done | Templates use {{REPO_NAME}}, {{DATE}}, {{OWNER}} placeholders. Level-1 files are generated from these templates by sync-workspace.sh (per Q1.1.2 decision). Each template must include the canonical source rule and authority map header so generated files self-document their origin. |
| `Q1.1.3` | `Q` | Decide: control-plane release and consumption model | done | Decision recorded from interactive governance alignment. |
| `T1.1.3` | `T` | Generate PLAN.md and PLAN.dot from this PLAN.yaml | done | PLAN.md and PLAN.dot are committed in the same commit as this PLAN.yaml update, not as separate commits (per Q1.1.5 decision). |
| `D1.1.4` | `D` | Strengthen and align commit body/footer recommendation wording | done | Standardized wording to: "Optional body and footer sections are strongly suggested, especially for medium or large commits." across all authoritative governance surfaces. |
| `M1.1.4` | `M` | Create agent-os/scripts/render-plan.py and validate-plan.py | done | validate-plan.py: validates PLAN.yaml against plan.schema.json; checks state transition legality, dangling depends_on, container items in depends_on, required fields. Exits non-zero on any hard-fail. render-plan.py: deterministic PLAN.yaml → PLAN.md + PLAN.yaml → PLAN.dot. Both scripts must be idempotent and callable standalone. |
| `Q1.1.4` | `Q` | Decide: scope field format and collision-detection semantics | done | Decision recorded from interactive governance alignment. |
| `M1.1.5` | `M` | Create agent-os/scripts/bootstrap-repo.sh and sync-workspace.sh | done | bootstrap-repo.sh: instantiates a new repo-local layer (Level-2) from templates. Supports --dry-run. Emits a PLAN.yaml seed from the template. sync-workspace.sh: pulls latest from control plane (per Q1.1.3 decision) and regenerates Level-1 runtime files from Level-0 templates (per Q1.1.2 decision). |
| `Q1.1.5` | `Q` | Decide: tooling failure semantics and commit hygiene rules | done | Decision recorded from interactive governance alignment. |
| `M1.1.6` | `M` | Create root governance files for this Level-0 repository | done | This repository is itself the Level-0 control-plane OS. Root AGENTS.md and ARCHITECTURE.md define local authority mapping and structural constraints for building and evolving agent-os/. |

### X2

- ID: `X2`
- Title: Layer-0 Governance Hardening
- Status: done
- Note: Close the compliance gaps between the design authority document (docs/design/documento-architetturale-control-plane-coding-agents.md) and the authoritative governance workflow files under agent-os/workflow/. Deliver a working agent-os/ scaffold with schema, workflow docs, templates, and tooling. Self-validate by running validate-plan.py on this PLAN.yaml.

#### S2.1 Items

Sprint: Sprint 1 — Propagate missing architectural rules to governance files
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `C2.1.1` | `C` | Architecture finalization checkpoint — close review gaps G1-G5 | done | Marks architecture baseline as finalized for Level-0 governance, with unresolved work shifted from open questions into explicit governed policy. |
| `D2.1.1` | `D` | Enforce missing architectural doc rules in workflow governance files | done | Close compliance gaps between the architecture doc (§6.2–6.4, §11.3–11.4, §4.2, §13.2) and the authoritative workflow files. Adds: full authority concern table, precedence rule, non-duplication rule, single-writer rule detail, grouping and collision rules, deferred automation list, and Kilo portability mapping example. |
| `D2.1.2` | `D` | Create English translation of the Italian architectural document | done | 1:1 English translation of docs/design/documento-architetturale-control-plane-coding-agents.md, placed in the same directory. Structural fidelity to the original is required: all sections, tables, code blocks, and math equations must be preserved verbatim in structure. |
| `D2.1.3` | `D` | Simplify commit title contract by removing item ID from header | done | Updated commit title contract everywhere from the item-ID-inclusive format to <type>(<scope>): <description> while keeping body/footer recommendation unchanged. |
| `D2.1.4` | `D` | Define prompts directory contract and lifecycle | done | Closes G1 by specifying prompt file format, required metadata, versioning, and lifecycle triggers in authoritative workflow guidance. |
| `D2.1.5` | `D` | Define skills packaging contract and compatibility mapping | done | Closes G2 by defining a neutral skill package format and adapter mapping expectations across agent runtimes. |
| `D2.1.6` | `D` | Define REPO_MAP freshness policy and update triggers | done | Closes G3 by defining ownership, refresh triggers, and freshness metadata for REPO_MAP.md so map staleness is detectable and reviewable. |
| `D2.1.7` | `D` | Define ADR template, numbering, and lifecycle states | done | Closes G4 by introducing a canonical ADR template with lifecycle states and linkage guidance to PLAN decision items. |
| `D2.1.8` | `D` | Define canonical-authority conflict detection and recovery procedure | done | Closes G5 by defining conflict detection, recovery actions, escalation, and a safety gate before Phase B automation. |

### X3

- ID: `X3`
- Title: Control-Plane Hardening
- Status: done
- Note: Address the 149-point review findings: fix source-of-truth integrity issues, harden schema enforcement, strengthen validation tooling, improve rendering and bootstrap, enrich workspace materialization, add documentation and operational guardrails.

#### S3.1 Items

Sprint: Sprint 1 — Source-of-truth integrity and schema hardening
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `F3.1.1` | `F` | Fix duplicate note key in PLAN.yaml X2 milestone | done | PLAN.yaml had two note: keys on milestone X2 (lines 35-41). YAML parsers silently override earlier values; PyYAML keeps the last. Merged both notes into a single field to preserve all content. |
| `M3.1.2` | `M` | Add actions, parent, commit_group to schema required fields for items | done | Changed item required from [id, type, title, status, role, effort] to [id, type, title, status, role, effort, actions, parent, commit_group]. Safe: all 28 existing items already have these fields. |
| `D3.1.3` | `D` | Document new required fields in item-taxonomy.md | done | Split Metadata Fields section into Required Item Fields and Optional Metadata Fields. Documents that actions, parent, and commit_group are now mandatory for all executable items. |
| `T3.1.4` | `T` | Validate PLAN.yaml against hardened schema | done | Gate for Sprint S3.1: the hardened schema must validate the current PLAN.yaml without errors. |

#### S3.2 Items

Sprint: Sprint 2 — Validation tooling hardening
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `M3.2.1` | `M` | Implement DAG cycle detection in validate-plan.py | done | Add detect_cycles() using Kahn's algorithm (topological sort). If remaining nodes after BFS, report cycle. Hard-fail on any cycle in depends_on relationships. |
| `M3.2.2` | `M` | Implement bidirectional commit_group/item consistency check | done | Three checks: (1) every commit_group.items[] resolves to existing item, (2) every item.commit_group references existing commit_group, (3) bidirectional membership is coherent. All hard-fail. |
| `M3.2.3` | `M` | Implement type/action coherence warnings | done | Encode recommended type/action coherence table from item-taxonomy.md. Warning-only, not hard-fail, since taxonomy says "recommended" not "mandatory". |
| `T3.2.4` | `T` | Validate all new validation checks against current PLAN.yaml | done | Gate for Sprint S3.2: all new validation checks must pass on the current PLAN.yaml without false positives. |
| `C3.2.5` | `C` | Sprint S3.2 checkpoint — validation hardening complete | done | Marks validation tooling as hardened for control-plane-grade enforcement. |

#### S3.3 Items

Sprint: Sprint 3 — Rendering, bootstrap, and workspace improvements
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `M3.3.1` | `M` | Add status/type visual styling to DOT rendering | done | Color nodes by status (done=green, blocked=red, in_progress=blue, etc.) and shape by type (Q=diamond, C=doubleoctagon, T=ellipse, etc.). |
| `M3.3.2` | `M` | Add per-item detail sections to markdown rendering | done | After items table, add Item Details section with per-item subsections showing notes, checks, decision, artifacts_out, and depends_on. |
| `M3.3.3` | `M` | Harden bootstrap-repo.sh with --owner, --ref, post-validation, ADR/README scaffolds | done | Add --owner/--ref flags, run validate-plan.py post-bootstrap, create docs/adr/ADR-0001.md and README.md scaffolds from templates. |
| `M3.3.4` | `M` | Create repo-README.md.template | done | New template for bootstrap-generated README.md in target repos. Uses existing {{REPO_NAME}}, {{OWNER}}, {{DATE}}, {{CONTROL_PLANE_REF}} placeholders. |
| `M3.3.5` | `M` | Enrich workspace templates with operational content | done | Add precedence rules, workflow summary, authority split reminder, commit contract, and links to runtime-relevant files. Workspace templates must be useful runtime references, not just stubs. |
| `T3.3.6` | `T` | Validate rendering and bootstrap improvements | done | Gate for Sprint S3.3: rendering, bootstrap, and workspace improvements must all work correctly. |

#### S3.4 Items

Sprint: Sprint 4 — Documentation, operational guardrails, and closure
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D3.4.1` | `D` | Create root README.md for this repository | done | Hand-maintained README (not template-generated) for the AgentOrchestrator repo itself. Contains: purpose, directory structure, quickstart, governance file links, license reference. |
| `D3.4.2` | `D` | Define REPO_MAP freshness operational mechanism | done | Define freshness computation (today - last_validated_on > freshness_window_days), update triggers, and checkpoint consumption rules. Close the gap between concept and operational mechanism. |
| `D3.4.3` | `D` | Add design-doc discipline guardrail | done | Add Design Document Governance section to shared-workflow.md: docs/design is non-authoritative, normative rules must migrate to canonical authority. Reinforce in ARCHITECTURE.md invariants. |
| `M3.4.4` | `M` | Add REPO_MAP staleness warning to validate-plan.py | done | Add --check-freshness flag. Parse REPO_MAP.md metadata, warn if stale when checkpoint items exist in review/verified state. Warning-only. |
| `T3.4.5` | `T` | Validate S3.4 documentation and operational mechanisms | done | Gate for Sprint S3.4: all documentation, guardrails, and operational mechanisms must be in place. |
| `C3.4.6` | `C` | Milestone X3 closure checkpoint — control-plane hardening complete | done | Marks the control plane as hardened per the 149-point review findings. |

### X4

- ID: `X4`
- Title: Governance Baseline Hardening
- Status: done
- Note: Remediate 19 findings from the post-X3 governance review: contradictions between canonical authorities, soft language where hard gates are intended, undefined field semantics, and missing enforcement mechanisms. All architectural decisions resolved interactively with the human owner.

#### S4.1 Items

Sprint: Sprint 1 — Language enforcement and clarity
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `M4.1.1` | `M` | Tighten soft language to hard gates in governance files | done | Findings #2, #6, #12, #13: "may only" → "MUST only" in shared-workflow.md, "should not" → "MUST NOT" for design doc rule, "can optionally detect" → prescriptive in lifecycle.md, add explicit parallelism prohibition. |
| `M4.1.2` | `M` | Document type/action coherence as warning-only | done | Finding #3: add note to type/action coherence table clarifying it is advisory — violations produce warnings, not hard failures. |
| `T4.1.3` | `T` | Validate language fixes are consistent across governance docs | done |  |

#### S4.2 Items

Sprint: Sprint 2 — Semantic alignment (closure and freshness)
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `M4.2.1` | `M` | Align commit group closure to require both status and checks | done | Finding #1: state both predicates together in both files — items must be in review/verified/done AND required checks must be satisfied. |
| `M4.2.2` | `M` | Make REPO_MAP freshness a hard gate in docs and validator | done | Finding #5: remove "advisory" language from lifecycle.md, change validate-plan.py check_repo_map_freshness() from warning to hard-fail. |
| `T4.2.3` | `T` | Validate closure and freshness alignment | done |  |

#### S4.3 Items

Sprint: Sprint 3 — Schema and taxonomy hardening
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `M4.3.1` | `M` | Restrict depends_on to exclude milestoneId in schema | done | Finding #4: create dependencyTarget definition as oneOf [sprintId, itemId]. Update depends_on items ref to use dependencyTarget instead of planId. |
| `M4.3.2` | `M` | Define scope, checks, and suffix semantics in item-taxonomy | done | Findings #8, #9, #17: scope is path prefix for collision detection, checks is array of human-readable descriptions, suffixes are contiguous lowercase sequence in derivation order with no gaps. |
| `M4.3.3` | `M` | Add decision if/then Q-only constraint in schema | done | Finding #18: add JSON Schema if/then to forbid decision property on non-Q-type items. |
| `M4.3.4` | `M` | Add scope pattern constraint to schema | done | Finding #8 (schema side): add pattern for scope field to restrict to path-like characters. |
| `T4.3.5` | `T` | Validate PLAN.yaml against hardened schema | done |  |

#### S4.4 Items

Sprint: Sprint 4 — Lifecycle unification and deferred fields
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D4.4.1` | `D` | Unify governance asset states to draft/active/deprecated/superseded | done | Finding #7: change ADR states from proposed/accepted to draft/active. Add unified Governance Asset Lifecycle section applicable to prompts, ADRs, and skills. |
| `D4.4.2` | `D` | Add DEFERRED notes for triggers and tools_profile fields | done | Findings #15, #16: mark triggers and tools_profile as DEFERRED adapter-level fields with semantics TBD, optional and non-normative in MVP. |
| `D4.4.3` | `D` | Clarify single-writer rule as documentation/review-enforced | done | Finding #10: add note that enforcement is governance-based (code review and escalation), not automated. No validator check for single-writer. |
| `T4.4.4` | `T` | Validate lifecycle and field documentation changes | done |  |

#### S4.5 Items

Sprint: Sprint 5 — Commit format, Phase B, and phase-gate enforcement
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D4.5.1` | `D` | Define recommended commit body/footer format | done | Finding #19: define recommended (SHOULD) body/footer structure including summary, scope, items, validation, refs, ADR, and follow-up sections. |
| `M4.5.2` | `M` | Simplify ARCHITECTURE.md Phase B to cross-reference | done | Finding #11: replace single-condition Phase B statement with cross-reference to shared-workflow.md Phase B Safety Gate for the full prerequisite list. |
| `D4.5.3` | `D` | Add phase-gate protocol for deferred automations | done | Finding #20 (part 1): add Phase Gate Protocol section requiring dedicated decision item, human sign-off, and ADR for each deferred automation. |
| `M4.5.4` | `M` | Add phase-gate schema fields (requires_phase, approval_ref) | done | Finding #20 (part 2): add requires_phase enum [A,B,C,D] and approval_ref string as optional item fields in schema and document in taxonomy. |
| `M4.5.5` | `M` | Add phase-gate validator enforcement | done | Finding #20 (part 3): add validate_phase_gates() — hard-fail if item has requires_phase and is ready/in_progress/review without approval_ref. Soft warning for deferred automation keywords without requires_phase. |
| `T4.5.6` | `T` | Validate commit format, Phase B, and phase-gate changes | done |  |
| `C4.5.7` | `C` | Milestone X4 closure checkpoint — governance baseline hardened | done |  |

#### S4.6 Items

Sprint: Sprint 6 — Validator enforcement for commit_group presence
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `M4.6.1` | `M` | Enforce executable item commit_group presence in validate-plan.py | done | Add hard-fail validation: every executable item type (Q, D, M, F, T, C) must declare commit_group. This makes commit boundary enforcement explicit in runtime validation, in addition to existing bidirectional coherence. |
| `T4.6.2` | `T` | Validate strict commit_group presence and coherence checks | done |  |
| `C4.6.3` | `C` | Commit governance enforcement checkpoint — validation executable | done |  |

#### S4.7 Items

Sprint: Sprint 7 — Commit hook enforcement and runtime wording alignment
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `M4.7.1` | `M` | Add local commit-msg hook guard for commit title contract | done | Add lightweight commit-msg hook enforcing the title pattern ^([a-z]+)\(([a-z0-9._/-]+)\): .+$ for local commits. The hook prints a clear error and references the canonical governance policy location. |
| `D4.7.2` | `D` | Document hook enablement workflow in README.md | done | Add explicit setup instructions so contributors and agents enable the repository hook path consistently. |
| `D4.7.3` | `D` | Align workspace runtime wording with mandatory commit_group hard gate | done | Add explicit runtime wording that the mandatory commit_group hard gate is defined in shared-workflow.md and git-automation-policy.md. |
| `T4.7.4` | `T` | Validate commit hook pattern and documentation alignment | done |  |
| `C4.7.5` | `C` | Commit tooling checkpoint — local enforcement and runtime clarity complete | done |  |

### X5

- ID: `X5`
- Title: Tracking Discipline and Canonical Consistency Hardening
- Status: done
- Note: Strengthen plan-first execution discipline and repair the remaining authority/template drift after the architecture review. This milestone makes commit_group boundaries explicit and non-ad-hoc, propagates the tracking and commit traceability rule across Level-0/1/2 artifacts, aligns ADR and REPO_MAP template semantics with canonical workflow rules, makes workspace sync materialize from local state without implicit remote mutation, and packages Python tooling dependencies for fresh checkouts.

#### S5.1 Items

Sprint: Sprint 1 — Tracking-first governance hardening
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D5.1.1` | `D` | Codify tracking-first execution in Level-0 authorities | done | Makes PLAN-first execution explicit: work must be tracked in PLAN.yaml before file edits begin, and untracked modifications are a governance violation. |
| `D5.1.2` | `D` | Define exact commit_group traceability and non-ad-hoc commit closure | done | Makes commit_group boundaries a plan-time decision, requires each git commit to close exactly one commit_group, and requires explicit item and commit_group references in the commit footer. |
| `C5.1.3` | `C` | Governance checkpoint — tracking-first hard gate is canonical | done |  |

#### S5.2 Items

Sprint: Sprint 2 — Cross-layer propagation, tooling enforcement, and operator flow
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D5.2.1` | `D` | Propagate tracking-first and commit traceability rules into Level-1 and Level-2 templates | done | Makes the rule visible beyond Level-0 so workspace runtime files and bootstrapped repo-local governance files carry the same hard gate. |
| `M5.2.2` | `M` | Enforce commit title and Refs footer contract in repo-local tooling | done | Extends the local commit hook to require both the canonical title contract and a Refs footer with PLAN item IDs plus exactly one commit_group, and bootstraps the same guard into downstream repos. |
| `M5.2.3` | `M` | Repair template drift, local provenance, and fresh-checkout operator flow | done | Aligns ADR and REPO_MAP templates with canonical lifecycle policy, removes implicit remote mutation from workspace sync, stamps workspace files with local provenance, and makes the repo self-hosted with an explicit dependency manifest and runnable operator documentation. |
| `T5.2.4` | `T` | Validate nn-2 flow for plan tooling, bootstrap, sync, and hook enforcement | done |  |
| `C5.2.5` | `C` | Consistency repair checkpoint — cross-layer rules and operator flow aligned | done |  |

### X6

- ID: `X6`
- Title: Planning Model Execution Optimization Clarification
- Status: done
- Note: Clarify in canonical authorities that the planning model is an execution-oriented control artifact optimized for independently executable decomposition, safe aggregation into reviewable commit groups, and controlled parallel execution under explicit dependency, boundary, and policy constraints.

#### S6.1 Items

Sprint: Sprint 1 — Planning model optimization principle
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D6.1.1` | `D` | Codify the planning model as an execution-optimization artifact | done | Adds the planning-model optimization principle to the canonical workflow authority, reflects it as an architectural principle, and records the repository-level execution intent in PLAN.yaml without creating a second conflicting workflow authority. |
| `T6.1.2` | `T` | Validate planning-model principle wording and regenerated plan views | done |  |
| `C6.1.3` | `C` | Planning-model optimization checkpoint | done |  |

### X7

- ID: `X7`
- Title: Skill Packaging and Cross-Layer Execution
- Status: done
- Note: Deliver the first operational skill under agent-os/skills/ and document the workspace topology and artifact placement model that enables shared skills and tooling to operate on Layer-2 repos.

#### S7.1 Items

Sprint: Sprint 1 — Checkpoint closure skill and workspace topology documentation
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D7.1.1` | `D` | Create plan-checkpoint-close skill | done | First operational skill under agent-os/skills/. Implements a procedural, tool-neutral checkpoint closure workflow that operates at both Layer 0 and Layer 2 using a two-root model (control_plane_root for shared tooling, repo_root for target data). Satisfies the skill packaging contract defined in agent-os/skills/README.md and agent-os/workflow/portability-model.md. |
| `D7.1.2` | `D` | Document workspace topology and artifact placement in shared workflow | done | Adds Workspace Topology diagram and Artifact Placement Across Layers table to the Three-Layer Model section of shared-workflow.md. Documents the two-root resolution model (control_plane_root vs repo_root) and how sync-workspace.sh stamps CONTROL_PLANE_ROOT for discovery. Content is additive — no duplication with existing canonical authorities. |
| `T7.1.3` | `T` | Validate skill contract compliance and plan consistency | done |  |
| `C7.1.4` | `C` | Skill packaging and cross-layer execution checkpoint | done |  |

### X8

- ID: `X8`
- Title: Adapter Layer Configuration and Repo Hygiene
- Status: done
- Note: Create thin adapter-layer files (CLAUDE.md, and future equivalents for Codex/Copilot/Kilo) that point agents to canonical governance authorities and override adapter-specific defaults that conflict with governance rules.

#### S8.1 Items

Sprint: Sprint 1 — Claude Code adapter CLAUDE.md
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D8.1.1` | `D` | Create CLAUDE.md as thin adapter layer pointing to canonical governance | done | Thin adapter-layer file for Claude Code. Points to AGENTS.md and canonical workflow authorities. Overrides Claude Code's default ask-before-committing behavior to align with the mandatory commit rule. Does not duplicate normative content — adapter boundary rule preserved. |
| `F8.1.2` | `F` | Add .mypy_cache and workspace patterns to .gitignore | done | Adds .mypy_cache/ and *-workspace/ patterns to .gitignore to keep eval working directories and type-check caches out of version control. |
| `C8.1.3` | `C` | Adapter layer and repo hygiene checkpoint | done |  |

### X9

- ID: `X9`
- Title: Shared Layer-0 Asset Distribution and Two-Root Consumption
- Status: done
- Note: Implements the shared-asset foundation for stable Layer-0 prompts, skills, profiles, and protocols with a canonical registry, PLAN item references, workspace-first two-root resolution, and optional explicit vendoring for standalone Layer-2 repos. Local milestone numbering uses X9 because X7 is already allocated in this repository's canonical plan.

#### S9.1 Items

Sprint: Sprint 1 — Shared assets, registry, and two-root consumption
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D9.1.1` | `D` | Define canonical shared-asset families, registry, and seed assets | done | Establishes the explicit shared asset families (skills, prompts, profiles, protocols), adds the canonical registry, and ships the first real seed assets. Contracts remain tool-neutral; runtime-specific behavior belongs in profiles and adapter notes, not in the shared prompt or skill. |
| `M9.1.2` | `M` | Extend PLAN schema and validator for shared_assets registry-backed references | done | Adds the optional shared_assets object to executable PLAN items, constrains context_policy and resolution_mode values, and validates that referenced asset IDs resolve through the canonical registry. Deferred triggers and tools_profile fields remain untouched. |
| `M9.1.3` | `M` | Implement shared asset resolver, materialization, and runtime doc propagation | done | Implements two-root shared asset discovery with workspace-first CONTROL_PLANE_ROOT resolution and optional explicit vendoring under .agent-os/vendor/. Generated workspace and repo runtime docs must explain workspace mode and vendored mode without making Layer-2 copies authoritative. |
| `T9.1.4` | `T` | Validate shared asset consistency, resolver behavior, and plan rendering | done |  |
| `C9.1.5` | `C` | Shared asset distribution and two-root consumption checkpoint | done |  |

### X10

- ID: `X10`
- Title: Script Test Suite and Local Quality Gates
- Status: done
- Note: Add a repo-owned pytest suite for agent-os/scripts/, a deterministic local gate runner for Ruff, mypy, compile checks, pytest, and conditional ShellCheck, plus the required tooling configuration and documentation for the nn-2 environment.

#### S10.1 Items

Sprint: Sprint 1 — Script tests, tooling config, and local gates
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D10.1.1` | `D` | Define script test/gate scope and tooling surface | done | Establishes the repo-local test and gate contract for agent-os/scripts/, keeps requirements.txt runtime-only, and documents nn-2 as the canonical execution environment for tests and local gates. |
| `M10.1.2` | `M` | Implement pytest suite for Python and Bash scripts | done | Adds behavior-focused pytest coverage for the Python scripts and subprocess smoke tests for bootstrap, sync-workspace, and materialize-shared-asset using temporary directories only. |
| `M10.1.3` | `M` | Add deterministic local gate runner and tooling config | done | Adds one local gate entrypoint that runs Ruff, mypy, Python compile checks, pytest, and conditional ShellCheck in a fixed order with readable output and deterministic failure behavior. |
| `T10.1.4` | `T` | Validate script tests and local gates in nn-2 | done |  |
| `C10.1.5` | `C` | Script test suite and local gates checkpoint | done |  |

### X11

- ID: `X11`
- Title: Runtime Portability Expansion
- Status: done
- Note: Formalize the runtime lifecycle model (experimental / supported / first-class), populate the Codex adapter, add Kilo as an experimental runtime, and document Copilot as deferred. Closes the gap between the agent-agnostic architecture and the actual adapter coverage.

#### S11.1 Items

Sprint: Sprint 1 — Runtime lifecycle, Codex adapter, Kilo experimental, Copilot deferral
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D11.1.1` | `D` | Design runtime lifecycle model and plan portability expansion | done | Adds a formal three-tier runtime lifecycle (experimental, supported, first-class) to portability-model.md. Assigns current runtimes: claude = first-class, codex = supported, kilo = experimental. Documents Copilot as recognized but deferred with rationale about its different adapter shape. |
| `M11.1.2` | `M` | Populate Codex adapter and add lifecycle references to READMEs | done | Populates the empty .codex file following the CLAUDE.md thin adapter pattern. Same canonical authorities, same three adapter overrides. Codex-specific sandbox notes for tooling. Updates skills/README.md and prompts/README.md to reference the runtime lifecycle tiers. |
| `M11.1.3` | `M` | Add Kilo as experimental runtime with adapter, profile, and registry | done | Creates KILO.md as a thin experimental adapter at repo root. Creates kilo profile. Adds kilo to neutral asset compatibility in the registry. Updates skill frontmatter. Adds .sixth/ to .gitignore. |
| `T11.1.4` | `T` | Validate portability expansion and runtime artifacts | done |  |
| `C11.1.5` | `C` | Runtime portability expansion checkpoint | done |  |

### X12

- ID: `X12`
- Title: Promote Codex to First-Class Runtime
- Status: done
- Note: Promote Codex from supported to first-class by adding a workspace template, extending sync-workspace.sh to render it, and updating the runtime status table.

#### S12.1 Items

Sprint: Sprint 1 — Codex workspace template, sync-workspace extension, tier promotion
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `M12.1.1` | `M` | Create Codex workspace template and extend sync-workspace.sh | done | Creates workspace-CODEX.md.template following the CLAUDE template pattern with Codex-specific sandbox notes. Extends sync-workspace.sh to render the Codex template alongside AGENTS.md and CLAUDE.md. Updates portability-model.md runtime status table to mark codex as first-class. |
| `T12.1.2` | `T` | Validate Codex first-class promotion | done |  |
| `C12.1.3` | `C` | Codex first-class promotion checkpoint | done |  |

### X13

- ID: `X13`
- Title: Workspace Template Parity and Test Coverage Repair
- Status: done
- Note: Fix workspace-CLAUDE.md.template missing adapter overrides section found during governance audit. Expand sync-workspace.sh test to verify all three rendered files.

#### S13.1 Items

Sprint: Sprint 1 — Template parity fix and test expansion
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `F13.1.1` | `F` | Add adapter overrides to workspace-CLAUDE.md.template | done | Governance audit found workspace-CLAUDE.md.template is missing the adapter overrides section that workspace-CODEX.md.template has. Layer 2 Claude agents would not receive the mandatory commit override. |
| `F13.1.2` | `F` | Expand sync-workspace.sh test to verify all rendered files | done | Test only checks AGENTS.md existence and content. Must also verify CLAUDE.md and .codex are generated with correct CONTROL_PLANE_ROOT stamping. |
| `C13.1.3` | `C` | Workspace template parity and test coverage checkpoint | done |  |

### X14

- ID: `X14`
- Title: Portability Milestone Completion — Copilot Support and Kilo Realignment
- Status: done
- Note: Complete the runtime portability milestone without splitting authority. Add GitHub Copilot as a supported runtime through a thin repo-level entrypoint, replace the KILO.md adapter fiction with native Kilo portability through AGENTS.md plus shared assets, and update the portability contract to speak in terms of runtime entrypoint artifacts instead of a single adapter file shape.

#### S14.1 Items

Sprint: Sprint 1 — Copilot support and Kilo entrypoint realignment
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D14.1.1` | `D` | Track portability completion milestone and runtime entrypoint contract update | done | Adds X14 as the tracked follow-on to X11–X13. Records the contract shift from singular adapter files to runtime entrypoint artifacts, targets Copilot as supported, and realigns Kilo to native portability through AGENTS.md instead of a dedicated KILO.md authority file. |
| `M14.1.2` | `M` | Implement Copilot support and Kilo realignment across docs, templates, registry, and tooling | done | Adds a thin `.github/copilot-instructions.md` bootstrap template, registers the Copilot profile, broadens neutral shared-asset compatibility to include Copilot, removes KILO.md from the portability contract and verification expectations, and keeps runtime authority centralized in canonical governance files. |
| `T14.1.3` | `T` | Validate Copilot support and Kilo realignment | done |  |
| `C14.1.4` | `C` | Portability completion checkpoint | done |  |

### X15

- ID: `X15`
- Title: Environment Portability — Remove Hardcoded Conda Environment
- Status: done
- Note: Remove hardcoded nn-2 conda environment from all scripts, adapters, and documentation. Replace with AGENT_PYTHON environment variable loaded from .env per workstation. Ship .env.example as reference.

#### S15.1 Items

Sprint: Sprint 1 — AGENT_PYTHON env var, .env.example, script and docs portability
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `M15.1.1` | `M` | Replace hardcoded nn-2 with AGENT_PYTHON env var across scripts and docs | done | Creates .env.example with AGENT_PYTHON variable. Refactors run-gates.sh to source .env and use AGENT_PYTHON instead of hardcoded nn-2 discovery. Updates CLAUDE.md and README.md to reference the env var pattern. |
| `T15.1.2` | `T` | Validate environment portability | done |  |
| `C15.1.3` | `C` | Environment portability checkpoint | done |  |

### X16

- ID: `X16`
- Title: Human-Readable TODO Checklist
- Status: done
- Note: Add a non-normative TODO.md checklist for the human operator to track macro-features across the project. Not governance, not read by agents.

#### S16.1 Items

Sprint: Sprint 1 — Create TODO.md
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D16.1.1` | `D` | Create non-normative TODO.md checklist | done | Human-readable checklist of macro-features done and pending. Not governance, not read by agents. |
| `D16.1.2` | `D` | Fix TODO typo from NFC to RFC for normative review section | done | Corrects the TODO heading/checkbox label typo from NFC to RFC in the non-normative future-considerations section. |

### X17

- ID: `X17`
- Title: Git Flow Design Doc English Translation
- Status: done
- Note: Add an English peer document under docs/design/ for the existing gitflow_pr_only_terminal_workflow.md source, preserving the original structure, command examples, and reference set in a 1:1 translation.

#### S17.1 Items

Sprint: Sprint 1 — Create English peer document for the gitflow design workflow
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D17.1.1` | `D` | Create an English peer document for the Git Flow PR-only terminal workflow | done | Create a new English design document alongside the existing Italian source file, keeping headings, lists, commands, Mermaid diagrams, and references aligned 1:1 with the original workflow document under the peer filename docs/design/gitflow-pr-only-terminal-workflow.md. |
| `T17.1.2` | `T` | Validate the English peer document and regenerated plan views | done | validate-plan.py completed successfully against the schema. render-plan.py regenerated PLAN.md and PLAN.dot. Structural parity checks confirmed 61 headings, 100 code fences, and 21 references in both the Italian source and the English peer document. |
| `C17.1.3` | `C` | Git Flow design doc English translation checkpoint | done | Checkpoint closure prepared with the plan-checkpoint-close procedure at Layer 0. REPO_MAP.md is not present in this repository, so freshness is not applicable. The Italian source document remained unchanged. |

### X18

- ID: `X18`
- Title: Git Flow Conflict Resolution and Operational Refinements
- Status: done
- Note: Add conflict resolution scenarios (single-PR and two-PR flows), operational refinements (always-draft-PR, explicit staging, no agent branch deletion, release-branch exception for hotfix back-merge), and branch protection requirements to the Git Flow design document. These decisions were made interactively with the human owner and must be captured before the governance file and skill are authored.

#### S18.1 Items

Sprint: Sprint 1 — Conflict resolution scenarios and operational refinements
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D18.1.1` | `D` | Add conflict resolution scenarios and operational refinements to the Git Flow design doc | done | Add new sections to the English design document covering: Scenario A (single-PR conflict resolution for feature/bugfix), Scenario B (two-PR conflict resolution for hotfix/release with release-branch exception), conflict classification rules (trivial vs non-trivial), always-draft-PR policy, explicit staging rule (no git add -A), no agent branch deletion rule, and branch protection requirements placeholder. |

### X19

- ID: `X19`
- Title: Git Flow Governance Extraction
- Status: done
- Note: Extract normative rules from the Git Flow design document (docs/design/gitflow-pr-only-terminal-workflow.md) into a canonical workflow authority (agent-os/workflow/git-flow-policy.md). Register the new authority in the Canonical Concern Split table and add a supersession note to the design document.

#### S19.1 Items

Sprint: Sprint 1 — Git Flow governance file and authority registration
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D19.1.1` | `D` | Create git-flow-policy.md governance authority | done | Extract normative rules from the Git Flow design document into agent-os/workflow/git-flow-policy.md. Covers: branch model definition, workflow invariants, forbidden operations, synchronization rules, conflict resolution model, PR topology, tagging policy, operational refinements, and branch protection enforcement. |
| `D19.1.2` | `D` | Register git-flow-policy.md in canonical concern split and add design doc supersession note | done | Add git-flow-policy.md to the Canonical Concern Split table in shared-workflow.md. Add a supersession note at the top of the design document indicating which rules have been migrated to the canonical authority. |
| `C19.1.3` | `C` | Checkpoint closure — X19 Git Flow governance extraction | done | Validate plan, render views, verify that the governance file exists, that the concern split table is updated, and that the design doc carries the supersession note. Close X19, S19.1. |

### X20

- ID: `X20`
- Title: Git Flow PR-Only Skill
- Status: done
- Note: Deliver the gitflow-pr-only operational skill under agent-os/skills/. The skill implements five actions (start, sync, merge, tag, back-merge) as procedural steps applying the rules from git-flow-policy.md. It supports the two-root model (Layer 0 and Layer 2) and is agent-agnostic (Claude, Codex, Kilo, Copilot).

#### S20.1 Items

Sprint: Sprint 1 — gitflow-pr-only skill implementation
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D20.1.1` | `D` | Create gitflow-pr-only SKILL.md | done | Write the gitflow-pr-only skill with five actions (start, sync, merge, tag, back-merge). Follows the packaging contract from agent-os/skills/README.md, the two-root model from plan-checkpoint-close, and applies the governance rules from agent-os/workflow/git-flow-policy.md. Agent-agnostic with adapter notes for Claude, Codex, Kilo, and Copilot. |
| `C20.1.2` | `C` | Checkpoint closure — X20 gitflow-pr-only skill | done | Validate plan, render views, verify skill file exists with correct frontmatter. Close X20, S20.1. |

### X21

- ID: `X21`
- Title: Skill Discovery Table in AGENTS.md
- Status: done
- Note: Add an available-skills table to AGENTS.md § Skills so agents can discover skills by name and trigger condition without scanning the directory. Keeps AGENTS.md as the single authority for skill discovery.

#### S21.1 Items

Sprint: Sprint 1 — Skill discovery table
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D21.1.1` | `D` | Add available-skills table to AGENTS.md § Skills | done | Add a table listing each skill ID, its trigger conditions, and path to AGENTS.md § Skills. This makes AGENTS.md the single authority for skill discovery — agents read the table instead of scanning the directory. |
| `C21.1.2` | `C` | Checkpoint closure — X21 skill discovery table | done |  |

### X22

- ID: `X22`
- Title: Planning-to-Git Mapping and Branch Naming Convention
- Status: done
- Note: Document the mapping between the planning hierarchy (milestone, sprint, commit_group, checkpoint) and git concepts (branch, work phase, commit, PR merge). Define a branch naming convention that includes the milestone ID for traceability. Establish the hybrid approach: agent follows the documented rule, human can override. Based on industry consensus (Linear, GitLab, DORA research, agentic workflow literature).

#### S22.1 Items

Sprint: Sprint 1 — Planning-to-git mapping documentation
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D22.1.1` | `D` | Document planning-to-git mapping in shared-workflow.md | done | Add a Planning-to-Git Mapping section to shared-workflow.md covering: the hierarchy mapping (milestone→branch, sprint→work phase, commit_group→commit, milestone closure→PR merge), the branch naming convention (<family>/<XNN>-<kebab-description>), the agent rule (trigger gitflow-pr-only start on milestone activation), the human override mechanism (planning-only milestones can skip branching), and the hook validation reference. Based on hybrid approach from industry consensus. |
| `D22.1.2` | `D` | Add branch naming validation to git-flow-policy.md | done | Add a branch naming convention section to git-flow-policy.md that cross-references the mapping in shared-workflow.md. Include the naming pattern and hook validation rule. |
| `C22.1.3` | `C` | Checkpoint closure — X22 planning-to-git mapping | done |  |

### X23

- ID: `X23`
- Title: Git Flow Skill Portability Repairs
- Status: done
- Note: Repair the portability gaps found in the gitflow-pr-only rollout: register the skill in the shared asset registry, restore compliance with the skill packaging contract, and propagate portable skill discovery to the repo AGENTS template without widening scope.

#### S23.1 Items

Sprint: Sprint 1 — Registry, skill contract, and template portability fixes
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `M23.1.1` | `M` | Register gitflow-pr-only as a portable shared skill and propagate discovery metadata | done | Fix the portability issues identified in review by registering the gitflow-pr-only skill in the canonical shared asset registry, adding the missing Expected Outputs section required by the skill packaging contract, and propagating the available-skills discovery table to the repo AGENTS template used by bootstrapped repos. |
| `T23.1.2` | `T` | Validate gitflow skill registry resolution and plan/render consistency | done |  |
| `C23.1.3` | `C` | Checkpoint closure — X23 gitflow skill portability repairs | done | Close the gitflow skill portability repair milestone after registry resolution, packaging-contract compliance, and template propagation are verified. Close X23, S23.1. |

### X24

- ID: `X24`
- Title: TODO Checklist Refresh After Git Flow Rollout
- Status: done
- Note: Refresh the non-authoritative human checklist in TODO.md so it reflects the recent Git Flow governance, skill, portability, and planning-to-git mapping commits without expanding it into a second source of truth.

#### S24.1 Items

Sprint: Sprint 1 — TODO.md refresh
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D24.1.1` | `D` | Refresh human-readable TODO.md for the recent Git Flow work | done | Update the non-authoritative personal checklist to reflect the recent completion of the Git Flow governance extraction, gitflow-pr-only skill, discovery metadata, planning-to-git mapping, and portability repair work. |

### X25

- ID: `X25`
- Title: Full Runtime Parity and First-Class Promotion
- Status: done
- Note: Achieve full runtime parity by creating bootstrap templates for all four runtimes (Claude, Codex, Copilot, Kilo), refining the first-class tier definition to support both workspace-scoped and repo-scoped runtimes, and promoting all runtimes to first-class status with end-to-end validation.

#### S25.1 Items

Sprint: Sprint 1 — Governance model update and bootstrap template creation
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D25.1.1` | `D` | Refine portability-model.md first-class tier for workspace-scoped and repo-scoped runtimes | done |  |
| `M25.1.2` | `M` | Create repo-CLAUDE.md.template for downstream repo bootstrap | done |  |
| `M25.1.3` | `M` | Create repo-CODEX.md.template for downstream repo bootstrap | done |  |
| `M25.1.4` | `M` | Add adapter overrides section to repo-copilot-instructions.md.template | done |  |
| `M25.1.5` | `M` | Create repo-kilo-rules.md.template for Kilo bootstrap entrypoint | done |  |

#### S25.2 Items

Sprint: Sprint 2 — Tooling integration, profile updates, and validation
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `M25.2.1` | `M` | Update bootstrap-repo.sh to generate Claude, Codex, and Kilo entrypoints | done |  |
| `M25.2.2` | `M` | Update runtime profiles, portability status table, and shared-workflow.md | done |  |
| `D25.2.3` | `D` | Update TODO.md for runtime parity completion | done |  |
| `T25.2.4` | `T` | Validate full runtime parity across bootstrap, sync, profiles, and governance | done |  |
| `C25.2.5` | `C` | Checkpoint closure — X25 full runtime parity and first-class promotion | done |  |

### X26

- ID: `X26`
- Title: Gemini and Cursor First-Class Portability
- Status: done
- Note: Extend the first-class runtime portability model to Gemini and Cursor through thin repo-scoped native entrypoints, bootstrap integration, active profiles, registry/runtime compatibility updates, and end-to-end validation while preserving the existing workspace-vs-repo entrypoint boundary.

#### S26.1 Items

Sprint: Sprint 1 — Gemini/Cursor governance update and bootstrap templates
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D26.1.1` | `D` | Extend the portability model for Gemini and Cursor repo-scoped first-class runtimes | done |  |
| `M26.1.2` | `M` | Create repo-GEMINI.md.template for downstream repo bootstrap | done |  |
| `M26.1.3` | `M` | Create repo-cursor-rules.mdc.template for downstream repo bootstrap | done |  |

#### S26.2 Items

Sprint: Sprint 2 — Tooling integration, runtime updates, and validation
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `M26.2.1` | `M` | Update bootstrap-repo.sh to generate Gemini and Cursor entrypoints | done |  |
| `M26.2.2` | `M` | Add Gemini/Cursor profiles and update runtime compatibility across shared assets, workflow docs, and skills | done |  |
| `D26.2.3` | `D` | Remediate runtime portability drift in README.md and TODO.md | done |  |
| `T26.2.4` | `T` | Validate six-runtime portability across bootstrap, sync, profiles, and governance | done |  |
| `C26.2.5` | `C` | Checkpoint closure — X26 Gemini and Cursor first-class portability | done |  |
| `M26.2.6` | `M` | Harden run-gates.sh against stale mypy cache failures | done |  |

### X27

- ID: `X27`
- Title: Repo Bootstrap Skill Packaging
- Status: done
- Note: Package the existing bootstrap-repo.sh script as a portable skill under agent-os/skills/. Add pre-flight validation, post-bootstrap verification, and structured reporting. Register in the shared asset registry and propagate discovery to AGENTS.md and the repo template.

#### S27.1 Items

Sprint: Sprint 1 — Skill implementation, registry, and discovery propagation
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D27.1.1` | `D` | Create repo-bootstrap skill SKILL.md with pre-flight, execution, and verification procedure | done | Create SKILL.md following the skill packaging contract. Wraps bootstrap-repo.sh with pre-flight validation, execution orchestration, post-bootstrap verification, and structured reporting. Supports all six first-class runtimes with adapter notes. |
| `M27.1.2` | `M` | Register repo-bootstrap in shared asset registry and propagate discovery metadata | done | Add the repo-bootstrap skill entry to shared-assets.yaml registry. Add the skill to the available-skills table in AGENTS.md (Level-0) and in repo-AGENTS.md.template (Level-2 template). Check off TODO.md. |
| `T27.1.3` | `T` | Validate repo-bootstrap skill packaging and plan consistency | done |  |
| `C27.1.4` | `C` | Checkpoint closure — X27 repo-bootstrap skill packaging | done |  |

### X28

- ID: `X28`
- Title: Plan Validate-Render Skill Packaging
- Status: done
- Note: Package the existing validate-plan.py and render-plan.py scripts as a portable skill under agent-os/skills/. Add two-root resolution, warning/error classification, render drift detection, and structured reporting via check-result-v1. Register in the shared asset registry and propagate discovery to AGENTS.md and the repo template.

#### S28.1 Items

Sprint: Sprint 1 — Skill definition and procedure authoring
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D28.1.1` | `D` | Create plan-validate-render skill SKILL.md with validation, rendering, drift detection, and reporting procedure | done | Create SKILL.md following the skill packaging contract. Wraps two scripts: validate-plan.py (17 validation checks, exit 0/1/2) and render-plan.py (PLAN.md + PLAN.dot generation, exit 0/2). Procedure covers two-root resolution, pre-flight checks, validation execution with flag assembly, output interpretation (parse OK/WARNING/ERROR lines, classify hard-fail vs advisory across 17 check categories), rendering, render drift detection via git diff, and structured verdict assembly via check-result-v1 protocol. Adapter notes for all six runtimes. |

#### S28.2 Items

Sprint: Sprint 2 — Registry, discovery propagation, validation, and closure
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `M28.2.1` | `M` | Register plan-validate-render in shared asset registry and propagate discovery metadata | done | Add the plan-validate-render skill entry to shared-assets.yaml (kind skill, version 0.1.0, six-runtime compatibility). Add a row to the available-skills table in AGENTS.md and in repo-AGENTS.md.template. Check off the plan-validate-render entry in TODO.md. |
| `T28.2.2` | `T` | Validate plan-validate-render skill packaging, registry, and plan consistency | done |  |
| `C28.2.3` | `C` | Checkpoint closure — X28 plan-validate-render skill packaging | done |  |

### X29

- ID: `X29`
- Title: Portability and Governance Enforcement Bugfixes
- Status: done
- Note: Fix the validate-plan.py schema-validation fallback, remove remaining non-portable interpreter assumptions from active docs and tooling, add the canonical no-AI-traces hard rule plus matching workflow enforcement, and align bootstrap, hooks, and docs around local pre-push protection for governed repositories.

#### S29.1 Items

Sprint: Sprint 1 — Tracking and governance propagation
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D29.1.1` | `D` | Add X29 tracking to PLAN.yaml and regenerate plan views | done | Introduce milestone X29, its sprints, executable items, and commit-group boundaries. Regenerate PLAN.md and PLAN.dot so the generated views remain derived from the canonical plan source. |
| `D29.1.2` | `D` | Add the canonical no-AI-traces hard rule and propagate AGENTS materializations | done | Add a single canonical hard rule forbidding signatures, trailers, comments, PR text, or other traces attributable to generative AI or code generation. Propagate it only through AGENTS materialization surfaces. |
| `D29.1.3` | `D` | Extend Git Flow policy and skills with no-AI-traces workflow enforcement | done | Add explicit workflow-level prohibitions and cleanliness checks for AI/codegen attribution markers across commits, PR titles and bodies, PR comments, PR reviews, and proposed commit messages. |
| `D29.1.4` | `D` | Restore the minimal gitflow-pr-only cleanliness guidance without rewriting the evaluated baseline | done | Re-apply only the X29 workflow content cleanliness sub-procedure and the required action hooks in gitflow-pr-only after restoring the develop baseline. Preserve the Claude Code section and the existing normative structure unless a direct conflict requires otherwise. |
| `C29.1.5` | `C` | Checkpoint closure — X29 minimal gitflow-pr-only cleanliness restoration | done |  |

#### S29.2 Items

Sprint: Sprint 2 — Tooling, hooks, portability, and validation
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `F29.2.1` | `F` | Fix validate-plan.py fallback when jsonschema is unavailable | done | Route schema validation through a helper that uses jsonschema when available and the existing subset fallback when it is not, preserving readable failures and non-zero exit codes without crashing. |
| `F29.2.2` | `F` | Normalize interpreter portability across .env, docs, Codex entrypoints, and run-gates.sh | done | Standardize active repo-tracked instructions on AGENT_PYTHON from .env, make the tracked default generic, and keep Codex sandbox guidance thin and non-host-specific. |
| `F29.2.3` | `F` | Add pre-push protection and extend hook/bootstrap enforcement for banned AI attribution markers | done | Keep direct-push protection for main and develop, bootstrap both hooks, and reject narrow AI/codegen attribution markers in commit-message and pushed-text enforcement without blocking legitimate human co-author trailers. |
| `T29.2.4` | `T` | Validate portability, hook behavior, validator fallback, bootstrap outputs, and gates | done |  |
| `C29.2.5` | `C` | Checkpoint closure — X29 portability and governance enforcement bugfixes | done |  |

### X30

- ID: `X30`
- Title: TODO Roadmap Expansion
- Status: done
- Note: Expand the non-authoritative TODO.md checklist from a compact feature summary into a broader human-facing roadmap and architectural checklist. Keep it explicitly non-normative and avoid duplicating canonical governance, architecture, or execution-plan authorities.

#### S30.1 Items

Sprint: Sprint 1 — TODO.md roadmap rewrite
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D30.1.1` | `D` | Expand TODO.md into a broader human-facing roadmap and architectural checklist | done | Rewrite TODO.md so it remains a concise personal checklist while expanding plan-scaling, runtime, live-tracking, continuity, routing, integration, observability, issue-intake, validation, and context-economy coverage. Keep it non-normative and avoid repeating canonical rules from AGENTS.md, ARCHITECTURE.md, PLAN.yaml, or the workflow authorities. |

### X31

- ID: `X31`
- Title: PLAN Splitting and Archival Foundation
- Status: done
- Note: Split the monolithic repo plan into a canonical plan/ entrypoint with active and archived fragments, keep aggregate validation and rendering deterministic, and propagate the new plan layout through Layer-0 tooling, skills, templates, and bootstrap flows. Sprint 3 reopens X31 to harden the split-plan runtime, remove legacy aggregate support from shared Python tooling, and bring the governed Python surface to warning-strict green gates with >95% per-file coverage for agent-os/scripts/. Sprint 4 reopens X31 one final time to harden deterministic closure behavior so the canonical generated plan views stay clean, consistent, and review-ready after the full gate path.

#### S31.1 Items

Sprint: Sprint 1 — Split model, migration, and bootstrap foundation
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D31.1.1` | `D` | Track X31 in the legacy root plan and reserve the feature branch before split migration | done | Reserve feature/X31-plan-splitting-archival for the milestone, add both X31 sprints and commit groups to the legacy root PLAN.yaml before any non-generated edits, and record the one-time migration rule: cg63 is the last commit tracked in the root PLAN.yaml before the canonical entrypoint moves to plan/PLAN-index.yaml in cg64. |
| `M31.1.2` | `M` | Add split-plan schemas, shared loader, and deterministic split-plan migration tooling | done | Introduce the split plan storage model, migrate this repository from the legacy monolithic root PLAN.yaml into plan/PLAN-index.yaml plus plan fragments, and keep aggregate render output deterministic and reviewable. |
| `T31.1.3` | `T` | Prove split migration preserves the aggregate logical plan and rendered views | done |  |
| `C31.1.4` | `C` | Checkpoint closure — X31 split-plan model and migration foundation | done |  |

#### S31.2 Items

Sprint: Sprint 2 — Aggregate tooling, archival automation, and propagation
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `M31.2.1` | `M` | Refactor validate-plan.py onto the shared split-plan loader with active and archived reporting | done | Keep aggregate governance enforcement intact while teaching validation to load plan/PLAN-index.yaml and report separate Active and Archived blocks. |
| `M31.2.2` | `M` | Refactor render-plan.py onto the shared split-plan loader without changing aggregate output shape | done |  |
| `M31.2.3` | `M` | Add deterministic archive-plan automation and wire milestone archival into the git-flow path | done | Archive a milestone only after its final checkpoint commit group is complete and before the milestone branch is synchronized for PR merge. |
| `F31.2.4` | `F` | Propagate the split-plan entrypoint through docs, templates, bootstrap, and runtime adapters | done | Update only the canonical path and split-plan workflow surfaces that must change, and keep non-authoritative or previously Claude-shaped skill text edits as small as possible. |
| `T31.2.5` | `T` | Extend automated coverage for split loading, migration, archival, rendering, validation, and bootstrap | done |  |
| `C31.2.6` | `C` | Checkpoint closure — X31 split-plan archival and propagation | done |  |

#### S31.3 Items

Sprint: Sprint 3 — Warning-strict gates and script coverage hardening
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D31.3.1` | `D` | Reopen X31 and record the split-only, warning-strict coverage hardening decisions | done | Sprint 3 keeps the existing feature branch, applies the >95% per-file coverage target to agent-os/scripts/*.py only, treats Python/test warnings as failures, and removes legacy aggregate PLAN.yaml runtime support from shared Python tooling while keeping split-plan.py as the one-time migration entrypoint. |
| `M31.3.2` | `M` | Make the Python gate runnable, warning-strict, and coverage-enforced for agent-os/scripts | done | Wire pytest, pytest-cov, branch coverage reporting, warning-as-error handling, and deterministic per-file coverage enforcement into the canonical Python gate for the governed script surface. |
| `M31.3.3` | `M` | Remove legacy aggregate PLAN.yaml runtime support from shared Python tooling | done | Shared Python runtime tooling becomes split-plan-only. split-plan.py remains the explicit legacy migration path; no compatibility shims or aggregate runtime fallbacks remain. |
| `T31.3.4` | `T` | Add high-signal hardening coverage for plan_loader.py, split-plan.py, and archive-plan.py | done |  |
| `M31.3.5` | `M` | Fix runtime defects exposed by loader, split, and archive hardening tests | done |  |
| `T31.3.6` | `T` | Add high-signal hardening coverage for validate-plan.py, render-plan.py, and resolve-shared-asset.py | done |  |
| `M31.3.7` | `M` | Fix runtime defects exposed by validate, render, and asset-resolution hardening tests | done |  |
| `C31.3.8` | `C` | Checkpoint closure — X31 warning-strict coverage hardening | done |  |

#### S31.4 Items

Sprint: Sprint 4 — Final closure audit and consistency cleanup
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D31.4.1` | `D` | Reopen X31 for a final closure audit and record deterministic cleanup acceptance criteria | done | Sprint 4 is closure remediation only. Acceptance requires deterministic test and gate execution, canonical PLAN.md and PLAN.dot outputs sourced from plan/PLAN-index.yaml, zero Python warnings, and a clean worktree immediately after the full closure path. |
| `T31.4.2` | `T` | Add closure-audit regression coverage for deterministic generated-view isolation | done |  |
| `M31.4.3` | `M` | Fix final closure drift, consistency gaps, and deterministic generated-view behavior | done | Keep public behavior unchanged while ensuring closure-gate execution leaves the canonical split-plan source, generated views, and tracked metadata fully aligned and review-clean. |
| `C31.4.4` | `C` | Checkpoint closure — X31 final closure audit and consistency cleanup | done |  |

### X33

- ID: `X33`
- Title: Issue #8 Review Response and TODO Roadmap Integration
- Status: done
- Note: Respond to Gianni Massi's code review (issue #8) with a deep technical analysis, integrate actionable suggestions into the TODO roadmap with per-section priorities, and consistency-check the result.

#### S33.1 Items

Sprint: Sprint 1 — Issue reply, TODO integration, consistency check
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D33.1.1` | `D` | Track X33 milestone in PLAN-current.yaml and regenerate plan views | done |  |
| `D33.1.2` | `D` | Reply to issue | done | GitHub issue comment only. No file changes. |
| `D33.1.3` | `D` | Integrate review suggestions into TODO.md with section priorities | done |  |
| `D33.1.4` | `D` | Consistency-check TODO.md against codebase state and fix drift | done |  |
| `C33.1.5` | `C` | Checkpoint closure — X33 | done |  |
| `F33.1.6` | `F` | Fix hardcoded milestone/item IDs in archive and validate tests | done | Tests hardcode X31 and item IDs like C31.2.6 and M31.2.3 from the old PLAN-current.yaml. Since copy_split_plan copies the live plan/ directory, the tests break whenever the active milestone changes. Fix by discovering milestone and item IDs dynamically. |

### X34

- ID: `X34`
- Title: Make plan tests independent from active PLAN-current state
- Status: done
- Note: Tests crash with IndexError when PLAN-current.yaml is empty after archival. Root cause: copy_split_plan copies live plan/ directory and tests assume non-empty active content. Fix by injecting synthetic fixture data so tests are self-contained. Closes #25.

#### S34.1 Items

Sprint: Sprint 1 — Self-contained test fixtures and empty-state coverage
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D34.1.1` | `D` | Track X34 milestone and regenerate plan views | done |  |
| `F34.1.2` | `F` | Add synthetic fixture helper and fix archive tests for empty-state | done | Add a synthetic_current_fragment() helper to conftest that builds a minimal valid PLAN-current.yaml fixture. Replace active_milestone_id() with inject_synthetic_fragment() so tests never depend on live data. Add explicit empty-state test for archive-plan behavior. |
| `F34.1.3` | `F` | Fix validate tests for empty-state | done | Fix the two validate tests that index into empty items lists. Use synthetic fixture data injected into the copied plan. |
| `T34.1.4` | `T` | Verify tests pass in both empty and non-empty PLAN-current states | done |  |
| `C34.1.5` | `C` | Checkpoint closure — X34 | done |  |

### X35

- ID: `X35`
- Title: YAML hash-quoting guard and data repair
- Status: done
- Note: Prevent data truncation caused by unquoted # in YAML plain scalars. Add a raw-text pre-load lint to validate-plan.py, repair truncated titles in PLAN-X33.yaml and PLAN-index.yaml, and add regression tests. Closes #21.

#### S35.1 Items

Sprint: Sprint 1 — Lint guard, data repair, regression tests
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D35.1.1` | `D` | Track X35 milestone and regenerate plan views | done |  |
| `F35.1.2` | `F` | Repair truncated title in PLAN-X33.yaml and PLAN-index.yaml | done |  |
| `F35.1.3` | `F` | Add raw-text unquoted-hash lint to validate-plan.py | done |  |
| `T35.1.4` | `T` | Regression tests for hash-in-title lint and round-trip | done |  |
| `C35.1.5` | `C` | Checkpoint closure — X35 | done |  |

### X36

- ID: `X36`
- Title: Add compute-ready readiness query to validate-plan.py
- Status: done
- Note: Add a read-only `--compute-ready` query to the plan validator so operators can inspect the current ready-set without mutating plan state. Covers implementation, tests, docs, and checkpoint closure for issue #11.

#### S36.1 Items

Sprint: Sprint 1 — Tracking, ready-set query, tests, docs
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D36.1.1` | `D` | Track X36 active work and keep generated plan views in sync | done |  |
| `M36.1.2` | `M` | Add --compute-ready query to validate-plan.py | done | Compute the ready-set from existing dependency semantics and emit a deterministic JSON payload without changing default validation behavior. |
| `T36.1.3` | `T` | Add compute-ready helper and CLI regression coverage | done |  |
| `D36.1.4` | `D` | Document compute-ready CLI usage in README | done |  |
| `C36.1.5` | `C` | Checkpoint closure — X36 | done |  |

### X37

- ID: `X37`
- Title: X36 gate repair and archival
- Status: done
- Note: Verify and repair any formatter drift introduced by the X36 branch, rerun the quality gates, then archive the closed X36 milestone into plan/archive and refresh generated plan views.

#### S37.1 Items

Sprint: Sprint 1 — Gate repair, validation, archive X36
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D37.1.1` | `D` | Track X37 follow-up work and keep generated plan views in sync | done |  |
| `F37.1.2` | `F` | Repair formatter drift in the X36 branch diff | done | Limit formatting changes to files that are actually part of the branch diff unless verification shows additional branch-owned files need repair. |
| `T37.1.3` | `T` | Re-run format-sensitive gates for the X36 branch | done |  |
| `D37.1.4` | `D` | Archive the closed X36 milestone into plan/archive | done |  |
| `C37.1.5` | `C` | Checkpoint closure — X37 | done |  |

### X38

- ID: `X38`
- Title: Kilo Entrypoint Migration (.kilocode → .kilo)
- Status: done
- Note: Migrate all .kilocode references to .kilo, create thin .kilo/rules/governance.md entrypoint, update bootstrap template, and verify tests pass.

#### S38.1 Items

Sprint: Sprint 1 — Migration Implementation
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D38.1.1` | `D` | Archive X37 milestone and update PLAN-index | done |  |
| `D38.1.2` | `D` | Create X38 milestone for Kilo migration | done |  |
| `F38.1.3` | `F` | Replace all .kilocode text references with .kilo | done | 23 occurrences across 12 files. Single sed pass. Skip generated and archived files. |
| `F38.1.4` | `F` | Create .kilo/rules/governance.md thin entrypoint | done | Follow thin adapter pattern from CLAUDE.md and .codex. No duplication of governance rules. |
| `F38.1.5` | `F` | Update bootstrap template for .kilo path | done | Update output path from .kilocode to .kilo in bootstrap-repo.sh render_template call. |
| `T38.1.6` | `T` | Verify text replacements with grep | done |  |
| `T38.1.7` | `T` | Run validation gates | done |  |
| `C38.1.8` | `C` | Checkpoint closure — X38 | done |  |

#### S38.2 Items

Sprint: Sprint 2 — Maintenance
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `F38.2.1` | `F` | Merge .kilo/.gitignore into repo .gitignore | done | Consolidate Kilo CLI ignores into repo .gitignore. Plan authority remains in plan/ only. |
| `C38.2.2` | `C` | Checkpoint closure — X38 final | done |  |

### X39

- ID: `X39`
- Title: Workspace Sync Skill Packaging
- Status: done
- Note: Package sync-workspace.sh as a portable workspace-sync skill under agent-os/skills/. Add pre-flight validation, provenance drift detection, and structured reporting. Register in the shared asset registry and propagate discovery to AGENTS.md and the repo template.

#### S39.1 Items

Sprint: Sprint 1 -- Skill definition, registry, and discovery propagation
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D39.1.1` | `D` | Create workspace-sync skill SKILL.md with pre-flight, execution, drift detection, and reporting | done |  |
| `M39.1.2` | `M` | Register workspace-sync in shared asset registry and propagate discovery metadata | done |  |
| `T39.1.3` | `T` | Validate workspace-sync skill packaging, registry, and plan consistency | done |  |
| `C39.1.4` | `C` | Checkpoint closure -- X39 workspace-sync skill packaging | done |  |

#### S39.2 Items

Sprint: Sprint 2 -- Skill evaluation, testing, and iteration
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `T39.2.1` | `T` | Run skill evaluation with 4 test prompts and baseline comparison | done |  |
| `M39.2.2` | `M` | Iterate on SKILL.md based on evaluation feedback | done |  |
| `T39.2.3` | `T` | Re-validate skill after iteration and confirm gates pass | done |  |
| `C39.2.4` | `C` | Checkpoint closure -- S39.2 skill evaluation and iteration | done |  |

### X40

- ID: `X40`
- Title: Structured Checks for Programmatic Verification
- Status: done
- Note: Implement mixed prose and structured PLAN item checks for issue #13. Structured checks are validated as metadata only and are not executed by validate-plan.py.

#### S40.1 Items

Sprint: Sprint 1 -- Schema, validator, docs, and validation
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D40.1.1` | `D` | Create X40 tracking plan and commit groups | done |  |
| `M40.1.2` | `M` | Add structured checks to schema and validator fallback | done |  |
| `T40.1.3` | `T` | Add structured check validation test coverage | done |  |
| `D40.1.4` | `D` | Document structured checks and update roadmap state | done |  |
| `T40.1.5` | `T` | Validate X40 structured checks feature | done |  |
| `C40.1.6` | `C` | Checkpoint closure -- X40 structured checks | done |  |

### X41

- ID: `X41`
- Title: Issue and TODO Reconciliation Cleanup
- Status: done
- Note: Reconcile stale post-merge state after PR #32: close the completed structured checks issue and correct the human TODO checklist for already-implemented compute-ready support.

#### S41.1 Items

Sprint: Sprint 1 -- Tracking, reconciliation, validation, and closure
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D41.1.1` | `D` | Create X41 reconciliation tracking plan | done |  |
| `F41.1.2` | `F` | Reconcile stale issue and TODO checklist state | done | Close stale issue #13 externally after verifying PR #32 merged structured checks, and mark the already-implemented compute-ready TODO item as complete. |
| `T41.1.3` | `T` | Verify reconciliation state | done |  |
| `C41.1.4` | `C` | Checkpoint closure -- X41 reconciliation cleanup | done |  |

### X42

- ID: `X42`
- Title: Declarative on_fail Policy Metadata
- Status: done
- Note: Implement optional PLAN item on_fail failure-policy metadata for issue #12. The field is declarative only; runtime retry, pivot dispatch, and worker behavior remain out of scope.

#### S42.1 Items

Sprint: Sprint 1 -- Schema, validator, docs, and closure
Status: done

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D42.1.1` | `D` | Open X42 tracking plan and commit groups | done |  |
| `M42.1.2` | `M` | Add on_fail schema, validator fallback, renderer, and tests | done |  |
| `D42.1.3` | `D` | Document on_fail policy metadata and update roadmap state | done |  |
| `C42.1.4` | `C` | Checkpoint closure -- X42 on_fail policy metadata | done |  |

### X43

- ID: `X43`
- Title: Dangling on_fail Pivot Warning
- Status: in_progress
- Note: Add warning-only validation for on_fail pivot targets that parse as item IDs but do not exist in the loaded plan. This is a root correction after X42 archival, not a legacy workaround.

#### S43.1 Items

Sprint: Sprint 1 -- Validator warning, docs, tests, and closure
Status: in_progress

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D43.1.1` | `D` | Open X43 tracking plan and commit groups | done |  |
| `M43.1.2` | `M` | Warn on dangling on_fail pivot targets | planned |  |
| `D43.1.3` | `D` | Document dangling pivot warning semantics | planned |  |
| `C43.1.4` | `C` | Checkpoint closure -- X43 dangling pivot warning | planned |  |

## Commit Groups

| ID | Title | Items |
|---|---|---|
| cg0 | Repository bootstrap hygiene | `D1.1.1` |
| cg1 | Review and planning artifacts | `D1.1.2` |
| cg2 | Decision gates — Q1.1.1 through Q1.1.5 answers recorded | `Q1.1.1`, `Q1.1.2`, `Q1.1.3`, `Q1.1.4`, `Q1.1.5` |
| cg3 | Scaffold — workflow docs, schema, templates | `M1.1.1`, `M1.1.2`, `M1.1.3`, `M1.1.6` |
| cg4 | Scripts — render, validate, bootstrap, sync | `M1.1.4`, `M1.1.5` |
| cg5 | Sprint 1 closure — tests and checkpoint | `T1.1.1`, `T1.1.2`, `T1.1.3`, `C1.1.1` |
| cg6 | Governance hardening updates | `D1.1.3`, `D1.1.4` |
| cg7 | Governance compliance — propagate architectural rules to workflow docs | `D2.1.1`, `D2.1.2`, `D2.1.3` |
| cg8 | Architecture finalization — close specification gaps G1-G5 | `D2.1.4`, `D2.1.5`, `D2.1.6`, `D2.1.7`, `D2.1.8`, `C2.1.1` |
| cg9 | Source-of-truth integrity and schema hardening | `F3.1.1`, `M3.1.2`, `D3.1.3`, `T3.1.4` |
| cg10 | Validation tooling hardening — cycle detection, commit group coherence, type/action warnings | `M3.2.1`, `M3.2.2`, `M3.2.3`, `T3.2.4`, `C3.2.5` |
| cg11 | Rendering, bootstrap, and workspace template improvements | `M3.3.1`, `M3.3.2`, `M3.3.3`, `M3.3.4`, `M3.3.5`, `T3.3.6` |
| cg12 | Documentation, operational guardrails, and milestone closure | `D3.4.1`, `D3.4.2`, `D3.4.3`, `M3.4.4`, `T3.4.5`, `C3.4.6` |
| cg13 | Language enforcement — tighten soft language to hard gates | `M4.1.1`, `M4.1.2`, `T4.1.3` |
| cg14 | Closure criteria and freshness hard gate alignment | `M4.2.1`, `M4.2.2`, `T4.2.3` |
| cg15 | Schema and taxonomy hardening — depends_on, scope, checks, decision | `M4.3.1`, `M4.3.2`, `M4.3.3`, `M4.3.4`, `T4.3.5` |
| cg16 | Lifecycle unification and deferred field markers | `D4.4.1`, `D4.4.2`, `D4.4.3`, `T4.4.4` |
| cg17 | Commit format, phase-gate enforcement, and milestone closure | `D4.5.1`, `M4.5.2`, `D4.5.3`, `M4.5.4`, `M4.5.5`, `T4.5.6`, `C4.5.7` |
| cg18 | Validator hardening — enforce executable item commit_group presence | `M4.6.1`, `T4.6.2`, `C4.6.3` |
| cg19 | Commit tooling hardening — hook enforcement and runtime wording alignment | `M4.7.1`, `D4.7.2`, `D4.7.3`, `T4.7.4`, `C4.7.5` |
| cg20 | Governance hardening — tracking-first execution and exact commit_group traceability | `D5.1.1`, `D5.1.2`, `C5.1.3` |
| cg21 | Cross-layer consistency repairs — templates, hook/bootstrap enforcement, local provenance, and tooling bootstrap | `D5.2.1`, `M5.2.2`, `M5.2.3`, `T5.2.4`, `C5.2.5` |
| cg22 | Planning model clarification — execution optimization, aggregation, and controlled parallelization | `D6.1.1`, `T6.1.2`, `C6.1.3` |
| cg23 | Skill packaging — checkpoint closure skill and workspace topology documentation | `D7.1.1`, `D7.1.2`, `T7.1.3`, `C7.1.4` |
| cg24 | Adapter layer — CLAUDE.md as thin governance pointer | `D8.1.1` |
| cg25 | Repo hygiene — gitignore patterns for eval workspaces and caches | `F8.1.2`, `C8.1.3` |
| cg26 | Shared assets — registry, PLAN references, two-root resolution, vendoring, and seed runtime assets | `D9.1.1`, `M9.1.2`, `M9.1.3`, `T9.1.4`, `C9.1.5` |
| cg27 | Testing and gates — pytest coverage, tooling config, and local quality runner | `D10.1.1`, `M10.1.2`, `M10.1.3`, `T10.1.4`, `C10.1.5` |
| cg28 | Portability model — runtime lifecycle design and Copilot deferral | `D11.1.1` |
| cg29 | Codex adapter — populate .codex with thin adapter content | `M11.1.2` |
| cg30 | Kilo experimental — adapter, profile, registry, and gitignore | `M11.1.3` |
| cg31 | Verification and checkpoint — validate portability expansion and close X11 | `T11.1.4`, `C11.1.5` |
| cg32 | Codex first-class — workspace template, sync extension, tier promotion | `M12.1.1`, `T12.1.2`, `C12.1.3` |
| cg33 | Template parity fix — CLAUDE workspace adapter overrides and test expansion | `F13.1.1`, `F13.1.2`, `C13.1.3` |
| cg34 | Portability completion tracking — milestone, runtime contract, and commit boundaries | `D14.1.1` |
| cg35 | Portability implementation — Copilot support and Kilo realignment | `M14.1.2` |
| cg36 | Portability verification and closure — validate X14 end to end | `T14.1.3`, `C14.1.4` |
| cg37 | Environment portability — AGENT_PYTHON env var and .env.example | `M15.1.1`, `T15.1.2`, `C15.1.3` |
| cg38 | Add non-normative TODO.md checklist | `D16.1.1` |
| cg39 | TODO wording fix — NFC to RFC | `D16.1.2` |
| cg40 | Design docs — add English peer translation for the Git Flow PR-only workflow | `D17.1.1`, `T17.1.2`, `C17.1.3` |
| cg41 | Design doc update — conflict resolution scenarios and operational refinements | `D18.1.1` |
| cg42 | Git Flow governance extraction and authority registration | `D19.1.1`, `D19.1.2`, `C19.1.3` |
| cg43 | gitflow-pr-only skill implementation | `D20.1.1`, `C20.1.2` |
| cg44 | Skill discovery table in AGENTS.md | `D21.1.1`, `C21.1.2` |
| cg45 | Planning-to-git mapping and branch naming convention | `D22.1.1`, `D22.1.2`, `C22.1.3` |
| cg46 | Git Flow skill portability repairs — registry, contract, and template propagation | `M23.1.1`, `T23.1.2`, `C23.1.3` |
| cg47 | TODO checklist refresh for recent Git Flow work | `D24.1.1` |
| cg48 | Runtime parity governance update and bootstrap templates | `D25.1.1`, `M25.1.2`, `M25.1.3`, `M25.1.4`, `M25.1.5` |
| cg49 | Tooling integration and profile updates for first-class promotion | `M25.2.1`, `M25.2.2`, `D25.2.3` |
| cg50 | Validation and milestone closure for X25 | `T25.2.4`, `C25.2.5` |
| cg51 | Gemini/Cursor portability governance update and bootstrap templates | `D26.1.1`, `M26.1.2`, `M26.1.3` |
| cg52 | Gemini/Cursor tooling integration and runtime compatibility updates | `M26.2.1`, `M26.2.2`, `D26.2.3` |
| cg53 | Gemini/Cursor portability validation and milestone closure | `M26.2.6`, `T26.2.4`, `C26.2.5` |
| cg54 | Repo bootstrap skill — SKILL.md, registry entry, and discovery propagation | `D27.1.1`, `M27.1.2`, `T27.1.3`, `C27.1.4` |
| cg55 | Plan validate-render skill — SKILL.md authoring | `D28.1.1` |
| cg56 | Plan validate-render skill — registry, discovery, validation, and closure | `M28.2.1`, `T28.2.2`, `C28.2.3` |
| cg57 | X29 plan tracking and generated plan views | `D29.1.1` |
| cg58 | Canonical no-AI-traces rule and Git Flow workflow propagation | `D29.1.2`, `D29.1.3` |
| cg59 | Validator fallback and interpreter portability repairs | `F29.2.1`, `F29.2.2` |
| cg60 | Hook, bootstrap, validation, and closure repairs for X29 | `F29.2.3`, `T29.2.4`, `C29.2.5` |
| cg61 | X29 refinement — minimal gitflow-pr-only cleanliness restoration | `D29.1.4`, `C29.1.5` |
| cg62 | TODO roadmap expansion | `D30.1.1` |
| cg63 | X31 tracking bootstrap on the reserved feature branch | `D31.1.1` |
| cg64 | Split-plan model, loader, migration tooling, and repository self-migration | `M31.1.2`, `T31.1.3`, `C31.1.4` |
| cg65 | Aggregate validator and renderer split-plan loader refactor | `M31.2.1`, `M31.2.2` |
| cg66 | Archival automation and split-plan propagation | `M31.2.3`, `F31.2.4` |
| cg67 | Split-plan validation matrix and X31 closure | `T31.2.5`, `C31.2.6` |
| cg68 | X31 sprint-3 tracking bootstrap | `D31.3.1` |
| cg69 | Warning-strict Python gate and split-only runtime contract | `M31.3.2`, `M31.3.3` |
| cg70 | Loader, split, and archive hardening loop | `T31.3.4`, `M31.3.5` |
| cg71 | Validate, render, and asset-resolution hardening loop | `T31.3.6`, `M31.3.7` |
| cg72 | Warning-strict gate closure for X31 sprint 3 | `C31.3.8` |
| cg73 | X31 sprint-4 closure audit bootstrap | `D31.4.1` |
| cg74 | Deterministic generated-view isolation and closure consistency remediation | `T31.4.2`, `M31.4.3` |
| cg75 | X31 final closure audit and checkpoint | `C31.4.4` |
| cg78 | X33 tracking bootstrap | `D33.1.1` |
| cg79 | Issue reply and TODO integration | `D33.1.2`, `D33.1.3`, `D33.1.4` |
| cg80 | X33 checkpoint closure | `C33.1.5` |
| cg81 | Fix hardcoded test IDs | `F33.1.6` |
| cg82 | X34 tracking bootstrap | `D34.1.1` |
| cg83 | Self-contained test fixtures and empty-state coverage | `F34.1.2`, `F34.1.3`, `T34.1.4` |
| cg84 | X34 checkpoint closure | `C34.1.5` |
| cg85 | X35 tracking bootstrap | `D35.1.1` |
| cg86 | YAML hash-quoting lint and data repair | `F35.1.2`, `F35.1.3`, `T35.1.4` |
| cg87 | X35 checkpoint closure | `C35.1.5` |
| cg88 | Compute-ready query, tests, and documentation | `D36.1.1`, `M36.1.2`, `T36.1.3`, `D36.1.4` |
| cg89 | X36 checkpoint closure | `C36.1.5` |
| cg90 | X36 gate repair and gate verification | `D37.1.1`, `F37.1.2`, `T37.1.3` |
| cg91 | Archive the closed X36 milestone | `D37.1.4` |
| cg92 | X37 checkpoint closure | `C37.1.5` |
| cg93 | Archive X37, create X38 milestone | `D38.1.1`, `D38.1.2` |
| cg94 | Text replacements and new .kilo entrypoint | `F38.1.3`, `F38.1.4`, `F38.1.5` |
| cg95 | Verification and test gates | `T38.1.6`, `T38.1.7` |
| cg96 | X38 checkpoint closure | `C38.1.8` |
| cg97 | Merge .kilo/.gitignore into repo | `F38.2.1` |
| cg98 | Archive X38 and close feature | `C38.2.2` |
| cg99 | Workspace sync skill -- SKILL.md authoring | `D39.1.1` |
| cg100 | Workspace sync skill -- registry, discovery, validation, and closure | `M39.1.2`, `T39.1.3`, `C39.1.4` |
| cg101 | Workspace sync skill -- evaluation, iteration, and closure | `T39.2.1`, `M39.2.2`, `T39.2.3`, `C39.2.4` |
| cg102 | Structured checks -- tracking plan | `D40.1.1` |
| cg103 | Structured checks -- schema, validator, and tests | `M40.1.2`, `T40.1.3` |
| cg104 | Structured checks -- docs, TODO, validation, and closure | `D40.1.4`, `T40.1.5`, `C40.1.6` |
| cg105 | X41 reconciliation tracking | `D41.1.1` |
| cg106 | Issue and TODO reconciliation | `F41.1.2`, `T41.1.3` |
| cg107 | X41 checkpoint closure and archive | `C41.1.4` |
| cg108 | on_fail policy -- tracking plan | `D42.1.1` |
| cg109 | on_fail policy -- schema, validation, docs, and tests | `M42.1.2`, `D42.1.3` |
| cg110 | on_fail policy -- validation and closure | `C42.1.4` |
| cg111 | dangling pivot warning -- tracking plan | `D43.1.1` |
| cg112 | dangling pivot warning -- validator, docs, and tests | `M43.1.2`, `D43.1.3` |
| cg113 | dangling pivot warning -- validation and closure | `C43.1.4` |

## Item Details

### C1.1.1: Sprint 1 checkpoint — Level-0 scaffold complete and self-validating

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: review, checkpoint, verify
- **Depends on**: `T1.1.1`, `T1.1.2`, `T1.1.3`
- **Commit group**: `cg5`
- **Checks**:
  - All S1.1 items are status: verified or done
  - PLAN.md and PLAN.dot are committed and match PLAN.yaml
  - No concern duplication detected (AGENTS vs ARCHITECTURE vs PLAN)
  - agent-os/ directory structure matches §15.1 of architecture doc
  - Each template file includes canonical source rule header
  - Commit messages follow: <type>(<scope>): <description>
  - validate-plan.py passes on this PLAN.yaml
- **Notes**: After this checkpoint, the control plane is operational and able to bootstrap its first real target repo (Level-2) as Sprint 2 work.

### D1.1.1: Create non-authoritative docs directory and initialize .gitignore

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: document
- **Commit group**: `cg0`
- **Artifacts**: .gitignore, docs/design/documento-architetturale-control-plane-coding-agents.md, docs/design/gitflow_pr_only_terminal_workflow.md, docs/design/REVIEW-AND-OPEN-QUESTIONS.md
- **Notes**: Moved startup documentation to docs/design/ as non-authoritative reference material and added baseline ignore rules for local/editor/runtime artifacts.

### M1.1.1: Create agent-os/workflow/ documentation files

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S1.1`
- **Actions**: implement, document
- **Depends on**: `Q1.1.1`, `Q1.1.2`, `Q1.1.3`
- **Commit group**: `cg3`
- **Artifacts**: agent-os/workflow/shared-workflow.md, agent-os/workflow/item-taxonomy.md, agent-os/workflow/lifecycle.md, agent-os/workflow/git-automation-policy.md, agent-os/workflow/portability-model.md
- **Notes**: Content sourced from docs/design/documento-architetturale-control-plane-coding-agents.md and docs/design/gitflow_pr_only_terminal_workflow.md. Do NOT duplicate content; these files are the canonical split of the monolithic architecture doc.

### Q1.1.1: Decide: PLAN.yaml required fields and state transition rules

- **Type**: Q | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: decide
- **Depends on**: `D1.1.2`
- **Commit group**: `cg2`
- **Decision**: Required executable fields are id, type, title, status, role, effort. State machine is planned -> ready -> in_progress -> review -> verified -> done, with blocked as a side-state reachable from active states. Container items (X, S) must not appear in depends_on. verified means all required checks pass; done means verified plus repository bookkeeping closure (committed, optionally pushed).
- **Notes**: Decision recorded from interactive governance alignment.

### T1.1.1: Validate this PLAN.yaml against plan.schema.json

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: test, verify
- **Depends on**: `M1.1.2`, `M1.1.4`
- **Commit group**: `cg5`
- **Checks**:
  - python agent-os/scripts/validate-plan.py PLAN.yaml exits 0
  - no required fields missing
  - no dangling depends_on references
- **Notes**: This is the self-validation gate: the control plane must validate its own plan before it can claim to be a working control plane.

### D1.1.2: Create architecture review and open-questions document

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: document
- **Commit group**: `cg1`
- **Artifacts**: docs/design/REVIEW-AND-OPEN-QUESTIONS.md
- **Notes**: Captures what is confirmed, what is ambiguous, and five open questions (Q1.1.1–Q1.1.5) that must be decided before schema and scripts can be written.

### M1.1.2: Create agent-os/schemas/plan.schema.json

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S1.1`
- **Actions**: design, implement
- **Depends on**: `Q1.1.1`, `Q1.1.4`
- **Commit group**: `cg3`
- **Artifacts**: agent-os/schemas/plan.schema.json
- **Notes**: JSON Schema (draft-2020-12) for PLAN.yaml. Must encode required fields, enum values for type/status/role/effort/actions, and scope field format as decided in Q1.1.1 and Q1.1.4. Must be self-consistent so that this PLAN.yaml passes validation once M1.1.4 is done.

### Q1.1.2: Decide: Level-1 runtime materialization strategy

- **Type**: Q | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: decide
- **Depends on**: `D1.1.2`
- **Commit group**: `cg2`
- **Decision**: Level-1 runtime files are fully generated by sync-workspace.sh from Level-0 templates. Generated files are read-only outputs and must include an AUTO-GENERATED header.
- **Notes**: Decision recorded from interactive governance alignment.

### T1.1.2: Dry-run bootstrap-repo.sh on a temp path

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: test, verify
- **Depends on**: `M1.1.5`
- **Commit group**: `cg5`
- **Checks**:
  - bash agent-os/scripts/bootstrap-repo.sh --dry-run /tmp/test-repo exits 0
  - expected output files listed without being created
- **Notes**: Must confirm bootstrap is idempotent and does not write to disk in dry-run mode. A second run on the same target must produce identical output.

### D1.1.3: Enforce commit message contract in Layer-0 governance

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: document, checkpoint
- **Commit group**: `cg6`
- **Artifacts**: AGENTS.md, agent-os/workflow/shared-workflow.md, agent-os/workflow/git-automation-policy.md, agent-os/templates/repo-AGENTS.md.template
- **Notes**: Added mandatory commit title contract: <type>(<scope>): <description> with optional body/footer sections. This is a Layer-0 global rule.

### M1.1.3: Create agent-os/templates/ (AGENTS, ARCHITECTURE, REPO_MAP, PLAN)

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S1.1`
- **Actions**: design, implement
- **Depends on**: `Q1.1.2`, `M1.1.1`
- **Commit group**: `cg3`
- **Artifacts**: agent-os/templates/repo-AGENTS.md.template, agent-os/templates/repo-ARCHITECTURE.md.template, agent-os/templates/repo-REPO_MAP.md.template, agent-os/templates/PLAN.yaml.template
- **Notes**: Templates use {{REPO_NAME}}, {{DATE}}, {{OWNER}} placeholders. Level-1 files are generated from these templates by sync-workspace.sh (per Q1.1.2 decision). Each template must include the canonical source rule and authority map header so generated files self-document their origin.

### Q1.1.3: Decide: control-plane release and consumption model

- **Type**: Q | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: decide
- **Depends on**: `D1.1.2`
- **Commit group**: `cg2`
- **Decision**: MVP consumption tracks the control-plane main branch. Tag-based pinning will be introduced when a second external consumer is onboarded.
- **Notes**: Decision recorded from interactive governance alignment.

### T1.1.3: Generate PLAN.md and PLAN.dot from this PLAN.yaml

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: test, verify
- **Depends on**: `M1.1.4`
- **Commit group**: `cg5`
- **Checks**:
  - python agent-os/scripts/render-plan.py PLAN.yaml produces PLAN.md
  - python agent-os/scripts/render-plan.py PLAN.yaml produces PLAN.dot
  - running render a second time produces identical output (idempotency)
- **Notes**: PLAN.md and PLAN.dot are committed in the same commit as this PLAN.yaml update, not as separate commits (per Q1.1.5 decision).

### D1.1.4: Strengthen and align commit body/footer recommendation wording

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: document
- **Commit group**: `cg6`
- **Artifacts**: AGENTS.md, agent-os/workflow/shared-workflow.md, agent-os/workflow/git-automation-policy.md, agent-os/templates/repo-AGENTS.md.template
- **Notes**: Standardized wording to: "Optional body and footer sections are strongly suggested, especially for medium or large commits." across all authoritative governance surfaces.

### M1.1.4: Create agent-os/scripts/render-plan.py and validate-plan.py

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: high
- **Sprint**: `S1.1`
- **Actions**: implement
- **Depends on**: `M1.1.2`, `Q1.1.5`
- **Commit group**: `cg4`
- **Artifacts**: agent-os/scripts/render-plan.py, agent-os/scripts/validate-plan.py
- **Notes**: validate-plan.py: validates PLAN.yaml against plan.schema.json; checks state transition legality, dangling depends_on, container items in depends_on, required fields. Exits non-zero on any hard-fail. render-plan.py: deterministic PLAN.yaml → PLAN.md + PLAN.yaml → PLAN.dot. Both scripts must be idempotent and callable standalone.

### Q1.1.4: Decide: scope field format and collision-detection semantics

- **Type**: Q | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: decide
- **Depends on**: `D1.1.2`
- **Commit group**: `cg2`
- **Decision**: scope is a repository-relative path prefix. validate-plan.py emits a warning (not hard-fail) when two in_progress items share a scope prefix.
- **Notes**: Decision recorded from interactive governance alignment.

### M1.1.5: Create agent-os/scripts/bootstrap-repo.sh and sync-workspace.sh

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S1.1`
- **Actions**: implement
- **Depends on**: `M1.1.3`, `Q1.1.3`
- **Commit group**: `cg4`
- **Artifacts**: agent-os/scripts/bootstrap-repo.sh, agent-os/scripts/sync-workspace.sh
- **Notes**: bootstrap-repo.sh: instantiates a new repo-local layer (Level-2) from templates. Supports --dry-run. Emits a PLAN.yaml seed from the template. sync-workspace.sh: pulls latest from control plane (per Q1.1.3 decision) and regenerates Level-1 runtime files from Level-0 templates (per Q1.1.2 decision).

### Q1.1.5: Decide: tooling failure semantics and commit hygiene rules

- **Type**: Q | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: decide
- **Depends on**: `D1.1.2`
- **Commit group**: `cg2`
- **Decision**: validate-plan.py hard-fails on missing required fields, unknown enum values, dangling depends_on references, and container types (X, S) in depends_on. Other policy checks can be warnings.
- **Notes**: Decision recorded from interactive governance alignment.

### M1.1.6: Create root governance files for this Level-0 repository

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S1.1`
- **Actions**: design, implement, document
- **Depends on**: `Q1.1.1`, `Q1.1.2`, `Q1.1.3`
- **Commit group**: `cg3`
- **Artifacts**: AGENTS.md, ARCHITECTURE.md
- **Notes**: This repository is itself the Level-0 control-plane OS. Root AGENTS.md and ARCHITECTURE.md define local authority mapping and structural constraints for building and evolving agent-os/.

### C2.1.1: Architecture finalization checkpoint — close review gaps G1-G5

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S2.1`
- **Actions**: review, checkpoint, verify
- **Depends on**: `D2.1.4`, `D2.1.5`, `D2.1.6`, `D2.1.7`, `D2.1.8`
- **Commit group**: `cg8`
- **Checks**:
  - Open gaps G1-G5 are resolved or explicitly governed with final policy
  - REVIEW-AND-OPEN-QUESTIONS.md is updated from working status to closure status
  - Prompt, skill, ADR, and REPO_MAP policies are defined in canonical authorities
  - Phase B automation includes explicit safety gate for authority-conflict recovery
  - validate-plan.py passes on this PLAN.yaml
  - render-plan.py regenerates PLAN.md and PLAN.dot deterministically
- **Notes**: Marks architecture baseline as finalized for Level-0 governance, with unresolved work shifted from open questions into explicit governed policy.

### D2.1.1: Enforce missing architectural doc rules in workflow governance files

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: medium
- **Sprint**: `S2.1`
- **Actions**: document, review
- **Commit group**: `cg7`
- **Artifacts**: agent-os/workflow/shared-workflow.md, agent-os/workflow/git-automation-policy.md, agent-os/workflow/portability-model.md
- **Notes**: Close compliance gaps between the architecture doc (§6.2–6.4, §11.3–11.4, §4.2, §13.2) and the authoritative workflow files. Adds: full authority concern table, precedence rule, non-duplication rule, single-writer rule detail, grouping and collision rules, deferred automation list, and Kilo portability mapping example.

### D2.1.2: Create English translation of the Italian architectural document

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: medium
- **Sprint**: `S2.1`
- **Actions**: document
- **Commit group**: `cg7`
- **Artifacts**: docs/design/architectural-document-control-plane-coding-agents.md
- **Notes**: 1:1 English translation of docs/design/documento-architetturale-control-plane-coding-agents.md, placed in the same directory. Structural fidelity to the original is required: all sections, tables, code blocks, and math equations must be preserved verbatim in structure.

### D2.1.3: Simplify commit title contract by removing item ID from header

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S2.1`
- **Actions**: document
- **Commit group**: `cg7`
- **Artifacts**: AGENTS.md, agent-os/workflow/shared-workflow.md, agent-os/workflow/git-automation-policy.md, agent-os/templates/repo-AGENTS.md.template, PLAN.yaml
- **Notes**: Updated commit title contract everywhere from the item-ID-inclusive format to <type>(<scope>): <description> while keeping body/footer recommendation unchanged.

### D2.1.4: Define prompts directory contract and lifecycle

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: medium
- **Sprint**: `S2.1`
- **Actions**: design, document
- **Commit group**: `cg8`
- **Artifacts**: agent-os/prompts/README.md, agent-os/workflow/shared-workflow.md
- **Notes**: Closes G1 by specifying prompt file format, required metadata, versioning, and lifecycle triggers in authoritative workflow guidance.

### D2.1.5: Define skills packaging contract and compatibility mapping

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: medium
- **Sprint**: `S2.1`
- **Actions**: design, document
- **Commit group**: `cg8`
- **Artifacts**: agent-os/skills/README.md, agent-os/workflow/portability-model.md, agent-os/workflow/shared-workflow.md
- **Notes**: Closes G2 by defining a neutral skill package format and adapter mapping expectations across agent runtimes.

### D2.1.6: Define REPO_MAP freshness policy and update triggers

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S2.1`
- **Actions**: design, document
- **Commit group**: `cg8`
- **Artifacts**: agent-os/templates/repo-REPO_MAP.md.template, agent-os/workflow/shared-workflow.md, agent-os/workflow/lifecycle.md
- **Notes**: Closes G3 by defining ownership, refresh triggers, and freshness metadata for REPO_MAP.md so map staleness is detectable and reviewable.

### D2.1.7: Define ADR template, numbering, and lifecycle states

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: medium
- **Sprint**: `S2.1`
- **Actions**: design, document
- **Commit group**: `cg8`
- **Artifacts**: agent-os/templates/repo-ADR.md.template, agent-os/workflow/shared-workflow.md, agent-os/templates/repo-ARCHITECTURE.md.template
- **Notes**: Closes G4 by introducing a canonical ADR template with lifecycle states and linkage guidance to PLAN decision items.

### D2.1.8: Define canonical-authority conflict detection and recovery procedure

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: high
- **Sprint**: `S2.1`
- **Actions**: design, document, review
- **Commit group**: `cg8`
- **Artifacts**: agent-os/workflow/shared-workflow.md, ARCHITECTURE.md, AGENTS.md
- **Notes**: Closes G5 by defining conflict detection, recovery actions, escalation, and a safety gate before Phase B automation.

### F3.1.1: Fix duplicate note key in PLAN.yaml X2 milestone

- **Type**: F | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S3.1`
- **Actions**: implement, verify
- **Commit group**: `cg9`
- **Artifacts**: PLAN.yaml
- **Notes**: PLAN.yaml had two note: keys on milestone X2 (lines 35-41). YAML parsers silently override earlier values; PyYAML keeps the last. Merged both notes into a single field to preserve all content.

### M3.1.2: Add actions, parent, commit_group to schema required fields for items

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S3.1`
- **Actions**: design, implement
- **Depends on**: `F3.1.1`
- **Commit group**: `cg9`
- **Artifacts**: agent-os/schemas/plan.schema.json
- **Notes**: Changed item required from [id, type, title, status, role, effort] to [id, type, title, status, role, effort, actions, parent, commit_group]. Safe: all 28 existing items already have these fields.

### D3.1.3: Document new required fields in item-taxonomy.md

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: low
- **Sprint**: `S3.1`
- **Actions**: document
- **Depends on**: `M3.1.2`
- **Commit group**: `cg9`
- **Artifacts**: agent-os/workflow/item-taxonomy.md
- **Notes**: Split Metadata Fields section into Required Item Fields and Optional Metadata Fields. Documents that actions, parent, and commit_group are now mandatory for all executable items.

### T3.1.4: Validate PLAN.yaml against hardened schema

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S3.1`
- **Actions**: test, verify
- **Depends on**: `M3.1.2`, `F3.1.1`
- **Commit group**: `cg9`
- **Checks**:
  - python agent-os/scripts/validate-plan.py PLAN.yaml exits 0
  - No schema validation errors for any existing item
  - Duplicate note key is resolved
- **Notes**: Gate for Sprint S3.1: the hardened schema must validate the current PLAN.yaml without errors.

### M3.2.1: Implement DAG cycle detection in validate-plan.py

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: high
- **Sprint**: `S3.2`
- **Actions**: design, implement
- **Depends on**: `T3.1.4`
- **Commit group**: `cg10`
- **Artifacts**: agent-os/scripts/validate-plan.py
- **Notes**: Add detect_cycles() using Kahn's algorithm (topological sort). If remaining nodes after BFS, report cycle. Hard-fail on any cycle in depends_on relationships.

### M3.2.2: Implement bidirectional commit_group/item consistency check

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S3.2`
- **Actions**: design, implement
- **Depends on**: `T3.1.4`
- **Commit group**: `cg10`
- **Artifacts**: agent-os/scripts/validate-plan.py
- **Notes**: Three checks: (1) every commit_group.items[] resolves to existing item, (2) every item.commit_group references existing commit_group, (3) bidirectional membership is coherent. All hard-fail.

### M3.2.3: Implement type/action coherence warnings

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S3.2`
- **Actions**: design, implement
- **Depends on**: `T3.1.4`
- **Commit group**: `cg10`
- **Artifacts**: agent-os/scripts/validate-plan.py
- **Notes**: Encode recommended type/action coherence table from item-taxonomy.md. Warning-only, not hard-fail, since taxonomy says "recommended" not "mandatory".

### T3.2.4: Validate all new validation checks against current PLAN.yaml

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S3.2`
- **Actions**: test, verify
- **Depends on**: `M3.2.1`, `M3.2.2`, `M3.2.3`
- **Commit group**: `cg10`
- **Checks**:
  - python agent-os/scripts/validate-plan.py PLAN.yaml exits 0
  - No false-positive warnings from type/action coherence
  - No cycle detection false positives on the existing acyclic plan
  - Commit group coherence passes for all existing commit groups
- **Notes**: Gate for Sprint S3.2: all new validation checks must pass on the current PLAN.yaml without false positives.

### C3.2.5: Sprint S3.2 checkpoint — validation hardening complete

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S3.2`
- **Actions**: review, checkpoint, verify
- **Depends on**: `T3.2.4`
- **Commit group**: `cg10`
- **Checks**:
  - All S3.2 items are verified or done
  - Cycle detection produces hard-fail on circular depends_on
  - Commit group coherence produces hard-fail on mismatches
  - Type/action coherence produces warnings on non-recommended combinations
  - validate-plan.py passes on current PLAN.yaml
  - render-plan.py regenerates PLAN.md and PLAN.dot deterministically
- **Notes**: Marks validation tooling as hardened for control-plane-grade enforcement.

### M3.3.1: Add status/type visual styling to DOT rendering

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S3.3`
- **Actions**: design, implement
- **Depends on**: `T3.1.4`
- **Commit group**: `cg11`
- **Artifacts**: agent-os/scripts/render-plan.py
- **Notes**: Color nodes by status (done=green, blocked=red, in_progress=blue, etc.) and shape by type (Q=diamond, C=doubleoctagon, T=ellipse, etc.).

### M3.3.2: Add per-item detail sections to markdown rendering

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S3.3`
- **Actions**: design, implement
- **Depends on**: `T3.1.4`
- **Commit group**: `cg11`
- **Artifacts**: agent-os/scripts/render-plan.py
- **Notes**: After items table, add Item Details section with per-item subsections showing notes, checks, decision, artifacts_out, and depends_on.

### M3.3.3: Harden bootstrap-repo.sh with --owner, --ref, post-validation, ADR/README scaffolds

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S3.3`
- **Actions**: design, implement
- **Depends on**: `T3.1.4`, `M3.3.4`
- **Commit group**: `cg11`
- **Artifacts**: agent-os/scripts/bootstrap-repo.sh
- **Notes**: Add --owner/--ref flags, run validate-plan.py post-bootstrap, create docs/adr/ADR-0001.md and README.md scaffolds from templates.

### M3.3.4: Create repo-README.md.template

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S3.3`
- **Actions**: design, implement
- **Commit group**: `cg11`
- **Artifacts**: agent-os/templates/repo-README.md.template
- **Notes**: New template for bootstrap-generated README.md in target repos. Uses existing {{REPO_NAME}}, {{OWNER}}, {{DATE}}, {{CONTROL_PLANE_REF}} placeholders.

### M3.3.5: Enrich workspace templates with operational content

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S3.3`
- **Actions**: design, implement, document
- **Depends on**: `T3.1.4`
- **Commit group**: `cg11`
- **Artifacts**: agent-os/templates/workspace-AGENTS.md.template, agent-os/templates/workspace-CLAUDE.md.template
- **Notes**: Add precedence rules, workflow summary, authority split reminder, commit contract, and links to runtime-relevant files. Workspace templates must be useful runtime references, not just stubs.

### T3.3.6: Validate rendering and bootstrap improvements

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S3.3`
- **Actions**: test, verify
- **Depends on**: `M3.3.1`, `M3.3.2`, `M3.3.3`, `M3.3.4`, `M3.3.5`
- **Commit group**: `cg11`
- **Checks**:
  - render-plan.py produces enriched PLAN.md with item details
  - render-plan.py produces DOT with color/shape styling
  - Rendering is idempotent (second run produces identical output)
  - bootstrap-repo.sh --dry-run /tmp/test-X3 exits 0 and lists ADR + README
  - Workspace templates contain operational content
- **Notes**: Gate for Sprint S3.3: rendering, bootstrap, and workspace improvements must all work correctly.

### D3.4.1: Create root README.md for this repository

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: medium
- **Sprint**: `S3.4`
- **Actions**: document
- **Commit group**: `cg12`
- **Artifacts**: README.md
- **Notes**: Hand-maintained README (not template-generated) for the AgentOrchestrator repo itself. Contains: purpose, directory structure, quickstart, governance file links, license reference.

### D3.4.2: Define REPO_MAP freshness operational mechanism

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: medium
- **Sprint**: `S3.4`
- **Actions**: design, document
- **Depends on**: `C3.2.5`
- **Commit group**: `cg12`
- **Artifacts**: agent-os/workflow/lifecycle.md, agent-os/templates/repo-REPO_MAP.md.template
- **Notes**: Define freshness computation (today - last_validated_on > freshness_window_days), update triggers, and checkpoint consumption rules. Close the gap between concept and operational mechanism.

### D3.4.3: Add design-doc discipline guardrail

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S3.4`
- **Actions**: design, document, review
- **Commit group**: `cg12`
- **Artifacts**: agent-os/workflow/shared-workflow.md, ARCHITECTURE.md
- **Notes**: Add Design Document Governance section to shared-workflow.md: docs/design is non-authoritative, normative rules must migrate to canonical authority. Reinforce in ARCHITECTURE.md invariants.

### M3.4.4: Add REPO_MAP staleness warning to validate-plan.py

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S3.4`
- **Actions**: implement
- **Depends on**: `D3.4.2`, `C3.2.5`
- **Commit group**: `cg12`
- **Artifacts**: agent-os/scripts/validate-plan.py
- **Notes**: Add --check-freshness flag. Parse REPO_MAP.md metadata, warn if stale when checkpoint items exist in review/verified state. Warning-only.

### T3.4.5: Validate S3.4 documentation and operational mechanisms

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S3.4`
- **Actions**: test, verify
- **Depends on**: `D3.4.1`, `D3.4.2`, `D3.4.3`, `M3.4.4`
- **Commit group**: `cg12`
- **Checks**:
  - README.md exists and renders correctly
  - lifecycle.md freshness mechanism is fully specified
  - shared-workflow.md contains design-doc guardrail
  - validate-plan.py REPO_MAP staleness warning works
  - Full validate-plan.py run passes on PLAN.yaml
  - render-plan.py regenerates views deterministically
- **Notes**: Gate for Sprint S3.4: all documentation, guardrails, and operational mechanisms must be in place.

### C3.4.6: Milestone X3 closure checkpoint — control-plane hardening complete

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S3.4`
- **Actions**: review, checkpoint, verify
- **Depends on**: `T3.3.6`, `T3.4.5`
- **Commit group**: `cg12`
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

### M4.1.1: Tighten soft language to hard gates in governance files

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S4.1`
- **Actions**: implement
- **Commit group**: `cg13`
- **Artifacts**: agent-os/workflow/shared-workflow.md, agent-os/workflow/lifecycle.md
- **Notes**: Findings #2, #6, #12, #13: "may only" → "MUST only" in shared-workflow.md, "should not" → "MUST NOT" for design doc rule, "can optionally detect" → prescriptive in lifecycle.md, add explicit parallelism prohibition.

### M4.1.2: Document type/action coherence as warning-only

- **Type**: M | **Status**: done | **Role**: documenter | **Effort**: low
- **Sprint**: `S4.1`
- **Actions**: document
- **Commit group**: `cg13`
- **Artifacts**: agent-os/workflow/item-taxonomy.md
- **Notes**: Finding #3: add note to type/action coherence table clarifying it is advisory — violations produce warnings, not hard failures.

### T4.1.3: Validate language fixes are consistent across governance docs

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S4.1`
- **Actions**: verify
- **Depends on**: `M4.1.1`, `M4.1.2`
- **Commit group**: `cg13`
- **Checks**:
  - shared-workflow.md uses MUST only for commit group closure
  - shared-workflow.md uses MUST NOT for design doc rule
  - shared-workflow.md has explicit parallelism prohibition
  - lifecycle.md uses prescriptive language for freshness detection
  - item-taxonomy.md type/action table marked as advisory
  - validate-plan.py PLAN.yaml exits 0

### M4.2.1: Align commit group closure to require both status and checks

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S4.2`
- **Actions**: implement, document
- **Depends on**: `T4.1.3`
- **Commit group**: `cg14`
- **Artifacts**: agent-os/workflow/lifecycle.md, agent-os/workflow/shared-workflow.md
- **Notes**: Finding #1: state both predicates together in both files — items must be in review/verified/done AND required checks must be satisfied.

### M4.2.2: Make REPO_MAP freshness a hard gate in docs and validator

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S4.2`
- **Actions**: implement
- **Depends on**: `T4.1.3`
- **Commit group**: `cg14`
- **Artifacts**: agent-os/workflow/lifecycle.md, agent-os/scripts/validate-plan.py
- **Notes**: Finding #5: remove "advisory" language from lifecycle.md, change validate-plan.py check_repo_map_freshness() from warning to hard-fail.

### T4.2.3: Validate closure and freshness alignment

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S4.2`
- **Actions**: test, verify
- **Depends on**: `M4.2.1`, `M4.2.2`
- **Commit group**: `cg14`
- **Checks**:
  - lifecycle.md and shared-workflow.md have consistent closure predicates
  - lifecycle.md freshness is documented as hard gate
  - validate-plan.py --check-freshness hard-fails on stale REPO_MAP
  - validate-plan.py PLAN.yaml exits 0

### M4.3.1: Restrict depends_on to exclude milestoneId in schema

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S4.3`
- **Actions**: implement
- **Depends on**: `T4.2.3`
- **Commit group**: `cg15`
- **Artifacts**: agent-os/schemas/plan.schema.json
- **Notes**: Finding #4: create dependencyTarget definition as oneOf [sprintId, itemId]. Update depends_on items ref to use dependencyTarget instead of planId.

### M4.3.2: Define scope, checks, and suffix semantics in item-taxonomy

- **Type**: M | **Status**: done | **Role**: documenter | **Effort**: medium
- **Sprint**: `S4.3`
- **Actions**: document
- **Depends on**: `T4.2.3`
- **Commit group**: `cg15`
- **Artifacts**: agent-os/workflow/item-taxonomy.md
- **Notes**: Findings #8, #9, #17: scope is path prefix for collision detection, checks is array of human-readable descriptions, suffixes are contiguous lowercase sequence in derivation order with no gaps.

### M4.3.3: Add decision if/then Q-only constraint in schema

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S4.3`
- **Actions**: implement
- **Depends on**: `T4.2.3`
- **Commit group**: `cg15`
- **Artifacts**: agent-os/schemas/plan.schema.json
- **Notes**: Finding #18: add JSON Schema if/then to forbid decision property on non-Q-type items.

### M4.3.4: Add scope pattern constraint to schema

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S4.3`
- **Actions**: implement
- **Depends on**: `T4.2.3`
- **Commit group**: `cg15`
- **Artifacts**: agent-os/schemas/plan.schema.json
- **Notes**: Finding #8 (schema side): add pattern for scope field to restrict to path-like characters.

### T4.3.5: Validate PLAN.yaml against hardened schema

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S4.3`
- **Actions**: test, verify
- **Depends on**: `M4.3.1`, `M4.3.2`, `M4.3.3`, `M4.3.4`
- **Commit group**: `cg15`
- **Checks**:
  - validate-plan.py PLAN.yaml exits 0 with hardened schema
  - depends_on rejects milestone IDs
  - decision field rejected on non-Q items
  - scope pattern validates existing scopes

### D4.4.1: Unify governance asset states to draft/active/deprecated/superseded

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: medium
- **Sprint**: `S4.4`
- **Actions**: document
- **Depends on**: `T4.2.3`
- **Commit group**: `cg16`
- **Artifacts**: agent-os/workflow/lifecycle.md
- **Notes**: Finding #7: change ADR states from proposed/accepted to draft/active. Add unified Governance Asset Lifecycle section applicable to prompts, ADRs, and skills.

### D4.4.2: Add DEFERRED notes for triggers and tools_profile fields

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: low
- **Sprint**: `S4.4`
- **Actions**: document
- **Depends on**: `T4.2.3`
- **Commit group**: `cg16`
- **Artifacts**: agent-os/workflow/item-taxonomy.md, agent-os/workflow/portability-model.md
- **Notes**: Findings #15, #16: mark triggers and tools_profile as DEFERRED adapter-level fields with semantics TBD, optional and non-normative in MVP.

### D4.4.3: Clarify single-writer rule as documentation/review-enforced

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: low
- **Sprint**: `S4.4`
- **Actions**: document
- **Depends on**: `T4.2.3`
- **Commit group**: `cg16`
- **Artifacts**: agent-os/workflow/shared-workflow.md
- **Notes**: Finding #10: add note that enforcement is governance-based (code review and escalation), not automated. No validator check for single-writer.

### T4.4.4: Validate lifecycle and field documentation changes

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S4.4`
- **Actions**: verify
- **Depends on**: `D4.4.1`, `D4.4.2`, `D4.4.3`
- **Commit group**: `cg16`
- **Checks**:
  - lifecycle.md has unified governance asset states
  - ADR states use draft/active not proposed/accepted
  - item-taxonomy.md has DEFERRED notes for triggers and tools_profile
  - portability-model.md has DEFERRED notes
  - shared-workflow.md single-writer section has enforcement note
  - validate-plan.py PLAN.yaml exits 0

### D4.5.1: Define recommended commit body/footer format

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: medium
- **Sprint**: `S4.5`
- **Actions**: document
- **Depends on**: `T4.3.5`, `T4.4.4`
- **Commit group**: `cg17`
- **Artifacts**: AGENTS.md, agent-os/workflow/shared-workflow.md, agent-os/workflow/git-automation-policy.md, agent-os/templates/repo-AGENTS.md.template
- **Notes**: Finding #19: define recommended (SHOULD) body/footer structure including summary, scope, items, validation, refs, ADR, and follow-up sections.

### M4.5.2: Simplify ARCHITECTURE.md Phase B to cross-reference

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S4.5`
- **Actions**: implement
- **Depends on**: `T4.3.5`, `T4.4.4`
- **Commit group**: `cg17`
- **Artifacts**: ARCHITECTURE.md
- **Notes**: Finding #11: replace single-condition Phase B statement with cross-reference to shared-workflow.md Phase B Safety Gate for the full prerequisite list.

### D4.5.3: Add phase-gate protocol for deferred automations

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: medium
- **Sprint**: `S4.5`
- **Actions**: design, document
- **Depends on**: `T4.3.5`, `T4.4.4`
- **Commit group**: `cg17`
- **Artifacts**: agent-os/workflow/git-automation-policy.md
- **Notes**: Finding #20 (part 1): add Phase Gate Protocol section requiring dedicated decision item, human sign-off, and ADR for each deferred automation.

### M4.5.4: Add phase-gate schema fields (requires_phase, approval_ref)

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S4.5`
- **Actions**: implement, document
- **Depends on**: `T4.3.5`, `T4.4.4`
- **Commit group**: `cg17`
- **Artifacts**: agent-os/schemas/plan.schema.json, agent-os/workflow/item-taxonomy.md
- **Notes**: Finding #20 (part 2): add requires_phase enum [A,B,C,D] and approval_ref string as optional item fields in schema and document in taxonomy.

### M4.5.5: Add phase-gate validator enforcement

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S4.5`
- **Actions**: implement
- **Depends on**: `M4.5.4`
- **Commit group**: `cg17`
- **Artifacts**: agent-os/scripts/validate-plan.py
- **Notes**: Finding #20 (part 3): add validate_phase_gates() — hard-fail if item has requires_phase and is ready/in_progress/review without approval_ref. Soft warning for deferred automation keywords without requires_phase.

### T4.5.6: Validate commit format, Phase B, and phase-gate changes

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S4.5`
- **Actions**: test, verify
- **Depends on**: `D4.5.1`, `M4.5.2`, `D4.5.3`, `M4.5.4`, `M4.5.5`
- **Commit group**: `cg17`
- **Checks**:
  - Commit body/footer format defined in AGENTS.md, shared-workflow.md, git-automation-policy.md
  - ARCHITECTURE.md Phase B cross-references shared-workflow.md
  - git-automation-policy.md has Phase Gate Protocol section
  - plan.schema.json has requires_phase and approval_ref fields
  - validate-plan.py phase-gate enforcement works
  - validate-plan.py PLAN.yaml exits 0
  - render-plan.py regenerates views deterministically

### C4.5.7: Milestone X4 closure checkpoint — governance baseline hardened

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S4.5`
- **Actions**: review, checkpoint, verify
- **Depends on**: `T4.5.6`
- **Commit group**: `cg17`
- **Checks**:
  - All S4.1-S4.5 items are verified or done
  - All 19 findings are resolved
  - No soft language remains for hard gates
  - Schema enforces depends_on, decision, scope constraints
  - Governance asset lifecycle is unified
  - Phase-gate enforcement is operational
  - PLAN.md and PLAN.dot are regenerated and committed
  - validate-plan.py PLAN.yaml exits 0

### M4.6.1: Enforce executable item commit_group presence in validate-plan.py

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S4.6`
- **Actions**: implement, verify
- **Depends on**: `T4.5.6`
- **Commit group**: `cg18`
- **Artifacts**: agent-os/scripts/validate-plan.py
- **Notes**: Add hard-fail validation: every executable item type (Q, D, M, F, T, C) must declare commit_group. This makes commit boundary enforcement explicit in runtime validation, in addition to existing bidirectional coherence.

### T4.6.2: Validate strict commit_group presence and coherence checks

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S4.6`
- **Actions**: test, verify
- **Depends on**: `M4.6.1`
- **Commit group**: `cg18`
- **Checks**:
  - validate-plan.py hard-fails when executable items omit commit_group
  - validate-plan.py keeps bidirectional commit_group coherence strict
  - validate-plan.py PLAN.yaml exits 0

### C4.6.3: Commit governance enforcement checkpoint — validation executable

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S4.6`
- **Actions**: review, checkpoint, verify
- **Depends on**: `T4.6.2`
- **Commit group**: `cg18`
- **Checks**:
  - Commit-group presence is enforced in validator for executable items
  - Commit-group/item bidirectional coherence remains strict
  - Canonical commit policy remains in git-automation-policy.md
  - PLAN.md and PLAN.dot are regenerated and committed

### M4.7.1: Add local commit-msg hook guard for commit title contract

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S4.7`
- **Actions**: implement, verify
- **Depends on**: `C4.6.3`
- **Commit group**: `cg19`
- **Artifacts**: .githooks/commit-msg
- **Notes**: Add lightweight commit-msg hook enforcing the title pattern ^([a-z]+)\(([a-z0-9._/-]+)\): .+$ for local commits. The hook prints a clear error and references the canonical governance policy location.

### D4.7.2: Document hook enablement workflow in README.md

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: low
- **Sprint**: `S4.7`
- **Actions**: document
- **Depends on**: `M4.7.1`
- **Commit group**: `cg19`
- **Artifacts**: README.md
- **Notes**: Add explicit setup instructions so contributors and agents enable the repository hook path consistently.

### D4.7.3: Align workspace runtime wording with mandatory commit_group hard gate

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: low
- **Sprint**: `S4.7`
- **Actions**: document
- **Depends on**: `C4.6.3`
- **Commit group**: `cg19`
- **Artifacts**: agent-os/templates/workspace-AGENTS.md.template
- **Notes**: Add explicit runtime wording that the mandatory commit_group hard gate is defined in shared-workflow.md and git-automation-policy.md.

### T4.7.4: Validate commit hook pattern and documentation alignment

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S4.7`
- **Actions**: test, verify
- **Depends on**: `M4.7.1`, `D4.7.2`, `D4.7.3`
- **Commit group**: `cg19`
- **Checks**:
  - commit-msg hook enforces ^([a-z]+)\(([a-z0-9._/-]+)\): .+$
  - README.md documents core.hooksPath setup and validation command
  - workspace-AGENTS template references mandatory commit_group hard gate
  - validate-plan.py PLAN.yaml exits 0

### C4.7.5: Commit tooling checkpoint — local enforcement and runtime clarity complete

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S4.7`
- **Actions**: review, checkpoint, verify
- **Depends on**: `T4.7.4`
- **Commit group**: `cg19`
- **Checks**:
  - Commit title guard exists in repo tooling
  - README setup enables consistent local enforcement
  - Runtime template wording is unambiguous about hard gate authority
  - PLAN.md and PLAN.dot are regenerated and committed

### D5.1.1: Codify tracking-first execution in Level-0 authorities

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: low
- **Sprint**: `S5.1`
- **Actions**: document, review
- **Depends on**: `C4.7.5`
- **Commit group**: `cg20`
- **Artifacts**: AGENTS.md, agent-os/workflow/shared-workflow.md, agent-os/workflow/git-automation-policy.md
- **Notes**: Makes PLAN-first execution explicit: work must be tracked in PLAN.yaml before file edits begin, and untracked modifications are a governance violation.

### D5.1.2: Define exact commit_group traceability and non-ad-hoc commit closure

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: low
- **Sprint**: `S5.1`
- **Actions**: document, review
- **Depends on**: `D5.1.1`
- **Commit group**: `cg20`
- **Artifacts**: AGENTS.md, agent-os/workflow/shared-workflow.md, agent-os/workflow/git-automation-policy.md, agent-os/workflow/item-taxonomy.md
- **Notes**: Makes commit_group boundaries a plan-time decision, requires each git commit to close exactly one commit_group, and requires explicit item and commit_group references in the commit footer.

### C5.1.3: Governance checkpoint — tracking-first hard gate is canonical

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S5.1`
- **Actions**: review, checkpoint, verify
- **Depends on**: `D5.1.2`
- **Commit group**: `cg20`
- **Artifacts**: PLAN.yaml, PLAN.md, PLAN.dot
- **Checks**:
  - Level-0 authorities state that PLAN.yaml tracking must exist before edits
  - Level-0 authorities state that each commit closes exactly one commit_group
  - Commit footer contract requires PLAN item IDs plus exactly one commit_group ID
  - PLAN.md and PLAN.dot are regenerated from the updated PLAN.yaml

### D5.2.1: Propagate tracking-first and commit traceability rules into Level-1 and Level-2 templates

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: medium
- **Sprint**: `S5.2`
- **Actions**: document, review
- **Depends on**: `C5.1.3`
- **Commit group**: `cg21`
- **Artifacts**: agent-os/templates/repo-AGENTS.md.template, agent-os/templates/repo-README.md.template, agent-os/templates/workspace-AGENTS.md.template, agent-os/templates/workspace-CLAUDE.md.template
- **Notes**: Makes the rule visible beyond Level-0 so workspace runtime files and bootstrapped repo-local governance files carry the same hard gate.

### M5.2.2: Enforce commit title and Refs footer contract in repo-local tooling

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S5.2`
- **Actions**: implement, verify
- **Depends on**: `C5.1.3`
- **Commit group**: `cg21`
- **Artifacts**: .githooks/commit-msg, agent-os/scripts/bootstrap-repo.sh, agent-os/templates/repo-commit-msg.template
- **Notes**: Extends the local commit hook to require both the canonical title contract and a Refs footer with PLAN item IDs plus exactly one commit_group, and bootstraps the same guard into downstream repos.

### M5.2.3: Repair template drift, local provenance, and fresh-checkout operator flow

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S5.2`
- **Actions**: implement, refactor, verify
- **Depends on**: `C5.1.3`
- **Commit group**: `cg21`
- **Artifacts**: .gitignore, ARCHITECTURE.md, README.md, agent-os/scripts/render-plan.py, agent-os/scripts/sync-workspace.sh, agent-os/scripts/validate-plan.py, agent-os/templates/repo-ADR.md.template, agent-os/templates/repo-ARCHITECTURE.md.template, agent-os/templates/repo-REPO_MAP.md.template, requirements.txt
- **Notes**: Aligns ADR and REPO_MAP templates with canonical lifecycle policy, removes implicit remote mutation from workspace sync, stamps workspace files with local provenance, and makes the repo self-hosted with an explicit dependency manifest and runnable operator documentation.

### T5.2.4: Validate nn-2 flow for plan tooling, bootstrap, sync, and hook enforcement

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S5.2`
- **Actions**: test, verify
- **Depends on**: `D5.2.1`, `M5.2.2`, `M5.2.3`
- **Commit group**: `cg21`
- **Checks**:
  - conda run -n nn-2 python -m pip install -r requirements.txt succeeds
  - conda run -n nn-2 python agent-os/scripts/validate-plan.py PLAN.yaml exits 0
  - conda run -n nn-2 python agent-os/scripts/render-plan.py PLAN.yaml updates PLAN.md and PLAN.dot deterministically
  - .githooks/commit-msg accepts a valid title plus Refs footer and rejects missing Refs
  - bootstrap-repo.sh --dry-run derives current local control-plane ref when --ref is omitted and renders .githooks/commit-msg
  - sync-workspace.sh writes branch or detached state plus commit SHA without pulling from remote

### C5.2.5: Consistency repair checkpoint — cross-layer rules and operator flow aligned

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S5.2`
- **Actions**: review, checkpoint, verify
- **Depends on**: `T5.2.4`
- **Commit group**: `cg21`
- **Checks**:
  - Level-1 and Level-2 artifacts carry the tracking-first and commit_group hard gate clearly
  - Repo-local hook/bootstrap path enforces title plus Refs footer contract
  - Templates no longer contradict canonical ADR or REPO_MAP lifecycle rules
  - Workspace sync is non-mutating and provenance-stamped
  - Fresh checkout README path is executable with requirements.txt
  - PLAN.md and PLAN.dot are regenerated and committed

### D6.1.1: Codify the planning model as an execution-optimization artifact

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: low
- **Sprint**: `S6.1`
- **Actions**: document, review
- **Depends on**: `C5.2.5`
- **Commit group**: `cg22`
- **Artifacts**: ARCHITECTURE.md, PLAN.yaml, agent-os/workflow/shared-workflow.md
- **Notes**: Adds the planning-model optimization principle to the canonical workflow authority, reflects it as an architectural principle, and records the repository-level execution intent in PLAN.yaml without creating a second conflicting workflow authority.

### T6.1.2: Validate planning-model principle wording and regenerated plan views

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S6.1`
- **Actions**: test, verify
- **Depends on**: `D6.1.1`
- **Commit group**: `cg22`
- **Checks**:
  - conda run -n nn-2 python agent-os/scripts/validate-plan.py PLAN.yaml exits 0
  - conda run -n nn-2 python agent-os/scripts/render-plan.py PLAN.yaml updates PLAN.md and PLAN.dot deterministically
  - shared-workflow.md carries the canonical execution-optimization wording
  - ARCHITECTURE.md states the execution-oriented planning principle without conflicting with workflow authority
  - PLAN.yaml mission/meta text records the repository-level intent without becoming a second workflow specification

### C6.1.3: Planning-model optimization checkpoint

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S6.1`
- **Actions**: review, checkpoint, verify
- **Depends on**: `T6.1.2`
- **Commit group**: `cg22`
- **Checks**:
  - Planning model is explicitly framed as execution-oriented in canonical workflow authority
  - Architectural principle is recorded without authority duplication
  - PLAN.md and PLAN.dot are regenerated and committed

### D7.1.1: Create plan-checkpoint-close skill

- **Type**: D | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S7.1`
- **Actions**: design, implement, document
- **Depends on**: `C6.1.3`
- **Commit group**: `cg23`
- **Artifacts**: agent-os/skills/plan-checkpoint-close/SKILL.md
- **Notes**: First operational skill under agent-os/skills/. Implements a procedural, tool-neutral checkpoint closure workflow that operates at both Layer 0 and Layer 2 using a two-root model (control_plane_root for shared tooling, repo_root for target data). Satisfies the skill packaging contract defined in agent-os/skills/README.md and agent-os/workflow/portability-model.md.

### D7.1.2: Document workspace topology and artifact placement in shared workflow

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: low
- **Sprint**: `S7.1`
- **Actions**: document
- **Commit group**: `cg23`
- **Artifacts**: agent-os/workflow/shared-workflow.md
- **Notes**: Adds Workspace Topology diagram and Artifact Placement Across Layers table to the Three-Layer Model section of shared-workflow.md. Documents the two-root resolution model (control_plane_root vs repo_root) and how sync-workspace.sh stamps CONTROL_PLANE_ROOT for discovery. Content is additive — no duplication with existing canonical authorities.

### T7.1.3: Validate skill contract compliance and plan consistency

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S7.1`
- **Actions**: test, verify
- **Depends on**: `D7.1.1`, `D7.1.2`
- **Commit group**: `cg23`
- **Checks**:
  - validate-plan.py PLAN.yaml exits 0
  - render-plan.py PLAN.yaml updates PLAN.md and PLAN.dot deterministically
  - SKILL.md frontmatter has all required fields (id, description, owner, version, compatibility)
  - SKILL.md body has all required sections (purpose, required inputs, expected outputs, constraints, failure handling)
  - shared-workflow.md carries workspace topology without duplicating other authorities

### C7.1.4: Skill packaging and cross-layer execution checkpoint

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S7.1`
- **Actions**: review, checkpoint, verify
- **Depends on**: `T7.1.3`
- **Commit group**: `cg23`
- **Checks**:
  - First operational skill exists and satisfies packaging contract
  - Workspace topology is documented in canonical workflow authority
  - No normative duplication introduced across authorities
  - PLAN.md and PLAN.dot are regenerated and committed

### D8.1.1: Create CLAUDE.md as thin adapter layer pointing to canonical governance

- **Type**: D | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S8.1`
- **Actions**: document, implement
- **Depends on**: `C7.1.4`
- **Commit group**: `cg24`
- **Artifacts**: CLAUDE.md
- **Notes**: Thin adapter-layer file for Claude Code. Points to AGENTS.md and canonical workflow authorities. Overrides Claude Code's default ask-before-committing behavior to align with the mandatory commit rule. Does not duplicate normative content — adapter boundary rule preserved.

### F8.1.2: Add .mypy_cache and workspace patterns to .gitignore

- **Type**: F | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S8.1`
- **Actions**: implement
- **Depends on**: `D8.1.1`
- **Commit group**: `cg25`
- **Artifacts**: .gitignore
- **Notes**: Adds .mypy_cache/ and *-workspace/ patterns to .gitignore to keep eval working directories and type-check caches out of version control.

### C8.1.3: Adapter layer and repo hygiene checkpoint

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S8.1`
- **Actions**: review, checkpoint, verify
- **Depends on**: `F8.1.2`
- **Commit group**: `cg25`
- **Checks**:
  - .gitignore includes .mypy_cache/ and *-workspace/ patterns
  - validate-plan.py exits 0
  - PLAN.md and PLAN.dot are regenerated and committed

### D9.1.1: Define canonical shared-asset families, registry, and seed assets

- **Type**: D | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S9.1`
- **Actions**: design, document, implement
- **Depends on**: `C8.1.3`
- **Commit group**: `cg26`
- **Artifacts**: ARCHITECTURE.md, agent-os/registry/shared-assets.yaml, agent-os/skills/plan-checkpoint-close/SKILL.md, agent-os/prompts/checkpoint-closure-review.md, agent-os/profiles/claude/check-medium.yaml, agent-os/profiles/codex/check-medium.yaml, agent-os/protocols/check-result-v1.yaml, agent-os/prompts/README.md, agent-os/skills/README.md, agent-os/workflow/portability-model.md, agent-os/workflow/shared-workflow.md
- **Notes**: Establishes the explicit shared asset families (skills, prompts, profiles, protocols), adds the canonical registry, and ships the first real seed assets. Contracts remain tool-neutral; runtime-specific behavior belongs in profiles and adapter notes, not in the shared prompt or skill.

### M9.1.2: Extend PLAN schema and validator for shared_assets registry-backed references

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S9.1`
- **Actions**: design, implement, verify
- **Depends on**: `D9.1.1`
- **Commit group**: `cg26`
- **Artifacts**: agent-os/schemas/plan.schema.json, agent-os/scripts/validate-plan.py, agent-os/scripts/render-plan.py, agent-os/templates/PLAN.yaml.template, agent-os/workflow/item-taxonomy.md
- **Notes**: Adds the optional shared_assets object to executable PLAN items, constrains context_policy and resolution_mode values, and validates that referenced asset IDs resolve through the canonical registry. Deferred triggers and tools_profile fields remain untouched.

### M9.1.3: Implement shared asset resolver, materialization, and runtime doc propagation

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S9.1`
- **Actions**: design, implement, verify
- **Depends on**: `D9.1.1`
- **Commit group**: `cg26`
- **Artifacts**: agent-os/scripts/resolve-shared-asset.py, agent-os/scripts/materialize-shared-asset.sh, agent-os/scripts/bootstrap-repo.sh, agent-os/scripts/sync-workspace.sh, agent-os/templates/workspace-AGENTS.md.template, agent-os/templates/workspace-CLAUDE.md.template, agent-os/templates/repo-AGENTS.md.template, agent-os/templates/repo-README.md.template
- **Notes**: Implements two-root shared asset discovery with workspace-first CONTROL_PLANE_ROOT resolution and optional explicit vendoring under .agent-os/vendor/. Generated workspace and repo runtime docs must explain workspace mode and vendored mode without making Layer-2 copies authoritative.

### T9.1.4: Validate shared asset consistency, resolver behavior, and plan rendering

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: medium
- **Sprint**: `S9.1`
- **Actions**: test, verify
- **Depends on**: `M9.1.2`, `M9.1.3`
- **Commit group**: `cg26`
- **Shared assets**: prompt=checkpoint-closure-review, profile=codex/check-medium, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace
- **Checks**:
  - validate-plan.py PLAN.yaml exits 0 after shared_assets schema changes
  - render-plan.py PLAN.yaml updates PLAN.md and PLAN.dot deterministically
  - Registry entries resolve to existing asset paths
  - resolve-shared-asset.py resolves seed assets in workspace mode
  - materialize-shared-asset.sh vendors an asset with provenance manifest and vendored resolution works
  - Generated workspace and repo docs describe two-root discovery, workspace mode, and vendored mode

### C9.1.5: Shared asset distribution and two-root consumption checkpoint

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S9.1`
- **Actions**: review, checkpoint, verify
- **Depends on**: `T9.1.4`
- **Commit group**: `cg26`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, profile=codex/check-medium, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace
- **Checks**:
  - Layer-0 registry, schema, validator, and resolver agree on shared asset IDs and paths
  - Seed skill, prompt, profiles, and protocol are internally consistent
  - Layer-2 workspace mode consumes shared assets without copying
  - Vendored mode consumes explicit snapshots without creating a new authority
  - PLAN.md and PLAN.dot are regenerated and committed

### D10.1.1: Define script test/gate scope and tooling surface

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: medium
- **Sprint**: `S10.1`
- **Actions**: plan, document
- **Depends on**: `C9.1.5`
- **Commit group**: `cg27`
- **Artifacts**: PLAN.yaml, README.md, CLAUDE.md, pyproject.toml, requirements-dev.txt, .gitignore
- **Notes**: Establishes the repo-local test and gate contract for agent-os/scripts/, keeps requirements.txt runtime-only, and documents nn-2 as the canonical execution environment for tests and local gates.

### M10.1.2: Implement pytest suite for Python and Bash scripts

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S10.1`
- **Actions**: design, implement, verify
- **Depends on**: `D10.1.1`
- **Commit group**: `cg27`
- **Artifacts**: tests/conftest.py, tests/test_validate_plan.py, tests/test_render_plan.py, tests/test_resolve_shared_asset.py, tests/test_shell_scripts.py
- **Notes**: Adds behavior-focused pytest coverage for the Python scripts and subprocess smoke tests for bootstrap, sync-workspace, and materialize-shared-asset using temporary directories only.

### M10.1.3: Add deterministic local gate runner and tooling config

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S10.1`
- **Actions**: design, implement, verify
- **Depends on**: `D10.1.1`
- **Commit group**: `cg27`
- **Artifacts**: agent-os/scripts/bootstrap-repo.sh, agent-os/scripts/materialize-shared-asset.sh, agent-os/scripts/render-plan.py, agent-os/scripts/resolve-shared-asset.py, agent-os/scripts/run-gates.sh, agent-os/scripts/validate-plan.py, pyproject.toml, requirements-dev.txt
- **Notes**: Adds one local gate entrypoint that runs Ruff, mypy, Python compile checks, pytest, and conditional ShellCheck in a fixed order with readable output and deterministic failure behavior.

### T10.1.4: Validate script tests and local gates in nn-2

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: medium
- **Sprint**: `S10.1`
- **Actions**: test, verify
- **Depends on**: `M10.1.2`, `M10.1.3`
- **Commit group**: `cg27`
- **Checks**:
  - conda run -n nn-2 python -m pytest -q exits 0
  - bash agent-os/scripts/run-gates.sh exits 0 in nn-2
  - README and CLAUDE document nn-2 test/gate commands consistently
  - Gate help/output is explicit about conditional ShellCheck behavior

### C10.1.5: Script test suite and local gates checkpoint

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S10.1`
- **Actions**: review, checkpoint, verify
- **Depends on**: `T10.1.4`
- **Commit group**: `cg27`
- **Checks**:
  - agent-os/scripts/ has repo-owned pytest coverage for Python and Bash entrypoints
  - Local gate runner covers Ruff, mypy, compile checks, pytest, and conditional ShellCheck
  - requirements.txt remains runtime-only
  - PLAN.md and PLAN.dot are regenerated and committed

### D11.1.1: Design runtime lifecycle model and plan portability expansion

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: medium
- **Sprint**: `S11.1`
- **Actions**: design, document
- **Depends on**: `C10.1.5`
- **Commit group**: `cg28`
- **Artifacts**: PLAN.yaml, agent-os/workflow/portability-model.md
- **Notes**: Adds a formal three-tier runtime lifecycle (experimental, supported, first-class) to portability-model.md. Assigns current runtimes: claude = first-class, codex = supported, kilo = experimental. Documents Copilot as recognized but deferred with rationale about its different adapter shape.

### M11.1.2: Populate Codex adapter and add lifecycle references to READMEs

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S11.1`
- **Actions**: implement, document
- **Depends on**: `D11.1.1`
- **Commit group**: `cg29`
- **Artifacts**: .codex, agent-os/skills/README.md, agent-os/prompts/README.md
- **Notes**: Populates the empty .codex file following the CLAUDE.md thin adapter pattern. Same canonical authorities, same three adapter overrides. Codex-specific sandbox notes for tooling. Updates skills/README.md and prompts/README.md to reference the runtime lifecycle tiers.

### M11.1.3: Add Kilo as experimental runtime with adapter, profile, and registry

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S11.1`
- **Actions**: implement, document
- **Depends on**: `D11.1.1`
- **Commit group**: `cg30`
- **Artifacts**: KILO.md, agent-os/profiles/kilo/check-medium.yaml, agent-os/registry/shared-assets.yaml, agent-os/skills/plan-checkpoint-close/SKILL.md, .gitignore
- **Notes**: Creates KILO.md as a thin experimental adapter at repo root. Creates kilo profile. Adds kilo to neutral asset compatibility in the registry. Updates skill frontmatter. Adds .sixth/ to .gitignore.

### T11.1.4: Validate portability expansion and runtime artifacts

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: medium
- **Sprint**: `S11.1`
- **Actions**: test, verify
- **Depends on**: `M11.1.2`, `M11.1.3`
- **Commit group**: `cg31`
- **Checks**:
  - validate-plan.py PLAN.yaml exits 0
  - render-plan.py PLAN.yaml updates PLAN.md and PLAN.dot deterministically
  - .codex is non-empty and follows the thin adapter pattern
  - KILO.md exists and follows the thin adapter pattern
  - agent-os/profiles/kilo/check-medium.yaml exists with target_runtime kilo
  - Registry neutral assets include kilo in compatibility
  - portability-model.md contains runtime lifecycle tiers and status table
  - .gitignore includes .sixth/
  - run-gates.sh passes

### C11.1.5: Runtime portability expansion checkpoint

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S11.1`
- **Actions**: review, checkpoint, verify
- **Depends on**: `T11.1.4`
- **Commit group**: `cg31`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, profile=claude/check-medium, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace
- **Checks**:
  - Portability model defines explicit runtime lifecycle tiers
  - Codex adapter is populated and follows the thin adapter pattern
  - Kilo is registered as experimental with profile, adapter, and neutral asset compatibility
  - Copilot is documented as deferred with rationale
  - No normative duplication between adapters and canonical authorities
  - PLAN.md and PLAN.dot are regenerated and committed

### M12.1.1: Create Codex workspace template and extend sync-workspace.sh

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S12.1`
- **Actions**: implement
- **Depends on**: `C11.1.5`
- **Commit group**: `cg32`
- **Artifacts**: agent-os/templates/workspace-CODEX.md.template, agent-os/scripts/sync-workspace.sh, agent-os/workflow/portability-model.md
- **Notes**: Creates workspace-CODEX.md.template following the CLAUDE template pattern with Codex-specific sandbox notes. Extends sync-workspace.sh to render the Codex template alongside AGENTS.md and CLAUDE.md. Updates portability-model.md runtime status table to mark codex as first-class.

### T12.1.2: Validate Codex first-class promotion

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S12.1`
- **Actions**: test, verify
- **Depends on**: `M12.1.1`
- **Commit group**: `cg32`
- **Checks**:
  - validate-plan.py PLAN.yaml exits 0
  - workspace-CODEX.md.template exists and follows workspace template pattern
  - sync-workspace.sh renders .codex alongside AGENTS.md and CLAUDE.md
  - portability-model.md shows codex as first-class
  - run-gates.sh passes

### C12.1.3: Codex first-class promotion checkpoint

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S12.1`
- **Actions**: review, checkpoint, verify
- **Depends on**: `T12.1.2`
- **Commit group**: `cg32`
- **Checks**:
  - Codex has adapter, profile, workspace template, and sync support
  - Runtime status table is consistent with actual artifact presence
  - PLAN.md and PLAN.dot are regenerated and committed

### F13.1.1: Add adapter overrides to workspace-CLAUDE.md.template

- **Type**: F | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S13.1`
- **Actions**: implement
- **Depends on**: `C12.1.3`
- **Commit group**: `cg33`
- **Artifacts**: agent-os/templates/workspace-CLAUDE.md.template
- **Notes**: Governance audit found workspace-CLAUDE.md.template is missing the adapter overrides section that workspace-CODEX.md.template has. Layer 2 Claude agents would not receive the mandatory commit override.

### F13.1.2: Expand sync-workspace.sh test to verify all rendered files

- **Type**: F | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S13.1`
- **Actions**: implement
- **Depends on**: `F13.1.1`
- **Commit group**: `cg33`
- **Artifacts**: tests/test_shell_scripts.py
- **Notes**: Test only checks AGENTS.md existence and content. Must also verify CLAUDE.md and .codex are generated with correct CONTROL_PLANE_ROOT stamping.

### C13.1.3: Workspace template parity and test coverage checkpoint

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S13.1`
- **Actions**: review, checkpoint, verify
- **Depends on**: `F13.1.2`
- **Commit group**: `cg33`
- **Checks**:
  - workspace-CLAUDE.md.template has adapter overrides matching workspace-CODEX.md.template
  - sync-workspace.sh test verifies AGENTS.md, CLAUDE.md, and .codex
  - run-gates.sh and pytest pass
  - PLAN.md and PLAN.dot are regenerated and committed

### D14.1.1: Track portability completion milestone and runtime entrypoint contract update

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: medium
- **Sprint**: `S14.1`
- **Actions**: design, document
- **Depends on**: `C13.1.3`
- **Commit group**: `cg34`
- **Artifacts**: PLAN.yaml
- **Notes**: Adds X14 as the tracked follow-on to X11–X13. Records the contract shift from singular adapter files to runtime entrypoint artifacts, targets Copilot as supported, and realigns Kilo to native portability through AGENTS.md instead of a dedicated KILO.md authority file.

### M14.1.2: Implement Copilot support and Kilo realignment across docs, templates, registry, and tooling

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: high
- **Sprint**: `S14.1`
- **Actions**: implement, document, refactor
- **Depends on**: `D14.1.1`
- **Commit group**: `cg35`
- **Artifacts**: .github/copilot-instructions.md, agent-os/workflow/portability-model.md, agent-os/workflow/shared-workflow.md, agent-os/registry/shared-assets.yaml, agent-os/profiles/copilot/check-medium.yaml, agent-os/profiles/kilo/check-medium.yaml, agent-os/skills/plan-checkpoint-close/SKILL.md, agent-os/templates/repo-copilot-instructions.md.template, agent-os/templates/repo-README.md.template, agent-os/scripts/bootstrap-repo.sh, agent-os/scripts/resolve-shared-asset.py, tests/test_shell_scripts.py, README.md, PLAN.yaml
- **Notes**: Adds a thin `.github/copilot-instructions.md` bootstrap template, registers the Copilot profile, broadens neutral shared-asset compatibility to include Copilot, removes KILO.md from the portability contract and verification expectations, and keeps runtime authority centralized in canonical governance files.

### T14.1.3: Validate Copilot support and Kilo realignment

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: medium
- **Sprint**: `S14.1`
- **Actions**: test, verify
- **Depends on**: `M14.1.2`
- **Commit group**: `cg36`
- **Checks**:
  - bootstrap-repo.sh creates .github/copilot-instructions.md with thin-pointer content only
  - sync-workspace.sh still renders only AGENTS.md, CLAUDE.md, and .codex
  - Registry neutral assets and runtime profiles are internally consistent for claude, codex, kilo, and copilot
  - No docs, tests, or verification expectations require KILO.md
  - portability-model.md shows copilot and kilo as supported under the entrypoint-artifact model
  - validate-plan.py PLAN.yaml exits 0
  - render-plan.py PLAN.yaml updates PLAN.md and PLAN.dot deterministically
  - python -m pytest -q passes
  - bash agent-os/scripts/run-gates.sh passes

### C14.1.4: Portability completion checkpoint

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S14.1`
- **Actions**: review, checkpoint, verify
- **Depends on**: `T14.1.3`
- **Commit group**: `cg36`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, profile=copilot/check-medium, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace
- **Checks**:
  - All runtime entrypoint artifacts remain thin pointers to canonical authorities
  - Copilot is supported through repo-level bootstrap entrypoints without authority duplication
  - Kilo support no longer depends on KILO.md
  - Workspace sync remains limited to workspace-scoped runtimes
  - PLAN.md and PLAN.dot are regenerated and committed

### M15.1.1: Replace hardcoded nn-2 with AGENT_PYTHON env var across scripts and docs

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S15.1`
- **Actions**: implement
- **Depends on**: `C14.1.4`
- **Commit group**: `cg37`
- **Artifacts**: .env.example, agent-os/scripts/run-gates.sh, CLAUDE.md, README.md
- **Notes**: Creates .env.example with AGENT_PYTHON variable. Refactors run-gates.sh to source .env and use AGENT_PYTHON instead of hardcoded nn-2 discovery. Updates CLAUDE.md and README.md to reference the env var pattern.

### T15.1.2: Validate environment portability

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S15.1`
- **Actions**: test, verify
- **Depends on**: `M15.1.1`
- **Commit group**: `cg37`
- **Checks**:
  - validate-plan.py PLAN.yaml exits 0
  - run-gates.sh passes with AGENT_PYTHON set
  - .env.example exists and documents AGENT_PYTHON
  - No hardcoded nn-2 in run-gates.sh
  - CLAUDE.md references AGENT_PYTHON pattern
  - README.md references AGENT_PYTHON pattern

### C15.1.3: Environment portability checkpoint

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S15.1`
- **Actions**: review, checkpoint, verify
- **Depends on**: `T15.1.2`
- **Commit group**: `cg37`
- **Checks**:
  - No hardcoded conda environment names in executable scripts
  - AGENT_PYTHON env var is the canonical override mechanism
  - .env is gitignored, .env.example is committed
  - PLAN.md and PLAN.dot are regenerated and committed

### D16.1.1: Create non-normative TODO.md checklist

- **Type**: D | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S16.1`
- **Actions**: document
- **Commit group**: `cg38`
- **Artifacts**: TODO.md
- **Notes**: Human-readable checklist of macro-features done and pending. Not governance, not read by agents.

### D16.1.2: Fix TODO typo from NFC to RFC for normative review section

- **Type**: D | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S16.1`
- **Actions**: document
- **Depends on**: `D16.1.1`
- **Commit group**: `cg39`
- **Artifacts**: PLAN.yaml, TODO.md
- **Notes**: Corrects the TODO heading/checkbox label typo from NFC to RFC in the non-normative future-considerations section.

### D17.1.1: Create an English peer document for the Git Flow PR-only terminal workflow

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: medium
- **Sprint**: `S17.1`
- **Actions**: document
- **Commit group**: `cg40`
- **Artifacts**: PLAN.yaml, docs/design/gitflow-pr-only-terminal-workflow.md
- **Notes**: Create a new English design document alongside the existing Italian source file, keeping headings, lists, commands, Mermaid diagrams, and references aligned 1:1 with the original workflow document under the peer filename docs/design/gitflow-pr-only-terminal-workflow.md.

### T17.1.2: Validate the English peer document and regenerated plan views

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S17.1`
- **Actions**: test, verify
- **Depends on**: `D17.1.1`
- **Commit group**: `cg40`
- **Checks**:
  - validate-plan.py PLAN.yaml exits 0
  - render-plan.py PLAN.yaml updates PLAN.md and PLAN.dot deterministically
  - docs/design/gitflow-pr-only-terminal-workflow.md exists as a peer English document
  - English document preserves the original section structure, commands, Mermaid diagrams, and references
- **Notes**: validate-plan.py completed successfully against the schema. render-plan.py regenerated PLAN.md and PLAN.dot. Structural parity checks confirmed 61 headings, 100 code fences, and 21 references in both the Italian source and the English peer document.

### C17.1.3: Git Flow design doc English translation checkpoint

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S17.1`
- **Actions**: review, checkpoint, verify
- **Depends on**: `T17.1.2`
- **Commit group**: `cg40`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, profile=copilot/check-medium, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace
- **Checks**:
  - English peer document is committed without modifying the Italian source
  - Translation remains 1:1 at the document-structure level
  - PLAN.md and PLAN.dot are regenerated and committed
- **Notes**: Checkpoint closure prepared with the plan-checkpoint-close procedure at Layer 0. REPO_MAP.md is not present in this repository, so freshness is not applicable. The Italian source document remained unchanged.

### D18.1.1: Add conflict resolution scenarios and operational refinements to the Git Flow design doc

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: medium
- **Sprint**: `S18.1`
- **Actions**: document
- **Commit group**: `cg41`
- **Artifacts**: PLAN.yaml, docs/design/gitflow-pr-only-terminal-workflow.md
- **Notes**: Add new sections to the English design document covering: Scenario A (single-PR conflict resolution for feature/bugfix), Scenario B (two-PR conflict resolution for hotfix/release with release-branch exception), conflict classification rules (trivial vs non-trivial), always-draft-PR policy, explicit staging rule (no git add -A), no agent branch deletion rule, and branch protection requirements placeholder.

### D19.1.1: Create git-flow-policy.md governance authority

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: medium
- **Sprint**: `S19.1`
- **Actions**: document
- **Commit group**: `cg42`
- **Artifacts**: PLAN.yaml, agent-os/workflow/git-flow-policy.md
- **Notes**: Extract normative rules from the Git Flow design document into agent-os/workflow/git-flow-policy.md. Covers: branch model definition, workflow invariants, forbidden operations, synchronization rules, conflict resolution model, PR topology, tagging policy, operational refinements, and branch protection enforcement.

### D19.1.2: Register git-flow-policy.md in canonical concern split and add design doc supersession note

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: low
- **Sprint**: `S19.1`
- **Actions**: document
- **Depends on**: `D19.1.1`
- **Commit group**: `cg42`
- **Artifacts**: agent-os/workflow/shared-workflow.md, docs/design/gitflow-pr-only-terminal-workflow.md
- **Notes**: Add git-flow-policy.md to the Canonical Concern Split table in shared-workflow.md. Add a supersession note at the top of the design document indicating which rules have been migrated to the canonical authority.

### C19.1.3: Checkpoint closure — X19 Git Flow governance extraction

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S19.1`
- **Actions**: checkpoint, verify
- **Depends on**: `D19.1.1`, `D19.1.2`
- **Commit group**: `cg42`
- **Notes**: Validate plan, render views, verify that the governance file exists, that the concern split table is updated, and that the design doc carries the supersession note. Close X19, S19.1.

### D20.1.1: Create gitflow-pr-only SKILL.md

- **Type**: D | **Status**: done | **Role**: implementer | **Effort**: high
- **Sprint**: `S20.1`
- **Actions**: implement
- **Commit group**: `cg43`
- **Artifacts**: agent-os/skills/gitflow-pr-only/SKILL.md
- **Notes**: Write the gitflow-pr-only skill with five actions (start, sync, merge, tag, back-merge). Follows the packaging contract from agent-os/skills/README.md, the two-root model from plan-checkpoint-close, and applies the governance rules from agent-os/workflow/git-flow-policy.md. Agent-agnostic with adapter notes for Claude, Codex, Kilo, and Copilot.

### C20.1.2: Checkpoint closure — X20 gitflow-pr-only skill

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S20.1`
- **Actions**: checkpoint, verify
- **Depends on**: `D20.1.1`
- **Commit group**: `cg43`
- **Checks**:
  - validate-plan.py exits 0
  - render-plan.py produces no drift
  - SKILL.md exists at agent-os/skills/gitflow-pr-only/SKILL.md
  - SKILL.md frontmatter contains required fields (id, description, owner, version, compatibility)
- **Notes**: Validate plan, render views, verify skill file exists with correct frontmatter. Close X20, S20.1.

### D21.1.1: Add available-skills table to AGENTS.md § Skills

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: low
- **Sprint**: `S21.1`
- **Actions**: document
- **Commit group**: `cg44`
- **Artifacts**: AGENTS.md
- **Notes**: Add a table listing each skill ID, its trigger conditions, and path to AGENTS.md § Skills. This makes AGENTS.md the single authority for skill discovery — agents read the table instead of scanning the directory.

### C21.1.2: Checkpoint closure — X21 skill discovery table

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S21.1`
- **Actions**: checkpoint, verify
- **Depends on**: `D21.1.1`
- **Commit group**: `cg44`
- **Checks**:
  - validate-plan.py exits 0
  - render-plan.py produces no drift
  - AGENTS.md § Skills contains available-skills table

### D22.1.1: Document planning-to-git mapping in shared-workflow.md

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: medium
- **Sprint**: `S22.1`
- **Actions**: document
- **Commit group**: `cg45`
- **Artifacts**: agent-os/workflow/shared-workflow.md
- **Notes**: Add a Planning-to-Git Mapping section to shared-workflow.md covering: the hierarchy mapping (milestone→branch, sprint→work phase, commit_group→commit, milestone closure→PR merge), the branch naming convention (<family>/<XNN>-<kebab-description>), the agent rule (trigger gitflow-pr-only start on milestone activation), the human override mechanism (planning-only milestones can skip branching), and the hook validation reference. Based on hybrid approach from industry consensus.

### D22.1.2: Add branch naming validation to git-flow-policy.md

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: low
- **Sprint**: `S22.1`
- **Actions**: document
- **Depends on**: `D22.1.1`
- **Commit group**: `cg45`
- **Artifacts**: agent-os/workflow/git-flow-policy.md
- **Notes**: Add a branch naming convention section to git-flow-policy.md that cross-references the mapping in shared-workflow.md. Include the naming pattern and hook validation rule.

### C22.1.3: Checkpoint closure — X22 planning-to-git mapping

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S22.1`
- **Actions**: checkpoint, verify
- **Depends on**: `D22.1.1`, `D22.1.2`
- **Commit group**: `cg45`
- **Checks**:
  - validate-plan.py exits 0
  - render-plan.py produces no drift
  - shared-workflow.md contains Planning-to-Git Mapping section
  - git-flow-policy.md contains Branch Naming Convention section

### M23.1.1: Register gitflow-pr-only as a portable shared skill and propagate discovery metadata

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S23.1`
- **Actions**: implement
- **Commit group**: `cg46`
- **Artifacts**: PLAN.yaml, agent-os/registry/shared-assets.yaml, agent-os/skills/gitflow-pr-only/SKILL.md, agent-os/templates/repo-AGENTS.md.template
- **Notes**: Fix the portability issues identified in review by registering the gitflow-pr-only skill in the canonical shared asset registry, adding the missing Expected Outputs section required by the skill packaging contract, and propagating the available-skills discovery table to the repo AGENTS template used by bootstrapped repos.

### T23.1.2: Validate gitflow skill registry resolution and plan/render consistency

- **Type**: T | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S23.1`
- **Actions**: verify
- **Depends on**: `M23.1.1`
- **Commit group**: `cg46`
- **Checks**:
  - validate-plan.py exits 0
  - render-plan.py produces no drift
  - resolve-shared-asset.py resolves gitflow-pr-only in workspace mode
  - repo-AGENTS.md.template contains the available-skills table entry for gitflow-pr-only

### C23.1.3: Checkpoint closure — X23 gitflow skill portability repairs

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S23.1`
- **Actions**: checkpoint, verify
- **Depends on**: `T23.1.2`
- **Commit group**: `cg46`
- **Notes**: Close the gitflow skill portability repair milestone after registry resolution, packaging-contract compliance, and template propagation are verified. Close X23, S23.1.

### D24.1.1: Refresh human-readable TODO.md for the recent Git Flow work

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: low
- **Sprint**: `S24.1`
- **Actions**: document
- **Commit group**: `cg47`
- **Artifacts**: PLAN.yaml, TODO.md
- **Notes**: Update the non-authoritative personal checklist to reflect the recent completion of the Git Flow governance extraction, gitflow-pr-only skill, discovery metadata, planning-to-git mapping, and portability repair work.

### D25.1.1: Refine portability-model.md first-class tier for workspace-scoped and repo-scoped runtimes

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: medium
- **Sprint**: `S25.1`
- **Actions**: design, document
- **Commit group**: `cg48`
- **Artifacts**: agent-os/workflow/portability-model.md

### M25.1.2: Create repo-CLAUDE.md.template for downstream repo bootstrap

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S25.1`
- **Actions**: implement
- **Depends on**: `D25.1.1`
- **Commit group**: `cg48`
- **Artifacts**: agent-os/templates/repo-CLAUDE.md.template

### M25.1.3: Create repo-CODEX.md.template for downstream repo bootstrap

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S25.1`
- **Actions**: implement
- **Depends on**: `D25.1.1`
- **Commit group**: `cg48`
- **Artifacts**: agent-os/templates/repo-CODEX.md.template

### M25.1.4: Add adapter overrides section to repo-copilot-instructions.md.template

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S25.1`
- **Actions**: implement, refactor
- **Depends on**: `D25.1.1`
- **Commit group**: `cg48`
- **Artifacts**: agent-os/templates/repo-copilot-instructions.md.template

### M25.1.5: Create repo-kilo-rules.md.template for Kilo bootstrap entrypoint

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S25.1`
- **Actions**: implement
- **Depends on**: `D25.1.1`
- **Commit group**: `cg48`
- **Artifacts**: agent-os/templates/repo-kilo-rules.md.template

### M25.2.1: Update bootstrap-repo.sh to generate Claude, Codex, and Kilo entrypoints

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S25.2`
- **Actions**: implement
- **Depends on**: `M25.1.2`, `M25.1.3`, `M25.1.5`
- **Commit group**: `cg49`
- **Artifacts**: agent-os/scripts/bootstrap-repo.sh

### M25.2.2: Update runtime profiles, portability status table, and shared-workflow.md

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S25.2`
- **Actions**: implement, document
- **Depends on**: `M25.2.1`
- **Commit group**: `cg49`
- **Artifacts**: agent-os/workflow/portability-model.md, agent-os/workflow/shared-workflow.md, agent-os/profiles/kilo/check-medium.yaml

### D25.2.3: Update TODO.md for runtime parity completion

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: low
- **Sprint**: `S25.2`
- **Actions**: document
- **Depends on**: `M25.2.2`
- **Commit group**: `cg49`
- **Artifacts**: TODO.md

### T25.2.4: Validate full runtime parity across bootstrap, sync, profiles, and governance

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: medium
- **Sprint**: `S25.2`
- **Actions**: test, verify
- **Depends on**: `D25.2.3`
- **Commit group**: `cg50`
- **Checks**:
  - bootstrap-repo.sh creates CLAUDE.md with adapter overrides
  - bootstrap-repo.sh creates .codex with adapter overrides and sandbox notes
  - bootstrap-repo.sh creates .github/copilot-instructions.md with adapter overrides
  - bootstrap-repo.sh creates .kilocode/rules/governance.md
  - sync-workspace.sh still renders only AGENTS.md, CLAUDE.md, and .codex
  - portability-model.md shows all four runtimes as first-class
  - validate-plan.py exits 0
  - render-plan.py produces no drift
  - pytest -q passes
  - run-gates.sh passes

### C25.2.5: Checkpoint closure — X25 full runtime parity and first-class promotion

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S25.2`
- **Actions**: checkpoint, verify
- **Depends on**: `T25.2.4`
- **Commit group**: `cg50`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, profile=claude/check-medium, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace

### D26.1.1: Extend the portability model for Gemini and Cursor repo-scoped first-class runtimes

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: medium
- **Sprint**: `S26.1`
- **Actions**: design, document
- **Commit group**: `cg51`
- **Artifacts**: agent-os/workflow/portability-model.md

### M26.1.2: Create repo-GEMINI.md.template for downstream repo bootstrap

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S26.1`
- **Actions**: implement
- **Depends on**: `D26.1.1`
- **Commit group**: `cg51`
- **Artifacts**: agent-os/templates/repo-GEMINI.md.template

### M26.1.3: Create repo-cursor-rules.mdc.template for downstream repo bootstrap

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S26.1`
- **Actions**: implement
- **Depends on**: `D26.1.1`
- **Commit group**: `cg51`
- **Artifacts**: agent-os/templates/repo-cursor-rules.mdc.template

### M26.2.1: Update bootstrap-repo.sh to generate Gemini and Cursor entrypoints

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S26.2`
- **Actions**: implement
- **Depends on**: `M26.1.2`, `M26.1.3`
- **Commit group**: `cg52`
- **Artifacts**: agent-os/scripts/bootstrap-repo.sh

### M26.2.2: Add Gemini/Cursor profiles and update runtime compatibility across shared assets, workflow docs, and skills

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: high
- **Sprint**: `S26.2`
- **Actions**: implement, document
- **Depends on**: `M26.2.1`
- **Commit group**: `cg52`
- **Artifacts**: agent-os/workflow/shared-workflow.md, agent-os/registry/shared-assets.yaml, agent-os/profiles/gemini/check-medium.yaml, agent-os/profiles/cursor/check-medium.yaml, agent-os/skills/README.md, agent-os/prompts/README.md, agent-os/skills/plan-checkpoint-close/SKILL.md, agent-os/skills/gitflow-pr-only/SKILL.md

### D26.2.3: Remediate runtime portability drift in README.md and TODO.md

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: low
- **Sprint**: `S26.2`
- **Actions**: document
- **Depends on**: `M26.2.2`
- **Commit group**: `cg52`
- **Artifacts**: README.md, TODO.md

### T26.2.4: Validate six-runtime portability across bootstrap, sync, profiles, and governance

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: medium
- **Sprint**: `S26.2`
- **Actions**: test, verify
- **Depends on**: `D26.2.3`, `M26.2.6`
- **Commit group**: `cg53`
- **Checks**:
  - bootstrap-repo.sh creates CLAUDE.md with adapter overrides
  - bootstrap-repo.sh creates .codex with adapter overrides and sandbox notes
  - bootstrap-repo.sh creates .github/copilot-instructions.md with adapter overrides
  - bootstrap-repo.sh creates .kilocode/rules/governance.md
  - bootstrap-repo.sh creates GEMINI.md with adapter overrides
  - bootstrap-repo.sh creates .cursor/rules/governance.mdc with adapter overrides
  - sync-workspace.sh still renders only AGENTS.md, CLAUDE.md, and .codex
  - portability-model.md shows all six runtimes as first-class
  - validate-plan.py exits 0
  - render-plan.py produces no drift
  - pytest -q passes
  - run-gates.sh passes

### C26.2.5: Checkpoint closure — X26 Gemini and Cursor first-class portability

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S26.2`
- **Actions**: checkpoint, verify
- **Depends on**: `T26.2.4`
- **Commit group**: `cg53`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, profile=codex/check-medium, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace

### M26.2.6: Harden run-gates.sh against stale mypy cache failures

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S26.2`
- **Actions**: implement, refactor
- **Depends on**: `D26.2.3`
- **Commit group**: `cg53`
- **Artifacts**: agent-os/scripts/run-gates.sh

### D27.1.1: Create repo-bootstrap skill SKILL.md with pre-flight, execution, and verification procedure

- **Type**: D | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S27.1`
- **Actions**: document
- **Commit group**: `cg54`
- **Artifacts**: agent-os/skills/repo-bootstrap/SKILL.md
- **Notes**: Create SKILL.md following the skill packaging contract. Wraps bootstrap-repo.sh with pre-flight validation, execution orchestration, post-bootstrap verification, and structured reporting. Supports all six first-class runtimes with adapter notes.

### M27.1.2: Register repo-bootstrap in shared asset registry and propagate discovery metadata

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S27.1`
- **Actions**: implement
- **Depends on**: `D27.1.1`
- **Commit group**: `cg54`
- **Artifacts**: agent-os/registry/shared-assets.yaml, AGENTS.md, agent-os/templates/repo-AGENTS.md.template, TODO.md
- **Notes**: Add the repo-bootstrap skill entry to shared-assets.yaml registry. Add the skill to the available-skills table in AGENTS.md (Level-0) and in repo-AGENTS.md.template (Level-2 template). Check off TODO.md.

### T27.1.3: Validate repo-bootstrap skill packaging and plan consistency

- **Type**: T | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S27.1`
- **Actions**: verify
- **Depends on**: `M27.1.2`
- **Commit group**: `cg54`
- **Checks**:
  - validate-plan.py exits 0
  - render-plan.py produces no drift
  - run-gates.sh passes
  - AGENTS.md contains available-skills entry for repo-bootstrap
  - repo-AGENTS.md.template contains available-skills entry for repo-bootstrap
  - shared-assets.yaml contains repo-bootstrap entry

### C27.1.4: Checkpoint closure — X27 repo-bootstrap skill packaging

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S27.1`
- **Actions**: checkpoint, verify
- **Depends on**: `T27.1.3`
- **Commit group**: `cg54`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, profile=codex/check-medium, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace

### D28.1.1: Create plan-validate-render skill SKILL.md with validation, rendering, drift detection, and reporting procedure

- **Type**: D | **Status**: done | **Role**: implementer | **Effort**: high
- **Sprint**: `S28.1`
- **Actions**: document
- **Depends on**: `C27.1.4`
- **Commit group**: `cg55`
- **Artifacts**: agent-os/skills/plan-validate-render/SKILL.md
- **Notes**: Create SKILL.md following the skill packaging contract. Wraps two scripts: validate-plan.py (17 validation checks, exit 0/1/2) and render-plan.py (PLAN.md + PLAN.dot generation, exit 0/2). Procedure covers two-root resolution, pre-flight checks, validation execution with flag assembly, output interpretation (parse OK/WARNING/ERROR lines, classify hard-fail vs advisory across 17 check categories), rendering, render drift detection via git diff, and structured verdict assembly via check-result-v1 protocol. Adapter notes for all six runtimes.

### M28.2.1: Register plan-validate-render in shared asset registry and propagate discovery metadata

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S28.2`
- **Actions**: implement
- **Depends on**: `D28.1.1`
- **Commit group**: `cg56`
- **Artifacts**: agent-os/registry/shared-assets.yaml, AGENTS.md, agent-os/templates/repo-AGENTS.md.template, TODO.md
- **Notes**: Add the plan-validate-render skill entry to shared-assets.yaml (kind skill, version 0.1.0, six-runtime compatibility). Add a row to the available-skills table in AGENTS.md and in repo-AGENTS.md.template. Check off the plan-validate-render entry in TODO.md.

### T28.2.2: Validate plan-validate-render skill packaging, registry, and plan consistency

- **Type**: T | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S28.2`
- **Actions**: verify
- **Depends on**: `M28.2.1`
- **Commit group**: `cg56`
- **Checks**:
  - agent-os/skills/plan-validate-render/SKILL.md exists with valid YAML frontmatter
  - SKILL.md frontmatter contains id, description, owner, version, and six-entry compatibility
  - SKILL.md body contains Purpose, Two-Root Model, Required Inputs, Expected Outputs, Procedure, Constraints, Failure Handling, and Adapter Notes
  - Adapter Notes covers all six runtimes
  - shared-assets.yaml contains plan-validate-render entry with kind skill
  - AGENTS.md available-skills table contains plan-validate-render row
  - repo-AGENTS.md.template available-skills table contains plan-validate-render row
  - TODO.md shows plan-validate-render checked off
  - validate-plan.py exits 0
  - render-plan.py produces no drift
  - run-gates.sh passes

### C28.2.3: Checkpoint closure — X28 plan-validate-render skill packaging

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S28.2`
- **Actions**: checkpoint, verify
- **Depends on**: `T28.2.2`
- **Commit group**: `cg56`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, profile=codex/check-medium, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace

### D29.1.1: Add X29 tracking to PLAN.yaml and regenerate plan views

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S29.1`
- **Actions**: plan, document
- **Depends on**: `C28.2.3`
- **Commit group**: `cg57`
- **Artifacts**: PLAN.yaml, PLAN.md, PLAN.dot
- **Notes**: Introduce milestone X29, its sprints, executable items, and commit-group boundaries. Regenerate PLAN.md and PLAN.dot so the generated views remain derived from the canonical plan source.

### D29.1.2: Add the canonical no-AI-traces hard rule and propagate AGENTS materializations

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: low
- **Sprint**: `S29.1`
- **Actions**: document
- **Depends on**: `D29.1.1`
- **Commit group**: `cg58`
- **Artifacts**: AGENTS.md, agent-os/templates/repo-AGENTS.md.template, agent-os/templates/workspace-AGENTS.md.template
- **Notes**: Add a single canonical hard rule forbidding signatures, trailers, comments, PR text, or other traces attributable to generative AI or code generation. Propagate it only through AGENTS materialization surfaces.

### D29.1.3: Extend Git Flow policy and skills with no-AI-traces workflow enforcement

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: medium
- **Sprint**: `S29.1`
- **Actions**: document
- **Depends on**: `D29.1.1`
- **Commit group**: `cg58`
- **Artifacts**: agent-os/workflow/git-flow-policy.md, agent-os/skills/gitflow-pr-only/SKILL.md, agent-os/skills/plan-checkpoint-close/SKILL.md, agent-os/skills/repo-bootstrap/SKILL.md
- **Notes**: Add explicit workflow-level prohibitions and cleanliness checks for AI/codegen attribution markers across commits, PR titles and bodies, PR comments, PR reviews, and proposed commit messages.

### D29.1.4: Restore the minimal gitflow-pr-only cleanliness guidance without rewriting the evaluated baseline

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: low
- **Sprint**: `S29.1`
- **Actions**: document
- **Depends on**: `D29.1.3`
- **Commit group**: `cg61`
- **Artifacts**: PLAN.yaml, PLAN.md, PLAN.dot, agent-os/skills/gitflow-pr-only/SKILL.md
- **Notes**: Re-apply only the X29 workflow content cleanliness sub-procedure and the required action hooks in gitflow-pr-only after restoring the develop baseline. Preserve the Claude Code section and the existing normative structure unless a direct conflict requires otherwise.

### C29.1.5: Checkpoint closure — X29 minimal gitflow-pr-only cleanliness restoration

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S29.1`
- **Actions**: checkpoint, verify
- **Depends on**: `D29.1.4`
- **Commit group**: `cg61`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, profile=codex/check-medium, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace
- **Checks**:
  - gitflow-pr-only restores the workflow content cleanliness sub-procedure and action hooks
  - The Claude Code adapter section remains unchanged unless a direct conflict required otherwise
  - PLAN.md and PLAN.dot match PLAN.yaml

### F29.2.1: Fix validate-plan.py fallback when jsonschema is unavailable

- **Type**: F | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S29.2`
- **Actions**: implement, verify
- **Depends on**: `D29.1.2`, `D29.1.3`
- **Commit group**: `cg59`
- **Artifacts**: agent-os/scripts/validate-plan.py, tests/test_validate_plan.py
- **Notes**: Route schema validation through a helper that uses jsonschema when available and the existing subset fallback when it is not, preserving readable failures and non-zero exit codes without crashing.

### F29.2.2: Normalize interpreter portability across .env, docs, Codex entrypoints, and run-gates.sh

- **Type**: F | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S29.2`
- **Actions**: implement, verify
- **Depends on**: `D29.1.2`, `D29.1.3`
- **Commit group**: `cg59`
- **Artifacts**: .env.example, README.md, .codex, agent-os/scripts/run-gates.sh, agent-os/templates/repo-CODEX.md.template, agent-os/templates/workspace-CODEX.md.template, tests/test_shell_scripts.py
- **Notes**: Standardize active repo-tracked instructions on AGENT_PYTHON from .env, make the tracked default generic, and keep Codex sandbox guidance thin and non-host-specific.

### F29.2.3: Add pre-push protection and extend hook/bootstrap enforcement for banned AI attribution markers

- **Type**: F | **Status**: done | **Role**: implementer | **Effort**: high
- **Sprint**: `S29.2`
- **Actions**: implement, verify
- **Depends on**: `D29.1.2`, `D29.1.3`
- **Commit group**: `cg60`
- **Artifacts**: .githooks/commit-msg, .githooks/pre-push, README.md, agent-os/scripts/bootstrap-repo.sh, agent-os/templates/repo-README.md.template, agent-os/templates/repo-commit-msg.template, agent-os/templates/repo-pre-push.template, tests/test_shell_scripts.py
- **Notes**: Keep direct-push protection for main and develop, bootstrap both hooks, and reject narrow AI/codegen attribution markers in commit-message and pushed-text enforcement without blocking legitimate human co-author trailers.

### T29.2.4: Validate portability, hook behavior, validator fallback, bootstrap outputs, and gates

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: medium
- **Sprint**: `S29.2`
- **Actions**: verify
- **Depends on**: `F29.2.1`, `F29.2.2`, `F29.2.3`
- **Commit group**: `cg60`
- **Checks**:
  - validate-plan.py passes with jsonschema installed
  - validate-plan.py falls back cleanly when jsonschema is unavailable
  - commit-msg rejects banned AI/codegen attribution markers and accepts valid messages
  - pre-push rejects direct pushes to main/develop and AI-attributed pushed content
  - bootstrap dry-run and real bootstrap create both local hooks
  - repo README template documents both hooks and the portable interpreter contract
  - pytest -q passes
  - ruff check passes
  - ruff format --check passes
  - mypy --no-incremental passes
  - python -m py_compile passes
  - bash agent-os/scripts/run-gates.sh passes
  - validate-plan.py exits 0
  - render-plan.py produces no drift

### C29.2.5: Checkpoint closure — X29 portability and governance enforcement bugfixes

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S29.2`
- **Actions**: checkpoint, verify
- **Depends on**: `T29.2.4`
- **Commit group**: `cg60`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, profile=codex/check-medium, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace

### D30.1.1: Expand TODO.md into a broader human-facing roadmap and architectural checklist

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: medium
- **Sprint**: `S30.1`
- **Actions**: document
- **Commit group**: `cg62`
- **Artifacts**: PLAN.yaml, TODO.md
- **Notes**: Rewrite TODO.md so it remains a concise personal checklist while expanding plan-scaling, runtime, live-tracking, continuity, routing, integration, observability, issue-intake, validation, and context-economy coverage. Keep it non-normative and avoid repeating canonical rules from AGENTS.md, ARCHITECTURE.md, PLAN.yaml, or the workflow authorities.

### D31.1.1: Track X31 in the legacy root plan and reserve the feature branch before split migration

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: medium
- **Sprint**: `S31.1`
- **Actions**: plan, document
- **Commit group**: `cg63`
- **Artifacts**: PLAN.yaml, PLAN.md, PLAN.dot
- **Notes**: Reserve feature/X31-plan-splitting-archival for the milestone, add both X31 sprints and commit groups to the legacy root PLAN.yaml before any non-generated edits, and record the one-time migration rule: cg63 is the last commit tracked in the root PLAN.yaml before the canonical entrypoint moves to plan/PLAN-index.yaml in cg64.

### M31.1.2: Add split-plan schemas, shared loader, and deterministic split-plan migration tooling

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: high
- **Sprint**: `S31.1`
- **Actions**: design, implement, migrate, verify
- **Depends on**: `D31.1.1`
- **Commit group**: `cg64`
- **Artifacts**: plan/PLAN-index.yaml, plan/PLAN-current.yaml, plan/archive/, agent-os/schemas/plan-index.schema.json, agent-os/schemas/plan-fragment.schema.json, agent-os/scripts/plan_loader.py, agent-os/scripts/split-plan.py, PLAN.md, PLAN.dot
- **Notes**: Introduce the split plan storage model, migrate this repository from the legacy monolithic root PLAN.yaml into plan/PLAN-index.yaml plus plan fragments, and keep aggregate render output deterministic and reviewable.

### T31.1.3: Prove split migration preserves the aggregate logical plan and rendered views

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: medium
- **Sprint**: `S31.1`
- **Actions**: test, verify
- **Depends on**: `M31.1.2`
- **Commit group**: `cg64`
- **Artifacts**: tests/test_plan_loader.py, tests/test_split_plan.py
- **Checks**:
  - split-plan.py deterministically migrates the legacy root plan into plan/
  - aggregate logical-plan content remains equivalent after migration
  - PLAN.md and PLAN.dot remain deterministic aggregate views after migration

### C31.1.4: Checkpoint closure — X31 split-plan model and migration foundation

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S31.1`
- **Actions**: checkpoint, verify
- **Depends on**: `T31.1.3`
- **Commit group**: `cg64`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, profile=codex/check-medium, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace

### M31.2.1: Refactor validate-plan.py onto the shared split-plan loader with active and archived reporting

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: high
- **Sprint**: `S31.2`
- **Actions**: implement, refactor, verify
- **Depends on**: `C31.1.4`
- **Commit group**: `cg65`
- **Artifacts**: agent-os/scripts/plan_loader.py, agent-os/scripts/validate-plan.py, agent-os/skills/plan-validate-render/SKILL.md
- **Notes**: Keep aggregate governance enforcement intact while teaching validation to load plan/PLAN-index.yaml and report separate Active and Archived blocks.

### M31.2.2: Refactor render-plan.py onto the shared split-plan loader without changing aggregate output shape

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S31.2`
- **Actions**: implement, refactor, verify
- **Depends on**: `C31.1.4`
- **Commit group**: `cg65`
- **Artifacts**: agent-os/scripts/render-plan.py, PLAN.md, PLAN.dot

### M31.2.3: Add deterministic archive-plan automation and wire milestone archival into the git-flow path

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: high
- **Sprint**: `S31.2`
- **Actions**: design, implement, verify
- **Depends on**: `M31.2.1`, `M31.2.2`
- **Commit group**: `cg66`
- **Artifacts**: agent-os/scripts/plan_loader.py, agent-os/scripts/archive-plan.py, agent-os/skills/gitflow-pr-only/SKILL.md, plan/PLAN-index.yaml, plan/PLAN-current.yaml, plan/archive/
- **Notes**: Archive a milestone only after its final checkpoint commit group is complete and before the milestone branch is synchronized for PR merge.

### F31.2.4: Propagate the split-plan entrypoint through docs, templates, bootstrap, and runtime adapters

- **Type**: F | **Status**: done | **Role**: implementer | **Effort**: high
- **Sprint**: `S31.2`
- **Actions**: implement, verify
- **Depends on**: `M31.2.3`
- **Commit group**: `cg66`
- **Artifacts**: README.md, AGENTS.md, ARCHITECTURE.md, CLAUDE.md, .codex, agent-os/skills/plan-checkpoint-close/SKILL.md, agent-os/skills/plan-validate-render/SKILL.md, agent-os/skills/repo-bootstrap/SKILL.md, agent-os/workflow/git-automation-policy.md, agent-os/workflow/portability-model.md, agent-os/workflow/shared-workflow.md, agent-os/workflow/git-flow-policy.md, agent-os/templates/, agent-os/scripts/bootstrap-repo.sh
- **Notes**: Update only the canonical path and split-plan workflow surfaces that must change, and keep non-authoritative or previously Claude-shaped skill text edits as small as possible.

### T31.2.5: Extend automated coverage for split loading, migration, archival, rendering, validation, and bootstrap

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: high
- **Sprint**: `S31.2`
- **Actions**: test, verify
- **Depends on**: `F31.2.4`
- **Commit group**: `cg67`
- **Artifacts**: tests/conftest.py, tests/test_archive_plan.py, tests/test_plan_loader.py, tests/test_render_plan.py, tests/test_shell_scripts.py, tests/test_split_plan.py, tests/test_validate_plan.py
- **Checks**:
  - loader tests cover duplicate and missing archive references, empty current plans, and milestone ownership
  - migration tests confirm split-plan.py preserves aggregate logical-plan content
  - validator tests cover Active and Archived reporting plus archive immutability and cross-fragment failures
  - renderer tests confirm aggregate PLAN.md and PLAN.dot output remains stable
  - bootstrap tests confirm new repos start with plan/PLAN-index.yaml and validate successfully

### C31.2.6: Checkpoint closure — X31 split-plan archival and propagation

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S31.2`
- **Actions**: checkpoint, verify
- **Depends on**: `T31.2.5`
- **Commit group**: `cg67`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, profile=codex/check-medium, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace

### D31.3.1: Reopen X31 and record the split-only, warning-strict coverage hardening decisions

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: medium
- **Sprint**: `S31.3`
- **Actions**: plan, document
- **Depends on**: `C31.2.6`
- **Commit group**: `cg68`
- **Artifacts**: plan/PLAN-current.yaml, PLAN.md, PLAN.dot
- **Notes**: Sprint 3 keeps the existing feature branch, applies the >95% per-file coverage target to agent-os/scripts/*.py only, treats Python/test warnings as failures, and removes legacy aggregate PLAN.yaml runtime support from shared Python tooling while keeping split-plan.py as the one-time migration entrypoint.

### M31.3.2: Make the Python gate runnable, warning-strict, and coverage-enforced for agent-os/scripts

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: high
- **Sprint**: `S31.3`
- **Actions**: implement, verify
- **Depends on**: `D31.3.1`
- **Commit group**: `cg69`
- **Artifacts**: pyproject.toml, requirements-dev.txt, agent-os/scripts/run-gates.sh, tests/
- **Notes**: Wire pytest, pytest-cov, branch coverage reporting, warning-as-error handling, and deterministic per-file coverage enforcement into the canonical Python gate for the governed script surface.

### M31.3.3: Remove legacy aggregate PLAN.yaml runtime support from shared Python tooling

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: high
- **Sprint**: `S31.3`
- **Actions**: implement, refactor, verify
- **Depends on**: `D31.3.1`
- **Commit group**: `cg69`
- **Artifacts**: agent-os/scripts/plan_loader.py, agent-os/scripts/render-plan.py, agent-os/scripts/validate-plan.py, tests/
- **Notes**: Shared Python runtime tooling becomes split-plan-only. split-plan.py remains the explicit legacy migration path; no compatibility shims or aggregate runtime fallbacks remain.

### T31.3.4: Add high-signal hardening coverage for plan_loader.py, split-plan.py, and archive-plan.py

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: high
- **Sprint**: `S31.3`
- **Actions**: test, verify
- **Depends on**: `M31.3.2`, `M31.3.3`
- **Commit group**: `cg70`
- **Artifacts**: tests/test_archive_plan.py, tests/test_plan_loader.py, tests/test_split_plan.py
- **Checks**:
  - high-signal composite and edge-case scenarios cover plan_loader.py, split-plan.py, and archive-plan.py above the per-file threshold
  - the targeted modules are warning-free under pytest warning-as-error execution

### M31.3.5: Fix runtime defects exposed by loader, split, and archive hardening tests

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: high
- **Sprint**: `S31.3`
- **Actions**: implement, verify
- **Depends on**: `T31.3.4`
- **Commit group**: `cg70`
- **Artifacts**: agent-os/scripts/plan_loader.py, agent-os/scripts/split-plan.py, agent-os/scripts/archive-plan.py, tests/

### T31.3.6: Add high-signal hardening coverage for validate-plan.py, render-plan.py, and resolve-shared-asset.py

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: high
- **Sprint**: `S31.3`
- **Actions**: test, verify
- **Depends on**: `M31.3.5`
- **Commit group**: `cg71`
- **Artifacts**: tests/test_render_plan.py, tests/test_resolve_shared_asset.py, tests/test_validate_plan.py
- **Checks**:
  - high-signal composite and edge-case scenarios cover validate-plan.py, render-plan.py, and resolve-shared-asset.py above the per-file threshold
  - the targeted modules are warning-free under pytest warning-as-error execution

### M31.3.7: Fix runtime defects exposed by validate, render, and asset-resolution hardening tests

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: high
- **Sprint**: `S31.3`
- **Actions**: implement, verify
- **Depends on**: `T31.3.6`
- **Commit group**: `cg71`
- **Artifacts**: agent-os/scripts/resolve-shared-asset.py, agent-os/scripts/render-plan.py, agent-os/scripts/validate-plan.py, tests/

### C31.3.8: Checkpoint closure — X31 warning-strict coverage hardening

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: medium
- **Sprint**: `S31.3`
- **Actions**: checkpoint, verify
- **Depends on**: `M31.3.7`
- **Commit group**: `cg72`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, profile=codex/check-medium, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace
- **Artifacts**: PLAN.md, PLAN.dot
- **Checks**:
  - pytest passes with zero Python warnings
  - canonical Python gates pass
  - each file under agent-os/scripts/*.py exceeds 95% coverage

### D31.4.1: Reopen X31 for a final closure audit and record deterministic cleanup acceptance criteria

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: medium
- **Sprint**: `S31.4`
- **Actions**: plan, document
- **Depends on**: `C31.3.8`
- **Commit group**: `cg73`
- **Artifacts**: plan/PLAN-current.yaml, PLAN.md, PLAN.dot
- **Notes**: Sprint 4 is closure remediation only. Acceptance requires deterministic test and gate execution, canonical PLAN.md and PLAN.dot outputs sourced from plan/PLAN-index.yaml, zero Python warnings, and a clean worktree immediately after the full closure path.

### T31.4.2: Add closure-audit regression coverage for deterministic generated-view isolation

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: medium
- **Sprint**: `S31.4`
- **Actions**: test, verify
- **Depends on**: `D31.4.1`
- **Commit group**: `cg74`
- **Artifacts**: tests/test_render_plan.py, tests/test_archive_plan.py
- **Checks**:
  - write-capable script entrypoint tests use isolated outputs and do not dirty repo-root PLAN.md or PLAN.dot
  - closure-audit regressions reproduce and prevent generated-view drift discovered after Sprint 3 gate execution

### M31.4.3: Fix final closure drift, consistency gaps, and deterministic generated-view behavior

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S31.4`
- **Actions**: implement, verify
- **Depends on**: `T31.4.2`
- **Commit group**: `cg74`
- **Artifacts**: agent-os/scripts/render-plan.py, tests/, plan/PLAN-index.yaml, PLAN.md, PLAN.dot
- **Notes**: Keep public behavior unchanged while ensuring closure-gate execution leaves the canonical split-plan source, generated views, and tracked metadata fully aligned and review-clean.

### C31.4.4: Checkpoint closure — X31 final closure audit and consistency cleanup

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: medium
- **Sprint**: `S31.4`
- **Actions**: checkpoint, review, verify
- **Depends on**: `M31.4.3`
- **Commit group**: `cg75`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, profile=codex/check-medium, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace
- **Artifacts**: PLAN.md, PLAN.dot
- **Checks**:
  - validate-plan.py, render-plan.py, pytest, and run-gates.sh all pass deterministically
  - canonical PLAN.md and PLAN.dot remain clean after the full closure gate sequence
  - X31 is consistent across plan metadata, generated outputs, and worktree state

### D33.1.1: Track X33 milestone in PLAN-current.yaml and regenerate plan views

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S33.1`
- **Actions**: plan, document
- **Commit group**: `cg78`
- **Artifacts**: plan/PLAN-current.yaml, PLAN.md, PLAN.dot

### D33.1.2: Reply to issue

- **Type**: D | **Status**: done | **Role**: reviewer | **Effort**: medium
- **Sprint**: `S33.1`
- **Actions**: review, document
- **Depends on**: `D33.1.1`
- **Commit group**: `cg79`
- **Notes**: GitHub issue comment only. No file changes.

### D33.1.3: Integrate review suggestions into TODO.md with section priorities

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: medium
- **Sprint**: `S33.1`
- **Actions**: document
- **Depends on**: `D33.1.1`
- **Commit group**: `cg79`
- **Artifacts**: TODO.md

### D33.1.4: Consistency-check TODO.md against codebase state and fix drift

- **Type**: D | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S33.1`
- **Actions**: review, verify
- **Depends on**: `D33.1.3`
- **Commit group**: `cg79`
- **Artifacts**: TODO.md

### C33.1.5: Checkpoint closure — X33

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S33.1`
- **Actions**: checkpoint, verify
- **Depends on**: `D33.1.2`, `D33.1.3`, `D33.1.4`, `F33.1.6`
- **Commit group**: `cg80`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace
- **Artifacts**: PLAN.md, PLAN.dot
- **Checks**:
  - validate-plan.py exits 0
  - render idempotent
  - pytest passes
  - issue
  - TODO.md has per-section priorities
  - no stale or duplicate items in TODO.md

### F33.1.6: Fix hardcoded milestone/item IDs in archive and validate tests

- **Type**: F | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S33.1`
- **Actions**: implement, test
- **Depends on**: `D33.1.4`
- **Commit group**: `cg81`
- **Artifacts**: tests/test_archive_plan.py, tests/test_validate_plan.py
- **Notes**: Tests hardcode X31 and item IDs like C31.2.6 and M31.2.3 from the old PLAN-current.yaml. Since copy_split_plan copies the live plan/ directory, the tests break whenever the active milestone changes. Fix by discovering milestone and item IDs dynamically.

### D34.1.1: Track X34 milestone and regenerate plan views

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S34.1`
- **Actions**: plan, document
- **Commit group**: `cg82`
- **Artifacts**: plan/PLAN-current.yaml, PLAN.md, PLAN.dot

### F34.1.2: Add synthetic fixture helper and fix archive tests for empty-state

- **Type**: F | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S34.1`
- **Actions**: implement, test
- **Depends on**: `D34.1.1`
- **Commit group**: `cg83`
- **Artifacts**: tests/conftest.py, tests/test_archive_plan.py
- **Notes**: Add a synthetic_current_fragment() helper to conftest that builds a minimal valid PLAN-current.yaml fixture. Replace active_milestone_id() with inject_synthetic_fragment() so tests never depend on live data. Add explicit empty-state test for archive-plan behavior.

### F34.1.3: Fix validate tests for empty-state

- **Type**: F | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S34.1`
- **Actions**: implement, test
- **Depends on**: `F34.1.2`
- **Commit group**: `cg83`
- **Artifacts**: tests/test_validate_plan.py
- **Notes**: Fix the two validate tests that index into empty items lists. Use synthetic fixture data injected into the copied plan.

### T34.1.4: Verify tests pass in both empty and non-empty PLAN-current states

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S34.1`
- **Actions**: test, verify
- **Depends on**: `F34.1.3`
- **Commit group**: `cg83`
- **Checks**:
  - pytest passes with empty PLAN-current.yaml
  - pytest passes with non-empty PLAN-current.yaml

### C34.1.5: Checkpoint closure — X34

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S34.1`
- **Actions**: checkpoint, verify
- **Depends on**: `F34.1.2`, `F34.1.3`, `T34.1.4`
- **Commit group**: `cg84`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace
- **Artifacts**: PLAN.md, PLAN.dot
- **Checks**:
  - validate-plan.py exits 0
  - render idempotent
  - pytest passes

### D35.1.1: Track X35 milestone and regenerate plan views

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S35.1`
- **Actions**: plan, document
- **Commit group**: `cg85`
- **Artifacts**: plan/PLAN-current.yaml, PLAN.md, PLAN.dot

### F35.1.2: Repair truncated title in PLAN-X33.yaml and PLAN-index.yaml

- **Type**: F | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S35.1`
- **Actions**: implement, verify
- **Depends on**: `D35.1.1`
- **Commit group**: `cg86`
- **Artifacts**: plan/archive/PLAN-X33.yaml, plan/PLAN-index.yaml

### F35.1.3: Add raw-text unquoted-hash lint to validate-plan.py

- **Type**: F | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S35.1`
- **Actions**: implement, test
- **Depends on**: `D35.1.1`
- **Commit group**: `cg86`

### T35.1.4: Regression tests for hash-in-title lint and round-trip

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: medium
- **Sprint**: `S35.1`
- **Actions**: test, verify
- **Depends on**: `F35.1.3`
- **Commit group**: `cg86`
- **Artifacts**: tests/test_validate_plan.py

### C35.1.5: Checkpoint closure — X35

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S35.1`
- **Actions**: checkpoint, verify
- **Depends on**: `F35.1.2`, `F35.1.3`, `T35.1.4`
- **Commit group**: `cg87`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace
- **Artifacts**: PLAN.md, PLAN.dot
- **Checks**:
  - validate-plan.py exits 0
  - render idempotent
  - pytest passes

### D36.1.1: Track X36 active work and keep generated plan views in sync

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S36.1`
- **Actions**: plan, document
- **Commit group**: `cg88`
- **Artifacts**: plan/PLAN-current.yaml, PLAN.md, PLAN.dot

### M36.1.2: Add --compute-ready query to validate-plan.py

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S36.1`
- **Actions**: implement, verify
- **Depends on**: `D36.1.1`
- **Commit group**: `cg88`
- **Artifacts**: agent-os/scripts/validate-plan.py
- **Notes**: Compute the ready-set from existing dependency semantics and emit a deterministic JSON payload without changing default validation behavior.

### T36.1.3: Add compute-ready helper and CLI regression coverage

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: medium
- **Sprint**: `S36.1`
- **Actions**: test, verify
- **Depends on**: `M36.1.2`
- **Commit group**: `cg88`
- **Artifacts**: tests/test_validate_plan.py

### D36.1.4: Document compute-ready CLI usage in README

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: low
- **Sprint**: `S36.1`
- **Actions**: document
- **Depends on**: `M36.1.2`
- **Commit group**: `cg88`
- **Artifacts**: README.md

### C36.1.5: Checkpoint closure — X36

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S36.1`
- **Actions**: checkpoint, verify
- **Depends on**: `M36.1.2`, `T36.1.3`, `D36.1.4`
- **Commit group**: `cg89`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace
- **Artifacts**: PLAN.md, PLAN.dot
- **Checks**:
  - validate-plan.py exits 0
  - render idempotent
  - pytest passes

### D37.1.1: Track X37 follow-up work and keep generated plan views in sync

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S37.1`
- **Actions**: plan, document
- **Commit group**: `cg90`
- **Artifacts**: plan/PLAN-current.yaml, PLAN.md, PLAN.dot

### F37.1.2: Repair formatter drift in the X36 branch diff

- **Type**: F | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S37.1`
- **Actions**: implement, verify
- **Depends on**: `D37.1.1`
- **Commit group**: `cg90`
- **Artifacts**: agent-os/scripts/validate-plan.py, tests/test_validate_plan.py
- **Notes**: Limit formatting changes to files that are actually part of the branch diff unless verification shows additional branch-owned files need repair.

### T37.1.3: Re-run format-sensitive gates for the X36 branch

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S37.1`
- **Actions**: test, verify
- **Depends on**: `F37.1.2`
- **Commit group**: `cg90`
- **Checks**:
  - ruff format check passes
  - run-gates.sh passes

### D37.1.4: Archive the closed X36 milestone into plan/archive

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S37.1`
- **Actions**: document, verify
- **Depends on**: `T37.1.3`
- **Commit group**: `cg91`
- **Artifacts**: plan/PLAN-current.yaml, plan/PLAN-index.yaml, plan/archive/PLAN-X36.yaml, PLAN.md, PLAN.dot

### C37.1.5: Checkpoint closure — X37

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S37.1`
- **Actions**: checkpoint, verify
- **Depends on**: `D37.1.4`
- **Commit group**: `cg92`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace
- **Artifacts**: PLAN.md, PLAN.dot
- **Checks**:
  - validate-plan.py exits 0
  - render idempotent
  - run-gates.sh passes

### D38.1.1: Archive X37 milestone and update PLAN-index

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S38.1`
- **Actions**: plan, document
- **Commit group**: `cg93`
- **Artifacts**: plan/PLAN-index.yaml, plan/archive/PLAN-X37.yaml

### D38.1.2: Create X38 milestone for Kilo migration

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S38.1`
- **Actions**: plan, document
- **Commit group**: `cg93`
- **Artifacts**: plan/PLAN-current.yaml, PLAN.md, PLAN.dot

### F38.1.3: Replace all .kilocode text references with .kilo

- **Type**: F | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S38.1`
- **Actions**: implement, verify
- **Depends on**: `D38.1.2`
- **Commit group**: `cg94`
- **Artifacts**: README.md, TODO.md, agent-os/workflow/shared-workflow.md, agent-os/workflow/portability-model.md, agent-os/skills/plan-checkpoint-close/SKILL.md, agent-os/skills/repo-bootstrap/SKILL.md, agent-os/skills/plan-validate-render/SKILL.md, agent-os/skills/gitflow-pr-only/SKILL.md, agent-os/scripts/bootstrap-repo.sh, agent-os/profiles/kilo/check-medium.yaml, tests/test_shell_scripts.py
- **Notes**: 23 occurrences across 12 files. Single sed pass. Skip generated and archived files.

### F38.1.4: Create .kilo/rules/governance.md thin entrypoint

- **Type**: F | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S38.1`
- **Actions**: implement
- **Depends on**: `D38.1.2`
- **Commit group**: `cg94`
- **Artifacts**: .kilo/rules/governance.md
- **Notes**: Follow thin adapter pattern from CLAUDE.md and .codex. No duplication of governance rules.

### F38.1.5: Update bootstrap template for .kilo path

- **Type**: F | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S38.1`
- **Actions**: implement, verify
- **Depends on**: `D38.1.2`
- **Commit group**: `cg94`
- **Artifacts**: agent-os/templates/repo-kilo-rules.md.template
- **Notes**: Update output path from .kilocode to .kilo in bootstrap-repo.sh render_template call.

### T38.1.6: Verify text replacements with grep

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S38.1`
- **Actions**: test, verify
- **Depends on**: `F38.1.3`, `F38.1.4`, `F38.1.5`
- **Commit group**: `cg95`
- **Checks**:
  - grep -r '\.kilocode' returns no matches in non-archived, non-generated files

### T38.1.7: Run validation gates

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S38.1`
- **Actions**: test, verify
- **Depends on**: `T38.1.6`
- **Commit group**: `cg95`
- **Checks**:
  - validate-plan.py exits 0
  - run-gates.sh passes
  - pytest passes

### C38.1.8: Checkpoint closure — X38

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S38.1`
- **Actions**: checkpoint, verify
- **Depends on**: `T38.1.7`
- **Commit group**: `cg96`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace
- **Artifacts**: PLAN.md, PLAN.dot
- **Checks**:
  - validate-plan.py exits 0
  - render idempotent
  - run-gates.sh passes

### F38.2.1: Merge .kilo/.gitignore into repo .gitignore

- **Type**: F | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S38.2`
- **Actions**: implement
- **Commit group**: `cg97`
- **Artifacts**: .gitignore
- **Notes**: Consolidate Kilo CLI ignores into repo .gitignore. Plan authority remains in plan/ only.

### C38.2.2: Checkpoint closure — X38 final

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S38.2`
- **Actions**: checkpoint, verify
- **Depends on**: `F38.2.1`
- **Commit group**: `cg98`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace
- **Artifacts**: PLAN.md, PLAN.dot, plan/PLAN-index.yaml
- **Checks**:
  - validate-plan.py exits 0
  - render idempotent

### D39.1.1: Create workspace-sync skill SKILL.md with pre-flight, execution, drift detection, and reporting

- **Type**: D | **Status**: done | **Role**: implementer | **Effort**: high
- **Sprint**: `S39.1`
- **Actions**: document
- **Commit group**: `cg99`
- **Artifacts**: agent-os/skills/workspace-sync/SKILL.md

### M39.1.2: Register workspace-sync in shared asset registry and propagate discovery metadata

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S39.1`
- **Actions**: implement
- **Depends on**: `D39.1.1`
- **Commit group**: `cg100`
- **Artifacts**: agent-os/registry/shared-assets.yaml, AGENTS.md, agent-os/templates/repo-AGENTS.md.template, TODO.md

### T39.1.3: Validate workspace-sync skill packaging, registry, and plan consistency

- **Type**: T | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S39.1`
- **Actions**: verify
- **Depends on**: `M39.1.2`
- **Commit group**: `cg100`
- **Checks**:
  - agent-os/skills/workspace-sync/SKILL.md exists with valid YAML frontmatter
  - SKILL.md frontmatter contains id, description, owner, version, and six-entry compatibility
  - SKILL.md body contains Purpose, Two-Root Model, Required Inputs, Expected Outputs, Procedure, Constraints, Failure Handling, and Adapter Notes
  - Adapter Notes covers all six runtimes
  - shared-assets.yaml contains workspace-sync entry with kind skill
  - AGENTS.md available-skills table contains workspace-sync row
  - repo-AGENTS.md.template available-skills table contains workspace-sync row
  - TODO.md shows workspace-sync checked off
  - validate-plan.py exits 0
  - render-plan.py produces no drift
  - run-gates.sh passes

### C39.1.4: Checkpoint closure -- X39 workspace-sync skill packaging

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S39.1`
- **Actions**: checkpoint, verify
- **Depends on**: `T39.1.3`
- **Commit group**: `cg100`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace

### T39.2.1: Run skill evaluation with 4 test prompts and baseline comparison

- **Type**: T | **Status**: done | **Role**: reviewer | **Effort**: medium
- **Sprint**: `S39.2`
- **Actions**: test, verify
- **Depends on**: `C39.1.4`
- **Commit group**: `cg101`

### M39.2.2: Iterate on SKILL.md based on evaluation feedback

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S39.2`
- **Actions**: implement, refactor
- **Depends on**: `T39.2.1`
- **Commit group**: `cg101`
- **Artifacts**: agent-os/skills/workspace-sync/SKILL.md

### T39.2.3: Re-validate skill after iteration and confirm gates pass

- **Type**: T | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S39.2`
- **Actions**: verify
- **Depends on**: `M39.2.2`
- **Commit group**: `cg101`
- **Checks**:
  - validate-plan.py exits 0
  - render-plan.py produces no drift
  - run-gates.sh passes

### C39.2.4: Checkpoint closure -- S39.2 skill evaluation and iteration

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S39.2`
- **Actions**: checkpoint, verify
- **Depends on**: `T39.2.3`
- **Commit group**: `cg101`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace

### D40.1.1: Create X40 tracking plan and commit groups

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S40.1`
- **Actions**: plan, document
- **Commit group**: `cg102`
- **Artifacts**: plan/PLAN-current.yaml, PLAN.md, PLAN.dot

### M40.1.2: Add structured checks to schema and validator fallback

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S40.1`
- **Actions**: implement, verify
- **Depends on**: `D40.1.1`
- **Commit group**: `cg103`
- **Artifacts**: agent-os/schemas/plan.schema.json, agent-os/scripts/validate-plan.py

### T40.1.3: Add structured check validation test coverage

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: medium
- **Sprint**: `S40.1`
- **Actions**: test, verify
- **Depends on**: `M40.1.2`
- **Commit group**: `cg103`
- **Artifacts**: tests/test_validate_plan.py

### D40.1.4: Document structured checks and update roadmap state

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: low
- **Sprint**: `S40.1`
- **Actions**: document
- **Depends on**: `T40.1.3`
- **Commit group**: `cg104`
- **Artifacts**: agent-os/workflow/item-taxonomy.md, agent-os/skills/plan-checkpoint-close/SKILL.md, agent-os/registry/shared-assets.yaml, TODO.md

### T40.1.5: Validate X40 structured checks feature

- **Type**: T | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S40.1`
- **Actions**: test, verify
- **Depends on**: `D40.1.4`
- **Commit group**: `cg104`
- **Checks**:
  - validate-plan.py exits 0
  - render-plan.py produces no drift
  - run-gates.sh passes

### C40.1.6: Checkpoint closure -- X40 structured checks

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S40.1`
- **Actions**: checkpoint, verify
- **Depends on**: `T40.1.5`
- **Commit group**: `cg104`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace
- **Artifacts**: plan/PLAN-current.yaml, plan/PLAN-index.yaml, plan/archive/PLAN-X40.yaml, PLAN.md, PLAN.dot

### D41.1.1: Create X41 reconciliation tracking plan

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S41.1`
- **Actions**: plan, document
- **Commit group**: `cg105`
- **Artifacts**: plan/PLAN-current.yaml, PLAN.md, PLAN.dot

### F41.1.2: Reconcile stale issue and TODO checklist state

- **Type**: F | **Status**: done | **Role**: implementer | **Effort**: low
- **Sprint**: `S41.1`
- **Actions**: implement, verify
- **Depends on**: `D41.1.1`
- **Commit group**: `cg106`
- **Artifacts**: TODO.md
- **Notes**: Close stale issue #13 externally after verifying PR #32 merged structured checks, and mark the already-implemented compute-ready TODO item as complete.

### T41.1.3: Verify reconciliation state

- **Type**: T | **Status**: done | **Role**: tester | **Effort**: low
- **Sprint**: `S41.1`
- **Actions**: test, verify
- **Depends on**: `F41.1.2`
- **Commit group**: `cg106`
- **Checks**:
  - issue #13 is closed
  - TODO.md marks compute-ready as done
  - validate-plan.py exits 0
  - render-plan.py produces no drift

### C41.1.4: Checkpoint closure -- X41 reconciliation cleanup

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S41.1`
- **Actions**: checkpoint, verify
- **Depends on**: `T41.1.3`
- **Commit group**: `cg107`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace
- **Artifacts**: plan/PLAN-current.yaml, plan/PLAN-index.yaml, plan/archive/PLAN-X41.yaml, PLAN.md, PLAN.dot

### D42.1.1: Open X42 tracking plan and commit groups

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S42.1`
- **Actions**: plan, document
- **Commit group**: `cg108`
- **Artifacts**: plan/PLAN-current.yaml, PLAN.md, PLAN.dot

### M42.1.2: Add on_fail schema, validator fallback, renderer, and tests

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S42.1`
- **Actions**: implement, verify
- **Depends on**: `D42.1.1`
- **Commit group**: `cg109`
- **Artifacts**: agent-os/schemas/plan.schema.json, agent-os/schemas/plan-fragment.schema.json, agent-os/scripts/validate-plan.py, agent-os/scripts/render-plan.py, tests/test_validate_plan.py, tests/test_render_plan.py

### D42.1.3: Document on_fail policy metadata and update roadmap state

- **Type**: D | **Status**: done | **Role**: documenter | **Effort**: low
- **Sprint**: `S42.1`
- **Actions**: document
- **Depends on**: `M42.1.2`
- **Commit group**: `cg109`
- **Artifacts**: agent-os/workflow/item-taxonomy.md, TODO.md, plan/PLAN-current.yaml

### C42.1.4: Checkpoint closure -- X42 on_fail policy metadata

- **Type**: C | **Status**: done | **Role**: reviewer | **Effort**: low
- **Sprint**: `S42.1`
- **Actions**: checkpoint, verify
- **Depends on**: `D42.1.3`
- **Commit group**: `cg110`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace
- **Artifacts**: plan/PLAN-current.yaml, plan/PLAN-index.yaml, plan/archive/PLAN-X42.yaml, PLAN.md, PLAN.dot, tests/test_validate_plan.py
- **Checks**:
  - validate-plan.py exits 0
  - render-plan.py produces no drift
  - run-gates.sh passes

### D43.1.1: Open X43 tracking plan and commit groups

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S43.1`
- **Actions**: plan, document
- **Commit group**: `cg111`
- **Artifacts**: plan/PLAN-current.yaml, PLAN.md, PLAN.dot

### M43.1.2: Warn on dangling on_fail pivot targets

- **Type**: M | **Status**: planned | **Role**: implementer | **Effort**: low
- **Sprint**: `S43.1`
- **Actions**: implement, verify
- **Depends on**: `D43.1.1`
- **Commit group**: `cg112`
- **Artifacts**: agent-os/scripts/validate-plan.py, tests/test_validate_plan.py

### D43.1.3: Document dangling pivot warning semantics

- **Type**: D | **Status**: planned | **Role**: documenter | **Effort**: low
- **Sprint**: `S43.1`
- **Actions**: document
- **Depends on**: `M43.1.2`
- **Commit group**: `cg112`
- **Artifacts**: agent-os/workflow/item-taxonomy.md, plan/PLAN-current.yaml

### C43.1.4: Checkpoint closure -- X43 dangling pivot warning

- **Type**: C | **Status**: planned | **Role**: reviewer | **Effort**: low
- **Sprint**: `S43.1`
- **Actions**: checkpoint, verify
- **Depends on**: `D43.1.3`
- **Commit group**: `cg113`
- **Shared assets**: skill=plan-checkpoint-close, prompt=checkpoint-closure-review, result_protocol=check-result-v1, context_policy=focused, resolution_mode=workspace
- **Artifacts**: plan/PLAN-current.yaml, plan/PLAN-index.yaml, plan/archive/PLAN-X43.yaml, PLAN.md, PLAN.dot
- **Checks**:
  - validate-plan.py exits 0
  - render-plan.py produces no drift
  - run-gates.sh passes
