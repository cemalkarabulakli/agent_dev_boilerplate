declare const process: { env?: Record<string, string | undefined> };

export interface WebToolsConfig {
  mode: "mock" | "live";
  searchProvider: "tavily" | "serpapi" | "mock";
  extractorProvider: "firecrawl" | "mock";
  browserProvider: "playwright" | "mock";
  crawlerProvider: "scrapy" | "mock";
  retry: { maxAttempts: number; backoffMs: number };
  rateLimit: { requestsPerMinute: number };
  env: Record<string, string | undefined>;
}

export function loadWebToolsConfig(env: Record<string, string | undefined> = process.env ?? {}): WebToolsConfig {
  const mode = env.WEB_TOOLS_MODE === "live" ? "live" : "mock";
  return {
    mode,
    searchProvider: mode === "live" && env.TAVILY_API_KEY ? "tavily" : "mock",
    extractorProvider: mode === "live" && env.FIRECRAWL_API_KEY ? "firecrawl" : "mock",
    browserProvider: mode === "live" ? "playwright" : "mock",
    crawlerProvider: mode === "live" ? "scrapy" : "mock",
    retry: { maxAttempts: 2, backoffMs: 1000 },
    rateLimit: { requestsPerMinute: 30 },
    env,
  };
}
