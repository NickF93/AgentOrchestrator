#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0"
  echo
  echo "Runs local quality gates for agent-os/scripts/ and tests."
  echo "The script prefers the nn-2 Python environment."
  echo "ShellCheck is conditional: if present on PATH it is enforced; if absent it is skipped with a notice."
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

find_nn2_python() {
  if [[ -n "${NN2_PYTHON:-}" && -x "${NN2_PYTHON}" ]]; then
    printf '%s\n' "${NN2_PYTHON}"
    return 0
  fi

  if [[ -n "${CONDA_PREFIX:-}" && "$(basename "${CONDA_PREFIX}")" == "nn-2" && -x "${CONDA_PREFIX}/bin/python" ]]; then
    printf '%s\n' "${CONDA_PREFIX}/bin/python"
    return 0
  fi

  if [[ -f "${HOME}/.conda/environments.txt" ]]; then
    while IFS= read -r env_root; do
      if [[ "${env_root}" == */envs/nn-2 && -x "${env_root}/bin/python" ]]; then
        printf '%s\n' "${env_root}/bin/python"
        return 0
      fi
    done < "${HOME}/.conda/environments.txt"
  fi

  if command -v conda >/dev/null 2>&1; then
    local discovered
    discovered="$(conda run -n nn-2 python -c 'import sys; print(sys.executable)' 2>/dev/null || true)"
    if [[ -n "${discovered}" && -x "${discovered}" ]]; then
      printf '%s\n' "${discovered}"
      return 0
    fi
  fi

  return 1
}

NN2_PYTHON_PATH="$(find_nn2_python || true)"
if [[ -z "${NN2_PYTHON_PATH}" ]]; then
  echo "ERROR: could not locate the nn-2 Python interpreter" >&2
  exit 1
fi

export PYTHON_BIN="${NN2_PYTHON_PATH}"

run_step() {
  local label="$1"
  shift
  echo "==> ${label}"
  "$@"
}

mapfile -t PY_FILES < <(find agent-os/scripts tests -type f -name '*.py' | sort)

run_step "ruff check" "${NN2_PYTHON_PATH}" -m ruff check agent-os/scripts tests
run_step "ruff format --check" "${NN2_PYTHON_PATH}" -m ruff format --check agent-os/scripts tests
run_step "mypy" "${NN2_PYTHON_PATH}" -m mypy agent-os/scripts tests

if [[ "${#PY_FILES[@]}" -gt 0 ]]; then
  run_step "python -m py_compile" "${NN2_PYTHON_PATH}" -m py_compile "${PY_FILES[@]}"
fi

run_step "pytest" "${NN2_PYTHON_PATH}" -m pytest -q

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
