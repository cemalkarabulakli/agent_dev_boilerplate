import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True, check=True)

def test_generation_scripts_run_without_api_keys() -> None:
    result = run_script("scripts/generate_offer_audit.py", "--agent", "offer_architect", "--context", "business_context.yaml", "--no-memory")
    assert "offer_architect_latest.md" in result.stdout

def test_github_workflows_exist() -> None:
    assert (ROOT / ".github" / "workflows" / "ci.yml").exists()
    assert (ROOT / ".github" / "workflows" / "agent-quality-check.yml").exists()
    assert (ROOT / ".github" / "workflows" / "scheduled-optimization.yml").exists()
    assert (ROOT / ".github" / "workflows" / "weekly-research.yml").exists()
    assert (ROOT / ".github" / "workflows" / "source-integrity-check.yml").exists()
