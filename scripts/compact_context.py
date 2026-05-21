from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.agent_loader import agent_dir, list_agents, load_agent_config  # noqa: E402
from core.context_compactor import compact_context, write_validation_report  # noqa: E402
from core.memory_manager import MemoryManager  # noqa: E402


def compact_agent(agent_name: str, root: Path = ROOT) -> bool:
    config = load_agent_config(agent_name, root)
    manager = MemoryManager(agent_dir(agent_name, root))
    result = compact_context(
        config=config,
        history=manager.read_raw_history(),
        session_notes=manager.load_session_notes(),
        long_term_memory=manager.load_long_term_memory(),
    )
    manager.write_compacted_context(result.markdown)
    write_validation_report(result, root / "reports" / f"{agent_name}_compaction_validation.md")
    print(f"{agent_name}: {'PASS' if result.validation.passed else 'FAIL'}")
    return result.validation.passed


def main() -> int:
    parser = argparse.ArgumentParser(description="Compact agent context.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--agent", help="Agent name under agents/.")
    group.add_argument("--all", action="store_true", help="Compact all non-template agents.")
    args = parser.parse_args()

    names = list_agents(ROOT) if args.all else [args.agent]
    passed = all(compact_agent(name) for name in names)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
