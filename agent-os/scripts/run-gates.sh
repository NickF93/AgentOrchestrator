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

CALLER_AGENT_PYTHON_SET=0
CALLER_AGENT_PYTHON=""
if [[ "${AGENT_PYTHON+x}" == "x" ]]; then
  CALLER_AGENT_PYTHON_SET=1
  CALLER_AGENT_PYTHON="${AGENT_PYTHON}"
fi

# Load .env if present (per-workstation overrides).
if [[ -f "${REPO_ROOT}/.env" ]]; then
  # shellcheck disable=SC1091
  source "${REPO_ROOT}/.env"
fi

# Resolve the Python command.
# Priority: caller-supplied AGENT_PYTHON env var > .env > system python3 > error.
if [[ "${CALLER_AGENT_PYTHON_SET}" -eq 1 ]]; then
  AGENT_PYTHON="${CALLER_AGENT_PYTHON}"
fi

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
# Use a deterministic mypy invocation that does not depend on any stale
# incremental cache format left over from a different mypy version.
run_step "mypy" "${AGENT_PYTHON_CMD[@]}" -m mypy --no-incremental agent-os/scripts tests

if [[ "${#PY_FILES[@]}" -gt 0 ]]; then
  run_step "python -m py_compile" "${AGENT_PYTHON_CMD[@]}" -m py_compile "${PY_FILES[@]}"
fi

COVERAGE_JSON="$(mktemp "${TMPDIR:-/tmp}/agent-os-coverage.XXXXXX.json")"
cleanup() {
  rm -f "${COVERAGE_JSON}"
}
trap cleanup EXIT

run_step \
  "pytest with coverage" \
  "${AGENT_PYTHON_CMD[@]}" \
  -m pytest \
  --cov=agent-os/scripts \
  --cov-branch \
  --cov-report=term-missing \
  --cov-report="json:${COVERAGE_JSON}"

run_step \
  "coverage per-file threshold >95%" \
  "${AGENT_PYTHON_CMD[@]}" \
  -c '
import json
import sys
from pathlib import Path

report_path = Path(sys.argv[1])
repo_root = Path(sys.argv[2]).resolve()
report = json.loads(report_path.read_text(encoding="utf-8"))
files = report.get("files", {})

def normalize(path_text: str) -> str:
    path = Path(path_text)
    resolved = path if path.is_absolute() else (repo_root / path).resolve()
    try:
        return resolved.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()

coverage_by_file = {
    normalize(path_text): payload.get("summary", {}).get("percent_covered", 0.0)
    for path_text, payload in files.items()
}
expected = sorted(
    path.relative_to(repo_root).as_posix()
    for path in (repo_root / "agent-os" / "scripts").rglob("*.py")
)
failing = [
    (path_text, coverage_by_file.get(path_text, 0.0))
    for path_text in expected
    if coverage_by_file.get(path_text, 0.0) <= 95.0
]
if failing:
    print("ERROR: per-file coverage threshold is >95% for agent-os/scripts/*.py", file=sys.stderr)
    for path_text, percent in failing:
        print(f"  - {path_text}: {percent:.2f}%", file=sys.stderr)
    raise SystemExit(1)
print("OK: all agent-os/scripts/*.py files exceed 95% coverage")
' \
  "${COVERAGE_JSON}" \
  "${REPO_ROOT}"

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
