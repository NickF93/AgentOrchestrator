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
| X4 | X | Governance Baseline Hardening | done |
| X5 | X | Tracking Discipline and Canonical Consistency Hardening | in_progress |

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
| `D1.1.1` | `D` | Create non-authoritative docs directory and initialize .gitignore | done | Moved startup documentation to docs/design/ as non-authoritative reference material and added baseline ignore rules for local/editor/runtime artifacts. |
| `D1.1.2` | `D` | Create architecture review and open-questions document | done | Captures what is confirmed, what is ambiguous, and five open questions (Q1.1.1–Q1.1.5) that must be decided before schema and scripts can be written. |
| `D1.1.3` | `D` | Enforce commit message contract in Layer-0 governance | done | Added mandatory commit title contract: <type>(<scope>): <description> with optional body/footer sections. This is a Layer-0 global rule. |
| `D1.1.4` | `D` | Strengthen and align commit body/footer recommendation wording | done | Standardized wording to: "Optional body and footer sections are strongly suggested, especially for medium or large commits." across all authoritative governance surfaces. |
| `Q1.1.1` | `Q` | Decide: PLAN.yaml required fields and state transition rules | done | Decision recorded from interactive governance alignment. |
| `Q1.1.2` | `Q` | Decide: Level-1 runtime materialization strategy | done | Decision recorded from interactive governance alignment. |
| `Q1.1.3` | `Q` | Decide: control-plane release and consumption model | done | Decision recorded from interactive governance alignment. |
| `Q1.1.4` | `Q` | Decide: scope field format and collision-detection semantics | done | Decision recorded from interactive governance alignment. |
| `Q1.1.5` | `Q` | Decide: tooling failure semantics and commit hygiene rules | done | Decision recorded from interactive governance alignment. |
| `M1.1.1` | `M` | Create agent-os/workflow/ documentation files | done | Content sourced from docs/design/documento-architetturale-control-plane-coding-agents.md and docs/design/gitflow_pr_only_terminal_workflow.md. Do NOT duplicate content; these files are the canonical split of the monolithic architecture doc. |
| `M1.1.6` | `M` | Create root governance files for this Level-0 repository | done | This repository is itself the Level-0 control-plane OS. Root AGENTS.md and ARCHITECTURE.md define local authority mapping and structural constraints for building and evolving agent-os/. |
| `M1.1.2` | `M` | Create agent-os/schemas/plan.schema.json | done | JSON Schema (draft-2020-12) for PLAN.yaml. Must encode required fields, enum values for type/status/role/effort/actions, and scope field format as decided in Q1.1.1 and Q1.1.4. Must be self-consistent so that this PLAN.yaml passes validation once M1.1.4 is done. |
| `M1.1.3` | `M` | Create agent-os/templates/ (AGENTS, ARCHITECTURE, REPO_MAP, PLAN) | done | Templates use {{REPO_NAME}}, {{DATE}}, {{OWNER}} placeholders. Level-1 files are generated from these templates by sync-workspace.sh (per Q1.1.2 decision). Each template must include the canonical source rule and authority map header so generated files self-document their origin. |
| `M1.1.4` | `M` | Create agent-os/scripts/render-plan.py and validate-plan.py | done | validate-plan.py: validates PLAN.yaml against plan.schema.json; checks state transition legality, dangling depends_on, container items in depends_on, required fields. Exits non-zero on any hard-fail. render-plan.py: deterministic PLAN.yaml → PLAN.md + PLAN.yaml → PLAN.dot. Both scripts must be idempotent and callable standalone. |
| `M1.1.5` | `M` | Create agent-os/scripts/bootstrap-repo.sh and sync-workspace.sh | done | bootstrap-repo.sh: instantiates a new repo-local layer (Level-2) from templates. Supports --dry-run. Emits a PLAN.yaml seed from the template. sync-workspace.sh: pulls latest from control plane (per Q1.1.3 decision) and regenerates Level-1 runtime files from Level-0 templates (per Q1.1.2 decision). |
| `T1.1.1` | `T` | Validate this PLAN.yaml against plan.schema.json | done | This is the self-validation gate: the control plane must validate its own plan before it can claim to be a working control plane. |
| `T1.1.2` | `T` | Dry-run bootstrap-repo.sh on a temp path | done | Must confirm bootstrap is idempotent and does not write to disk in dry-run mode. A second run on the same target must produce identical output. |
| `T1.1.3` | `T` | Generate PLAN.md and PLAN.dot from this PLAN.yaml | done | PLAN.md and PLAN.dot are committed in the same commit as this PLAN.yaml update, not as separate commits (per Q1.1.5 decision). |
| `C1.1.1` | `C` | Sprint 1 checkpoint — Level-0 scaffold complete and self-validating | done | After this checkpoint, the control plane is operational and able to bootstrap its first real target repo (Level-2) as Sprint 2 work. |

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
| `D2.1.1` | `D` | Enforce missing architectural doc rules in workflow governance files | done | Close compliance gaps between the architecture doc (§6.2–6.4, §11.3–11.4, §4.2, §13.2) and the authoritative workflow files. Adds: full authority concern table, precedence rule, non-duplication rule, single-writer rule detail, grouping and collision rules, deferred automation list, and Kilo portability mapping example. |
| `D2.1.2` | `D` | Create English translation of the Italian architectural document | done | 1:1 English translation of docs/design/documento-architetturale-control-plane-coding-agents.md, placed in the same directory. Structural fidelity to the original is required: all sections, tables, code blocks, and math equations must be preserved verbatim in structure. |
| `D2.1.3` | `D` | Simplify commit title contract by removing item ID from header | done | Updated commit title contract everywhere from the item-ID-inclusive format to <type>(<scope>): <description> while keeping body/footer recommendation unchanged. |
| `D2.1.4` | `D` | Define prompts directory contract and lifecycle | done | Closes G1 by specifying prompt file format, required metadata, versioning, and lifecycle triggers in authoritative workflow guidance. |
| `D2.1.5` | `D` | Define skills packaging contract and compatibility mapping | done | Closes G2 by defining a neutral skill package format and adapter mapping expectations across agent runtimes. |
| `D2.1.6` | `D` | Define REPO_MAP freshness policy and update triggers | done | Closes G3 by defining ownership, refresh triggers, and freshness metadata for REPO_MAP.md so map staleness is detectable and reviewable. |
| `D2.1.7` | `D` | Define ADR template, numbering, and lifecycle states | done | Closes G4 by introducing a canonical ADR template with lifecycle states and linkage guidance to PLAN decision items. |
| `D2.1.8` | `D` | Define canonical-authority conflict detection and recovery procedure | done | Closes G5 by defining conflict detection, recovery actions, escalation, and a safety gate before Phase B automation. |
| `C2.1.1` | `C` | Architecture finalization checkpoint — close review gaps G1-G5 | done | Marks architecture baseline as finalized for Level-0 governance, with unresolved work shifted from open questions into explicit governed policy. |

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
- Status: in_progress
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
Status: planned

| ID | Type | Description | Status | Notes |
| --- | --- | --- | --- | --- |
| `D5.2.1` | `D` | Propagate tracking-first and commit traceability rules into Level-1 and Level-2 templates | planned | Makes the rule visible beyond Level-0 so workspace runtime files and bootstrapped repo-local governance files carry the same hard gate. |
| `M5.2.2` | `M` | Enforce commit title and Refs footer contract in repo-local tooling | planned | Extends the local commit hook to require both the canonical title contract and a Refs footer with PLAN item IDs plus exactly one commit_group, and bootstraps the same guard into downstream repos. |
| `M5.2.3` | `M` | Repair template drift, local provenance, and fresh-checkout operator flow | planned | Aligns ADR and REPO_MAP templates with canonical lifecycle policy, removes implicit remote mutation from workspace sync, stamps workspace files with local provenance, and makes the repo self-hosted with an explicit dependency manifest and runnable operator documentation. |
| `T5.2.4` | `T` | Validate nn-2 flow for plan tooling, bootstrap, sync, and hook enforcement | planned |  |
| `C5.2.5` | `C` | Consistency repair checkpoint — cross-layer rules and operator flow aligned | planned |  |

## Commit Groups

| ID | Title | Items |
|---|---|---|
| cg7 | Governance compliance — propagate architectural rules to workflow docs | `D2.1.1`, `D2.1.2`, `D2.1.3` |
| cg8 | Architecture finalization — close specification gaps G1-G5 | `D2.1.4`, `D2.1.5`, `D2.1.6`, `D2.1.7`, `D2.1.8`, `C2.1.1` |
| cg0 | Repository bootstrap hygiene | `D1.1.1` |
| cg1 | Review and planning artifacts | `D1.1.2` |
| cg6 | Governance hardening updates | `D1.1.3`, `D1.1.4` |
| cg2 | Decision gates — Q1.1.1 through Q1.1.5 answers recorded | `Q1.1.1`, `Q1.1.2`, `Q1.1.3`, `Q1.1.4`, `Q1.1.5` |
| cg3 | Scaffold — workflow docs, schema, templates | `M1.1.1`, `M1.1.2`, `M1.1.3`, `M1.1.6` |
| cg4 | Scripts — render, validate, bootstrap, sync | `M1.1.4`, `M1.1.5` |
| cg5 | Sprint 1 closure — tests and checkpoint | `T1.1.1`, `T1.1.2`, `T1.1.3`, `C1.1.1` |
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

## Item Details

### D1.1.1: Create non-authoritative docs directory and initialize .gitignore

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: document
- **Commit group**: `cg0`
- **Artifacts**: .gitignore, docs/design/documento-architetturale-control-plane-coding-agents.md, docs/design/gitflow_pr_only_terminal_workflow.md, docs/design/REVIEW-AND-OPEN-QUESTIONS.md
- **Notes**: Moved startup documentation to docs/design/ as non-authoritative reference material and added baseline ignore rules for local/editor/runtime artifacts.

### D1.1.2: Create architecture review and open-questions document

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: document
- **Commit group**: `cg1`
- **Artifacts**: docs/design/REVIEW-AND-OPEN-QUESTIONS.md
- **Notes**: Captures what is confirmed, what is ambiguous, and five open questions (Q1.1.1–Q1.1.5) that must be decided before schema and scripts can be written.

### D1.1.3: Enforce commit message contract in Layer-0 governance

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: document, checkpoint
- **Commit group**: `cg6`
- **Artifacts**: AGENTS.md, agent-os/workflow/shared-workflow.md, agent-os/workflow/git-automation-policy.md, agent-os/templates/repo-AGENTS.md.template
- **Notes**: Added mandatory commit title contract: <type>(<scope>): <description> with optional body/footer sections. This is a Layer-0 global rule.

### D1.1.4: Strengthen and align commit body/footer recommendation wording

- **Type**: D | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: document
- **Commit group**: `cg6`
- **Artifacts**: AGENTS.md, agent-os/workflow/shared-workflow.md, agent-os/workflow/git-automation-policy.md, agent-os/templates/repo-AGENTS.md.template
- **Notes**: Standardized wording to: "Optional body and footer sections are strongly suggested, especially for medium or large commits." across all authoritative governance surfaces.

### Q1.1.1: Decide: PLAN.yaml required fields and state transition rules

- **Type**: Q | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: decide
- **Depends on**: `D1.1.2`
- **Commit group**: `cg2`
- **Decision**: Required executable fields are id, type, title, status, role, effort. State machine is planned -> ready -> in_progress -> review -> verified -> done, with blocked as a side-state reachable from active states. Container items (X, S) must not appear in depends_on. verified means all required checks pass; done means verified plus repository bookkeeping closure (committed, optionally pushed).
- **Notes**: Decision recorded from interactive governance alignment.

### Q1.1.2: Decide: Level-1 runtime materialization strategy

- **Type**: Q | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: decide
- **Depends on**: `D1.1.2`
- **Commit group**: `cg2`
- **Decision**: Level-1 runtime files are fully generated by sync-workspace.sh from Level-0 templates. Generated files are read-only outputs and must include an AUTO-GENERATED header.
- **Notes**: Decision recorded from interactive governance alignment.

### Q1.1.3: Decide: control-plane release and consumption model

- **Type**: Q | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: decide
- **Depends on**: `D1.1.2`
- **Commit group**: `cg2`
- **Decision**: MVP consumption tracks the control-plane main branch. Tag-based pinning will be introduced when a second external consumer is onboarded.
- **Notes**: Decision recorded from interactive governance alignment.

### Q1.1.4: Decide: scope field format and collision-detection semantics

- **Type**: Q | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: decide
- **Depends on**: `D1.1.2`
- **Commit group**: `cg2`
- **Decision**: scope is a repository-relative path prefix. validate-plan.py emits a warning (not hard-fail) when two in_progress items share a scope prefix.
- **Notes**: Decision recorded from interactive governance alignment.

### Q1.1.5: Decide: tooling failure semantics and commit hygiene rules

- **Type**: Q | **Status**: done | **Role**: orchestrator | **Effort**: low
- **Sprint**: `S1.1`
- **Actions**: decide
- **Depends on**: `D1.1.2`
- **Commit group**: `cg2`
- **Decision**: validate-plan.py hard-fails on missing required fields, unknown enum values, dangling depends_on references, and container types (X, S) in depends_on. Other policy checks can be warnings.
- **Notes**: Decision recorded from interactive governance alignment.

### M1.1.1: Create agent-os/workflow/ documentation files

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S1.1`
- **Actions**: implement, document
- **Depends on**: `Q1.1.1`, `Q1.1.2`, `Q1.1.3`
- **Commit group**: `cg3`
- **Artifacts**: agent-os/workflow/shared-workflow.md, agent-os/workflow/item-taxonomy.md, agent-os/workflow/lifecycle.md, agent-os/workflow/git-automation-policy.md, agent-os/workflow/portability-model.md
- **Notes**: Content sourced from docs/design/documento-architetturale-control-plane-coding-agents.md and docs/design/gitflow_pr_only_terminal_workflow.md. Do NOT duplicate content; these files are the canonical split of the monolithic architecture doc.

### M1.1.6: Create root governance files for this Level-0 repository

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S1.1`
- **Actions**: design, implement, document
- **Depends on**: `Q1.1.1`, `Q1.1.2`, `Q1.1.3`
- **Commit group**: `cg3`
- **Artifacts**: AGENTS.md, ARCHITECTURE.md
- **Notes**: This repository is itself the Level-0 control-plane OS. Root AGENTS.md and ARCHITECTURE.md define local authority mapping and structural constraints for building and evolving agent-os/.

### M1.1.2: Create agent-os/schemas/plan.schema.json

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S1.1`
- **Actions**: design, implement
- **Depends on**: `Q1.1.1`, `Q1.1.4`
- **Commit group**: `cg3`
- **Artifacts**: agent-os/schemas/plan.schema.json
- **Notes**: JSON Schema (draft-2020-12) for PLAN.yaml. Must encode required fields, enum values for type/status/role/effort/actions, and scope field format as decided in Q1.1.1 and Q1.1.4. Must be self-consistent so that this PLAN.yaml passes validation once M1.1.4 is done.

### M1.1.3: Create agent-os/templates/ (AGENTS, ARCHITECTURE, REPO_MAP, PLAN)

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S1.1`
- **Actions**: design, implement
- **Depends on**: `Q1.1.2`, `M1.1.1`
- **Commit group**: `cg3`
- **Artifacts**: agent-os/templates/repo-AGENTS.md.template, agent-os/templates/repo-ARCHITECTURE.md.template, agent-os/templates/repo-REPO_MAP.md.template, agent-os/templates/PLAN.yaml.template
- **Notes**: Templates use {{REPO_NAME}}, {{DATE}}, {{OWNER}} placeholders. Level-1 files are generated from these templates by sync-workspace.sh (per Q1.1.2 decision). Each template must include the canonical source rule and authority map header so generated files self-document their origin.

### M1.1.4: Create agent-os/scripts/render-plan.py and validate-plan.py

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: high
- **Sprint**: `S1.1`
- **Actions**: implement
- **Depends on**: `M1.1.2`, `Q1.1.5`
- **Commit group**: `cg4`
- **Artifacts**: agent-os/scripts/render-plan.py, agent-os/scripts/validate-plan.py
- **Notes**: validate-plan.py: validates PLAN.yaml against plan.schema.json; checks state transition legality, dangling depends_on, container items in depends_on, required fields. Exits non-zero on any hard-fail. render-plan.py: deterministic PLAN.yaml → PLAN.md + PLAN.yaml → PLAN.dot. Both scripts must be idempotent and callable standalone.

### M1.1.5: Create agent-os/scripts/bootstrap-repo.sh and sync-workspace.sh

- **Type**: M | **Status**: done | **Role**: implementer | **Effort**: medium
- **Sprint**: `S1.1`
- **Actions**: implement
- **Depends on**: `M1.1.3`, `Q1.1.3`
- **Commit group**: `cg4`
- **Artifacts**: agent-os/scripts/bootstrap-repo.sh, agent-os/scripts/sync-workspace.sh
- **Notes**: bootstrap-repo.sh: instantiates a new repo-local layer (Level-2) from templates. Supports --dry-run. Emits a PLAN.yaml seed from the template. sync-workspace.sh: pulls latest from control plane (per Q1.1.3 decision) and regenerates Level-1 runtime files from Level-0 templates (per Q1.1.2 decision).

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

- **Type**: D | **Status**: planned | **Role**: documenter | **Effort**: medium
- **Sprint**: `S5.2`
- **Actions**: document, review
- **Depends on**: `C5.1.3`
- **Commit group**: `cg21`
- **Artifacts**: agent-os/templates/repo-AGENTS.md.template, agent-os/templates/repo-README.md.template, agent-os/templates/workspace-AGENTS.md.template, agent-os/templates/workspace-CLAUDE.md.template
- **Notes**: Makes the rule visible beyond Level-0 so workspace runtime files and bootstrapped repo-local governance files carry the same hard gate.

### M5.2.2: Enforce commit title and Refs footer contract in repo-local tooling

- **Type**: M | **Status**: planned | **Role**: implementer | **Effort**: medium
- **Sprint**: `S5.2`
- **Actions**: implement, verify
- **Depends on**: `C5.1.3`
- **Commit group**: `cg21`
- **Artifacts**: .githooks/commit-msg, agent-os/scripts/bootstrap-repo.sh, agent-os/templates/repo-commit-msg.template
- **Notes**: Extends the local commit hook to require both the canonical title contract and a Refs footer with PLAN item IDs plus exactly one commit_group, and bootstraps the same guard into downstream repos.

### M5.2.3: Repair template drift, local provenance, and fresh-checkout operator flow

- **Type**: M | **Status**: planned | **Role**: implementer | **Effort**: medium
- **Sprint**: `S5.2`
- **Actions**: implement, refactor, verify
- **Depends on**: `C5.1.3`
- **Commit group**: `cg21`
- **Artifacts**: .gitignore, ARCHITECTURE.md, README.md, agent-os/scripts/render-plan.py, agent-os/scripts/sync-workspace.sh, agent-os/scripts/validate-plan.py, agent-os/templates/repo-ADR.md.template, agent-os/templates/repo-ARCHITECTURE.md.template, agent-os/templates/repo-REPO_MAP.md.template, agent-os/templates/workspace-AGENTS.md.template, agent-os/templates/workspace-CLAUDE.md.template, requirements.txt
- **Notes**: Aligns ADR and REPO_MAP templates with canonical lifecycle policy, removes implicit remote mutation from workspace sync, stamps workspace files with local provenance, and makes the repo self-hosted with an explicit dependency manifest and runnable operator documentation.

### T5.2.4: Validate nn-2 flow for plan tooling, bootstrap, sync, and hook enforcement

- **Type**: T | **Status**: planned | **Role**: tester | **Effort**: low
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

- **Type**: C | **Status**: planned | **Role**: reviewer | **Effort**: low
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
