"""scaffold.py — copies the template tree into a new project directory."""
from __future__ import annotations

import shutil
from pathlib import Path

# Directories and files copied from the template root into the new project.
SCAFFOLD_DIRS = [
    "agents/_template",
    "core",
    "scripts",
    "tools",
    "knowledge",
    "research",
    "checklists",
    "prompts",
]

SCAFFOLD_FILES = [
    "business_context.yaml",
    ".env.example",
    ".gitignore",
]

# Directories and patterns that are never copied.
_SKIP_NAMES = {
    "__pycache__", ".git", ".pytest_cache", ".claude",
    "outputs", "pipeline_context.json", "agent_forge",
    "dashboard", "todo_tools.md",
}


def _copy_tree(src: Path, dst: Path) -> int:
    """Recursively copy src → dst, skipping ignored names. Returns file count."""
    count = 0
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if item.name in _SKIP_NAMES or item.suffix == ".pyc":
            continue
        target = dst / item.name
        if item.is_dir():
            count += _copy_tree(item, target)
        else:
            shutil.copy2(item, target)
            count += 1
    return count


def scaffold_project(target: Path, template_root: Path) -> dict[str, int]:
    """
    Copy the template structure into `target`.

    Returns a summary dict: {"dirs": N, "files": N}
    """
    target.mkdir(parents=True, exist_ok=True)
    dirs_created = 0
    files_copied = 0

    for rel in SCAFFOLD_DIRS:
        src = template_root / rel
        if not src.exists():
            continue
        dst = target / rel
        files_copied += _copy_tree(src, dst)
        dirs_created += 1

    for rel in SCAFFOLD_FILES:
        src = template_root / rel
        if not src.exists():
            continue
        dst = target / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        files_copied += 1

    # Create empty runtime dirs so the project works out of the box.
    for d in ["outputs", "research/sources", "research/index", "research/insights",
              "research/processed"]:
        (target / d).mkdir(parents=True, exist_ok=True)

    # Empty pipeline context.
    (target / "pipeline_context.json").write_text("{}\n", encoding="utf-8")

    return {"dirs": dirs_created, "files": files_copied}
