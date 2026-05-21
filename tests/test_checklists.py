from __future__ import annotations

import shutil
from pathlib import Path

from core.checklist_runner import run_for_agent


ROOT = Path(__file__).resolve().parents[1]


def test_checklist_fails_when_required_files_missing(tmp_path: Path) -> None:
    shutil.copytree(ROOT / "agents", tmp_path / "agents")
    shutil.copytree(ROOT / "checklists", tmp_path / "checklists")
    shutil.copytree(ROOT / "prompts", tmp_path / "prompts")
    shutil.copytree(ROOT / "core", tmp_path / "core")
    (tmp_path / ".github" / "workflows").mkdir(parents=True)
    shutil.copytree(ROOT / ".github" / "workflows", tmp_path / ".github" / "workflows", dirs_exist_ok=True)
    shutil.copy2(ROOT / ".env.example", tmp_path / ".env.example")
    shutil.copy2(ROOT / ".gitignore", tmp_path / ".gitignore")

    (tmp_path / "agents" / "meta_ads_expert" / "system_prompt.md").unlink()
    report = run_for_agent("meta_ads_expert", tmp_path)
    assert not report.passed
    assert any(not result.passed and result.id == "agent_structure" for result in report.results)
