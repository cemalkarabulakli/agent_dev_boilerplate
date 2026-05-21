from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.agent_loader import agent_dir, list_agents, load_agent_config  # noqa: E402
from core.knowledge_loader import KnowledgeBase  # noqa: E402
from core.schema import utc_now  # noqa: E402


def update_agent_index(agent_name: str, root: Path = ROOT) -> Path:
    config = load_agent_config(agent_name, root)
    kb = KnowledgeBase(agent_dir(agent_name, root), config.knowledge.sources_file)
    sources = kb.load_sources()
    documents = kb.load_processed_documents()
    index = {
        "generated_at": utc_now(),
        "agent": agent_name,
        "sources": [source.id for source in sources],
        "documents": [
            {
                "path": str(document.path.relative_to(root)),
                "source_id": document.source_id,
                "chars": len(document.text),
            }
            for document in documents
        ],
        "note": "This index records local files only. It does not invent or enrich knowledge.",
    }
    output = agent_dir(agent_name, root) / "knowledge" / "processed" / "index.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(index, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild local knowledge indexes.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--agent", help="Agent name under agents/.")
    group.add_argument("--all", action="store_true", help="Update all non-template agents.")
    args = parser.parse_args()

    names = list_agents(ROOT) if args.all else [args.agent]
    for name in names:
        print(f"{name}: {update_agent_index(name)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
