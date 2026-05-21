from __future__ import annotations

from pathlib import Path

from core.agent_loader import load_agent_config
from scripts.create_agent import create_agent
from scripts.validate_agent_structure import validate_agent


ROOT = Path(__file__).resolve().parents[1]


def test_agent_yaml_validates_against_schema() -> None:
    config = load_agent_config("meta_ads_expert", ROOT)
    assert config.name == "meta_ads_expert"
    assert config.role == "Meta Ads Expert"
    assert config.context.keep_last_n_turns == 5
    assert "read_knowledge" in config.tools.allowed


def test_create_agent_creates_valid_structure(tmp_path: Path) -> None:
    root = tmp_path
    source = ROOT / "agents" / "_template"
    target_template = root / "agents" / "_template"
    target_template.parent.mkdir(parents=True)
    import shutil

    shutil.copytree(source, target_template)
    created = create_agent("Product Manager", "Product Manager", root=root)
    assert created.name == "product_manager"
    errors = validate_agent("product_manager", root)
    assert errors == []


def test_github_workflow_files_exist() -> None:
    assert (ROOT / ".github" / "workflows" / "ci.yml").exists()
    assert (ROOT / ".github" / "workflows" / "agent-quality-check.yml").exists()
    assert (ROOT / ".github" / "workflows" / "scheduled-optimization.yml").exists()
