from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_]+", "_", value.strip().lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    if not slug:
        raise ValueError("Agent name must contain at least one letter or number")
    return slug


def create_agent(name: str, role: str, force: bool = False, root: Path = ROOT) -> Path:
    agent_name = slugify(name)
    template_dir = root / "agents" / "_template"
    target_dir = root / "agents" / agent_name
    if not template_dir.exists():
        raise FileNotFoundError(f"Template agent is missing: {template_dir}")
    if target_dir.exists():
        if not force:
            raise FileExistsError(f"Agent already exists: {target_dir}. Use --force to replace it.")
        shutil.rmtree(target_dir)
    shutil.copytree(template_dir, target_dir)

    replacements = {
        "__AGENT_NAME__": agent_name,
        "__AGENT_ROLE__": role,
        "__AGENT_DESCRIPTION__": f"Local-first {role} agent created from the reusable template.",
    }
    for path in target_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".yaml", ".md", ".json", ".jsonl", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")

    agent_yaml = target_dir / "agent.yaml"
    text = agent_yaml.read_text(encoding="utf-8")
    text = re.sub(r"^name: .*$", f"name: {agent_name}", text, flags=re.MULTILINE)
    text = re.sub(r'^role: ".*"$', f'role: "{role}"', text, flags=re.MULTILINE)
    text = re.sub(
        r'^description: ".*"$',
        f'description: "Local-first {role} agent created from the reusable template."',
        text,
        flags=re.MULTILINE,
    )
    agent_yaml.write_text(text, encoding="utf-8")
    return target_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new local-first agent from agents/_template.")
    parser.add_argument("--name", required=True, help="Agent folder name, for example meta_ads_expert.")
    parser.add_argument("--role", required=True, help="Human role name, for example Meta Ads Expert.")
    parser.add_argument("--force", action="store_true", help="Replace the target agent directory if it exists.")
    args = parser.parse_args()

    target = create_agent(args.name, args.role, args.force)
    print(f"Created agent at {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
