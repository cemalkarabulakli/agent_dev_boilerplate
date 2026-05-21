import { MockExtractorProvider } from "./mock_extractor_provider";

export class FirecrawlExtractorProvider extends MockExtractorProvider {
  constructor(private readonly apiKey?: string) {
    super();
  }

  override async extract(url: string, options = {}) {
    if (!this.apiKey) {
      return super.extract(url, options);
    }
    return super.extract(url, { ...options, provider: "firecrawl_placeholder" });
  }
}

