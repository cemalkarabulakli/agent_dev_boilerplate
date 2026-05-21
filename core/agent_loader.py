"""Agent loading helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from core.schema import AgentConfig
from core.yaml_utils import load_yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class LoadedAgent:
    root: Path
    agent_dir: Path
    config: AgentConfig
    system_prompt: str


def repo_root() -> Path:
    return REPO_ROOT


def agents_root(root: Path | None = None) -> Path:
    return (root or repo_root()) / "agents"


def agent_dir(agent_name: str, root: Path | None = None) -> Path:
    return agents_root(root) / agent_name


def list_agents(root: Path | None = None, include_template: bool = False) -> list[str]:
    base = agents_root(root)
    if not base.exists():
        return []
    names = [path.name for path in base.iterdir() if path.is_dir()]
    if not include_template:
        names = [name for name in names if name != "_template"]
    return sorted(names)


def load_agent_config(agent_name: str, root: Path | None = None) -> AgentConfig:
    path = agent_dir(agent_name, root) / "agent.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Missing agent config: {path}")
    return AgentConfig.from_dict(load_yaml(path))


def load_system_prompt(agent_name: str, root: Path | None = None) -> str:
    path = agent_dir(agent_name, root) / "system_prompt.md"
    if not path.exists():
        raise FileNotFoundError(f"Missing system prompt: {path}")
    return path.read_text(encoding="utf-8")


def load_agent(agent_name: str, root: Path | None = None) -> LoadedAgent:
    actual_root = root or repo_root()
    return LoadedAgent(
        root=actual_root,
        agent_dir=agent_dir(agent_name, actual_root),
        config=load_agent_config(agent_name, actual_root),
        system_prompt=load_system_prompt(agent_name, actual_root),
    )
