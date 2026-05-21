from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.source_registry import SourceRegistry  # noqa: E402


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_]+", "_", value.strip().lower()).strip("_")
    if not slug:
        raise ValueError("source id is required")
    return slug


def class_name(source_id: str) -> str:
    return "".join(part.title() for part in source_id.split("_")) + "Adapter"

def provider_class_name(source_id: str) -> str:
    return "".join(part.title() for part in source_id.split("_")) + "SourceProvider"


def add_source(source_id: str, name: str, source_type: str, root: Path = ROOT) -> Path:
    source_id = slugify(source_id)
    base = root / "research" / "sources" / source_id
    (base / "raw").mkdir(parents=True, exist_ok=True)
    (base / "processed").mkdir(parents=True, exist_ok=True)
    (base / "reports").mkdir(parents=True, exist_ok=True)
    for child in ["raw", "processed", "reports"]:
        (base / child / ".gitkeep").touch()
    config = {
        "id": source_id,
        "name": name,
        "enabled": True,
        "mode": "mock",
        "queries": ["high ticket business pain"],
        "collection": {"max_results_per_query": 20, "save_raw": True, "save_processed": True, "include_references": True, "include_timestamps": True},
        "processing": {"extract": ["pain_points", "objections", "desired_outcomes", "repeated_phrases", "competitor_mentions", "tool_mentions", "offer_patterns", "content_angles", "ad_angles"]},
        "scoring": {"min_confidence_for_candidate": 0.5, "min_confidence_for_validated": 0.75, "require_cross_source_validation": True},
        "compliance": {"respect_robots_txt": True, "use_official_api_when_available": True, "store_personal_data": False, "notes": "Document source-specific compliance requirements."},
    }
    (base / "source_config.yaml").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    adapter_name = f"{source_id}_source_provider"
    adapter_path = root / "tools" / "adapters" / "research_sources" / f"{adapter_name}.py"
    adapter_path.write_text(
        "from tools.adapters.research_sources.base_source_adapter import BaseSourceAdapter\n\n\n"
        f"class {class_name(source_id)}(BaseSourceAdapter):\n"
        f"    source_id = \"{source_id}\"\n"
        f"    source_type = \"{source_type}\"\n"
        "    signal_kind = \"custom_signal\"\n",
        encoding="utf-8",
    )
    ts_dir = root / "tools" / "web" / "sources"
    ts_dir.mkdir(parents=True, exist_ok=True)
    (ts_dir / f"{adapter_name}.ts").write_text(
        "import { BaseMockSourceProvider } from \"./custom_source_provider\";\n\n"
        f"export class {provider_class_name(source_id)} extends BaseMockSourceProvider {{\n"
        "  constructor() {\n"
        f"    super(\"{source_id}\", \"{source_type}\", \"en\", \"custom_signal\");\n"
        "  }\n"
        "}\n",
        encoding="utf-8",
    )
    registry = SourceRegistry(root)
    registry.register(
        source_id,
        {
            "name": name,
            "type": source_type,
            "status": "candidate",
            "adapter": adapter_name,
            "enabled": True,
            "requires_api_key": "optional",
            "requires_scraping": False,
            "compliance_note": "Use approved access and respect source terms.",
            "raw_dir": f"research/sources/{source_id}/raw",
            "processed_dir": f"research/sources/{source_id}/processed",
            "reports_dir": f"research/sources/{source_id}/reports",
            "best_for": ["custom research signals"],
        },
    )
    checklist = root / "checklists" / f"{source_id}_research_source_checklist.yaml"
    checklist.write_text(
        json.dumps(
            {
                "items": [
                    {"id": f"{source_id}_registered", "category": "Research Source", "description": f"{name} source is registered", "severity": "info", "check": "documented"}
                ]
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return base


def main() -> int:
    parser = argparse.ArgumentParser(description="Add a new modular research source.")
    parser.add_argument("--id", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--type", required=True)
    args = parser.parse_args()
    print(add_source(args.id, args.name, args.type))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
