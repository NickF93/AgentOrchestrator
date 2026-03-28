#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0"
  echo
  echo "Runs local quality gates for agent-os/scripts/ and tests."
  echo "Set AGENT_PYTHON to control which Python is used (see .env.example)."
  echo "ShellCheck is conditional: if present on PATH it is enforced; if absent it is skipped with a notice."
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Load .env if present (per-workstation overrides).
if [[ -f "${REPO_ROOT}/.env" ]]; then
  # shellcheck disable=SC1091
  source "${REPO_ROOT}/.env"
fi

# Resolve the Python command.
# Priority: AGENT_PYTHON env var > system python3 > error.
if [[ -z "${AGENT_PYTHON:-}" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    AGENT_PYTHON="python3"
  else
    echo "ERROR: AGENT_PYTHON is not set and python3 is not on PATH." >&2
    echo "Copy .env.example to .env and configure AGENT_PYTHON for your workstation." >&2
    exit 1
  fi
fi

# Expand AGENT_PYTHON into an array so "conda run -n env python" works.
# shellcheck disable=SC2206
AGENT_PYTHON_CMD=(${AGENT_PYTHON})

# Verify the Python command works.
if ! "${AGENT_PYTHON_CMD[@]}" -c "import sys" 2>/dev/null; then
  echo "ERROR: AGENT_PYTHON='${AGENT_PYTHON}' is not a working Python command." >&2
  exit 1
fi

run_step() {
  local label="$1"
  shift
  echo "==> ${label}"
  "$@"
}

mapfile -t PY_FILES < <(find agent-os/scripts tests -type f -name '*.py' | sort)

run_step "ruff check" "${AGENT_PYTHON_CMD[@]}" -m ruff check agent-os/scripts tests
run_step "ruff format --check" "${AGENT_PYTHON_CMD[@]}" -m ruff format --check agent-os/scripts tests
run_step "mypy" "${AGENT_PYTHON_CMD[@]}" -m mypy agent-os/scripts tests

if [[ "${#PY_FILES[@]}" -gt 0 ]]; then
  run_step "python -m py_compile" "${AGENT_PYTHON_CMD[@]}" -m py_compile "${PY_FILES[@]}"
fi

run_step "pytest" "${AGENT_PYTHON_CMD[@]}" -m pytest -q

SHELL_SCRIPTS=(
  "agent-os/scripts/bootstrap-repo.sh"
  "agent-os/scripts/materialize-shared-asset.sh"
  "agent-os/scripts/run-gates.sh"
  "agent-os/scripts/sync-workspace.sh"
)

if command -v shellcheck >/dev/null 2>&1; then
  run_step "shellcheck" shellcheck "${SHELL_SCRIPTS[@]}"
else
  echo "==> shellcheck"
  echo "SKIP: shellcheck not installed; bash lint step is conditional and non-blocking."
fi

echo "OK: all local gates passed"
