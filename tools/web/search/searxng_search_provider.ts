import { MockSearchProvider } from "./mock_search_provider";
import type { SearchOptions } from "../types/search_options";
import type { SearchResponse } from "../types/search_response";
import type { WebSearchResult } from "../types/web_search_result";

export class SearXNGSearchProvider extends MockSearchProvider {
  private readonly baseUrl: string;

  constructor(baseUrl = "http://localhost:8080") {
    super();
    this.baseUrl = baseUrl.replace(/\/$/, "");
  }

  override async search(query: string, options: SearchOptions = {}): Promise<SearchResponse> {
    const params = new URLSearchParams({
      q: query,
      format: "json",
      categories: "general",
      ...(options.language ? { language: options.language } : {}),
      ...(options.maxResults ? { pageno: "1" } : {}),
    });

    let raw: unknown;
    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), options.timeoutMs ?? 10000);
      const response = await fetch(`${this.baseUrl}/search?${params.toString()}`, {
        signal: controller.signal,
        headers: { Accept: "application/json" },
      });
      clearTimeout(timer);

      if (!response.ok) {
        throw new Error(`SearXNG returned ${response.status}`);
      }
      raw = await response.json();
    } catch {
      const fallback = await super.search(query, options);
      return {
        ...fallback,
        warnings: [`SearXNG unreachable at ${this.baseUrl}, using mock fallback`],
      };
    }

    const data = raw as {
      results?: Array<{
        title?: string;
        url?: string;
        content?: string;
        publishedDate?: string;
        score?: number;
        engine?: string;
      }>;
      answers?: string[];
    };

    const maxResults = options.maxResults ?? 10;
    const results: WebSearchResult[] = (data.results ?? []).slice(0, maxResults).map((item) => ({
      title: item.title ?? item.url ?? "",
      url: item.url ?? "",
      snippet: item.content ?? "",
      source: item.engine ?? "searxng",
      score: item.score ?? 0,
      publishedAt: item.publishedDate,
      isMock: false,
      metadata: { query, provider: "searxng" },
    }));

    return {
      provider: "searxng",
      query,
      results,
      answer: data.answers?.[0],
      raw,
      isMock: false,
      retrievedAt: new Date().toISOString(),
    };
  }

  override async findLatest(query: string, options?: SearchOptions): Promise<SearchResponse> {
    return this.search(query, { ...options, freshness: "week" });
  }

  override async findCompetitors(query: string, options?: SearchOptions): Promise<SearchResponse> {
    return this.search(`top competitors for ${query}`, options);
  }
}
