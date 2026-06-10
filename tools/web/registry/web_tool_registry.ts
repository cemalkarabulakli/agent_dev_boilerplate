import { MockSearchProvider } from "../search/mock_search_provider";
import { TavilySearchProvider } from "../search/tavily_search_provider";
import { SearXNGSearchProvider } from "../search/searxng_search_provider";
import { MockExtractorProvider } from "../extraction/mock_extractor_provider";
import { FirecrawlExtractorProvider } from "../extraction/firecrawl_extractor_provider";
import { MockBrowserProvider } from "../browser/mock_browser_provider";
import { PlaywrightBrowserProvider } from "../browser/playwright_browser_provider";
import { MockSemanticSearchProvider } from "../semantic/mock_semantic_search_provider";
import { ExaSemanticSearchProvider } from "../semantic/exa_semantic_search_provider";
import { webToolsConfig } from "../config/web_tools_config";

export function createWebTools(overrides: Partial<typeof webToolsConfig> = {}) {
  const config = { ...webToolsConfig, ...overrides };
  const env = config.providers;
  const isLive = config.mode === "live";

  const search = isLive && env.tavily.apiKey
    ? new TavilySearchProvider(env.tavily.apiKey)
    : new MockSearchProvider();

  const openSourceSearch = env.searxng.baseUrl
    ? new SearXNGSearchProvider(env.searxng.baseUrl)
    : new SearXNGSearchProvider();

  const semanticSearch = isLive && env.exa.apiKey
    ? new ExaSemanticSearchProvider(env.exa.apiKey)
    : new MockSemanticSearchProvider();

  const mockSearch = new MockSearchProvider();

  const extractor = isLive && env.firecrawl.apiKey
    ? new FirecrawlExtractorProvider(env.firecrawl.apiKey)
    : new MockExtractorProvider();

  const browser = isLive && env.playwright.enabled
    ? new PlaywrightBrowserProvider()
    : new MockBrowserProvider();

  const crawler = {
    async crawl(startUrl: string) {
      return {
        startUrl,
        pages: [],
        crawledAt: new Date().toISOString(),
        retrievedAt: new Date().toISOString(),
        provider: config.defaults.crawlerProvider,
        isMock: true,
      };
    },
    async crawlDomain(domain: string) {
      return {
        startUrl: `mock://crawl/${domain}`,
        pages: [],
        crawledAt: new Date().toISOString(),
        retrievedAt: new Date().toISOString(),
        provider: config.defaults.crawlerProvider,
        isMock: true,
      };
    },
    async scheduleCrawl(jobConfig: Record<string, unknown>) {
      return { jobId: jobConfig["id"] ?? "mock_job", scheduled: true, isMock: true };
    },
  };

  /** @deprecated Use extractor */
  const extraction = extractor;

  return { search, openSourceSearch, semanticSearch, mockSearch, extractor, extraction, browser, crawler };
}

export type WebTools = ReturnType<typeof createWebTools>;
