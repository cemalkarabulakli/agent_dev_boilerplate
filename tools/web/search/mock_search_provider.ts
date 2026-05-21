import type { WebSearchOptions, WebSearchTool } from "../interfaces/web_search_tool";
import type { WebSearchResult } from "../types/web_search_result";

export class MockSearchProvider implements WebSearchTool {
  async search(query: string, options: WebSearchOptions = {}): Promise<WebSearchResult[]> {
    const maxResults = options.maxResults ?? 3;
    return Array.from({ length: maxResults }).map((_, index) => ({
      title: `Mock search result ${index + 1} for ${query}`,
      url: `mock://web-search/${encodeURIComponent(query)}/${index + 1}`,
      snippet: "Mock result. Configure Tavily or SerpAPI for live web research.",
      source: "mock_search",
      score: 0.5,
      isMock: true,
      metadata: { query, provider: "mock" },
    }));
  }

  async searchNews(query: string, options?: WebSearchOptions): Promise<WebSearchResult[]> {
    return this.search(`latest news ${query}`, options);
  }

  async findCompetitors(companyOrNicheOrUrl: string, options?: WebSearchOptions): Promise<WebSearchResult[]> {
    return this.search(`competitors for ${companyOrNicheOrUrl}`, options);
  }

  async findLatest(query: string, options?: WebSearchOptions): Promise<WebSearchResult[]> {
    return this.search(`latest public information about ${query}`, options);
  }
}

