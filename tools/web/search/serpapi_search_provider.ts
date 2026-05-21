import { MockSearchProvider } from "./mock_search_provider";

export class SerpApiSearchProvider extends MockSearchProvider {
  constructor(private readonly apiKey?: string) {
    super();
  }

  override async search(query: string, options = {}) {
    if (!this.apiKey) {
      return super.search(query, options);
    }
    return super.search(query, { ...options, provider: "serpapi_placeholder" });
  }
}

