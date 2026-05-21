from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.cross_source_analyzer import CrossSourceAnalyzer  # noqa: E402


def main() -> int:
    path = CrossSourceAnalyzer(ROOT).write_report()
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
