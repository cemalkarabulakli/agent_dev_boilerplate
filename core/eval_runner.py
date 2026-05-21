"""Deterministic eval runner with an extension point for real model evals."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from core.agent_loader import agent_dir, load_agent_config, repo_root
from core.schema import EvalCase
from core.yaml_utils import load_yaml


@dataclass
class EvalResult:
    id: str
    passed: bool
    message: str
    response: str


@dataclass
class EvalReport:
    agent: str
    results: list[EvalResult]

    @property
    def passed(self) -> bool:
        return all(result.passed for result in self.results)


def mock_response(agent_name: str, message: str, root: Path | None = None) -> str:
    config = load_agent_config(agent_name, root or repo_root())
    return (
        f"Local mock response for {config.role}. "
        "Recommendation: answer conservatively, separate facts from assumptions, "
        "and cite configured source IDs when using knowledge. "
        f"Input reviewed: {message}"
    )


def run_evals(agent_name: str, root: Path | None = None) -> EvalReport:
    actual_root = root or repo_root()
    path = agent_dir(agent_name, actual_root) / "evals" / "eval_cases.yaml"
    data = load_yaml(path)
    cases = [EvalCase.from_dict(item) for item in data.get("cases", [])]
    results: list[EvalResult] = []
    for case in cases:
        response = mock_response(agent_name, case.input, actual_root)
        missing = [term for term in case.required_terms if term.lower() not in response.lower()]
        forbidden = [term for term in case.forbidden_terms if term.lower() in response.lower()]
        passed = not missing and not forbidden
        details: list[str] = []
        if missing:
            details.append("Missing required terms: " + ", ".join(missing))
        if forbidden:
            details.append("Forbidden terms present: " + ", ".join(forbidden))
        results.append(
            EvalResult(
                id=case.id,
                passed=passed,
                message="PASS" if passed else "; ".join(details),
                response=response,
            )
        )
    return EvalReport(agent=agent_name, results=results)


def write_eval_report(report: EvalReport, reports_dir: Path) -> Path:
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = reports_dir / f"{report.agent}_eval_report.md"
    lines = [
        f"# Eval Report: {report.agent}",
        "",
        f"Status: {'PASS' if report.passed else 'FAIL'}",
        "",
    ]
    for result in report.results:
        lines.append(f"## {'PASS' if result.passed else 'FAIL'} - {result.id}")
        lines.append(f"- Message: {result.message}")
        lines.append(f"- Response: {result.response}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
