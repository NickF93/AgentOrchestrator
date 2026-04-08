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
CONTROL_PLANE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TEMPLATES_DIR="$(cd "$SCRIPT_DIR/../templates" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

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
  CONTROL_PLANE_REF="$(git -C "$CONTROL_PLANE_ROOT" symbolic-ref --quiet --short HEAD 2>/dev/null || true)"
  if [[ -z "$CONTROL_PLANE_REF" ]]; then
    CONTROL_PLANE_REF="$(git -C "$CONTROL_PLANE_ROOT" rev-parse --short HEAD 2>/dev/null || echo "unknown")"
  fi
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
render_template "$TEMPLATES_DIR/PLAN-index.yaml.template" "$TARGET/plan/PLAN-index.yaml"
render_template "$TEMPLATES_DIR/PLAN-current.yaml.template" "$TARGET/plan/PLAN-current.yaml"
render_template "$TEMPLATES_DIR/repo-README.md.template" "$TARGET/README.md"
render_template "$TEMPLATES_DIR/repo-ADR.md.template" "$TARGET/docs/adr/ADR-0001.md"
render_template "$TEMPLATES_DIR/repo-commit-msg.template" "$TARGET/.githooks/commit-msg"
render_template "$TEMPLATES_DIR/repo-pre-push.template" "$TARGET/.githooks/pre-push"
render_template "$TEMPLATES_DIR/repo-copilot-instructions.md.template" "$TARGET/.github/copilot-instructions.md"
render_template "$TEMPLATES_DIR/repo-CLAUDE.md.template" "$TARGET/CLAUDE.md"
render_template "$TEMPLATES_DIR/repo-CODEX.md.template" "$TARGET/.codex"
render_template "$TEMPLATES_DIR/repo-GEMINI.md.template" "$TARGET/GEMINI.md"
render_template "$TEMPLATES_DIR/repo-cursor-rules.mdc.template" "$TARGET/.cursor/rules/governance.mdc"
render_template "$TEMPLATES_DIR/repo-kilo-rules.md.template" "$TARGET/.kilo/rules/governance.md"

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "DRY-RUN: create $TARGET/plan/archive"
else
  mkdir -p "$TARGET/plan/archive"
  echo "OK: created $TARGET/plan/archive"
fi

if [[ "$DRY_RUN" -eq 0 ]]; then
  for hook_path in "$TARGET/.githooks/commit-msg" "$TARGET/.githooks/pre-push"; do
    if [[ -f "$hook_path" ]]; then
      chmod +x "$hook_path"
      echo "OK: marked executable $hook_path"
    fi
  done
fi

# Post-bootstrap validation (skip in dry-run mode)
if [[ "$DRY_RUN" -eq 0 ]]; then
  VALIDATE_SCRIPT="$SCRIPT_DIR/validate-plan.py"
  SCHEMA="$SCRIPT_DIR/../schemas/plan.schema.json"
  if [[ -f "$VALIDATE_SCRIPT" && -f "$SCHEMA" && -f "$TARGET/plan/PLAN-index.yaml" ]]; then
    echo "INFO: Running post-bootstrap validation..."
    if "$PYTHON_BIN" "$VALIDATE_SCRIPT" "$TARGET/plan/PLAN-index.yaml" --schema "$SCHEMA"; then
      echo "OK: Post-bootstrap validation passed"
    else
      echo "ERROR: Post-bootstrap validation failed" >&2
      exit 1
    fi
  fi
fi

if [[ "$DRY_RUN" -eq 0 ]]; then
  echo "INFO: Enable repo-local hooks with: git -C \"$TARGET\" config core.hooksPath .githooks"
  echo "INFO: Shared assets resolve from CONTROL_PLANE_ROOT in workspace mode"
  echo "INFO: Optional vendoring is explicit via materialize-shared-asset.sh; bootstrap does not auto-vendor"
fi

echo "Done."
