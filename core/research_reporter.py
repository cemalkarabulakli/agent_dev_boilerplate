from __future__ import annotations

from pathlib import Path
from typing import Iterable


class ResearchReporter:
    def __init__(self, root: Path):
        self.root = root

    def write_markdown_report(self, relative_path: str, title: str, sections: dict[str, Iterable[str] | str]) -> Path:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [f"# {title}", ""]
        for heading, content in sections.items():
            lines.extend([f"## {heading}"])
            if isinstance(content, str):
                lines.append(content or "- None")
            else:
                values = list(content)
                lines.extend([f"- {item}" for item in values] or ["- None"])
            lines.append("")
        path.write_text("\n".join(lines), encoding="utf-8")
        return path

