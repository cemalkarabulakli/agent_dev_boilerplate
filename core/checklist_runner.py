from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from core.agent_loader import agent_dir, list_agents, load_agent_config, repo_root
from core.business_context_schema import BusinessContext
from core.reference_manager import ReferenceManager
from core.schema import ChecklistItem, load_yaml
from core.source_registry import SourceRegistry

PROMPT_SECTIONS = ["# Role", "# Goal", "# Operating Principles", "# High-Ticket Business Logic", "# Memory Rules", "# Context Compaction Rules", "# Output Rules", "# Ethical Marketing Rules", "# Self-Review Checklist"]

@dataclass(frozen=True)
class CheckResult:
    id: str
    category: str
    description: str
    severity: str
    passed: bool
    message: str

@dataclass(frozen=True)
class ChecklistReport:
    agent: str
    results: list[CheckResult]
    @property
    def passed(self) -> bool:
        return not any(result.severity == "critical" and not result.passed for result in self.results)

def run_for_agent(agent_name: str, root: Path | None = None) -> ChecklistReport:
    actual = root or repo_root()
    items = []
    for path in sorted((actual / "checklists").glob("*.yaml")):
        items += [ChecklistItem.from_dict(item) for item in load_yaml(path).get("items", [])]
    data = load_yaml(agent_dir(agent_name, actual) / "checklist.yaml")
    items += [ChecklistItem.from_dict(item) for item in data.get("items", [])]
    return ChecklistReport(agent_name, [_run_item(item, agent_name, actual) for item in items])

def run_for_all(root: Path | None = None) -> list[ChecklistReport]:
    actual = root or repo_root()
    return [run_for_agent(agent, actual) for agent in list_agents(actual)]

def run_named_checklist(checklist_name: str, root: Path | None = None) -> ChecklistReport:
    actual = root or repo_root()
    path = actual / "checklists" / f"{checklist_name}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Unknown checklist: {checklist_name}")
    data = load_yaml(path)
    items = [ChecklistItem.from_dict(item) for item in data.get("items", [])]
    agent = checklist_name
    return ChecklistReport(agent, [_run_item(item, agent, actual) for item in items])

def write_report(report: ChecklistReport, reports_dir: Path) -> Path:
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = reports_dir / f"{report.agent}_checklist_report.md"
    lines = [f"# Checklist Report: {report.agent}", "", f"Status: {'PASS' if report.passed else 'FAIL'}", ""]
    for result in report.results:
        lines += [f"## {'PASS' if result.passed else 'FAIL'} - {result.id}", f"- Category: {result.category}", f"- Severity: {result.severity}", f"- Message: {result.message}", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path

def _run_item(item: ChecklistItem, agent_name: str, root: Path) -> CheckResult:
    checks = {"agent_structure": _agent_structure, "prompt_quality": _prompt_quality, "github_ready": _github_ready, "mock_mode": _mock_mode, "ethical_guardrails": _ethical_guardrails, "context_compaction": _context_compaction, "business_context_schema": _business_context_schema, "research_source_structure": _research_source_structure, "reference_integrity": _reference_integrity, "cross_source_validation": _cross_source_validation, "web_tool_provider": _web_tool_provider, "competitor_monitoring": _competitor_monitoring}
    passed, message = checks.get(item.check, lambda *_: (True, "Documented checklist item."))(agent_name, root)
    return CheckResult(item.id, item.category, item.description, item.severity, passed, message)

def _agent_structure(agent_name: str, root: Path) -> tuple[bool, str]:
    base = agent_dir(agent_name, root)
    required = ["agent.yaml", "system_prompt.md", "checklist.yaml", "knowledge/README.md", "memory/raw_history.jsonl", "memory/session_notes.md", "memory/long_term_memory.json", "memory/compacted_context.md", "outputs/README.md", "evals/eval_cases.yaml"]
    missing = [item for item in required if not (base / item).exists()]
    return (not missing, "All required files exist." if not missing else "Missing: " + ", ".join(missing))

def _prompt_quality(agent_name: str, root: Path) -> tuple[bool, str]:
    prompt = (agent_dir(agent_name, root) / "system_prompt.md").read_text(encoding="utf-8")
    missing = [section for section in PROMPT_SECTIONS if section not in prompt]
    return (not missing, "Prompt complete." if not missing else "Missing: " + ", ".join(missing))

def _github_ready(agent_name: str, root: Path) -> tuple[bool, str]:
    del agent_name
    required = ["README.md", ".env.example", ".gitignore", "requirements.txt", ".github/workflows/ci.yml", ".github/workflows/agent-quality-check.yml", ".github/workflows/scheduled-optimization.yml"]
    missing = [item for item in required if not (root / item).exists()]
    return (not missing, "GitHub files exist." if not missing else "Missing: " + ", ".join(missing))

def _mock_mode(agent_name: str, root: Path) -> tuple[bool, str]:
    config = load_agent_config(agent_name, root)
    return (config.model.provider == "mock" and config.model.name == "local-mock", "Agent defaults to mock/local mode.")

def _ethical_guardrails(agent_name: str, root: Path) -> tuple[bool, str]:
    guardrails = set(load_agent_config(agent_name, root).guardrails.get("output", []))
    required = {"no_fake_claims", "no_fake_testimonials", "no_fake_scarcity", "no_unrealistic_income_promises", "separate_fact_assumption_recommendation"}
    missing = sorted(required - guardrails)
    return (not missing, "Ethical guardrails configured." if not missing else "Missing: " + ", ".join(missing))

def _context_compaction(agent_name: str, root: Path) -> tuple[bool, str]:
    del agent_name
    required = ["core/context_compactor.py", "scripts/compact_context.py", "prompts/compact_context_prompt.md"]
    missing = [item for item in required if not (root / item).exists()]
    return (not missing, "Context compaction exists." if not missing else "Missing: " + ", ".join(missing))

def _business_context_schema(agent_name: str, root: Path) -> tuple[bool, str]:
    del agent_name
    BusinessContext.load(root / "business_context.yaml")
    return True, "business_context.yaml schema is valid."

def evaluate_business_quality(context: BusinessContext) -> list[str]:
    errors = []
    if not context.has_value("market", "market_name"):
        errors.append("market is missing")
    avatar = str(context.get("customer", "specific_avatar", "")).lower()
    if not avatar or avatar in {"everyone", "people", "business owners", "experts"}:
        errors.append("target avatar is too broad or missing")
    if not context.has_value("customer", "target_customer"):
        errors.append("offer has no target customer")
    serialized = str(context.data).lower()
    if any(term in serialized for term in ["fake testimonial", "fake scarcity", "guaranteed income"]):
        errors.append("fake or unsupported claims are present")
    return errors

def _research_source_structure(agent_name: str, root: Path) -> tuple[bool, str]:
    del agent_name
    registry = SourceRegistry(root)
    errors: list[str] = []
    for source_id, entry in registry.sources().items():
        source_dir = root / "research" / "sources" / source_id
        for rel in ["source_config.yaml", "raw", "processed", "reports"]:
            if not (source_dir / rel).exists():
                errors.append(f"{source_id} missing {rel}")
        adapter_name = str(entry.get("provider") or entry["adapter"])
        adapter = root / "tools" / "adapters" / "research_sources" / f"{adapter_name}.py"
        provider = root / "tools" / "web" / "sources" / f"{adapter_name}.ts"
        if not adapter.exists() and not provider.exists():
            errors.append(f"{source_id} missing adapter/provider {entry['adapter']}")
        config = load_yaml(source_dir / "source_config.yaml")
        if config.get("mode") != "mock":
            errors.append(f"{source_id} must support mock mode by default")
        if not entry.get("compliance_note"):
            errors.append(f"{source_id} missing compliance note")
        if not config.get("collection", {}).get("include_references"):
            errors.append(f"{source_id} references not enabled")
    return (not errors, "Research source structure is valid." if not errors else "; ".join(errors))

def _reference_integrity(agent_name: str, root: Path) -> tuple[bool, str]:
    del agent_name
    manager = ReferenceManager(root)
    errors: list[str] = []
    for reference in manager.read_all():
        errors.extend(manager.validate_reference(reference))
    for path in (root / "research" / "sources").glob("*/processed/*_processed.json"):
        signals = load_yaml(path)
        for signal in signals:
            if not signal.get("reference_ids"):
                errors.append(f"{path} has processed signal without reference_ids")
    for path in (root / "research" / "sources").glob("*/reports/*_report.md"):
        text = path.read_text(encoding="utf-8")
        if "## References" not in text:
            errors.append(f"{path} missing references section")
    return (not errors, "Reference integrity checks passed." if not errors else "; ".join(errors))

def _cross_source_validation(agent_name: str, root: Path) -> tuple[bool, str]:
    del agent_name
    report = root / "research" / "processed" / "cross_source_reports" / "cross_source_report.md"
    if not report.exists():
        return True, "Cross-source report not generated yet; run analyze_cross_source_signals.py after collection."
    text = report.read_text(encoding="utf-8")
    required = ["## Weak Signals", "## Conflicting Signals", "## References", "Confidence:", "Source quality:", "Sources:"]
    missing = [item for item in required if item not in text]
    return (not missing, "Cross-source validation report contains required evidence fields." if not missing else "Missing: " + ", ".join(missing))

def _web_tool_provider(agent_name: str, root: Path) -> tuple[bool, str]:
    del agent_name
    required = [
        "tools/web/interfaces/web_search_tool.ts",
        "tools/web/interfaces/web_extractor_tool.ts",
        "tools/web/interfaces/browser_automation_tool.ts",
        "tools/web/interfaces/web_crawler_tool.ts",
        "tools/web/interfaces/source_collector_tool.ts",
        "tools/web/interfaces/trend_provider_tool.ts",
        "tools/web/registry/web_tool_registry.ts",
        "tools/web/registry/source_provider_registry.ts",
        "tools/web/search/mock_search_provider.ts",
        "tools/web/extraction/mock_extractor_provider.ts",
        "tools/web/browser/mock_browser_provider.ts",
        "tools/web/crawling/mock_crawler_provider.py",
    ]
    missing = [item for item in required if not (root / item).exists()]
    env_text = (root / ".env.example").read_text(encoding="utf-8")
    for key in ["TAVILY_API_KEY", "FIRECRAWL_API_KEY", "WEB_TOOLS_MODE"]:
        if key not in env_text:
            missing.append(f".env.example missing {key}")
    direct_import_terms = ["tavily", "firecrawl", "playwright", "scrapy"]
    for path in (root / "agents").glob("**/*"):
        if path.is_file() and path.suffix in {".md", ".yaml"}:
            text = path.read_text(encoding="utf-8").lower()
            if any(f"import {term}" in text or f"from {term}" in text for term in direct_import_terms):
                missing.append(f"agent imports provider directly: {path.relative_to(root)}")
    return (not missing, "Web tool interfaces and provider registries are valid." if not missing else "; ".join(missing))

def _competitor_monitoring(agent_name: str, root: Path) -> tuple[bool, str]:
    del agent_name
    registry = SourceRegistry(root)
    errors: list[str] = []
    if "competitors" not in registry.sources():
        errors.append("competitors source is not registered")
    required = [
        "research/sources/competitors/source_config.yaml",
        "research/sources/competitors/raw",
        "research/sources/competitors/processed",
        "research/sources/competitors/reports",
        "research/sources/competitors/screenshots",
        "core/competitor_monitor.py",
        "scripts/monitor_competitors.py",
        "outputs/competitor_monitoring",
    ]
    errors.extend(item for item in required if not (root / item).exists())
    return (not errors, "Competitor monitoring structure is valid." if not errors else "; ".join(errors))
