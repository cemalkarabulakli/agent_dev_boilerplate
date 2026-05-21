from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import argparse
from core.agent_loader import agent_dir, list_agents, load_agent_config
from core.context_compactor import compact_context, write_validation_report
from core.memory_manager import MemoryManager

def compact(agent: str) -> bool:
    config = load_agent_config(agent, ROOT)
    manager = MemoryManager(agent_dir(agent, ROOT))
    result = compact_context(config, manager.read_raw_history(), manager.load_session_notes(), manager.load_long_term_memory())
    manager.write_compacted_context(result.markdown)
    write_validation_report(result, ROOT / "outputs" / "quality_reports" / f"{agent}_compaction_validation.md")
    print(f"{agent}: {'PASS' if result.passed else 'FAIL'}")
    return result.passed

def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--agent")
    group.add_argument("--all", action="store_true")
    args = parser.parse_args()
    agents = list_agents(ROOT) if args.all else [args.agent]
    return 0 if all(compact(agent) for agent in agents) else 1

if __name__ == "__main__":
    raise SystemExit(main())
