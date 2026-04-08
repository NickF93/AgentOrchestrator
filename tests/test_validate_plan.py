from __future__ import annotations

import importlib.util
import json
import os
import runpy
import subprocess
import sys
import types
from pathlib import Path
from typing import Any

import pytest
from conftest import (
    PLAN_PATH,
    SCHEMA_PATH,
    copy_split_plan,
    load_yaml,
    run_python_script,
    write_yaml,
)


def load_module(module_name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    spec.loader.exec_module(module)
    return module


def run_validate_plan_without_jsonschema(
    repo_root: Path, plan_path: Path, schema_path: Path, temp_path: Path
) -> subprocess.CompletedProcess[str]:
    blocker = temp_path / "sitecustomize.py"
    blocker.write_text(
        "import builtins\n"
        "_original_import = builtins.__import__\n"
        "def _guarded_import(name, globals=None, locals=None, fromlist=(), level=0):\n"
        "    if name == 'jsonschema':\n"
        "        raise ImportError('blocked for test')\n"
        "    return _original_import(name, globals, locals, fromlist, level)\n"
        "builtins.__import__ = _guarded_import\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        f"{temp_path}{os.pathsep}{existing_pythonpath}" if existing_pythonpath else str(temp_path)
    )
    return subprocess.run(
        [
            sys.executable,
            str(repo_root / "agent-os" / "scripts" / "validate-plan.py"),
            str(plan_path),
            "--schema",
            str(schema_path),
        ],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )


def write_current_fragment(plan_dir: Path, fragment: dict) -> None:
    write_yaml(plan_dir / "PLAN-current.yaml", fragment)


def test_validate_plan_accepts_current_plan(repo_root: Path) -> None:
    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "validate-plan.py",
        str(PLAN_PATH),
        "--schema",
        str(SCHEMA_PATH),
    )
    assert result.returncode == 0, result.stderr
    assert "ACTIVE:" in result.stdout
    assert "ARCHIVED:" in result.stdout
    assert "OK:" in result.stdout


def test_validate_plan_rejects_unknown_shared_asset(repo_root: Path, tmp_path: Path) -> None:
    from conftest import inject_synthetic_current

    index_path = copy_split_plan(tmp_path)
    fragment = inject_synthetic_current(index_path.parent)
    # C99.1.3 in the synthetic fragment has shared_assets
    target_item = next(item for item in fragment["items"] if item.get("shared_assets"))
    target_item["shared_assets"]["prompt"] = "does-not-exist"
    write_yaml(index_path.parent / "PLAN-current.yaml", fragment)

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "validate-plan.py",
        str(index_path),
        "--schema",
        str(SCHEMA_PATH),
    )
    assert result.returncode == 1
    combined = f"{result.stdout}\n{result.stderr}"
    assert "unknown asset id 'does-not-exist'" in combined


def test_validate_plan_rejects_missing_required_field(repo_root: Path, tmp_path: Path) -> None:
    index_path = copy_split_plan(tmp_path)
    index = load_yaml(index_path)
    del index["meta"]["repo"]
    write_yaml(index_path, index)

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "validate-plan.py",
        str(index_path),
        "--schema",
        str(SCHEMA_PATH),
    )
    assert result.returncode == 1
    combined = f"{result.stdout}\n{result.stderr}"
    assert "Schema validation failed" in combined or "meta.repo" in combined


def test_validate_plan_accepts_current_plan_without_jsonschema(
    repo_root: Path, tmp_path: Path
) -> None:
    index_path = copy_split_plan(tmp_path)
    result = run_validate_plan_without_jsonschema(repo_root, index_path, SCHEMA_PATH, tmp_path)
    assert result.returncode == 0, f"{result.stdout}\n{result.stderr}"
    assert "ACTIVE:" in result.stdout
    assert "ARCHIVED:" in result.stdout
    assert "OK:" in result.stdout


def test_validate_plan_rejects_missing_required_field_without_jsonschema(
    repo_root: Path, tmp_path: Path
) -> None:
    index_path = copy_split_plan(tmp_path)
    index = load_yaml(index_path)
    del index["meta"]["repo"]
    write_yaml(index_path, index)

    result = run_validate_plan_without_jsonschema(repo_root, index_path, SCHEMA_PATH, tmp_path)
    assert result.returncode == 1
    combined = f"{result.stdout}\n{result.stderr}"
    assert "Schema validation failed" in combined
    assert "meta.repo: expected non-empty string" in combined
    assert "AttributeError" not in combined


def test_validate_plan_rejects_archive_digest_mismatch(repo_root: Path, tmp_path: Path) -> None:
    index_path = copy_split_plan(tmp_path)
    index = load_yaml(index_path)
    archive_path = index_path.parent / index["archives"][0]["path"]
    archive_fragment = load_yaml(archive_path)
    archive_fragment["items"][0]["title"] = "tampered archived item"
    write_yaml(archive_path, archive_fragment)

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "validate-plan.py",
        str(index_path),
        "--schema",
        str(SCHEMA_PATH),
    )

    assert result.returncode == 1
    combined = f"{result.stdout}\n{result.stderr}"
    assert "archive digest mismatch" in combined


def test_validate_plan_rejects_cross_fragment_archive_structure(
    repo_root: Path, tmp_path: Path
) -> None:
    index_path = copy_split_plan(tmp_path)
    index = load_yaml(index_path)
    archive_path = index_path.parent / index["archives"][0]["path"]
    archive_fragment = load_yaml(archive_path)
    archive_fragment["sprints"][0]["parent"] = "X999"
    write_yaml(archive_path, archive_fragment)

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "validate-plan.py",
        str(index_path),
        "--schema",
        str(SCHEMA_PATH),
    )

    assert result.returncode == 1
    combined = f"{result.stdout}\n{result.stderr}"
    assert "outside its fragment" in combined


def test_validate_plan_rejects_legacy_aggregate_runtime_input(
    repo_root: Path, tmp_path: Path
) -> None:
    legacy_path = tmp_path / "PLAN.yaml"
    write_yaml(
        legacy_path,
        {
            "meta": {
                "repo": "fixture",
                "owner": "tester",
                "version": "1",
                "schema_version": "1",
                "last_updated": "2026-04-02",
            },
            "mission": "Fixture mission",
            "milestones": [],
            "sprints": [],
            "items": [],
            "commit_groups": [],
        },
    )

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "validate-plan.py",
        str(legacy_path),
        "--schema",
        str(SCHEMA_PATH),
    )

    assert result.returncode == 1
    assert "split plan index" in result.stderr


def test_validate_plan_main_accepts_current_plan_in_process(
    repo_root: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    monkeypatch.setattr(
        sys,
        "argv",
        ["validate-plan.py", str(PLAN_PATH), "--schema", str(SCHEMA_PATH)],
    )

    assert module.main() == 0
    stdout = capsys.readouterr().out
    assert "ACTIVE:" in stdout
    assert "ARCHIVED:" in stdout
    assert "OK:" in stdout


def test_validate_plan_main_handles_missing_inputs(
    repo_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    missing_plan = tmp_path / "missing.yaml"

    monkeypatch.setattr(
        sys, "argv", ["validate-plan.py", str(missing_plan), "--schema", str(SCHEMA_PATH)]
    )
    assert module.main() == 2
    assert "Plan file not found" in capsys.readouterr().err

    monkeypatch.setattr(
        sys,
        "argv",
        ["validate-plan.py", str(PLAN_PATH), "--schema", str(tmp_path / "missing-schema.json")],
    )
    assert module.main() == 2
    assert "Schema file not found" in capsys.readouterr().err


def test_validate_plan_main_handles_missing_registry_and_lint_failures(
    repo_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    index_path = copy_split_plan(tmp_path)
    missing_registry = tmp_path / "missing-registry.yaml"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "validate-plan.py",
            str(index_path),
            "--schema",
            str(SCHEMA_PATH),
            "--shared-asset-registry",
            str(missing_registry),
        ],
    )
    assert module.main() == 2
    assert "Shared asset registry not found" in capsys.readouterr().err

    current_path = index_path.parent / "PLAN-current.yaml"
    current_path.write_text(
        "milestones:\n- id: X99\n  type: X\n  title: Issue #21 bad title\n"
        "  status: in_progress\nsprints: []\nitems: []\ncommit_groups: []\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["validate-plan.py", str(index_path), "--schema", str(SCHEMA_PATH)],
    )
    assert module.main() == 1
    assert "unquoted '#'" in capsys.readouterr().err


def test_load_helpers_reject_non_mappings_and_non_objects(repo_root: Path, tmp_path: Path) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    yaml_path = tmp_path / "list.yaml"
    yaml_path.write_text("- bad\n", encoding="utf-8")
    json_path = tmp_path / "array.json"
    json_path.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="Top-level YAML document must be a mapping"):
        module.load_yaml(yaml_path)
    with pytest.raises(ValueError, match="Shared asset registry must be a mapping"):
        module.load_shared_asset_registry(yaml_path)
    with pytest.raises(ValueError, match="Schema must be a JSON object"):
        module.load_schema(json_path)


def test_is_inside_quotes_handles_escaped_single_and_double_quotes(repo_root: Path) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    single_line = "title: 'It''s #safe'\n"
    double_line = 'title: "say \\"hi #there\\""\n'

    assert module._is_inside_quotes(single_line, single_line.index("#"))
    assert module._is_inside_quotes(double_line, double_line.index("#"))


def test_lint_yaml_unquoted_hash_all_handles_invalid_and_partial_split_inputs(
    repo_root: Path, tmp_path: Path
) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")

    invalid_index = tmp_path / "invalid-index.yaml"
    invalid_index.write_text("meta: [\n", encoding="utf-8")
    assert module.lint_yaml_unquoted_hash_all(invalid_index) == []

    partial_index = tmp_path / "partial-index.yaml"
    partial_index.write_text(
        "current_plan: PLAN-current.yaml\narchives:\n- path: archive/missing.yaml\n",
        encoding="utf-8",
    )
    assert module.lint_yaml_unquoted_hash_all(partial_index) == []


def test_validate_shared_asset_registry_rejects_malformed_entries(
    repo_root: Path, tmp_path: Path
) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    registry_path = tmp_path / "shared-assets.yaml"
    registry = {
        "assets": [
            "bad",
            {
                "id": "asset-1",
                "kind": "wrong-kind",
                "version": "",
                "path": "bad/path",
                "compatibility": [],
                "materializable": "yes",
                "depends_on_assets": ["missing"],
            },
        ]
    }

    asset_map, errors = module.validate_shared_asset_registry(registry, registry_path)

    assert asset_map["asset-1"]["id"] == "asset-1"
    assert any("entry must be a mapping" in error for error in errors)
    assert any("invalid kind" in error for error in errors)
    assert any("depends_on_assets references unknown asset 'missing'" in error for error in errors)


def test_validate_shared_asset_registry_rejects_missing_ids_duplicates_and_bad_dependencies(
    repo_root: Path, tmp_path: Path
) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    control_plane_root = tmp_path / "control"
    registry_path = control_plane_root / "agent-os" / "registry" / "shared-assets.yaml"
    registry_path.parent.mkdir(parents=True)
    valid_asset = control_plane_root / "agent-os" / "skills" / "valid" / "SKILL.md"
    valid_asset.parent.mkdir(parents=True)
    valid_asset.write_text("skill\n", encoding="utf-8")

    registry = {
        "assets": [
            {
                "kind": "skill",
                "version": "1",
                "path": str(valid_asset.relative_to(control_plane_root)),
                "compatibility": ["codex"],
                "materializable": True,
            },
            {
                "id": "dup",
                "kind": "skill",
                "version": "1",
                "path": "",
                "compatibility": ["codex"],
                "materializable": True,
                "depends_on_assets": "bad",
            },
            {
                "id": "dup",
                "kind": "skill",
                "version": "1",
                "path": "agent-os/skills/missing/SKILL.md",
                "compatibility": ["codex"],
                "materializable": True,
                "depends_on_assets": ["", "missing"],
            },
        ]
    }

    _asset_map, errors = module.validate_shared_asset_registry(registry, registry_path)

    assert any("missing non-empty id" in error for error in errors)
    assert any("shared asset registry has duplicate id 'dup'" in error for error in errors)
    assert any("shared asset 'dup' has no non-empty path" in error for error in errors)
    assert any("shared asset 'dup' has non-list depends_on_assets" in error for error in errors)


def test_validate_shared_asset_registry_checks_prefix_paths_and_dependency_entries(
    repo_root: Path, tmp_path: Path
) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    control_plane_root = tmp_path / "control"
    registry_path = control_plane_root / "agent-os" / "registry" / "shared-assets.yaml"
    registry_path.parent.mkdir(parents=True)

    registry = {
        "assets": [
            {
                "id": "asset-1",
                "kind": "prompt",
                "version": "1",
                "path": "agent-os/skills/not-a-prompt/SKILL.md",
                "compatibility": ["codex"],
                "materializable": True,
                "depends_on_assets": ["", "missing-asset"],
            }
        ]
    }

    _asset_map, errors = module.validate_shared_asset_registry(registry, registry_path)

    assert any("must live under 'agent-os/prompts/'" in error for error in errors)
    assert any("path does not exist" in error for error in errors)
    assert any("invalid depends_on_assets entry ''" in error for error in errors)
    assert any("references unknown asset 'missing-asset'" in error for error in errors)


def test_validate_shared_asset_refs_rejects_bad_mapping_and_kind(repo_root: Path) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    items = [
        {"id": "D1.1.1", "shared_assets": "bad"},
        {"id": "D1.1.2", "shared_assets": {"skill": "asset-1", "prompt": "asset-2"}},
    ]
    asset_map = {
        "asset-1": {"kind": "skill"},
        "asset-2": {"kind": "skill"},
    }

    errors = module.validate_shared_asset_refs(items, asset_map)

    assert any("shared_assets must be a mapping" in error for error in errors)
    assert any("expected 'prompt'" in error for error in errors)


def test_validate_plan_schema_subset_rejects_bad_shapes(repo_root: Path) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    errors = module.validate_plan_schema_subset({"meta": [], "mission": "", "milestones": "bad"})

    assert any("meta: expected mapping" in error for error in errors)
    assert any("mission: expected non-empty string" in error for error in errors)
    assert any("missing required top-level field 'sprints'" in error for error in errors)


def test_validate_plan_schema_subset_accepts_valid_full_shape(repo_root: Path) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    errors = module.validate_plan_schema_subset(
        {
            "meta": {
                "repo": "fixture",
                "owner": "tester",
                "version": "1",
                "schema_version": "1",
                "last_updated": "2026-04-02",
            },
            "mission": "Fixture mission",
            "milestones": [{"id": "X1", "type": "X", "title": "Milestone", "status": "planned"}],
            "sprints": [
                {"id": "S1.1", "type": "S", "parent": "X1", "title": "Sprint", "status": "planned"}
            ],
            "items": [
                {
                    "id": "Q1.1.1",
                    "parent": "S1.1",
                    "type": "Q",
                    "title": "Decision",
                    "status": "planned",
                    "role": "reviewer",
                    "effort": "low",
                    "actions": ["decide"],
                    "commit_group": "cg1",
                    "depends_on": [],
                    "scope": ".",
                    "checks": ["pytest -q"],
                    "artifacts_in": ["PLAN.yaml"],
                    "artifacts_out": ["PLAN.md"],
                    "decision": "approved",
                    "triggers": ["manual"],
                    "tools_profile": "check-medium",
                    "requires_phase": "A",
                    "approval_ref": "ADR-1",
                    "shared_assets": {
                        "skill": "plan-checkpoint-close",
                        "prompt": "checkpoint-closure-review",
                        "profile": "codex/check-medium",
                        "result_protocol": "check-result-v1",
                        "context_policy": "focused",
                        "resolution_mode": "workspace",
                    },
                }
            ],
            "commit_groups": [{"id": "cg1", "title": "Group", "items": ["Q1.1.1"]}],
        }
    )

    assert errors == []


def test_validate_plan_schema_subset_rejects_deep_invalid_shapes(repo_root: Path) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    errors = module.validate_plan_schema_subset(
        {
            "meta": {
                "repo": "",
                "owner": "",
                "version": "",
                "schema_version": "",
                "last_updated": "",
            },
            "mission": " ",
            "milestones": [{"id": "bad", "type": "M", "title": "", "status": "oops"}],
            "sprints": [{"id": "bad", "type": "X", "parent": "bad", "title": "", "status": "oops"}],
            "items": [
                {
                    "id": "bad",
                    "parent": "bad",
                    "type": "Z",
                    "title": "",
                    "status": "oops",
                    "role": "bad",
                    "effort": "bad",
                    "actions": ["bad"],
                    "commit_group": "bad",
                    "depends_on": "bad",
                    "scope": "?bad",
                    "checks": "bad",
                    "artifacts_in": "bad",
                    "artifacts_out": "bad",
                    "decision": 1,
                    "triggers": "bad",
                    "tools_profile": 1,
                    "requires_phase": "design-approved",
                    "approval_ref": "",
                    "shared_assets": {
                        "skill": "bad asset!",
                        "prompt": "bad asset!",
                        "profile": "bad asset!",
                        "result_protocol": "bad asset!",
                        "context_policy": "bad",
                        "resolution_mode": "bad",
                        "unexpected": "field",
                    },
                },
                {},
            ],
            "commit_groups": [{"id": "bad", "title": "", "items": ["bad"]}],
        }
    )

    assert any("meta.repo: expected non-empty string" in error for error in errors)
    assert any("milestones[0].id: expected milestone id like X1" in error for error in errors)
    assert any("sprints[0].parent: expected milestone id like X1" in error for error in errors)
    assert any("items[0].actions: invalid action 'bad'" in error for error in errors)
    assert any(
        "items[0].shared_assets: unexpected field(s): unexpected" in error for error in errors
    )
    assert any("items[1]: missing required field 'id'" in error for error in errors)
    assert any("commit_groups[0].items: expected item IDs" in error for error in errors)


def test_validate_plan_schema_uses_jsonschema_or_subset(
    repo_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")

    class FakeValidationError(Exception):
        def __init__(self, path: list[object], message: str) -> None:
            super().__init__(message)
            self.path = path
            self.message = message

    monkeypatch.setattr(
        module,
        "jsonschema",
        types.SimpleNamespace(validate=lambda **_kwargs: None, ValidationError=FakeValidationError),
    )
    errors, validator = module.validate_plan_schema({"meta": {}}, {"type": "object"})
    assert errors == []
    assert validator == "jsonschema"

    def raise_validation_error(**_kwargs: object) -> None:
        raise FakeValidationError(["items", 0, "id"], "bad id")

    monkeypatch.setattr(
        module,
        "jsonschema",
        types.SimpleNamespace(validate=raise_validation_error, ValidationError=FakeValidationError),
    )
    errors, validator = module.validate_plan_schema({"meta": {}}, {"type": "object"})
    assert validator == "jsonschema"
    assert errors == ["path: items/0/id", "message: bad id"]

    monkeypatch.setattr(module, "jsonschema", None)
    errors, validator = module.validate_plan_schema({"meta": [], "mission": ""}, {"type": "object"})
    assert validator == "subset"
    assert errors


def test_transition_and_cycle_helpers_report_errors(repo_root: Path) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    current = {"items": [{"id": "D1.1.1", "status": "ready"}]}
    previous = {"items": [{"id": "D1.1.1", "status": "in_progress"}]}
    cycle_items = [
        {"id": "D1.1.1", "depends_on": ["D1.1.2"]},
        {"id": "D1.1.2", "depends_on": ["D1.1.1"]},
    ]

    assert module.validate_transitions(current, previous)
    assert module.detect_cycles(cycle_items)


def test_collect_helpers_and_transition_skips_unknown_states(repo_root: Path) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    plan = {
        "milestones": [{"id": "X1", "type": "X", "status": "planned"}],
        "sprints": [{"id": "", "type": "S", "status": ""}],
        "items": [{"id": "D1.1.1", "type": "D", "status": "review"}, {"id": "D1.1.2", "type": "D"}],
    }

    assert module.collect_ids(plan) == {"X1": "X", "D1.1.1": "D", "D1.1.2": "D"}
    assert module.collect_statuses(plan) == {"X1": "planned", "D1.1.1": "review"}
    assert (
        module.validate_transitions(
            {"items": [{"id": "D1.1.1", "status": "planned"}]},
            {"items": [{"id": "D1.1.1", "status": "unknown"}]},
        )
        == []
    )


def test_compute_ready_items_returns_sorted_ready_candidates(repo_root: Path) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    plan = {
        "items": [
            {
                "id": "M1.1.3",
                "type": "M",
                "status": "planned",
                "commit_group": "cg1",
                "depends_on": ["T1.1.4"],
            },
            {
                "id": "D1.1.1",
                "type": "D",
                "status": "planned",
                "commit_group": "cg1",
                "depends_on": [],
            },
            {
                "id": "T1.1.4",
                "type": "T",
                "status": "verified",
                "commit_group": "cg1",
                "depends_on": [],
            },
            {
                "id": "F1.1.2",
                "type": "F",
                "status": "blocked",
                "commit_group": "cg1",
                "depends_on": [],
            },
            {
                "id": "C1.1.5",
                "type": "C",
                "status": "planned",
                "commit_group": "cg2",
                "depends_on": ["M1.1.6"],
            },
            {
                "id": "M1.1.6",
                "type": "M",
                "status": "review",
                "commit_group": "cg2",
                "depends_on": [],
            },
        ]
    }

    assert module.unresolved_dependencies(plan["items"][0], module.collect_statuses(plan)) == []
    assert module.compute_ready_items(plan) == [
        {
            "id": "D1.1.1",
            "type": "D",
            "status": "planned",
            "commit_group": "cg1",
            "unresolved_dependencies": [],
            "unresolved_dependencies_count": 0,
        },
        {
            "id": "M1.1.3",
            "type": "M",
            "status": "planned",
            "commit_group": "cg1",
            "unresolved_dependencies": [],
            "unresolved_dependencies_count": 0,
        },
    ]


def test_validate_plan_compute_ready_emits_multiple_ready_items_json(
    repo_root: Path, tmp_path: Path
) -> None:
    index_path = copy_split_plan(tmp_path)
    write_current_fragment(
        index_path.parent,
        {
            "milestones": [
                {
                    "id": "X99",
                    "type": "X",
                    "title": "Synthetic milestone",
                    "status": "in_progress",
                }
            ],
            "sprints": [
                {
                    "id": "S99.1",
                    "type": "S",
                    "parent": "X99",
                    "title": "Synthetic sprint",
                    "status": "in_progress",
                }
            ],
            "items": [
                {
                    "id": "D99.1.1",
                    "parent": "S99.1",
                    "type": "D",
                    "title": "Doc ready now",
                    "actions": ["document"],
                    "status": "planned",
                    "role": "documenter",
                    "effort": "low",
                    "commit_group": "cg990",
                },
                {
                    "id": "M99.1.2",
                    "parent": "S99.1",
                    "type": "M",
                    "title": "Already marked ready",
                    "actions": ["implement"],
                    "status": "ready",
                    "role": "implementer",
                    "effort": "medium",
                    "commit_group": "cg990",
                    "depends_on": ["T99.1.3"],
                },
                {
                    "id": "T99.1.3",
                    "parent": "S99.1",
                    "type": "T",
                    "title": "Verified dependency",
                    "actions": ["verify"],
                    "status": "verified",
                    "role": "tester",
                    "effort": "low",
                    "commit_group": "cg990",
                },
                {
                    "id": "F99.1.4",
                    "parent": "S99.1",
                    "type": "F",
                    "title": "Blocked by unresolved dependency",
                    "actions": ["implement"],
                    "status": "planned",
                    "role": "implementer",
                    "effort": "low",
                    "commit_group": "cg990",
                    "depends_on": ["D99.1.5"],
                },
                {
                    "id": "D99.1.5",
                    "parent": "S99.1",
                    "type": "D",
                    "title": "Dependency still in review",
                    "actions": ["document"],
                    "status": "review",
                    "role": "documenter",
                    "effort": "low",
                    "commit_group": "cg990",
                },
                {
                    "id": "D99.1.6",
                    "parent": "S99.1",
                    "type": "D",
                    "title": "Blocked side-state item",
                    "actions": ["document"],
                    "status": "blocked",
                    "role": "documenter",
                    "effort": "low",
                    "commit_group": "cg990",
                },
                {
                    "id": "M99.1.7",
                    "parent": "S99.1",
                    "type": "M",
                    "title": "Warning-producing ready item",
                    "actions": ["audit"],
                    "status": "planned",
                    "role": "implementer",
                    "effort": "low",
                    "commit_group": "cg990",
                },
            ],
            "commit_groups": [
                {
                    "id": "cg990",
                    "title": "Synthetic group",
                    "items": [
                        "D99.1.1",
                        "M99.1.2",
                        "T99.1.3",
                        "F99.1.4",
                        "D99.1.5",
                        "D99.1.6",
                        "M99.1.7",
                    ],
                }
            ],
        },
    )

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "validate-plan.py",
        str(index_path),
        "--schema",
        str(SCHEMA_PATH),
        "--compute-ready",
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["ready_items"] == [
        {
            "commit_group": "cg990",
            "id": "D99.1.1",
            "status": "planned",
            "type": "D",
            "unresolved_dependencies": [],
            "unresolved_dependencies_count": 0,
        },
        {
            "commit_group": "cg990",
            "id": "M99.1.2",
            "status": "ready",
            "type": "M",
            "unresolved_dependencies": [],
            "unresolved_dependencies_count": 0,
        },
        {
            "commit_group": "cg990",
            "id": "M99.1.7",
            "status": "planned",
            "type": "M",
            "unresolved_dependencies": [],
            "unresolved_dependencies_count": 0,
        },
    ]
    assert any("not in recommended set for type M" in warning for warning in payload["warnings"])


def test_validate_plan_compute_ready_emits_empty_ready_set(repo_root: Path, tmp_path: Path) -> None:
    index_path = copy_split_plan(tmp_path)
    write_current_fragment(
        index_path.parent,
        {
            "milestones": [
                {"id": "X99", "type": "X", "title": "Synthetic milestone", "status": "in_progress"}
            ],
            "sprints": [
                {
                    "id": "S99.1",
                    "type": "S",
                    "parent": "X99",
                    "title": "Synthetic sprint",
                    "status": "in_progress",
                }
            ],
            "items": [
                {
                    "id": "M99.1.1",
                    "parent": "S99.1",
                    "type": "M",
                    "title": "In progress item",
                    "actions": ["implement"],
                    "status": "in_progress",
                    "role": "implementer",
                    "effort": "medium",
                    "commit_group": "cg990",
                },
                {
                    "id": "T99.1.2",
                    "parent": "S99.1",
                    "type": "T",
                    "title": "Still waiting on dependency",
                    "actions": ["verify"],
                    "status": "planned",
                    "role": "tester",
                    "effort": "low",
                    "commit_group": "cg990",
                    "depends_on": ["M99.1.1"],
                },
                {
                    "id": "D99.1.3",
                    "parent": "S99.1",
                    "type": "D",
                    "title": "Blocked doc item",
                    "actions": ["document"],
                    "status": "blocked",
                    "role": "documenter",
                    "effort": "low",
                    "commit_group": "cg990",
                },
            ],
            "commit_groups": [
                {
                    "id": "cg990",
                    "title": "Synthetic group",
                    "items": [
                        "M99.1.1",
                        "T99.1.2",
                        "D99.1.3",
                    ],
                }
            ],
        },
    )

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "validate-plan.py",
        str(index_path),
        "--schema",
        str(SCHEMA_PATH),
        "--compute-ready",
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["ready_items"] == []
    assert isinstance(payload["warnings"], list)


def test_validate_plan_compute_ready_preserves_failure_paths(
    repo_root: Path, tmp_path: Path
) -> None:
    missing_plan = tmp_path / "missing.yaml"

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "validate-plan.py",
        str(missing_plan),
        "--schema",
        str(SCHEMA_PATH),
        "--compute-ready",
    )

    assert result.returncode == 2
    assert result.stdout == ""
    assert "Plan file not found" in result.stderr


def test_commit_group_and_phase_gate_helpers_report_errors(repo_root: Path, tmp_path: Path) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    plan = {
        "milestones": [{"id": "X1", "type": "X", "status": "in_progress"}],
        "sprints": [{"id": "S1.1", "type": "S", "parent": "X1", "status": "in_progress"}],
        "items": [
            {
                "id": "M1.1.1",
                "parent": "S1.1",
                "type": "M",
                "title": "Work",
                "status": "in_progress",
                "role": "implementer",
                "effort": "medium",
                "actions": ["implement"],
                "commit_group": "cg1",
                "requires_phase": "design-approved",
            },
            {
                "id": "T1.1.2",
                "parent": "S1.1",
                "type": "T",
                "title": "Verify",
                "status": "planned",
                "role": "tester",
                "effort": "low",
                "actions": ["verify"],
                "commit_group": "cg2",
                "depends_on": [],
            },
        ],
        "commit_groups": [{"id": "cg1", "title": "Mismatch", "items": ["M1.1.1", "missing"]}],
    }
    repo_map = tmp_path / "REPO_MAP.md"
    repo_map.write_text("map\n", encoding="utf-8")

    assert module.validate_commit_group_coherence(plan)
    errors, warnings = module.validate_phase_gates(plan["items"])
    assert errors
    assert not warnings
    assert module.check_repo_map_freshness(plan, tmp_path) == []


def test_validate_custom_rules_reports_composite_errors_and_warnings(repo_root: Path) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    plan = {
        "milestones": [
            {"id": "bad", "type": "X", "status": "planned"},
            {"id": "X1", "type": "X", "status": "planned"},
        ],
        "sprints": [
            {"id": "bad", "type": "S", "parent": "bad", "status": "planned"},
            {"id": "S1.1", "type": "S", "parent": "X1", "status": "planned"},
        ],
        "items": [
            {
                "id": "bad",
                "type": "D",
                "status": "planned",
                "actions": ["plan"],
                "commit_group": "cg1",
                "depends_on": [],
            },
            {
                "id": "M1.1.1a",
                "type": "M",
                "status": "in_progress",
                "actions": ["audit"],
                "commit_group": "cg1",
                "depends_on": ["X1"],
                "scope": "pkg/src",
            },
            {
                "id": "M1.1.1c",
                "type": "M",
                "status": "in_progress",
                "actions": ["audit"],
                "commit_group": "cg2",
                "depends_on": ["missing"],
                "scope": "pkg",
            },
            {
                "id": "M1.1.1c",
                "type": "M",
                "status": "planned",
                "actions": ["implement"],
                "commit_group": "cg2",
                "depends_on": [],
            },
            {
                "id": "T1.1.2",
                "type": "T",
                "status": "ready",
                "actions": ["verify"],
                "commit_group": "cg3",
                "depends_on": ["M1.1.3"],
            },
            {
                "id": "M1.1.3",
                "type": "M",
                "status": "planned",
                "actions": ["implement"],
                "commit_group": "cg9",
                "depends_on": [],
            },
            {
                "id": "D1.1.4",
                "type": "D",
                "status": "review",
                "actions": ["document"],
                "commit_group": "cg4",
                "requires_phase": "A",
            },
            {
                "id": "F1.1.5",
                "type": "F",
                "status": "planned",
                "actions": ["implement"],
                "commit_group": "",
                "depends_on": [],
                "shared_assets": {"skill": "missing-skill"},
            },
        ],
        "commit_groups": [
            {"id": "cg1", "title": "Group one", "items": ["M1.1.1a", "missing"]},
            {"id": "cg2", "title": "Group two", "items": ["M1.1.1a"]},
            {"id": "cg3", "title": "Group three", "items": ["T1.1.2"]},
            {"id": "cg4", "title": "Group four", "items": ["D1.1.4"]},
        ],
    }

    errors, warnings = module.validate_custom_rules(plan, {"wrong-kind": {"kind": "prompt"}})

    assert any("milestone id 'bad' is invalid" in error for error in errors)
    assert any("sprint id 'bad' is invalid" in error for error in errors)
    assert any("item id 'bad' is invalid" in error for error in errors)
    assert any("M1.1.1: duplicate suffix detected" in error for error in errors)
    assert any("M1.1.1: suffixes must be chronological" in error for error in errors)
    assert any("depends_on references container id 'X1' of type X" in error for error in errors)
    assert any("depends_on references unknown id 'missing'" in error for error in errors)
    assert any("dependency 'M1.1.3' is planned" in error for error in errors)
    assert any("item 'F1.1.5' is executable" in error for error in errors)
    assert any("item 'M1.1.3' references unknown commit_group 'cg9'" in error for error in errors)
    assert any("commit_group 'cg1' references unknown item 'missing'" in error for error in errors)
    assert any("but is not listed in that commit_group's items" in error for error in errors)
    assert any(
        "lists item 'M1.1.1a' but that item declares commit_group 'cg1'" in error
        for error in errors
    )
    assert any("references unknown asset id 'missing-skill'" in error for error in errors)
    assert any("but no approval_ref" in error for error in errors)
    assert any("scope collision warning" in warning for warning in warnings)
    assert any("not in recommended set for type M" in warning for warning in warnings)


def test_check_repo_map_freshness_reports_checkpoint_metadata_errors(
    repo_root: Path, tmp_path: Path
) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    plan = {
        "items": [
            {"id": "C1.1.1", "type": "C", "status": "review"},
            {"id": "C1.1.2", "type": "C", "status": "verified"},
        ]
    }
    repo_map = tmp_path / "REPO_MAP.md"

    repo_map.write_text("repo map\n", encoding="utf-8")
    errors = module.check_repo_map_freshness(plan, tmp_path)
    assert any("has no last_validated_on date" in error for error in errors)

    repo_map.write_text(
        "last_validated_on: 2000-01-01\nfreshness_window_days: nope\n",
        encoding="utf-8",
    )
    errors = module.check_repo_map_freshness(plan, tmp_path)
    assert any("REPO_MAP.md is stale" in error for error in errors)


def test_check_repo_map_freshness_handles_missing_map_and_fresh_map(
    repo_root: Path, tmp_path: Path
) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    plan = {"items": [{"id": "C1.1.1", "type": "C", "status": "review"}]}

    assert module.check_repo_map_freshness(plan, tmp_path) == []

    repo_map = tmp_path / "REPO_MAP.md"
    repo_map.write_text(
        "last_validated_on: 2999-01-01\nfreshness_window_days: 30\n",
        encoding="utf-8",
    )
    assert module.check_repo_map_freshness(plan, tmp_path) == []


def test_print_split_plan_report_emits_active_and_archived_counts(
    repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    module.print_split_plan_report(
        {
            "current_path": "plan/PLAN-current.yaml",
            "archive_root": "plan/archive",
            "current_fragment": {
                "milestones": [{"id": "X1"}],
                "sprints": [{"id": "S1.1"}],
                "items": [{"id": "D1.1.1"}],
                "commit_groups": [{"id": "cg1"}],
            },
            "archives": [
                {
                    "fragment": {
                        "milestones": [{"id": "X0"}],
                        "sprints": [{"id": "S0.1"}],
                        "items": [{"id": "D0.1.1"}, {"id": "T0.1.2"}],
                        "commit_groups": [{"id": "cg0"}],
                    }
                }
            ],
        }
    )

    report = capsys.readouterr().out
    assert "ACTIVE:" in report
    assert "ARCHIVED:" in report
    assert "fragments: 1" in report
    assert "items: 2" in report


def test_validate_plan_main_handles_previous_plan_failure(
    repo_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    current_path = copy_split_plan(tmp_path)
    previous_path = copy_split_plan(tmp_path / "previous")
    from conftest import inject_synthetic_current

    # Inject synthetic content into both plans so shared item IDs allow
    # lifecycle transition comparison regardless of live PLAN-current state.
    inject_synthetic_current(current_path.parent)
    previous_fragment = inject_synthetic_current(previous_path.parent)
    # Set previous item to "review" — since the current synthetic has
    # "in_progress", validate_transitions detects backward transition.
    previous_fragment["items"][0]["status"] = "review"
    write_yaml(previous_path.parent / "PLAN-current.yaml", previous_fragment)

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "validate-plan.py",
            str(current_path),
            "--schema",
            str(SCHEMA_PATH),
            "--previous-plan",
            str(previous_path),
        ],
    )

    assert module.main() == 1
    assert "Lifecycle transition checks failed" in capsys.readouterr().err


def test_validate_plan_main_handles_loader_and_dependency_failures(
    repo_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    index_path = copy_split_plan(tmp_path)

    monkeypatch.setattr(
        module, "load_plan", lambda _path: (_ for _ in ()).throw(module.PlanLoadError("bad plan"))
    )
    monkeypatch.setattr(
        sys, "argv", ["validate-plan.py", str(index_path), "--schema", str(SCHEMA_PATH)]
    )
    assert module.main() == 1
    assert "ERROR: Failed to load plan: bad plan" in capsys.readouterr().err

    monkeypatch.setattr(
        module, "load_plan", lambda _path: (_ for _ in ()).throw(RuntimeError("boom"))
    )
    monkeypatch.setattr(
        sys, "argv", ["validate-plan.py", str(index_path), "--schema", str(SCHEMA_PATH)]
    )
    assert module.main() == 2
    assert "ERROR: Failed to load plan: boom" in capsys.readouterr().err

    monkeypatch.setattr(
        module, "load_plan", lambda _path: ({}, {"format": "split", "index_path": index_path})
    )
    monkeypatch.setattr(
        module, "load_schema", lambda _path: (_ for _ in ()).throw(ValueError("bad schema"))
    )
    monkeypatch.setattr(
        sys, "argv", ["validate-plan.py", str(index_path), "--schema", str(SCHEMA_PATH)]
    )
    assert module.main() == 2
    assert "ERROR: Failed to load schema JSON: bad schema" in capsys.readouterr().err

    monkeypatch.setattr(module, "load_schema", lambda _path: {})
    monkeypatch.setattr(
        module,
        "load_shared_asset_registry",
        lambda _path: (_ for _ in ()).throw(ValueError("bad registry")),
    )
    monkeypatch.setattr(
        sys, "argv", ["validate-plan.py", str(index_path), "--schema", str(SCHEMA_PATH)]
    )
    assert module.main() == 2
    assert (
        "ERROR: Failed to load shared asset registry YAML: bad registry" in capsys.readouterr().err
    )


def test_validate_plan_main_handles_schema_and_previous_plan_branches(
    repo_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    index_path = copy_split_plan(tmp_path)
    previous_path = copy_split_plan(tmp_path / "prev")
    plan: dict[str, object] = {"items": []}
    metadata = {
        "format": "split",
        "index_path": index_path,
        "current_path": index_path.parent / "PLAN-current.yaml",
        "archive_root": index_path.parent / "archive",
        "current_fragment": {"milestones": [], "sprints": [], "items": [], "commit_groups": []},
        "archives": [],
    }

    monkeypatch.setattr(module, "load_plan", lambda _path: (plan, metadata))
    monkeypatch.setattr(module, "load_schema", lambda _path: {})
    monkeypatch.setattr(module, "load_shared_asset_registry", lambda _path: {"assets": []})
    monkeypatch.setattr(
        module, "validate_plan_schema", lambda _plan, _schema: (["meta.repo: bad"], "subset")
    )
    monkeypatch.setattr(
        sys, "argv", ["validate-plan.py", str(index_path), "--schema", str(SCHEMA_PATH)]
    )
    assert module.main() == 1
    assert "using built-in subset validator" in capsys.readouterr().err

    monkeypatch.setattr(
        module, "validate_plan_schema", lambda _plan, _schema: (["path: items/0/id"], "jsonschema")
    )
    monkeypatch.setattr(
        sys, "argv", ["validate-plan.py", str(index_path), "--schema", str(SCHEMA_PATH)]
    )
    assert module.main() == 1
    assert "ERROR: Schema validation failed" in capsys.readouterr().err

    monkeypatch.setattr(module, "validate_plan_schema", lambda _plan, _schema: ([], "jsonschema"))
    missing_previous = tmp_path / "missing-previous.yaml"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "validate-plan.py",
            str(index_path),
            "--schema",
            str(SCHEMA_PATH),
            "--previous-plan",
            str(missing_previous),
        ],
    )
    assert module.main() == 2
    assert "ERROR: Previous plan file not found" in capsys.readouterr().err

    call_state = {"count": 0}

    def load_plan_previous_failure(_path: Path) -> tuple[dict, dict]:
        call_state["count"] += 1
        if call_state["count"] == 1:
            return plan, metadata
        raise module.PlanLoadError("bad previous")

    monkeypatch.setattr(module, "load_plan", load_plan_previous_failure)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "validate-plan.py",
            str(index_path),
            "--schema",
            str(SCHEMA_PATH),
            "--previous-plan",
            str(previous_path),
        ],
    )
    assert module.main() == 1
    assert "ERROR: Failed to load previous plan: bad previous" in capsys.readouterr().err

    call_state["count"] = 0

    def load_plan_previous_exception(_path: Path) -> tuple[dict, dict]:
        call_state["count"] += 1
        if call_state["count"] == 1:
            return plan, metadata
        raise RuntimeError("explode")

    monkeypatch.setattr(module, "load_plan", load_plan_previous_exception)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "validate-plan.py",
            str(index_path),
            "--schema",
            str(SCHEMA_PATH),
            "--previous-plan",
            str(previous_path),
        ],
    )
    assert module.main() == 2
    assert "ERROR: Failed to load previous plan: explode" in capsys.readouterr().err


def test_validate_plan_main_emits_warnings_and_freshness_errors(
    repo_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    index_path = copy_split_plan(tmp_path)
    metadata = {
        "format": "split",
        "index_path": index_path,
        "current_path": index_path.parent / "PLAN-current.yaml",
        "archive_root": index_path.parent / "archive",
        "current_fragment": {"milestones": [], "sprints": [], "items": [], "commit_groups": []},
        "archives": [],
    }
    monkeypatch.setattr(module, "load_plan", lambda _path: ({"items": []}, metadata))
    monkeypatch.setattr(module, "load_schema", lambda _path: {})
    monkeypatch.setattr(module, "load_shared_asset_registry", lambda _path: {"assets": []})
    monkeypatch.setattr(module, "validate_plan_schema", lambda _plan, _schema: ([], "jsonschema"))
    monkeypatch.setattr(
        module, "validate_shared_asset_registry", lambda _registry, _path: ({}, ["registry error"])
    )
    monkeypatch.setattr(
        module,
        "validate_custom_rules",
        lambda _plan, _asset_map: (["governance error"], ["warn one"]),
    )
    monkeypatch.setattr(
        module, "check_repo_map_freshness", lambda _plan, _root: ["freshness error"]
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["validate-plan.py", str(index_path), "--schema", str(SCHEMA_PATH), "--check-freshness"],
    )

    assert module.main() == 1
    captured = capsys.readouterr()
    assert "ACTIVE:" in captured.out
    assert "WARNING: warn one" in captured.out
    assert "ERROR: Governance checks failed" in captured.err
    assert "registry error" in captured.err
    assert "freshness error" in captured.err


def test_validate_plan_main_compute_ready_success_and_error_paths(
    repo_root: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    index_path = copy_split_plan(tmp_path)
    metadata = {
        "format": "split",
        "index_path": index_path,
        "current_path": index_path.parent / "PLAN-current.yaml",
        "archive_root": index_path.parent / "archive",
        "current_fragment": {"milestones": [], "sprints": [], "items": [], "commit_groups": []},
        "archives": [],
    }
    plan = {
        "items": [
            {
                "id": "D1.1.1",
                "type": "D",
                "status": "planned",
                "commit_group": "cg1",
                "depends_on": [],
            }
        ]
    }

    monkeypatch.setattr(module, "load_plan", lambda _path: (plan, metadata))
    monkeypatch.setattr(module, "load_schema", lambda _path: {})
    monkeypatch.setattr(module, "load_shared_asset_registry", lambda _path: {"assets": []})
    monkeypatch.setattr(module, "validate_plan_schema", lambda _plan, _schema: ([], "jsonschema"))
    monkeypatch.setattr(module, "validate_shared_asset_registry", lambda _registry, _path: ({}, []))
    monkeypatch.setattr(
        module, "validate_custom_rules", lambda _plan, _asset_map: ([], ["warn one"])
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["validate-plan.py", str(index_path), "--schema", str(SCHEMA_PATH), "--compute-ready"],
    )

    assert module.main() == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ready_items"][0]["id"] == "D1.1.1"
    assert payload["warnings"] == ["warn one"]

    monkeypatch.setattr(module, "validate_custom_rules", lambda _plan, _asset_map: (["boom"], []))
    monkeypatch.setattr(
        sys,
        "argv",
        ["validate-plan.py", str(index_path), "--schema", str(SCHEMA_PATH), "--compute-ready"],
    )
    assert module.main() == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "Governance checks failed" in captured.err
    assert "boom" in captured.err


def test_validate_plan_script_entrypoint_runs(
    repo_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        ["validate-plan.py", str(PLAN_PATH), "--schema", str(SCHEMA_PATH)],
    )

    with pytest.raises(SystemExit) as exc:
        runpy.run_path(
            str(repo_root / "agent-os" / "scripts" / "validate-plan.py"), run_name="__main__"
        )

    assert exc.value.code == 0


# ---------------------------------------------------------------------------
# YAML unquoted-hash lint tests (issue #21)
# ---------------------------------------------------------------------------


def test_lint_detects_unquoted_hash_in_title(repo_root: Path, tmp_path: Path) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    p = tmp_path / "bad.yaml"
    p.write_text("milestones:\n- id: X99\n  title: Issue #8 Review\n  status: done\n")

    errors = module.lint_yaml_unquoted_hash(p)
    assert len(errors) == 1
    assert "#" in errors[0]
    assert "bad.yaml:3" in errors[0]


def test_lint_passes_quoted_hash_in_title(repo_root: Path, tmp_path: Path) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    p = tmp_path / "good.yaml"
    p.write_text("milestones:\n- id: X99\n  title: 'Issue #8 Review'\n  status: done\n")

    errors = module.lint_yaml_unquoted_hash(p)
    assert errors == []


def test_lint_ignores_block_scalars(repo_root: Path, tmp_path: Path) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    p = tmp_path / "block.yaml"
    p.write_text("note: >\n  This references issue #8 and is fine.\n  More text here.\nid: X1\n")

    errors = module.lint_yaml_unquoted_hash(p)
    assert errors == []


def test_lint_ignores_full_line_comments(repo_root: Path, tmp_path: Path) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    p = tmp_path / "comments.yaml"
    p.write_text("# This is a comment with #hash\nid: X1\ntitle: Safe title\n")

    errors = module.lint_yaml_unquoted_hash(p)
    assert errors == []


def test_lint_ignores_multiline_single_quoted_scalar(repo_root: Path, tmp_path: Path) -> None:
    module = load_module("validate_plan", repo_root / "agent-os" / "scripts" / "validate-plan.py")
    p = tmp_path / "multiline.yaml"
    p.write_text("note: 'This is a multi-line\n  scalar that mentions issue #25.\n\n  '\nid: X1\n")

    errors = module.lint_yaml_unquoted_hash(p)
    assert errors == []


def test_validate_plan_rejects_unquoted_hash(repo_root: Path, tmp_path: Path) -> None:
    index_path = copy_split_plan(tmp_path)
    current_path = index_path.parent / "PLAN-current.yaml"
    # Raw-write an unquoted # into a title (bypassing safe_dump).
    current_path.write_text(
        "milestones:\n- id: X99\n  type: X\n  title: Issue #21 bad title\n"
        "  status: in_progress\nsprints: []\nitems: []\ncommit_groups: []\n",
        encoding="utf-8",
    )

    result = run_python_script(
        repo_root / "agent-os" / "scripts" / "validate-plan.py",
        str(index_path),
        "--schema",
        str(SCHEMA_PATH),
    )
    assert result.returncode == 1
    combined = f"{result.stdout}\n{result.stderr}"
    assert "unquoted '#'" in combined


def test_roundtrip_title_with_hash(repo_root: Path, tmp_path: Path) -> None:
    from conftest import load_yaml as _load_yaml

    data = {
        "milestones": [{"id": "X99", "title": "Issue #8 Review", "status": "done"}],
        "sprints": [],
        "items": [],
        "commit_groups": [],
    }
    p = tmp_path / "roundtrip.yaml"
    write_yaml(p, data)

    reloaded = _load_yaml(p)
    assert reloaded["milestones"][0]["title"] == "Issue #8 Review"
