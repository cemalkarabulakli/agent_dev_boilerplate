from __future__ import annotations

from pathlib import Path

from scripts.update_readme_project_scan import (
    END_MARKER,
    START_MARKER,
    diff_file_maps,
    should_scan_path,
    update_readme_section,
)


ROOT = Path(__file__).resolve().parents[1]


def test_diff_file_maps_detects_added_changed_and_deleted() -> None:
    previous = {
        "deleted.txt": {"sha256": "old", "size": 3},
        "changed.txt": {"sha256": "old", "size": 3},
        "same.txt": {"sha256": "same", "size": 4},
    }
    current = {
        "added.txt": {"sha256": "new", "size": 3},
        "changed.txt": {"sha256": "new", "size": 3},
        "same.txt": {"sha256": "same", "size": 4},
    }
    changes = diff_file_maps(previous, current)
    assert changes.added == ["added.txt"]
    assert changes.changed == ["changed.txt"]
    assert changes.deleted == ["deleted.txt"]


def test_update_readme_section_only_replaces_generated_block() -> None:
    readme = f"# Title\n\nKeep this.\n\n{START_MARKER}\nold\n{END_MARKER}\n\nKeep this too.\n"
    updated = update_readme_section(readme, f"{START_MARKER}\nnew\n{END_MARKER}")
    assert "Keep this." in updated
    assert "Keep this too." in updated
    assert "old" not in updated
    assert "new" in updated


def test_update_readme_section_creates_block_when_missing() -> None:
    updated = update_readme_section("# Title\n", f"{START_MARKER}\nnew\n{END_MARKER}")
    assert "# Title" in updated
    assert START_MARKER in updated
    assert END_MARKER in updated


def test_scan_excludes_readme_and_manifest_to_avoid_self_loops() -> None:
    assert not should_scan_path("README.md")
    assert not should_scan_path(".readme_project_manifest.json")
    assert not should_scan_path("reports/example.md")
    assert not should_scan_path("agents/cto/knowledge/processed/index.json")
    assert should_scan_path("core/schema.py")


def test_readme_project_scan_workflow_exists_with_cron_and_dispatch() -> None:
    workflow = ROOT / ".github" / "workflows" / "readme-project-scan.yml"
    text = workflow.read_text(encoding="utf-8")
    assert workflow.exists()
    assert "23 4 * * *" in text
    assert "workflow_dispatch" in text
    assert "gh pr create" in text
