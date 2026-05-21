from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts._common_generation import run_generation

if __name__ == "__main__":
    raise SystemExit(run_generation("avatar_pain_researcher"))
