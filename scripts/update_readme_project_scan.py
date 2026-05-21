from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
START_MARKER = "<!-- PROJECT_SCAN:START -->"
END_MARKER = "<!-- PROJECT_SCAN:END -->"
MANIFEST_NAME = ".readme_project_manifest.json"

EXCLUDED_EXACT = {
    "README.md",
    MANIFEST_NAME,
}
EXCLUDED_PREFIXES = (
    ".git/",
    ".venv/",
    "venv/",
    "reports/",
    ".pytest_cache/",
    ".mypy_cache/",
    ".ruff_cache/",
    "agent_template_system.egg-info/",
    "build/",
    "dist/",
)
EXCLUDED_PARTS = {
    "__pycache__",
}
EXCLUDED_PATTERNS = (
    "agents/*/knowledge/processed/index.json",
    "*.pyc",
)


@dataclass(frozen=True)
class ChangeSet:
    added: list[str]
    changed: list[str]
    deleted: list[str]

    @property
    def has_changes(self) -> bool:
        return bool(self.added or self.changed or self.deleted)


@dataclass(frozen=True)
class ReadmeUpdatePlan:
    readme_text: str
    manifest_text: str
    readme_changed: bool
    manifest_changed: bool
    changes: ChangeSet

    @property
    def has_writes(self) -> bool:
        return self.readme_changed or self.manifest_changed


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_path(path: str | Path) -> str:
    normalized = str(path).replace("\\", "/")
    if normalized.startswith("./"):
        return normalized[2:]
    return normalized


def should_scan_path(path: str | Path) -> bool:
    normalized = normalize_path(path)
    if normalized in EXCLUDED_EXACT:
        return False
    if any(normalized.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
        return False
    parts = set(normalized.split("/"))
    if parts & EXCLUDED_PARTS:
        return False
    return not any(fnmatch.fnmatch(normalized, pattern) for pattern in EXCLUDED_PATTERNS)


def git_list_files(root: Path) -> list[str]:
    command = ["git", "ls-files", "-co", "--exclude-standard"]
    try:
        completed = subprocess.run(
            command,
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return [
            normalize_path(path.relative_to(root))
            for path in root.rglob("*")
            if path.is_file()
        ]
    return [normalize_path(line) for line in completed.stdout.splitlines() if line.strip()]


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_file_map(root: Path) -> dict[str, dict[str, Any]]:
    files: dict[str, dict[str, Any]] = {}
    for relative in sorted(git_list_files(root)):
        if not should_scan_path(relative):
            continue
        path = root / relative
        if not path.is_file():
            continue
        files[relative] = {
            "sha256": file_sha256(path),
            "size": path.stat().st_size,
        }
    return files


def load_manifest(root: Path) -> dict[str, Any]:
    path = root / MANIFEST_NAME
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def diff_file_maps(previous_files: dict[str, Any], current_files: dict[str, Any]) -> ChangeSet:
    previous_paths = set(previous_files)
    current_paths = set(current_files)
    added = sorted(current_paths - previous_paths)
    deleted = sorted(previous_paths - current_paths)
    changed = sorted(
        path
        for path in previous_paths & current_paths
        if previous_files[path].get("sha256") != current_files[path].get("sha256")
    )
    return ChangeSet(added=added, changed=changed, deleted=deleted)


def list_agents(root: Path) -> list[str]:
    agents_root = root / "agents"
    if not agents_root.exists():
        return []
    return sorted(
        path.parent.name
        for path in agents_root.glob("*/agent.yaml")
        if path.parent.name != "_template"
    )


def list_workflows(root: Path) -> list[str]:
    workflows_root = root / ".github" / "workflows"
    if not workflows_root.exists():
        return []
    return sorted(path.name for path in workflows_root.glob("*.y*ml"))


def format_list(items: list[str], limit: int = 20) -> str:
    if not items:
        return "None"
    visible = items[:limit]
    suffix = "" if len(items) <= limit else f", ... and {len(items) - limit} more"
    return ", ".join(visible) + suffix


def render_change_items(label: str, items: list[str]) -> list[str]:
    if not items:
        return [f"- {label}: None"]
    return [f"- {label}: {format_list(items)}"]


def render_project_scan_section(
    *,
    generated_at: str,
    files_scanned: int,
    agents: list[str],
    workflows: list[str],
    changes: ChangeSet,
) -> str:
    lines = [
        START_MARKER,
        "## Project Scan",
        "",
        "This section is machine-generated by `scripts/update_readme_project_scan.py`.",
        "",
        f"Last scan: {generated_at}",
        "",
        f"- Files scanned: {files_scanned}",
        f"- Agents: {format_list(agents)}",
        f"- Workflows: {format_list(workflows)}",
        "",
        "### Changes Since Last Scan",
    ]
    lines.extend(render_change_items("Added", changes.added))
    lines.extend(render_change_items("Changed", changes.changed))
    lines.extend(render_change_items("Deleted", changes.deleted))
    lines.append(END_MARKER)
    return "\n".join(lines)


def update_readme_section(readme_text: str, section: str) -> str:
    has_start = START_MARKER in readme_text
    has_end = END_MARKER in readme_text
    if has_start != has_end:
        raise ValueError("README project scan markers are unbalanced")
    if not has_start:
        return readme_text.rstrip() + "\n\n" + section + "\n"
    before = readme_text.split(START_MARKER, 1)[0].rstrip()
    after = readme_text.split(END_MARKER, 1)[1].lstrip()
    return before + "\n\n" + section + "\n\n" + after


def build_update_plan(root: Path = ROOT, now: str | None = None) -> ReadmeUpdatePlan:
    readme_path = root / "README.md"
    if not readme_path.exists():
        raise FileNotFoundError(f"README.md not found at {readme_path}")

    original_readme = readme_path.read_text(encoding="utf-8")
    previous_manifest = load_manifest(root)
    previous_files = previous_manifest.get("files", {})
    current_files = build_file_map(root)
    changes = diff_file_maps(previous_files, current_files)
    generated_at = now or utc_now()
    if previous_manifest and not changes.has_changes:
        generated_at = str(previous_manifest.get("generated_at") or generated_at)

    manifest = {
        "schema_version": 1,
        "generated_at": generated_at,
        "files": current_files,
    }
    manifest_text = json.dumps(manifest, indent=2, sort_keys=True) + "\n"

    section = render_project_scan_section(
        generated_at=generated_at,
        files_scanned=len(current_files),
        agents=list_agents(root),
        workflows=list_workflows(root),
        changes=changes,
    )
    has_start = START_MARKER in original_readme
    has_end = END_MARKER in original_readme
    if has_start != has_end:
        raise ValueError("README project scan markers are unbalanced")
    if previous_manifest and not changes.has_changes and has_start:
        new_readme = original_readme
    else:
        new_readme = update_readme_section(original_readme, section)
    original_manifest_text = (root / MANIFEST_NAME).read_text(encoding="utf-8") if (root / MANIFEST_NAME).exists() else ""

    return ReadmeUpdatePlan(
        readme_text=new_readme,
        manifest_text=manifest_text,
        readme_changed=new_readme != original_readme,
        manifest_changed=manifest_text != original_manifest_text,
        changes=changes,
    )


def apply_update_plan(plan: ReadmeUpdatePlan, root: Path = ROOT) -> None:
    if plan.readme_changed:
        (root / "README.md").write_text(plan.readme_text, encoding="utf-8")
    if plan.manifest_changed:
        (root / MANIFEST_NAME).write_text(plan.manifest_text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Update README.md with a generated project scan section.")
    parser.add_argument("--check", action="store_true", help="Exit non-zero if README.md or manifest would change.")
    args = parser.parse_args()

    plan = build_update_plan(ROOT)
    if args.check:
        if plan.has_writes:
            print("README project scan is stale.")
            return 1
        print("README project scan is up to date.")
        return 0

    apply_update_plan(plan, ROOT)
    if plan.has_writes:
        print("README project scan updated.")
        print(f"Added: {len(plan.changes.added)}, changed: {len(plan.changes.changed)}, deleted: {len(plan.changes.deleted)}")
    else:
        print("README project scan already up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
