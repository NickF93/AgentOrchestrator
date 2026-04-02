from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest
import yaml


def load_module(module_name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    spec.loader.exec_module(module)
    return module


def write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def make_fragment(
    *,
    milestone_id: str,
    milestone_title: str,
    milestone_status: str,
    sprint_id: str,
    item_id: str,
    commit_group_id: str,
) -> dict:
    return {
        "milestones": [
            {
                "id": milestone_id,
                "type": "X",
                "title": milestone_title,
                "status": milestone_status,
            }
        ],
        "sprints": [
            {
                "id": sprint_id,
                "type": "S",
                "parent": milestone_id,
                "title": f"{milestone_title} sprint",
                "status": milestone_status,
            }
        ],
        "items": [
            {
                "id": item_id,
                "parent": sprint_id,
                "type": "D",
                "title": f"{milestone_title} item",
                "actions": ["plan"],
                "status": milestone_status,
                "role": "orchestrator",
                "effort": "low",
                "commit_group": commit_group_id,
                "scope": ".",
            }
        ],
        "commit_groups": [
            {
                "id": commit_group_id,
                "title": f"{milestone_title} commit group",
                "items": [item_id],
            }
        ],
    }


def build_index(
    repo_root: Path,
    tmp_path: Path,
    *,
    current_fragment: dict,
    archives: list[tuple[str, str, dict]],
) -> tuple[Path, Any]:
    loader = load_module("plan_loader", repo_root / "agent-os" / "scripts" / "plan_loader.py")
    current_path = tmp_path / "plan" / "PLAN-current.yaml"
    write_yaml(current_path, current_fragment)

    index_archives: list[dict[str, str]] = []
    for milestone_id, title, fragment in archives:
        archive_path = tmp_path / "plan" / "archive" / f"PLAN-{milestone_id}.yaml"
        write_yaml(archive_path, fragment)
        index_archives.append(
            {
                "milestone": milestone_id,
                "title": title,
                "path": f"archive/PLAN-{milestone_id}.yaml",
                "digest": loader.compute_fragment_digest(fragment),
            }
        )

    index = {
        "meta": {
            "repo": "fixture",
            "owner": "tester",
            "version": "1",
            "schema_version": "1",
            "last_updated": "2026-04-02",
        },
        "mission": "Fixture mission",
        "current_plan": "PLAN-current.yaml",
        "archive_root": "archive",
        "archives": index_archives,
    }
    index_path = tmp_path / "plan" / "PLAN-index.yaml"
    write_yaml(index_path, index)
    return index_path, loader


def test_load_split_plan_aggregates_archive_and_current_in_id_order(
    repo_root: Path, tmp_path: Path
) -> None:
    current_fragment = make_fragment(
        milestone_id="X2",
        milestone_title="Current milestone",
        milestone_status="in_progress",
        sprint_id="S2.1",
        item_id="D2.1.1",
        commit_group_id="cg2",
    )
    archive_fragment = make_fragment(
        milestone_id="X1",
        milestone_title="Archived milestone",
        milestone_status="done",
        sprint_id="S1.1",
        item_id="D1.1.1",
        commit_group_id="cg1",
    )
    index_path, loader = build_index(
        repo_root,
        tmp_path,
        current_fragment=current_fragment,
        archives=[("X1", "Archived milestone", archive_fragment)],
    )

    aggregate, metadata = loader.load_split_plan(index_path)

    assert metadata["format"] == "split"
    assert [obj["id"] for obj in aggregate["milestones"]] == ["X1", "X2"]
    assert [obj["id"] for obj in aggregate["sprints"]] == ["S1.1", "S2.1"]
    assert [obj["id"] for obj in aggregate["items"]] == ["D1.1.1", "D2.1.1"]
    assert [obj["id"] for obj in aggregate["commit_groups"]] == ["cg1", "cg2"]


def test_load_split_plan_accepts_empty_current_fragment(repo_root: Path, tmp_path: Path) -> None:
    archive_fragment = make_fragment(
        milestone_id="X1",
        milestone_title="Archived milestone",
        milestone_status="done",
        sprint_id="S1.1",
        item_id="D1.1.1",
        commit_group_id="cg1",
    )
    index_path, loader = build_index(
        repo_root,
        tmp_path,
        current_fragment={"milestones": [], "sprints": [], "items": [], "commit_groups": []},
        archives=[("X1", "Archived milestone", archive_fragment)],
    )

    aggregate, _ = loader.load_split_plan(index_path)

    assert [obj["id"] for obj in aggregate["milestones"]] == ["X1"]


def test_load_split_plan_rejects_missing_archive_path_reference(
    repo_root: Path, tmp_path: Path
) -> None:
    archive_fragment = make_fragment(
        milestone_id="X1",
        milestone_title="Archived milestone",
        milestone_status="done",
        sprint_id="S1.1",
        item_id="D1.1.1",
        commit_group_id="cg1",
    )
    index_path, loader = build_index(
        repo_root,
        tmp_path,
        current_fragment={"milestones": [], "sprints": [], "items": [], "commit_groups": []},
        archives=[("X1", "Archived milestone", archive_fragment)],
    )
    index = load_yaml(index_path)
    del index["archives"][0]["path"]
    write_yaml(index_path, index)

    with pytest.raises(loader.PlanLoadError, match=r"archives\[0\]\.path"):
        loader.load_split_plan(index_path)


def test_load_split_plan_rejects_duplicate_archive_milestones(
    repo_root: Path, tmp_path: Path
) -> None:
    archive_fragment = make_fragment(
        milestone_id="X1",
        milestone_title="Archived milestone",
        milestone_status="done",
        sprint_id="S1.1",
        item_id="D1.1.1",
        commit_group_id="cg1",
    )
    index_path, loader = build_index(
        repo_root,
        tmp_path,
        current_fragment={"milestones": [], "sprints": [], "items": [], "commit_groups": []},
        archives=[("X1", "Archived milestone", archive_fragment)],
    )
    index = load_yaml(index_path)
    duplicate_path = tmp_path / "plan" / "archive" / "PLAN-X1-duplicate.yaml"
    write_yaml(duplicate_path, archive_fragment)
    index["archives"].append(
        {
            "milestone": "X1",
            "title": "Archived milestone",
            "path": "archive/PLAN-X1-duplicate.yaml",
            "digest": loader.compute_fragment_digest(archive_fragment),
        }
    )
    write_yaml(index_path, index)

    with pytest.raises(loader.PlanLoadError, match="duplicate archived milestone 'X1'"):
        loader.load_split_plan(index_path)


def test_load_plan_rejects_legacy_aggregate_runtime_input(repo_root: Path, tmp_path: Path) -> None:
    loader = load_module("plan_loader", repo_root / "agent-os" / "scripts" / "plan_loader.py")
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

    with pytest.raises(loader.PlanLoadError, match="must be a split plan index"):
        loader.load_plan(legacy_path)


def test_load_split_plan_rejects_sprint_parent_outside_fragment(
    repo_root: Path, tmp_path: Path
) -> None:
    broken_archive = make_fragment(
        milestone_id="X1",
        milestone_title="Archived milestone",
        milestone_status="done",
        sprint_id="S1.1",
        item_id="D1.1.1",
        commit_group_id="cg1",
    )
    broken_archive["sprints"][0]["parent"] = "X9"
    index_path, loader = build_index(
        repo_root,
        tmp_path,
        current_fragment={"milestones": [], "sprints": [], "items": [], "commit_groups": []},
        archives=[("X1", "Archived milestone", broken_archive)],
    )

    with pytest.raises(loader.PlanLoadError, match="parent outside its fragment"):
        loader.load_split_plan(index_path)


def test_load_split_plan_rejects_commit_group_items_outside_fragment(
    repo_root: Path, tmp_path: Path
) -> None:
    broken_archive = make_fragment(
        milestone_id="X1",
        milestone_title="Archived milestone",
        milestone_status="done",
        sprint_id="S1.1",
        item_id="D1.1.1",
        commit_group_id="cg1",
    )
    broken_archive["commit_groups"][0]["items"] = ["D1.1.1", "D9.9.9"]
    index_path, loader = build_index(
        repo_root,
        tmp_path,
        current_fragment={"milestones": [], "sprints": [], "items": [], "commit_groups": []},
        archives=[("X1", "Archived milestone", broken_archive)],
    )

    with pytest.raises(loader.PlanLoadError, match="references items outside its fragment"):
        loader.load_split_plan(index_path)


def test_load_yaml_mapping_rejects_non_mapping_document(repo_root: Path, tmp_path: Path) -> None:
    loader = load_module("plan_loader", repo_root / "agent-os" / "scripts" / "plan_loader.py")
    path = tmp_path / "list.yaml"
    path.write_text("- not\n- a\n- mapping\n", encoding="utf-8")

    with pytest.raises(loader.PlanLoadError, match="top-level YAML document must be a mapping"):
        loader.load_yaml_mapping(path)


@pytest.mark.parametrize(
    ("fragment", "message"),
    [
        (
            {"milestones": [{"id": "bad"}], "sprints": [], "items": [], "commit_groups": []},
            "Invalid milestone ID",
        ),
        (
            {"milestones": [], "sprints": [{"id": "bad"}], "items": [], "commit_groups": []},
            "Invalid sprint ID",
        ),
        (
            {"milestones": [], "sprints": [], "items": [{"id": "bad"}], "commit_groups": []},
            "Invalid item ID",
        ),
        (
            {"milestones": [], "sprints": [], "items": [], "commit_groups": [{"id": "bad"}]},
            "Invalid commit group ID",
        ),
    ],
)
def test_sort_fragment_rejects_invalid_ids(repo_root: Path, fragment: dict, message: str) -> None:
    loader = load_module("plan_loader", repo_root / "agent-os" / "scripts" / "plan_loader.py")

    with pytest.raises(loader.PlanLoadError, match=message):
        loader.sort_fragment(fragment)


def test_load_fragment_rejects_missing_required_keys(repo_root: Path, tmp_path: Path) -> None:
    loader = load_module("plan_loader", repo_root / "agent-os" / "scripts" / "plan_loader.py")
    path = tmp_path / "fragment.yaml"
    write_yaml(path, {"milestones": [], "sprints": [], "items": []})

    with pytest.raises(loader.PlanLoadError, match="fragment is missing required keys"):
        loader.load_fragment(path, kind="current")


def test_load_fragment_rejects_non_list_commit_group_members(repo_root: Path, tmp_path: Path) -> None:
    loader = load_module("plan_loader", repo_root / "agent-os" / "scripts" / "plan_loader.py")
    fragment = make_fragment(
        milestone_id="X1",
        milestone_title="Archived milestone",
        milestone_status="done",
        sprint_id="S1.1",
        item_id="D1.1.1",
        commit_group_id="cg1",
    )
    fragment["commit_groups"][0]["items"] = "D1.1.1"
    path = tmp_path / "fragment.yaml"
    write_yaml(path, fragment)

    with pytest.raises(loader.PlanLoadError, match="must declare a non-empty items list"):
        loader.load_fragment(path, kind="archive", expected_milestone="X1")


def test_load_split_plan_rejects_invalid_index_fields(repo_root: Path, tmp_path: Path) -> None:
    index_path, loader = build_index(
        repo_root,
        tmp_path,
        current_fragment={"milestones": [], "sprints": [], "items": [], "commit_groups": []},
        archives=[],
    )
    index = load_yaml(index_path)
    index["meta"] = "bad"
    index["mission"] = ""
    index["archives"] = "bad"
    write_yaml(index_path, index)

    with pytest.raises(loader.PlanLoadError, match="'meta' must be a mapping"):
        loader.load_split_plan(index_path)


def test_load_split_plan_rejects_archive_title_mismatch(repo_root: Path, tmp_path: Path) -> None:
    archive_fragment = make_fragment(
        milestone_id="X1",
        milestone_title="Archived milestone",
        milestone_status="done",
        sprint_id="S1.1",
        item_id="D1.1.1",
        commit_group_id="cg1",
    )
    index_path, loader = build_index(
        repo_root,
        tmp_path,
        current_fragment={"milestones": [], "sprints": [], "items": [], "commit_groups": []},
        archives=[("X1", "Wrong title", archive_fragment)],
    )

    with pytest.raises(loader.PlanLoadError, match="archive title mismatch"):
        loader.load_split_plan(index_path)


def test_load_split_plan_rejects_archive_outside_archive_root(repo_root: Path, tmp_path: Path) -> None:
    archive_fragment = make_fragment(
        milestone_id="X1",
        milestone_title="Archived milestone",
        milestone_status="done",
        sprint_id="S1.1",
        item_id="D1.1.1",
        commit_group_id="cg1",
    )
    index_path, loader = build_index(
        repo_root,
        tmp_path,
        current_fragment={"milestones": [], "sprints": [], "items": [], "commit_groups": []},
        archives=[("X1", "Archived milestone", archive_fragment)],
    )
    index = load_yaml(index_path)
    outside_path = tmp_path / "plan" / "PLAN-X1.yaml"
    write_yaml(outside_path, archive_fragment)
    index["archives"][0]["path"] = "PLAN-X1.yaml"
    write_yaml(index_path, index)

    with pytest.raises(loader.PlanLoadError, match="must live under"):
        loader.load_split_plan(index_path)


def test_extract_fragment_rejects_cross_milestone_commit_group(repo_root: Path) -> None:
    loader = load_module("plan_loader", repo_root / "agent-os" / "scripts" / "plan_loader.py")
    plan = {
        "meta": {"repo": "fixture", "owner": "tester", "version": "1", "schema_version": "1"},
        "mission": "Fixture mission",
        "milestones": [
            {"id": "X1", "type": "X", "title": "One", "status": "done"},
            {"id": "X2", "type": "X", "title": "Two", "status": "in_progress"},
        ],
        "sprints": [
            {"id": "S1.1", "type": "S", "parent": "X1", "title": "One sprint", "status": "done"},
            {"id": "S2.1", "type": "S", "parent": "X2", "title": "Two sprint", "status": "in_progress"},
        ],
        "items": [
            {
                "id": "D1.1.1",
                "parent": "S1.1",
                "type": "D",
                "title": "One item",
                "actions": ["document"],
                "status": "done",
                "role": "documenter",
                "effort": "low",
                "commit_group": "cg1",
                "scope": ".",
            },
            {
                "id": "M2.1.1",
                "parent": "S2.1",
                "type": "M",
                "title": "Two item",
                "actions": ["implement"],
                "status": "in_progress",
                "role": "implementer",
                "effort": "medium",
                "commit_group": "cg1",
                "scope": ".",
            },
        ],
        "commit_groups": [{"id": "cg1", "title": "Cross milestone", "items": ["D1.1.1", "M2.1.1"]}],
    }

    with pytest.raises(loader.PlanLoadError, match="spans multiple milestone fragments"):
        loader.extract_fragment(plan, {"X1"})


def test_build_split_layout_archives_done_milestones_in_order(repo_root: Path) -> None:
    loader = load_module("plan_loader", repo_root / "agent-os" / "scripts" / "plan_loader.py")
    plan = {
        "meta": {"repo": "fixture", "owner": "tester", "version": "1", "schema_version": "1"},
        "mission": "Fixture mission",
        "milestones": [
            {"id": "X2", "type": "X", "title": "Two", "status": "done"},
            {"id": "X1", "type": "X", "title": "One", "status": "done"},
        ],
        "sprints": [
            {"id": "S2.1", "type": "S", "parent": "X2", "title": "Two sprint", "status": "done"},
            {"id": "S1.1", "type": "S", "parent": "X1", "title": "One sprint", "status": "done"},
        ],
        "items": [
            {
                "id": "D2.1.1",
                "parent": "S2.1",
                "type": "D",
                "title": "Two item",
                "actions": ["document"],
                "status": "done",
                "role": "documenter",
                "effort": "low",
                "commit_group": "cg2",
                "scope": ".",
            },
            {
                "id": "D1.1.1",
                "parent": "S1.1",
                "type": "D",
                "title": "One item",
                "actions": ["document"],
                "status": "done",
                "role": "documenter",
                "effort": "low",
                "commit_group": "cg1",
                "scope": ".",
            },
        ],
        "commit_groups": [
            {"id": "cg2", "title": "Two work", "items": ["D2.1.1"]},
            {"id": "cg1", "title": "One work", "items": ["D1.1.1"]},
        ],
    }

    index, current_fragment, archive_fragments = loader.build_split_layout(plan)

    assert current_fragment == {"milestones": [], "sprints": [], "items": [], "commit_groups": []}
    assert [entry["milestone"] for entry in index["archives"]] == ["X1", "X2"]
    assert sorted(archive_fragments) == ["archive/PLAN-X1.yaml", "archive/PLAN-X2.yaml"]


def test_ensure_list_of_mappings_rejects_invalid_shapes(repo_root: Path, tmp_path: Path) -> None:
    loader = load_module("plan_loader", repo_root / "agent-os" / "scripts" / "plan_loader.py")

    with pytest.raises(loader.PlanLoadError, match="'items' must be a list"):
        loader._ensure_list_of_mappings("bad", "items", tmp_path / "fragment.yaml")

    with pytest.raises(loader.PlanLoadError, match="'items\\[0\\]' must be a mapping"):
        loader._ensure_list_of_mappings(["bad"], "items", tmp_path / "fragment.yaml")


def test_resolve_relative_path_rejects_absolute_paths(repo_root: Path, tmp_path: Path) -> None:
    loader = load_module("plan_loader", repo_root / "agent-os" / "scripts" / "plan_loader.py")

    with pytest.raises(loader.PlanLoadError, match="must be relative"):
        loader._resolve_relative_path(tmp_path, "/abs/path.yaml", "current_plan")


def test_load_split_plan_rejects_non_index_documents(repo_root: Path, tmp_path: Path) -> None:
    loader = load_module("plan_loader", repo_root / "agent-os" / "scripts" / "plan_loader.py")
    path = tmp_path / "PLAN.yaml"
    write_yaml(
        path,
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

    with pytest.raises(loader.PlanLoadError, match="not a split plan index"):
        loader.load_split_plan(path)


def test_load_plan_accepts_split_index(repo_root: Path, tmp_path: Path) -> None:
    index_path, loader = build_index(
        repo_root,
        tmp_path,
        current_fragment={"milestones": [], "sprints": [], "items": [], "commit_groups": []},
        archives=[],
    )

    _, metadata = loader.load_plan(index_path)

    assert metadata["format"] == "split"


@pytest.mark.parametrize(
    ("mutator", "message"),
    [
        (lambda index: index.update({"mission": ""}), "'mission' must be a non-empty string"),
        (lambda index: index.update({"archives": "bad"}), "'archives' must be a list"),
    ],
)
def test_load_split_plan_rejects_other_invalid_index_fields(
    repo_root: Path, tmp_path: Path, mutator: Any, message: str
) -> None:
    index_path, loader = build_index(
        repo_root,
        tmp_path,
        current_fragment={"milestones": [], "sprints": [], "items": [], "commit_groups": []},
        archives=[],
    )
    index = load_yaml(index_path)
    mutator(index)
    write_yaml(index_path, index)

    with pytest.raises(loader.PlanLoadError, match=message):
        loader.load_split_plan(index_path)


@pytest.mark.parametrize(
    ("archive_entry", "message"),
    [
        ("bad", r"archives\[0\] must be a mapping"),
        ({}, r"archives\[0\]\.milestone must be a non-empty string"),
        (
            {"milestone": "X1", "title": "", "path": "archive/PLAN-X1.yaml", "digest": "sha256:abc"},
            r"archives\[0\]\.title must be a non-empty string",
        ),
        (
            {"milestone": "X1", "title": "Archived milestone", "path": "archive/PLAN-X1.yaml", "digest": ""},
            r"archives\[0\]\.digest must be a non-empty string",
        ),
    ],
)
def test_load_split_plan_rejects_invalid_archive_entries(
    repo_root: Path, tmp_path: Path, archive_entry: Any, message: str
) -> None:
    index_path, loader = build_index(
        repo_root,
        tmp_path,
        current_fragment={"milestones": [], "sprints": [], "items": [], "commit_groups": []},
        archives=[],
    )
    index = load_yaml(index_path)
    index["archives"] = [archive_entry]
    write_yaml(index_path, index)

    with pytest.raises(loader.PlanLoadError, match=message):
        loader.load_split_plan(index_path)


def test_load_split_plan_rejects_duplicate_archive_paths(repo_root: Path, tmp_path: Path) -> None:
    archive_fragment_one = make_fragment(
        milestone_id="X1",
        milestone_title="Archived one",
        milestone_status="done",
        sprint_id="S1.1",
        item_id="D1.1.1",
        commit_group_id="cg1",
    )
    archive_fragment_two = make_fragment(
        milestone_id="X2",
        milestone_title="Archived two",
        milestone_status="done",
        sprint_id="S2.1",
        item_id="D2.1.1",
        commit_group_id="cg2",
    )
    index_path, loader = build_index(
        repo_root,
        tmp_path,
        current_fragment={"milestones": [], "sprints": [], "items": [], "commit_groups": []},
        archives=[("X1", "Archived one", archive_fragment_one)],
    )
    archive_path = tmp_path / "plan" / "archive" / "PLAN-X2.yaml"
    write_yaml(archive_path, archive_fragment_two)
    index = load_yaml(index_path)
    index["archives"].append(
        {
            "milestone": "X2",
            "title": "Archived two",
            "path": "archive/PLAN-X1.yaml",
            "digest": loader.compute_fragment_digest(archive_fragment_two),
        }
    )
    write_yaml(index_path, index)

    with pytest.raises(loader.PlanLoadError, match="duplicate split-plan fragment path"):
        loader.load_split_plan(index_path)


@pytest.mark.parametrize(
    ("mutator", "message"),
    [
        (
            lambda fragment: fragment["milestones"].append(
                {"id": "X9", "type": "X", "title": "Extra", "status": "done"}
            ),
            "archive fragment must contain exactly one milestone",
        ),
        (
            lambda fragment: fragment["milestones"].__setitem__(
                0, {"id": "X9", "type": "X", "title": "Wrong", "status": "done"}
            ),
            "archive fragment milestone mismatch",
        ),
        (
            lambda fragment: fragment["milestones"][0].update({"status": "review"}),
            "archived milestone must have status 'done'",
        ),
        (
            lambda fragment: fragment["items"][0].update({"parent": "S9.9"}),
            "parent sprint outside its fragment",
        ),
    ],
)
def test_load_fragment_rejects_archive_validation_errors(
    repo_root: Path, tmp_path: Path, mutator: Any, message: str
) -> None:
    loader = load_module("plan_loader", repo_root / "agent-os" / "scripts" / "plan_loader.py")
    fragment = make_fragment(
        milestone_id="X1",
        milestone_title="Archived milestone",
        milestone_status="done",
        sprint_id="S1.1",
        item_id="D1.1.1",
        commit_group_id="cg1",
    )
    mutator(fragment)
    path = tmp_path / "fragment.yaml"
    write_yaml(path, fragment)

    with pytest.raises(loader.PlanLoadError, match=message):
        loader.load_fragment(path, kind="archive", expected_milestone="X1")


def test_load_split_plan_rejects_archive_digest_mismatch(repo_root: Path, tmp_path: Path) -> None:
    archive_fragment = make_fragment(
        milestone_id="X1",
        milestone_title="Archived milestone",
        milestone_status="done",
        sprint_id="S1.1",
        item_id="D1.1.1",
        commit_group_id="cg1",
    )
    index_path, loader = build_index(
        repo_root,
        tmp_path,
        current_fragment={"milestones": [], "sprints": [], "items": [], "commit_groups": []},
        archives=[("X1", "Archived milestone", archive_fragment)],
    )
    index = load_yaml(index_path)
    index["archives"][0]["digest"] = "sha256:000000000000"
    write_yaml(index_path, index)

    with pytest.raises(loader.PlanLoadError, match="archive digest mismatch"):
        loader.load_split_plan(index_path)


def test_load_split_plan_rejects_duplicate_aggregate_ids(repo_root: Path, tmp_path: Path) -> None:
    current_fragment = make_fragment(
        milestone_id="X2",
        milestone_title="Current milestone",
        milestone_status="in_progress",
        sprint_id="S2.1",
        item_id="D2.1.1",
        commit_group_id="cg2",
    )
    archive_fragment = make_fragment(
        milestone_id="X1",
        milestone_title="Archived milestone",
        milestone_status="done",
        sprint_id="S2.1",
        item_id="D1.1.1",
        commit_group_id="cg1",
    )
    index_path, loader = build_index(
        repo_root,
        tmp_path,
        current_fragment=current_fragment,
        archives=[("X1", "Archived milestone", archive_fragment)],
    )

    with pytest.raises(loader.PlanLoadError, match="duplicate sprint id 'S2.1'"):
        loader.load_split_plan(index_path)
