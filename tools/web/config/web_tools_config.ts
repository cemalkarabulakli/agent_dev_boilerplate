declare const process: { env?: Record<string, string | undefined> };

export const webToolsConfig = {
  mode: (process.env?.WEB_TOOLS_MODE ?? "mock") as "mock" | "live",

  defaults: {
    searchProvider: process.env?.DEFAULT_SEARCH_PROVIDER ?? "tavily",
    openSourceSearchProvider: process.env?.OPEN_SOURCE_SEARCH_PROVIDER ?? "searxng",
    semanticSearchProvider: process.env?.DEFAULT_SEMANTIC_SEARCH_PROVIDER ?? "exa",
    extractorProvider: process.env?.DEFAULT_EXTRACTOR_PROVIDER ?? "firecrawl",
    browserProvider: process.env?.DEFAULT_BROWSER_PROVIDER ?? "playwright",
    crawlerProvider: process.env?.DEFAULT_CRAWLER_PROVIDER ?? "scrapy",
    maxResults: Number(process.env?.SEARCH_MAX_RESULTS ?? 10),
    timeoutMs: Number(process.env?.SEARCH_TIMEOUT_MS ?? 30000),
    retries: Number(process.env?.SEARCH_RETRIES ?? 2),
  },

  providers: {
    searxng: {
      enabled: Boolean(process.env?.SEARXNG_BASE_URL),
      baseUrl: process.env?.SEARXNG_BASE_URL ?? "http://localhost:8080",
    },
    tavily: {
      enabled: Boolean(process.env?.TAVILY_API_KEY),
      apiKey: process.env?.TAVILY_API_KEY,
    },
    exa: {
      enabled: Boolean(process.env?.EXA_API_KEY),
      apiKey: process.env?.EXA_API_KEY,
    },
    firecrawl: {
      enabled: Boolean(process.env?.FIRECRAWL_API_KEY),
      apiKey: process.env?.FIRECRAWL_API_KEY,
    },
    playwright: {
      enabled: process.env?.PLAYWRIGHT_ENABLED !== "false",
    },
    scrapy: {
      enabled: process.env?.SCRAPY_ENABLED !== "false",
    },
  },
};

export type WebToolsConfig = typeof webToolsConfig;

/** @deprecated Use webToolsConfig; kept for test/legacy compatibility */
export function loadWebToolsConfig(env: Record<string, string | undefined> = process.env ?? {}): {
  mode: "mock" | "live";
  searchProvider: "tavily" | "searxng" | "mock";
  extractorProvider: "firecrawl" | "mock";
  browserProvider: "playwright" | "mock";
  crawlerProvider: "scrapy" | "mock";
  retry: { maxAttempts: number; backoffMs: number };
  rateLimit: { requestsPerMinute: number };
  env: Record<string, string | undefined>;
} {
  const mode = env.WEB_TOOLS_MODE === "live" ? "live" : "mock";
  return {
    mode,
    searchProvider: mode === "live" && env.TAVILY_API_KEY ? "tavily" : mode === "live" && env.SEARXNG_BASE_URL ? "searxng" : "mock",
    extractorProvider: mode === "live" && env.FIRECRAWL_API_KEY ? "firecrawl" : "mock",
    browserProvider: mode === "live" ? "playwright" : "mock",
    crawlerProvider: mode === "live" ? "scrapy" : "mock",
    retry: { maxAttempts: Number(env.SEARCH_RETRIES ?? 2), backoffMs: 1000 },
    rateLimit: { requestsPerMinute: 30 },
    env,
  };
}
