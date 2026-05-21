from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.business_context_schema import BusinessContext
from core.schema import load_yaml

def main() -> int:
    errors = []
    for path in list(ROOT.rglob("*.yaml")) + list(ROOT.rglob("*.yml")):
        if ".git" in path.parts or ".venv" in path.parts:
            continue
        try:
            load_yaml(path)
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
    try:
        BusinessContext.load(ROOT / "business_context.yaml")
    except Exception as exc:
        errors.append(f"business_context.yaml: {exc}")
    if errors:
        print("YAML validation failed:")
        print("\n".join(errors))
        return 1
    print("YAML validation passed.")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
