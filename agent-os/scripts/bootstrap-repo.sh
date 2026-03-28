#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 [--dry-run] [--owner <name>] [--ref <branch|tag|sha>] <target-repo-path>"
}

DRY_RUN=0
OWNER_ARG=""
REF_ARG=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --owner)
      OWNER_ARG="${2:-}"
      shift 2
      ;;
    --ref)
      REF_ARG="${2:-}"
      shift 2
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

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  usage
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$(cd "$SCRIPT_DIR/../templates" && pwd)"

REPO_NAME="$(basename "$TARGET")"
DATE_UTC="$(date -u +%F)"

if [[ -n "$OWNER_ARG" ]]; then
  OWNER="$OWNER_ARG"
else
  OWNER="${USER:-unknown}"
  echo "WARN: --owner not specified, falling back to \$USER ($OWNER)"
fi

if [[ -n "$REF_ARG" ]]; then
  CONTROL_PLANE_REF="$REF_ARG"
else
  CONTROL_PLANE_REF="main"
fi

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
    -e "s|{{ADR_NUMBER}}|0001|g" \
    -e "s|{{ADR_TITLE}}|Initial Architecture Decision|g" \
    "$src" > "$dst"

  echo "OK: created $dst"
}

render_template "$TEMPLATES_DIR/repo-AGENTS.md.template" "$TARGET/AGENTS.md"
render_template "$TEMPLATES_DIR/repo-ARCHITECTURE.md.template" "$TARGET/ARCHITECTURE.md"
render_template "$TEMPLATES_DIR/repo-REPO_MAP.md.template" "$TARGET/REPO_MAP.md"
render_template "$TEMPLATES_DIR/PLAN.yaml.template" "$TARGET/PLAN.yaml"
render_template "$TEMPLATES_DIR/repo-README.md.template" "$TARGET/README.md"
render_template "$TEMPLATES_DIR/repo-ADR.md.template" "$TARGET/docs/adr/ADR-0001.md"

# Post-bootstrap validation (skip in dry-run mode)
if [[ "$DRY_RUN" -eq 0 ]]; then
  VALIDATE_SCRIPT="$SCRIPT_DIR/validate-plan.py"
  SCHEMA="$SCRIPT_DIR/../schemas/plan.schema.json"
  if [[ -f "$VALIDATE_SCRIPT" && -f "$SCHEMA" && -f "$TARGET/PLAN.yaml" ]]; then
    echo "INFO: Running post-bootstrap validation..."
    if python3 "$VALIDATE_SCRIPT" "$TARGET/PLAN.yaml" --schema "$SCHEMA"; then
      echo "OK: Post-bootstrap validation passed"
    else
      echo "ERROR: Post-bootstrap validation failed" >&2
      exit 1
    fi
  fi
fi

echo "Done."
