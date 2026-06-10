from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_mock_semantic_provider_exists() -> None:
    path = ROOT / "tools" / "web" / "semantic" / "mock_semantic_search_provider.ts"
    assert path.exists(), "mock_semantic_search_provider.ts must exist"


def test_mock_semantic_provider_has_isMock_true() -> None:
    text = (ROOT / "tools" / "web" / "semantic" / "mock_semantic_search_provider.ts").read_text(encoding="utf-8")
    assert "isMock: true" in text


def test_mock_semantic_provider_has_required_methods() -> None:
    text = (ROOT / "tools" / "web" / "semantic" / "mock_semantic_search_provider.ts").read_text(encoding="utf-8")
    assert "search(" in text
    assert "findSourcesForRag(" in text
    assert "findSimilar(" in text


def test_exa_provider_exists_and_checks_api_key() -> None:
    path = ROOT / "tools" / "web" / "semantic" / "exa_semantic_search_provider.ts"
    assert path.exists(), "exa_semantic_search_provider.ts must exist"
    text = path.read_text(encoding="utf-8")
    assert "EXA_API_KEY" in text or "apiKey" in text, "Exa provider must check for API key"
    assert "MockSemanticSearchProvider" in text, "Exa provider must fall back to mock"


def test_exa_provider_does_not_hardcode_api_key() -> None:
    text = (ROOT / "tools" / "web" / "semantic" / "exa_semantic_search_provider.ts").read_text(encoding="utf-8")
    import re
    hardcoded = re.findall(r'["\'](?:exa[-_])?[a-z0-9]{20,}["\']', text)
    assert not hardcoded, f"Exa provider appears to have a hardcoded API key: {hardcoded}"


def test_semantic_interface_exists_with_required_methods() -> None:
    path = ROOT / "tools" / "web" / "interfaces" / "semantic_search_tool.ts"
    assert path.exists(), "semantic_search_tool.ts interface must exist"
    text = path.read_text(encoding="utf-8")
    assert "SemanticSearchTool" in text
    assert "search(" in text
    assert "findSourcesForRag" in text
    assert "findSimilar" in text


def test_no_hardcoded_api_keys_in_semantic_providers() -> None:
    import re
    for fname in ["exa_semantic_search_provider.ts", "mock_semantic_search_provider.ts"]:
        path = ROOT / "tools" / "web" / "semantic" / fname
        if path.exists():
            text = path.read_text(encoding="utf-8")
            hardcoded = re.findall(r'["\'][a-zA-Z0-9_\-]{32,}["\']', text)
            assert not hardcoded, f"{fname} may have hardcoded secrets: {hardcoded}"
