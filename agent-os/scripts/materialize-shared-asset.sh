#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 [--control-plane-root <path>] [--repo-root <path>] [--kind <kind>] <asset-id>"
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESOLVER="$SCRIPT_DIR/resolve-shared-asset.py"

CONTROL_PLANE_ROOT=""
REPO_ROOT="."
ASSET_KIND_HINT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --control-plane-root)
      CONTROL_PLANE_ROOT="${2:-}"
      shift 2
      ;;
    --repo-root)
      REPO_ROOT="${2:-}"
      shift 2
      ;;
    --kind)
      ASSET_KIND_HINT="${2:-}"
      shift 2
      ;;
    -*)
      echo "ERROR: unknown option: $1" >&2
      usage
      exit 2
      ;;
    *)
      break
      ;;
  esac
done

ASSET_ID="${1:-}"
if [[ -z "$ASSET_ID" ]]; then
  usage
  exit 2
fi

REPO_ROOT="$(cd "$REPO_ROOT" && pwd)"

RESOLVER_ARGS=(python3 "$RESOLVER" "$ASSET_ID" --repo-root "$REPO_ROOT" --resolution-mode workspace --format shell)
if [[ -n "$CONTROL_PLANE_ROOT" ]]; then
  RESOLVER_ARGS+=(--control-plane-root "$CONTROL_PLANE_ROOT")
fi
if [[ -n "$ASSET_KIND_HINT" ]]; then
  RESOLVER_ARGS+=(--kind "$ASSET_KIND_HINT")
fi

eval "$("${RESOLVER_ARGS[@]}")"

VENDOR_DIR="$REPO_ROOT/.agent-os/vendor/$ASSET_KIND/$ASSET_ID"
mkdir -p "$VENDOR_DIR"

VENDORED_FILE="$(basename "$ASSET_PATH")"
cp "$ASSET_PATH" "$VENDOR_DIR/$VENDORED_FILE"

if [[ -n "$ASSET_CONTROL_PLANE_ROOT" ]]; then
  SOURCE_COMMIT="$(git -C "$ASSET_CONTROL_PLANE_ROOT" rev-parse HEAD 2>/dev/null || echo "unknown")"
else
  SOURCE_COMMIT="unknown"
fi

MATERIALIZED_AT="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
PROVENANCE_PATH="$VENDOR_DIR/provenance.yaml"

{
  printf 'asset_id: %s\n' "$ASSET_ID"
  printf 'kind: %s\n' "$ASSET_KIND"
  printf 'version: "%s"\n' "$ASSET_VERSION"
  printf 'source_control_plane_root: %s\n' "$ASSET_CONTROL_PLANE_ROOT"
  printf 'source_control_plane_path: %s\n' "$ASSET_PATH"
  printf 'source_registry_path: %s\n' "$ASSET_REGISTRY_RELATIVE_PATH"
  printf 'source_registry_file: %s\n' "$ASSET_REGISTRY_FILE"
  printf 'source_commit: %s\n' "$SOURCE_COMMIT"
  printf 'materialized_at: %s\n' "$MATERIALIZED_AT"
  printf 'vendored_file: %s\n' "$VENDORED_FILE"
  printf 'compatibility: [%s]\n' "$ASSET_COMPATIBILITY"
  if [[ -n "$ASSET_DEPENDS_ON_ASSETS" ]]; then
    printf 'depends_on_assets: [%s]\n' "$ASSET_DEPENDS_ON_ASSETS"
  fi
} > "$PROVENANCE_PATH"

echo "OK: materialized $ASSET_ID to $VENDOR_DIR"
echo "OK: wrote provenance $PROVENANCE_PATH"
