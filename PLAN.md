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

## Sprints

| ID | Parent | Type | Title | Status |
|---|---|---|---|---|
| S1.1 | X1 | S | Sprint 1 — Decisions, scaffold, schema, workflow docs, templates, scripts | done |
| S2.1 | X2 | S | Sprint 1 — Propagate missing architectural rules to governance files | done |

## Items

| ID | Parent | Type | Status | Role | Effort | Commit Group | Depends On |
|---|---|---|---|---|---|---|---|
| C1.1.1 | S1.1 | C | done | reviewer | low | cg5 | T1.1.1, T1.1.2, T1.1.3 |
| D1.1.1 | S1.1 | D | done | orchestrator | low | cg0 |  |
| D1.1.2 | S1.1 | D | done | orchestrator | low | cg1 |  |
| D1.1.3 | S1.1 | D | done | orchestrator | low | cg6 |  |
| D1.1.4 | S1.1 | D | done | orchestrator | low | cg6 |  |
| D2.1.1 | S2.1 | D | done | orchestrator | medium | cg7 |  |
| D2.1.2 | S2.1 | D | done | orchestrator | medium | cg7 |  |
| M1.1.1 | S1.1 | M | done | implementer | medium | cg3 | Q1.1.1, Q1.1.2, Q1.1.3 |
| M1.1.2 | S1.1 | M | done | implementer | medium | cg3 | Q1.1.1, Q1.1.4 |
| M1.1.3 | S1.1 | M | done | implementer | medium | cg3 | Q1.1.2, M1.1.1 |
| M1.1.4 | S1.1 | M | done | implementer | high | cg4 | M1.1.2, Q1.1.5 |
| M1.1.5 | S1.1 | M | done | implementer | medium | cg4 | M1.1.3, Q1.1.3 |
| M1.1.6 | S1.1 | M | done | implementer | medium | cg3 | Q1.1.1, Q1.1.2, Q1.1.3 |
| Q1.1.1 | S1.1 | Q | done | orchestrator | low | cg2 | D1.1.2 |
| Q1.1.2 | S1.1 | Q | done | orchestrator | low | cg2 | D1.1.2 |
| Q1.1.3 | S1.1 | Q | done | orchestrator | low | cg2 | D1.1.2 |
| Q1.1.4 | S1.1 | Q | done | orchestrator | low | cg2 | D1.1.2 |
| Q1.1.5 | S1.1 | Q | done | orchestrator | low | cg2 | D1.1.2 |
| T1.1.1 | S1.1 | T | done | tester | low | cg5 | M1.1.2, M1.1.4 |
| T1.1.2 | S1.1 | T | done | tester | low | cg5 | M1.1.5 |
| T1.1.3 | S1.1 | T | done | tester | low | cg5 | M1.1.4 |

## Commit Groups

| ID | Title | Items |
|---|---|---|
| cg0 | Repository bootstrap hygiene | D1.1.1 |
| cg1 | Review and planning artifacts | D1.1.2 |
| cg2 | Decision gates — Q1.1.1 through Q1.1.5 answers recorded | Q1.1.1, Q1.1.2, Q1.1.3, Q1.1.4, Q1.1.5 |
| cg3 | Scaffold — workflow docs, schema, templates | M1.1.1, M1.1.2, M1.1.3, M1.1.6 |
| cg4 | Scripts — render, validate, bootstrap, sync | M1.1.4, M1.1.5 |
| cg5 | Sprint 1 closure — tests and checkpoint | T1.1.1, T1.1.2, T1.1.3, C1.1.1 |
| cg6 | Governance hardening updates | D1.1.3, D1.1.4 |
| cg7 | Governance compliance — propagate architectural rules to workflow docs | D2.1.1, D2.1.2 |
