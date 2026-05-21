from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import argparse
import json
import re
import shutil
from core.agent_loader import load_agent_config

def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_]+", "_", value.strip().lower()).strip("_")
    if not slug:
        raise ValueError("Agent name is required")
    return slug

def create_agent(name: str, role: str, force: bool = False, root: Path = ROOT) -> Path:
    agent_name = slugify(name)
    source = root / "agents" / "_template"
    target = root / "agents" / agent_name
    if target.exists():
        if not force:
            raise FileExistsError(f"Agent exists: {target}")
        shutil.rmtree(target)
    shutil.copytree(source, target)
    config_path = target / "agent.yaml"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["name"] = agent_name
    config["role"] = role
    config["description"] = f"Reusable high-ticket expert business agent for {role}."
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    prompt_path = target / "system_prompt.md"
    prompt_path.write_text(prompt_path.read_text(encoding="utf-8").replace("Template Agent", role).replace("[OUTPUT TITLE]", role), encoding="utf-8")
    load_agent_config(agent_name, root)
    return target

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--role", required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    print(create_agent(args.name, args.role, args.force))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
