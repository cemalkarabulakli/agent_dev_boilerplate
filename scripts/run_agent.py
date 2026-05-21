from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.agent_loader import load_agent  # noqa: E402
from core.checklist_runner import run_for_agent, write_report  # noqa: E402
from core.context_compactor import compact_context, write_validation_report  # noqa: E402
from core.eval_runner import mock_response  # noqa: E402
from core.guardrails import output_safety_notes, validate_input  # noqa: E402
from core.knowledge_loader import KnowledgeBase  # noqa: E402
from core.memory_manager import MemoryManager  # noqa: E402


def approximate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def run_agent(agent_name: str, message: str, root: Path = ROOT) -> str:
    loaded = load_agent(agent_name, root)
    errors = validate_input(message, loaded.config)
    manager = MemoryManager(loaded.agent_dir)
    manager.ensure_files()

    if errors:
        response = "Request refused by input guardrails: " + "; ".join(errors)
        manager.append_raw_history("user", message)
        manager.append_raw_history("assistant", response, {"guardrail_refusal": True})
        return response

    provider_mode = os.getenv("AGENT_PROVIDER_MODE", "mock").strip().lower()
    if provider_mode != "mock":
        raise RuntimeError("Real provider mode is not implemented in v1. Keep AGENT_PROVIDER_MODE=mock.")

    kb = KnowledgeBase(loaded.agent_dir, loaded.config.knowledge.sources_file)
    knowledge_note = kb.factuality_note()
    compacted_context = manager.load_compacted_context()
    session_notes = manager.load_session_notes()
    safety = " ".join(output_safety_notes(loaded.config))

    response = mock_response(agent_name, message, root)
    response = f"{response}\n\nKnowledge policy: {knowledge_note}\nSafety policy: {safety}"

    manager.append_raw_history("user", message)
    manager.append_raw_history(
        "assistant",
        response,
        {
            "provider_mode": "mock",
            "compacted_context_chars": len(compacted_context),
            "session_notes_chars": len(session_notes),
        },
    )

    if loaded.config.memory.allow_learning:
        manager.save_candidate_memory(
            text=f"Review whether this user message contains durable context: {message}",
            source="raw_history",
            memory_type="review_candidate",
            confidence=0.4,
        )

    history_text = "\n".join(item.get("content", "") for item in manager.read_raw_history())
    if approximate_tokens(history_text) >= loaded.config.context.compact_when_tokens_exceed:
        result = compact_context(
            config=loaded.config,
            history=manager.read_raw_history(),
            session_notes=manager.load_session_notes(),
            long_term_memory=manager.load_long_term_memory(),
        )
        manager.write_compacted_context(result.markdown)
        write_validation_report(result, root / "reports" / f"{agent_name}_compaction_validation.md")

    checklist_report = run_for_agent(agent_name, root)
    write_report(checklist_report, root / "reports")
    return response


def main() -> int:
    parser = argparse.ArgumentParser(description="Run an agent using the local deterministic runner.")
    parser.add_argument("--agent", required=True, help="Agent name under agents/.")
    parser.add_argument("--message", required=True, help="User message to process.")
    args = parser.parse_args()
    print(run_agent(args.agent, args.message))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
