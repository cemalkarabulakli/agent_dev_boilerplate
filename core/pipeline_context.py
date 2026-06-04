from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from core.schema import utc_now


class PipelineContext:
    """Thin structured pass-through between agents.

    Stores only declared key fields per agent — not full markdown outputs.
    Agents declare what they read and write via PIPELINE_SCHEMA in output_templates.py.
    """

    def __init__(self, path: Path):
        self.path = path
        self.data: dict[str, Any] = {}
        if path.exists():
            self.data = json.loads(path.read_text(encoding="utf-8"))

    def read_deps(self, reads: dict[str, list[str]]) -> tuple[dict[str, Any], list[str]]:
        """Extract only the declared upstream keys.

        Returns:
            deps: flat dict keyed as "agent_name.Section Name" → value
            gaps: list of missing upstream keys (for surface in rendered output)
        """
        deps: dict[str, Any] = {}
        gaps: list[str] = []
        for agent, keys in reads.items():
            agent_data = self.data.get(agent, {})
            if not agent_data:
                gaps.append(f"{agent} (not completed)")
                continue
            for key in keys:
                val = agent_data.get(key)
                if val not in (None, "", [], {}):
                    deps[f"{agent}.{key}"] = val
                else:
                    gaps.append(f"{agent}.{key}")
        return deps, gaps

    def write_output(self, agent_name: str, output: dict[str, Any], gaps: list[str]) -> None:
        """Write structured summary for agent_name. Overwrites prior entry."""
        self.data[agent_name] = {
            "_meta": {"completed_at": utc_now(), "upstream_gaps": gaps},
            **output,
        }
        self.path.write_text(
            json.dumps(self.data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
