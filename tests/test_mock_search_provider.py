from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_mock_search_provider_has_required_fields() -> None:
    text = (ROOT / "tools" / "web" / "search" / "mock_search_provider.ts").read_text(encoding="utf-8")
    assert "isMock" in text
    assert "search(" in text
    assert "mock" in text.lower()


def test_searxng_provider_exists_and_has_fallback_pattern() -> None:
    path = ROOT / "tools" / "web" / "search" / "searxng_search_provider.ts"
    assert path.exists(), "searxng_search_provider.ts must exist"
    text = path.read_text(encoding="utf-8")
    assert "SearXNGSearchProvider" in text
    assert "MockSearchProvider" in text, "SearXNG provider must fall back to mock"
    assert "isMock" in text
    assert "SEARXNG_BASE_URL" in text or "baseUrl" in text


def test_searxng_provider_does_not_hardcode_api_key() -> None:
    text = (ROOT / "tools" / "web" / "search" / "searxng_search_provider.ts").read_text(encoding="utf-8")
    assert "api_key" not in text.lower() or "process.env" in text or "apiKey" not in text


def test_tavily_provider_extends_mock() -> None:
    text = (ROOT / "tools" / "web" / "search" / "tavily_search_provider.ts").read_text(encoding="utf-8")
    assert "MockSearchProvider" in text


def test_mock_search_provider_isMock_true() -> None:
    text = (ROOT / "tools" / "web" / "search" / "mock_search_provider.ts").read_text(encoding="utf-8")
    assert "isMock: true" in text


def test_agents_do_not_import_searxng_directly() -> None:
    forbidden = ["import searxng", "from searxng", "SearXNGSearchProvider"]
    for path in (ROOT / "agents").glob("**/*"):
        if path.is_file() and path.suffix in {".md", ".yaml", ".yml", ".py", ".ts"}:
            text = path.read_text(encoding="utf-8")
            for term in forbidden:
                assert term not in text, f"Agent file {path} imports {term} directly"
