import { MockSemanticSearchProvider } from "./mock_semantic_search_provider";
import type { SearchOptions } from "../types/search_options";
import type { SearchResponse } from "../types/search_response";
import type { WebSearchResult } from "../types/web_search_result";

const EXA_BASE_URL = "https://api.exa.ai";

export class ExaSemanticSearchProvider extends MockSemanticSearchProvider {
  constructor(private readonly apiKey?: string) {
    super();
  }

  override async search(query: string, options: SearchOptions = {}): Promise<SearchResponse> {
    if (!this.apiKey) {
      const fallback = await super.search(query, options);
      return {
        ...fallback,
        warnings: ["EXA_API_KEY not set, using mock semantic fallback"],
      };
    }

    const body: Record<string, unknown> = {
      query,
      numResults: options.maxResults ?? 10,
      useAutoprompt: true,
      ...(options.includeRawContent ? { contents: { text: true } } : {}),
      ...(options.domains?.length ? { includeDomains: options.domains } : {}),
      ...(options.excludeDomains?.length ? { excludeDomains: options.excludeDomains } : {}),
    };

    const response = await fetch(`${EXA_BASE_URL}/search`, {
      method: "POST",
      headers: {
        "x-api-key": this.apiKey,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Exa search failed (${response.status}): ${error}`);
    }

    const data = (await response.json()) as {
      results?: Array<{
        title?: string;
        url?: string;
        text?: string;
        publishedDate?: string;
        score?: number;
        author?: string;
      }>;
    };

    const results: WebSearchResult[] = (data.results ?? []).map((item) => ({
      title: item.title ?? item.url ?? "",
      url: item.url ?? "",
      snippet: item.text?.slice(0, 300) ?? "",
      content: item.text,
      source: "exa",
      score: item.score ?? 0,
      publishedAt: item.publishedDate,
      isMock: false,
      metadata: { query, provider: "exa", author: item.author },
    }));

    return {
      provider: "exa",
      query,
      results,
      raw: data,
      isMock: false,
      retrievedAt: new Date().toISOString(),
    };
  }

  override async findSourcesForRag(query: string, options?: SearchOptions): Promise<SearchResponse> {
    return this.search(query, { ...options, includeRawContent: true });
  }

  override async findSimilar(urlOrText: string, options?: SearchOptions): Promise<SearchResponse> {
    if (!this.apiKey) {
      return super.findSimilar(urlOrText, options);
    }

    const isUrl = urlOrText.startsWith("http://") || urlOrText.startsWith("https://");
    const body: Record<string, unknown> = isUrl
      ? { url: urlOrText, numResults: options?.maxResults ?? 10 }
      : { query: urlOrText, numResults: options?.maxResults ?? 10, useAutoprompt: true };

    const endpoint = isUrl ? `${EXA_BASE_URL}/findSimilar` : `${EXA_BASE_URL}/search`;
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "x-api-key": this.apiKey, "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Exa findSimilar failed (${response.status}): ${error}`);
    }

    const data = (await response.json()) as {
      results?: Array<{ title?: string; url?: string; text?: string; score?: number }>;
    };

    const results: WebSearchResult[] = (data.results ?? []).map((item) => ({
      title: item.title ?? item.url ?? "",
      url: item.url ?? "",
      snippet: item.text?.slice(0, 300) ?? "",
      source: "exa",
      score: item.score ?? 0,
      isMock: false,
      metadata: { provider: "exa", input: urlOrText },
    }));

    return {
      provider: "exa",
      query: urlOrText,
      results,
      raw: data,
      isMock: false,
      retrievedAt: new Date().toISOString(),
    };
  }
}
