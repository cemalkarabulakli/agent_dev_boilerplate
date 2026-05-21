import { MockSearchProvider } from "./mock_search_provider";

export class TavilySearchProvider extends MockSearchProvider {
  constructor(private readonly apiKey?: string) {
    super();
  }

  override async search(query: string, options = {}) {
    if (!this.apiKey) {
      return super.search(query, options);
    }
    return super.search(query, { ...options, provider: "tavily_placeholder" });
  }
}

