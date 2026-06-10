from pathlib import Path
from core.business_context_schema import BusinessContext
from core.schema import load_yaml

ROOT = Path(__file__).resolve().parents[1]

def test_all_yaml_files_validate() -> None:
    for path in list(ROOT.rglob("*.yaml")) + list(ROOT.rglob("*.yml")):
        if ".git" not in path.parts and ".github" not in path.parts:
            assert load_yaml(path) is not None

def test_business_context_validates() -> None:
    context = BusinessContext.load(ROOT / "business_context.yaml")
    assert "market" in context.data
    assert "offer" in context.data
