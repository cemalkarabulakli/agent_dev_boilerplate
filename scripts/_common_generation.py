from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import argparse
from core.agent_loader import load_agent
from core.business_context_schema import BusinessContext
from core.memory_manager import MemoryManager
from core.output_templates import render_mock_output, save_output

def run_generation(default_agent: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", default=default_agent)
    parser.add_argument("--context", default="business_context.yaml")
    parser.add_argument("--no-memory", action="store_true", help="Skip memory writes for deterministic tests.")
    args = parser.parse_args()
    loaded = load_agent(args.agent, ROOT)
    context = BusinessContext.load(ROOT / args.context)
    markdown = render_mock_output(args.agent, context)
    path = save_output(ROOT, args.agent, markdown)
    if not args.no_memory:
        manager = MemoryManager(loaded.agent_dir)
        manager.append_raw_history("agent", f"Generated {path.name}", {"script": Path(sys.argv[0]).name})
        manager.save_candidate_memory("Generated mock output from business_context.yaml", "assumption", "agent", 0.4)
    print(path)
    return 0
