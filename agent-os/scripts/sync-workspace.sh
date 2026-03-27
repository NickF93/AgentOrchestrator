#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <workspace-root-path>"
}

WORKSPACE_ROOT="${1:-}"
if [[ -z "$WORKSPACE_ROOT" ]]; then
  usage
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTROL_PLANE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TEMPLATES_DIR="$(cd "$SCRIPT_DIR/../templates" && pwd)"
CONTROL_PLANE_REF="main"

if git -C "$CONTROL_PLANE_ROOT" remote get-url origin >/dev/null 2>&1; then
  echo "INFO: pulling latest control plane from main"
  git -C "$CONTROL_PLANE_ROOT" pull --ff-only origin main || {
    echo "WARN: pull failed, continuing with local control plane state"
  }
else
  echo "INFO: no origin remote configured, using local control plane state"
fi

mkdir -p "$WORKSPACE_ROOT"

DATE_UTC="$(date -u +%F)"

render_workspace_template() {
  local src="$1"
  local dst="$2"

  sed \
    -e "s|{{DATE}}|$DATE_UTC|g" \
    -e "s|{{CONTROL_PLANE_ROOT}}|$CONTROL_PLANE_ROOT|g" \
    -e "s|{{CONTROL_PLANE_REF}}|$CONTROL_PLANE_REF|g" \
    "$src" > "$dst"
}

render_workspace_template \
  "$TEMPLATES_DIR/workspace-AGENTS.md.template" \
  "$WORKSPACE_ROOT/AGENTS.md"
render_workspace_template \
  "$TEMPLATES_DIR/workspace-CLAUDE.md.template" \
  "$WORKSPACE_ROOT/CLAUDE.md"

echo "OK: generated $WORKSPACE_ROOT/AGENTS.md"
echo "OK: generated $WORKSPACE_ROOT/CLAUDE.md"
