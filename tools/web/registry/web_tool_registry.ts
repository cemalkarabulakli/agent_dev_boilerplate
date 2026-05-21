import { MockSearchProvider } from "../search/mock_search_provider";
import { TavilySearchProvider } from "../search/tavily_search_provider";
import { SerpApiSearchProvider } from "../search/serpapi_search_provider";
import { MockExtractorProvider } from "../extraction/mock_extractor_provider";
import { FirecrawlExtractorProvider } from "../extraction/firecrawl_extractor_provider";
import { MockBrowserProvider } from "../browser/mock_browser_provider";
import { PlaywrightBrowserProvider } from "../browser/playwright_browser_provider";
import { loadWebToolsConfig, type WebToolsConfig } from "../config/web_tools_config";

export function createWebTools(config: Partial<WebToolsConfig> = {}) {
  const loaded = { ...loadWebToolsConfig(), ...config };
  const search =
    loaded.searchProvider === "tavily"
      ? new TavilySearchProvider(loaded.env?.TAVILY_API_KEY)
      : loaded.searchProvider === "serpapi"
        ? new SerpApiSearchProvider(loaded.env?.SERPAPI_API_KEY)
        : new MockSearchProvider();
  const extraction =
    loaded.extractorProvider === "firecrawl"
      ? new FirecrawlExtractorProvider(loaded.env?.FIRECRAWL_API_KEY)
      : new MockExtractorProvider();
  const browser = loaded.browserProvider === "playwright" ? new PlaywrightBrowserProvider() : new MockBrowserProvider();
  const crawler = {
    async crawl(startUrl: string) {
      return { startUrl, pages: [], crawledAt: new Date().toISOString(), provider: loaded.crawlerProvider, isMock: true };
    },
    async crawlDomain(domain: string) {
      return { startUrl: `mock://crawl/${domain}`, pages: [], crawledAt: new Date().toISOString(), provider: loaded.crawlerProvider, isMock: true };
    },
    async scheduleCrawl(jobConfig: { id: string }) {
      return { jobId: jobConfig.id, scheduled: true };
    },
  };
  return { search, extraction, browser, crawler };
}
