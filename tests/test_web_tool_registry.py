from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_web_tool_registry_uses_interfaces_and_mock_fallbacks() -> None:
    registry = (ROOT / "tools" / "web" / "registry" / "web_tool_registry.ts").read_text(encoding="utf-8")
    config = (ROOT / "tools" / "web" / "config" / "web_tools_config.ts").read_text(encoding="utf-8")

    assert "createWebTools" in registry
    assert "MockSearchProvider" in registry
    assert "MockExtractorProvider" in registry
    assert "MockBrowserProvider" in registry
    assert "crawlDomain" in registry
    assert "scheduleCrawl" in registry
    assert "TAVILY_API_KEY" in config
    assert "FIRECRAWL_API_KEY" in config
    assert "WEB_TOOLS_MODE" in config


def test_web_tool_provider_checklist_exists() -> None:
    assert (ROOT / "checklists" / "web_tool_provider_checklist.yaml").exists()
