from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import argparse
from core.agent_loader import load_agent
from core.business_context_schema import BusinessContext
from core.context_compactor import compact_context, write_validation_report
from core.guardrails import validate_input
from core.memory_manager import MemoryManager
from core.output_templates import render_mock_output

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", required=True)
    parser.add_argument("--message", required=True)
    args = parser.parse_args()
    loaded = load_agent(args.agent, ROOT)
    manager = MemoryManager(loaded.agent_dir)
    manager.append_raw_history("user", args.message)
    errors = validate_input(args.message, loaded.config)
    response = "Request blocked by guardrails: " + "; ".join(errors) if errors else render_mock_output(args.agent, BusinessContext.load(ROOT / "business_context.yaml"))
    manager.append_raw_history("agent", response, {"mode": "mock"})
    manager.save_candidate_memory("Review whether the latest user message contains durable business context.", "assumption", "agent", 0.4)
    output_path = loaded.agent_dir / "outputs" / "latest.md"
    output_path.write_text(response, encoding="utf-8")
    print(output_path)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
