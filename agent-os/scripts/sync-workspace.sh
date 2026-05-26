#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 [--trust-codex-project] <workspace-root-path>"
}

TRUST_CODEX_PROJECT=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --trust-codex-project)
      TRUST_CODEX_PROJECT=1
      shift
      ;;
    -*)
      echo "ERROR: Unknown option: $1" >&2
      usage
      exit 2
      ;;
    *)
      break
      ;;
  esac
done

WORKSPACE_ROOT="${1:-}"
if [[ -z "$WORKSPACE_ROOT" ]]; then
  usage
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTROL_PLANE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TEMPLATES_DIR="$(cd "$SCRIPT_DIR/../templates" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
CONTROL_PLANE_REF="$(git -C "$CONTROL_PLANE_ROOT" symbolic-ref --quiet --short HEAD 2>/dev/null || true)"
if [[ -z "$CONTROL_PLANE_REF" ]]; then
  CONTROL_PLANE_REF="detached"
fi

CONTROL_PLANE_COMMIT="$(git -C "$CONTROL_PLANE_ROOT" rev-parse --short HEAD 2>/dev/null || echo "unknown")"

echo "INFO: using local control plane state"
echo "INFO:   root: $CONTROL_PLANE_ROOT"
echo "INFO:   ref: $CONTROL_PLANE_REF"
echo "INFO:   commit: $CONTROL_PLANE_COMMIT"

mkdir -p "$WORKSPACE_ROOT"

DATE_UTC="$(date -u +%F)"

render_workspace_template() {
  local src="$1"
  local dst="$2"

  mkdir -p "$(dirname "$dst")"
  sed \
    -e "s|{{DATE}}|$DATE_UTC|g" \
    -e "s|{{CONTROL_PLANE_ROOT}}|$CONTROL_PLANE_ROOT|g" \
    -e "s|{{CONTROL_PLANE_REF}}|$CONTROL_PLANE_REF|g" \
    -e "s|{{CONTROL_PLANE_COMMIT}}|$CONTROL_PLANE_COMMIT|g" \
    "$src" > "$dst"
}

render_workspace_template \
  "$TEMPLATES_DIR/workspace-AGENTS.md.template" \
  "$WORKSPACE_ROOT/AGENTS.md"
render_workspace_template \
  "$TEMPLATES_DIR/workspace-CLAUDE.md.template" \
  "$WORKSPACE_ROOT/CLAUDE.md"
render_workspace_template \
  "$TEMPLATES_DIR/workspace-codex-config.toml.template" \
  "$WORKSPACE_ROOT/.codex/config.toml"

echo "OK: generated $WORKSPACE_ROOT/AGENTS.md"
echo "OK: generated $WORKSPACE_ROOT/CLAUDE.md"
echo "OK: generated $WORKSPACE_ROOT/.codex/config.toml"
echo "INFO: shared assets resolve from CONTROL_PLANE_ROOT in workspace mode"
echo "INFO: vendoring remains optional and explicit via materialize-shared-asset.sh"

if [[ "$TRUST_CODEX_PROJECT" -eq 1 ]]; then
  "$PYTHON_BIN" "$SCRIPT_DIR/trust-codex-project.py" "$WORKSPACE_ROOT"
fi
