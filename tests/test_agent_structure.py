from pathlib import Path
from core.agent_loader import list_agents, load_agent_config
from scripts.create_agent import create_agent

ROOT = Path(__file__).resolve().parents[1]

def test_agent_folders_and_required_files_exist() -> None:
    agents = list_agents(ROOT)
    assert "offer_architect" in agents
    required = ["agent.yaml", "system_prompt.md", "checklist.yaml", "knowledge/README.md", "memory/raw_history.jsonl", "memory/session_notes.md", "memory/long_term_memory.json", "memory/compacted_context.md", "outputs/README.md", "evals/eval_cases.yaml"]
    for agent in agents:
        for rel in required:
            assert (ROOT / "agents" / agent / rel).exists()

def test_agent_yaml_validates() -> None:
    config = load_agent_config("offer_architect", ROOT)
    assert config.name == "offer_architect"
    assert config.model.provider == "mock"

def test_create_agent_creates_valid_structure(tmp_path: Path) -> None:
    import shutil
    shutil.copytree(ROOT / "agents" / "_template", tmp_path / "agents" / "_template")
    created = create_agent("sales_page_reviewer", "Sales Page Reviewer", root=tmp_path)
    assert (created / "agent.yaml").exists()
    assert load_agent_config("sales_page_reviewer", tmp_path).role == "Sales Page Reviewer"
