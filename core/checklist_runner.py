from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from core.agent_loader import agent_dir, list_agents, load_agent_config, repo_root
from core.business_context_schema import BusinessContext
from core.schema import ChecklistItem, load_yaml

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

def write_report(report: ChecklistReport, reports_dir: Path) -> Path:
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = reports_dir / f"{report.agent}_checklist_report.md"
    lines = [f"# Checklist Report: {report.agent}", "", f"Status: {'PASS' if report.passed else 'FAIL'}", ""]
    for result in report.results:
        lines += [f"## {'PASS' if result.passed else 'FAIL'} - {result.id}", f"- Category: {result.category}", f"- Severity: {result.severity}", f"- Message: {result.message}", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path

def _run_item(item: ChecklistItem, agent_name: str, root: Path) -> CheckResult:
    checks = {"agent_structure": _agent_structure, "prompt_quality": _prompt_quality, "github_ready": _github_ready, "mock_mode": _mock_mode, "ethical_guardrails": _ethical_guardrails, "context_compaction": _context_compaction, "business_context_schema": _business_context_schema}
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
