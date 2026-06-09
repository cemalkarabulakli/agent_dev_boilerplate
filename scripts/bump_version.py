"""
bump_version.py — Bump the package version and sync pyproject.toml.

Usage:
  python scripts/bump_version.py patch     # 0.1.0 -> 0.1.1
  python scripts/bump_version.py minor     # 0.1.0 -> 0.2.0
  python scripts/bump_version.py major     # 0.1.0 -> 1.0.0
  python scripts/bump_version.py 0.3.0     # set exact version
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "agent_forge" / "_version.py"
PYPROJECT = ROOT / "pyproject.toml"


def read_version() -> str:
    text = VERSION_FILE.read_text(encoding="utf-8")
    m = re.search(r'__version__\s*=\s*"([^"]+)"', text)
    if not m:
        raise ValueError("Could not find __version__ in _version.py")
    return m.group(1)


def bump(current: str, part: str) -> str:
    major, minor, patch = (int(x) for x in current.split("."))
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    if part == "patch":
        return f"{major}.{minor}.{patch + 1}"
    # Treat as explicit version string.
    if re.match(r"^\d+\.\d+\.\d+$", part):
        return part
    raise ValueError(f"Unknown bump part: {part}. Use major, minor, patch, or x.y.z")


def write_version(new: str) -> None:
    VERSION_FILE.write_text(f'__version__ = "{new}"\n', encoding="utf-8")

    text = PYPROJECT.read_text(encoding="utf-8")
    text = re.sub(r'(^version\s*=\s*")[^"]+(")', rf'\g<1>{new}\2', text, flags=re.MULTILINE)
    PYPROJECT.write_text(text, encoding="utf-8")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    part = sys.argv[1]
    current = read_version()
    new = bump(current, part)

    write_version(new)
    print(f"{current} -> {new}")
    print()
    print("Next steps:")
    print(f"  git add agent_forge/_version.py pyproject.toml")
    print(f"  git commit -m 'release: v{new}'")
    print(f"  git tag v{new}")
    print(f"  git push origin main --tags")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
