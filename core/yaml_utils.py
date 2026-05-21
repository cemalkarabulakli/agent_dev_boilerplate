"""Small YAML subset loader used to keep the runtime dependency-free.

The repository intentionally writes simple block-style YAML. This loader is not
a general YAML implementation; it supports the subset used by agent configs,
checklists, sources, and eval files.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


class SimpleYamlError(ValueError):
    """Raised when a file uses YAML outside the supported local subset."""


def load_yaml(path: Path) -> Any:
    return loads_yaml(path.read_text(encoding="utf-8"))


def loads_yaml(text: str) -> Any:
    stripped = text.strip()
    if not stripped:
        return {}
    if stripped[0] in "[{":
        return json.loads(stripped)

    lines = _prepare_lines(text)
    if not lines:
        return {}
    value, index = _parse_block(lines, 0, lines[0][0])
    if index != len(lines):
        raise SimpleYamlError(f"Could not parse line: {lines[index][1]}")
    return value


def _prepare_lines(text: str) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if indent % 2 != 0:
            raise SimpleYamlError(f"Indentation must use multiples of two spaces: {raw!r}")
        result.append((indent, raw.strip()))
    return result


def _parse_block(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[Any, int]:
    if index >= len(lines):
        return {}, index
    if lines[index][0] < indent:
        return {}, index
    if lines[index][1].startswith("- "):
        return _parse_list(lines, index, lines[index][0])
    return _parse_mapping(lines, index, lines[index][0])


def _parse_list(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[list[Any], int]:
    items: list[Any] = []
    while index < len(lines):
        current_indent, text = lines[index]
        if current_indent < indent:
            break
        if current_indent != indent or not text.startswith("- "):
            break

        item_text = text[2:].strip()
        index += 1

        if not item_text:
            if index < len(lines) and lines[index][0] > current_indent:
                item, index = _parse_block(lines, index, lines[index][0])
            else:
                item = None
            items.append(item)
            continue

        if _looks_like_key_value(item_text):
            key, raw_value = _split_key_value(item_text)
            item_dict: dict[str, Any] = {}
            if raw_value == "":
                if index < len(lines) and lines[index][0] > current_indent:
                    item_dict[key], index = _parse_block(lines, index, lines[index][0])
                else:
                    item_dict[key] = {}
            else:
                item_dict[key] = _parse_scalar(raw_value)

            if index < len(lines) and lines[index][0] > current_indent:
                child, index = _parse_block(lines, index, lines[index][0])
                if isinstance(child, dict):
                    item_dict.update(child)
                else:
                    item_dict["_items"] = child
            items.append(item_dict)
        else:
            items.append(_parse_scalar(item_text))

    return items, index


def _parse_mapping(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[dict[str, Any], int]:
    mapping: dict[str, Any] = {}
    while index < len(lines):
        current_indent, text = lines[index]
        if current_indent < indent:
            break
        if current_indent != indent:
            break
        if text.startswith("- "):
            break

        key, raw_value = _split_key_value(text)
        index += 1
        if raw_value == "":
            if index < len(lines) and lines[index][0] > current_indent:
                mapping[key], index = _parse_block(lines, index, lines[index][0])
            else:
                mapping[key] = {}
        else:
            mapping[key] = _parse_scalar(raw_value)

    return mapping, index


def _looks_like_key_value(text: str) -> bool:
    if ":" not in text:
        return False
    return bool(re.match(r"^[A-Za-z0-9_\-]+:", text))


def _split_key_value(text: str) -> tuple[str, str]:
    if ":" not in text:
        raise SimpleYamlError(f"Expected key: value line, got: {text}")
    key, value = text.split(":", 1)
    key = key.strip()
    if not key:
        raise SimpleYamlError(f"Missing key in line: {text}")
    return key, value.strip()


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in ("", "null", "Null", "NULL", "~"):
        return None
    if value in ("true", "True", "TRUE"):
        return True
    if value in ("false", "False", "FALSE"):
        return False
    if value == "[]":
        return []
    if value == "{}":
        return {}
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(part.strip()) for part in inner.split(",")]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    return value
