#!/usr/bin/env python3
"""Add a host-local Codex trusted-project entry."""

from __future__ import annotations

import argparse
import os
import re
import shutil
from pathlib import Path

TRUST_LINE = 'trust_level = "trusted"'


def escape_toml_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def project_header(project_path: Path) -> str:
    return f'[projects."{escape_toml_string(project_path.as_posix())}"]'


def resolve_config_path(args: argparse.Namespace) -> Path:
    if args.config:
        return Path(args.config).expanduser().resolve()

    codex_home = args.codex_home or os.environ.get("CODEX_HOME") or "~/.codex"
    return (Path(codex_home).expanduser() / "config.toml").resolve()


def find_table(lines: list[str], header: str) -> tuple[int, int] | None:
    start = None
    for index, line in enumerate(lines):
        if line.strip() == header:
            start = index
            break
    if start is None:
        return None

    end = len(lines)
    for index in range(start + 1, len(lines)):
        stripped = lines[index].strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            end = index
            break
    return start, end


def ensure_trusted(content: str, project_path: Path) -> tuple[str, bool]:
    header = project_header(project_path)
    lines = content.splitlines()
    table_range = find_table(lines, header)

    if table_range is None:
        block = [header, TRUST_LINE]
        if lines:
            if lines[-1].strip():
                lines.append("")
            lines.extend(block)
        else:
            lines = block
        return "\n".join(lines) + "\n", True

    start, end = table_range
    trust_pattern = re.compile(r"^\s*trust_level\s*=")
    for index in range(start + 1, end):
        if trust_pattern.match(lines[index]):
            if lines[index].strip() == TRUST_LINE:
                return content if content.endswith("\n") else content + "\n", False
            lines[index] = TRUST_LINE
            return "\n".join(lines) + "\n", True

    lines.insert(start + 1, TRUST_LINE)
    return "\n".join(lines) + "\n", True


def trust_project(config_path: Path, project_path: Path, dry_run: bool) -> bool:
    existing = config_path.read_text(encoding="utf-8") if config_path.exists() else ""
    updated, changed = ensure_trusted(existing, project_path)

    if not changed:
        print(f"OK: already trusted: {project_path}")
        return False

    if dry_run:
        print(f"DRY-RUN: would trust {project_path} in {config_path}")
        return True

    config_path.parent.mkdir(parents=True, exist_ok=True)
    if config_path.exists():
        backup_path = config_path.with_name(f"{config_path.name}.bak")
        shutil.copy2(config_path, backup_path)
        print(f"OK: backed up {config_path} to {backup_path}")

    config_path.write_text(updated, encoding="utf-8")
    print(f"OK: trusted {project_path} in {config_path}")
    return True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Trust a project in host-local Codex config")
    parser.add_argument("project_path", help="Project path to trust")
    parser.add_argument(
        "--codex-home",
        help="Codex home directory. Defaults to CODEX_HOME or ~/.codex.",
    )
    parser.add_argument(
        "--config",
        help="Explicit Codex config.toml path. Overrides --codex-home and CODEX_HOME.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Report the change without writing")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    project_path = Path(args.project_path).expanduser().resolve()
    config_path = resolve_config_path(args)
    trust_project(config_path, project_path, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
