from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from core.schema import AgentConfig, load_yaml

REPO_ROOT = Path(__file__).resolve().parents[1]

@dataclass(frozen=True)
class LoadedAgent:
    root: Path
    agent_dir: Path
    config: AgentConfig
    system_prompt: str

def repo_root() -> Path:
    return REPO_ROOT

def agent_dir(agent_name: str, root: Path | None = None) -> Path:
    return (root or REPO_ROOT) / "agents" / agent_name

def list_agents(root: Path | None = None, include_template: bool = False) -> list[str]:
    base = (root or REPO_ROOT) / "agents"
    names = sorted(path.name for path in base.iterdir() if path.is_dir()) if base.exists() else []
    return names if include_template else [name for name in names if name != "_template"]

def load_agent_config(agent_name: str, root: Path | None = None) -> AgentConfig:
    return AgentConfig.from_dict(load_yaml(agent_dir(agent_name, root) / "agent.yaml"))

def load_system_prompt(agent_name: str, root: Path | None = None) -> str:
    return (agent_dir(agent_name, root) / "system_prompt.md").read_text(encoding="utf-8")

def load_agent(agent_name: str, root: Path | None = None) -> LoadedAgent:
    actual = root or REPO_ROOT
    return LoadedAgent(actual, agent_dir(agent_name, actual), load_agent_config(agent_name, actual), load_system_prompt(agent_name, actual))
