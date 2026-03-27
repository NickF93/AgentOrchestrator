#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 [--dry-run] <target-repo-path>"
}

DRY_RUN=0
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
  shift
fi

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  usage
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$(cd "$SCRIPT_DIR/../templates" && pwd)"

REPO_NAME="$(basename "$TARGET")"
OWNER="${USER:-unknown}"
DATE_UTC="$(date -u +%F)"
CONTROL_PLANE_REF="main"

render_template() {
  local src="$1"
  local dst="$2"

  if [[ -e "$dst" ]]; then
    echo "SKIP: already exists: $dst"
    return 0
  fi

  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "DRY-RUN: create $dst from $src"
    return 0
  fi

  mkdir -p "$(dirname "$dst")"
  sed \
    -e "s|{{REPO_NAME}}|$REPO_NAME|g" \
    -e "s|{{OWNER}}|$OWNER|g" \
    -e "s|{{DATE}}|$DATE_UTC|g" \
    -e "s|{{CONTROL_PLANE_REF}}|$CONTROL_PLANE_REF|g" \
    "$src" > "$dst"

  echo "OK: created $dst"
}

render_template "$TEMPLATES_DIR/repo-AGENTS.md.template" "$TARGET/AGENTS.md"
render_template "$TEMPLATES_DIR/repo-ARCHITECTURE.md.template" "$TARGET/ARCHITECTURE.md"
render_template "$TEMPLATES_DIR/repo-REPO_MAP.md.template" "$TARGET/REPO_MAP.md"
render_template "$TEMPLATES_DIR/PLAN.yaml.template" "$TARGET/PLAN.yaml"

echo "Done."
