# .kilo/rules/governance.md — Thin Kilo Adapter

This file is a thin runtime entrypoint for Kilo. It does not define
governance rules.

Canonical authority is bounded in:

- `AGENTS.md`
- `ARCHITECTURE.md`
- `plan/PLAN-index.yaml`
- `agent-os/workflow/*`

## Runtime Notes

- Follow `AGENTS.md` for workflow and operating rules.
- Use `AGENT_PYTHON` from `.env` for Python commands.
- `bash agent-os/scripts/run-gates.sh` for quality gates.
