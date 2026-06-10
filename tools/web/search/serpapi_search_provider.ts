import { MockSearchProvider } from "./mock_search_provider";
import type { WebSearchOptions } from "../interfaces/web_search_tool";
import type { WebSearchResult } from "../types/web_search_result";

const SERPAPI_BASE_URL = "https://serpapi.com/search.json";

export class SerpApiSearchProvider extends MockSearchProvider {
  constructor(private readonly apiKey?: string) {
    super();
  }

  override async search(query: string, options: WebSearchOptions = {}): Promise<WebSearchResult[]> {
    if (!this.apiKey) {
      return super.search(query, options);
    }

    const params = new URLSearchParams({
      q: query,
      api_key: this.apiKey,
      engine: "google",
      num: String(options.maxResults ?? 10),
      ...(options.country ? { gl: options.country } : {}),
      ...(options.language ? { hl: options.language } : {}),
    });

    const response = await fetch(`${SERPAPI_BASE_URL}?${params.toString()}`);

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`SerpAPI search failed (${response.status}): ${error}`);
    }

    const data = (await response.json()) as {
      organic_results?: Array<{
        title?: string;
        link?: string;
        snippet?: string;
        displayed_link?: string;
        position?: number;
      }>;
    };

    const results = data.organic_results ?? [];

    return results.map((item, index) => ({
      title: item.title ?? "",
      url: item.link ?? "",
      snippet: item.snippet ?? "",
      source: item.displayed_link ?? item.link ?? "serpapi",
      score: 1 - index * 0.05,
      isMock: false,
      metadata: { query, position: item.position ?? index + 1, provider: "serpapi" },
    }));
  }

  override async searchNews(query: string, options: WebSearchOptions = {}): Promise<WebSearchResult[]> {
    if (!this.apiKey) {
      return super.searchNews(query, options);
    }

    const params = new URLSearchParams({
      q: query,
      api_key: this.apiKey,
      engine: "google",
      tbm: "nws",
      num: String(options.maxResults ?? 10),
      ...(options.country ? { gl: options.country } : {}),
    });

    const response = await fetch(`${SERPAPI_BASE_URL}?${params.toString()}`);

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`SerpAPI news search failed (${response.status}): ${error}`);
    }

    const data = (await response.json()) as {
      news_results?: Array<{
        title?: string;
        link?: string;
        snippet?: string;
        source?: string;
        date?: string;
        position?: number;
      }>;
    };

    const results = data.news_results ?? [];

    return results.map((item, index) => ({
      title: item.title ?? "",
      url: item.link ?? "",
      snippet: item.snippet ?? "",
      source: item.source ?? "serpapi_news",
      score: 1 - index * 0.05,
      publishedAt: item.date,
      isMock: false,
      metadata: { query, provider: "serpapi_news" },
    }));
  }

  override async findCompetitors(companyOrNicheOrUrl: string, options?: WebSearchOptions): Promise<WebSearchResult[]> {
    return this.search(`top competitors for ${companyOrNicheOrUrl}`, options);
  }

  override async findLatest(query: string, options?: WebSearchOptions): Promise<WebSearchResult[]> {
    return this.searchNews(query, options);
  }
}
