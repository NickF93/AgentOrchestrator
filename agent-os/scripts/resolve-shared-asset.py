#!/usr/bin/env python3
"""Resolve Layer-0 shared assets in workspace or vendored mode."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: pyyaml. Install tooling deps with: "
        "python3 -m pip install -r requirements.txt"
    ) from exc


REGISTRY_RELATIVE_PATH = Path("agent-os/registry/shared-assets.yaml")
WORKSPACE_ROOT_MARKERS = ("CONTROL_PLANE_ROOT:", "Control plane:")


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"YAML file must be a mapping: {path}")
    return data


def parse_workspace_control_plane_root(repo_root: Path) -> Path | None:
    workspace_root = repo_root.parent
    for name in ("AGENTS.md", "CLAUDE.md"):
        candidate = workspace_root / name
        if not candidate.exists():
            continue
        for line in candidate.read_text(encoding="utf-8").splitlines():
            for marker in WORKSPACE_ROOT_MARKERS:
                if line.startswith(marker):
                    value = line.split(":", 1)[1].strip()
                    if value:
                        return Path(value).expanduser().resolve()
    return None


def discover_control_plane_root(repo_root: Path, explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()

    env_value = os.environ.get("CONTROL_PLANE_ROOT", "").strip()
    if env_value:
        return Path(env_value).expanduser().resolve()

    stamped_root = parse_workspace_control_plane_root(repo_root)
    if stamped_root is not None:
        return stamped_root

    local_registry = repo_root / REGISTRY_RELATIVE_PATH
    if local_registry.exists():
        return repo_root

    raise FileNotFoundError(
        "Cannot locate control-plane root. Provide --control-plane-root, "
        "export CONTROL_PLANE_ROOT, or run sync-workspace.sh to stamp the workspace."
    )


def load_registry(control_plane_root: Path) -> dict:
    registry_path = control_plane_root / REGISTRY_RELATIVE_PATH
    if not registry_path.exists():
        raise FileNotFoundError(f"Shared asset registry not found: {registry_path}")
    return load_yaml(registry_path)


def find_registry_asset(asset_id: str, control_plane_root: Path) -> dict:
    registry = load_registry(control_plane_root)
    assets = registry.get("assets", []) or []
    for asset in assets:
        if not isinstance(asset, dict):
            raise ValueError(f"Registry entry for '{asset_id}' is not a mapping")
        if asset.get("id") == asset_id:
            return asset
    raise KeyError(f"Unknown shared asset id: {asset_id}")


def resolve_workspace_asset(
    asset_id: str, repo_root: Path, control_plane_root_arg: str | None
) -> dict:
    control_plane_root = discover_control_plane_root(repo_root, control_plane_root_arg)
    asset = find_registry_asset(asset_id, control_plane_root)
    registry_relative_path = asset.get("path", "")
    if not isinstance(registry_relative_path, str) or not registry_relative_path:
        raise ValueError(f"Registry entry for '{asset_id}' has no valid path")

    resolved_path = (control_plane_root / registry_relative_path).resolve()
    if not resolved_path.exists():
        raise FileNotFoundError(f"Resolved asset path does not exist: {resolved_path}")

    return {
        "asset_id": asset["id"],
        "kind": asset.get("kind", ""),
        "version": asset.get("version", ""),
        "compatibility": asset.get("compatibility", []) or [],
        "materializable": asset.get("materializable", False),
        "depends_on_assets": asset.get("depends_on_assets", []) or [],
        "path": str(resolved_path),
        "registry_relative_path": registry_relative_path,
        "registry_path": str((control_plane_root / REGISTRY_RELATIVE_PATH).resolve()),
        "control_plane_root": str(control_plane_root),
        "repo_root": str(repo_root),
        "resolution_mode": "workspace",
    }


def resolve_vendored_asset(asset_id: str, repo_root: Path, kind: str | None) -> dict:
    vendor_root = (repo_root / ".agent-os" / "vendor").resolve()
    if not vendor_root.exists():
        raise FileNotFoundError(f"Vendored asset root not found: {vendor_root}")

    manifests: list[Path]
    if kind:
        candidate = vendor_root / kind / asset_id / "provenance.yaml"
        manifests = [candidate]
    else:
        manifests = sorted(vendor_root.rglob("provenance.yaml"))

    for manifest_path in manifests:
        if not manifest_path.exists():
            continue
        manifest = load_yaml(manifest_path)
        if manifest.get("asset_id") != asset_id:
            continue
        if kind and manifest.get("kind") != kind:
            continue
        vendored_file = manifest.get("vendored_file")
        if not isinstance(vendored_file, str) or not vendored_file:
            raise ValueError(f"Vendored asset manifest missing vendored_file: {manifest_path}")
        asset_path = (manifest_path.parent / vendored_file).resolve()
        if not asset_path.exists():
            raise FileNotFoundError(f"Vendored asset path does not exist: {asset_path}")
        return {
            "asset_id": manifest.get("asset_id", asset_id),
            "kind": manifest.get("kind", kind or ""),
            "version": manifest.get("version", ""),
            "compatibility": manifest.get("compatibility", []) or [],
            "materializable": True,
            "depends_on_assets": manifest.get("depends_on_assets", []) or [],
            "path": str(asset_path),
            "registry_relative_path": manifest.get("source_registry_path", ""),
            "registry_path": manifest.get("source_registry_file", ""),
            "control_plane_root": manifest.get("source_control_plane_root", ""),
            "repo_root": str(repo_root),
            "resolution_mode": "vendored",
        }

    raise FileNotFoundError(f"Vendored asset '{asset_id}' was not found under {vendor_root}")


def emit(result: dict, output_format: str) -> None:
    if output_format == "path":
        print(result["path"])
        return

    if output_format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
        return

    compatibility = ",".join(result.get("compatibility", []) or [])
    depends_on_assets = ",".join(result.get("depends_on_assets", []) or [])
    shell_lines = {
        "ASSET_ID": result.get("asset_id", ""),
        "ASSET_KIND": result.get("kind", ""),
        "ASSET_VERSION": result.get("version", ""),
        "ASSET_PATH": result.get("path", ""),
        "ASSET_REGISTRY_RELATIVE_PATH": result.get("registry_relative_path", ""),
        "ASSET_REGISTRY_FILE": result.get("registry_path", ""),
        "ASSET_CONTROL_PLANE_ROOT": result.get("control_plane_root", ""),
        "ASSET_REPO_ROOT": result.get("repo_root", ""),
        "ASSET_RESOLUTION_MODE": result.get("resolution_mode", ""),
        "ASSET_COMPATIBILITY": compatibility,
        "ASSET_DEPENDS_ON_ASSETS": depends_on_assets,
    }
    for key, value in shell_lines.items():
        print(f"{key}={shlex.quote(str(value))}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve a Layer-0 shared asset")
    parser.add_argument("asset_id", help="Shared asset ID from the canonical registry")
    parser.add_argument(
        "--control-plane-root",
        default="",
        help="Explicit control-plane root override",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Target repository root for workspace or vendored resolution",
    )
    parser.add_argument(
        "--resolution-mode",
        default="workspace",
        choices=("workspace", "vendored"),
        help="Resolve from the live control plane or .agent-os/vendor/",
    )
    parser.add_argument(
        "--kind",
        default="",
        help="Optional asset kind hint for vendored lookup",
    )
    parser.add_argument(
        "--format",
        default="path",
        choices=("path", "json", "shell"),
        help="Output format",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve()
    if not repo_root.exists():
        print(f"ERROR: repo_root not found: {repo_root}", file=sys.stderr)
        return 2

    try:
        if args.resolution_mode == "workspace":
            result = resolve_workspace_asset(
                args.asset_id,
                repo_root,
                args.control_plane_root or None,
            )
        else:
            result = resolve_vendored_asset(
                args.asset_id,
                repo_root,
                args.kind or None,
            )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    emit(result, args.format)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
