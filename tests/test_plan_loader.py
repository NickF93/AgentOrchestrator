from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
import yaml


def load_module(module_name: str, path: Path) -> object:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


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
) -> tuple[Path, object]:
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
        archives=[
            ("X1", "Archived milestone", archive_fragment),
            ("X1", "Archived milestone", archive_fragment),
        ],
    )

    with pytest.raises(loader.PlanLoadError, match="duplicate archived milestone 'X1'"):
        loader.load_split_plan(index_path)


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
