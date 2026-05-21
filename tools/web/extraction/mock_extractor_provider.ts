import type { WebExtractionOptions, WebExtractorTool } from "../interfaces/web_extractor_tool";
import type { ExtractionResult } from "../types/extraction_result";

export class MockExtractorProvider implements WebExtractorTool {
  async extract(url: string, options: WebExtractionOptions = {}): Promise<ExtractionResult> {
    return {
      url,
      title: `Mock extraction for ${url}`,
      markdown: `# Mock Extracted Page\n\nConfigure Firecrawl for live extraction.\n`,
      text: "Mock extracted page text. Configure Firecrawl for live extraction.",
      extractedAt: new Date().toISOString(),
      provider: "mock_extractor",
      isMock: true,
      metadata: options,
    };
  }

  async extractMany(urls: string[], options?: WebExtractionOptions): Promise<ExtractionResult[]> {
    return Promise.all(urls.map((url) => this.extract(url, options)));
  }

  async extractMarkdown(url: string, options?: WebExtractionOptions): Promise<string> {
    return (await this.extract(url, options)).markdown;
  }

  async extractPricingPage(url: string, options?: WebExtractionOptions): Promise<ExtractionResult> {
    return this.extract(url, { ...options, pageType: "pricing" } as WebExtractionOptions);
  }

  async extractLandingPage(url: string, options?: WebExtractionOptions): Promise<ExtractionResult> {
    return this.extract(url, { ...options, pageType: "landing" } as WebExtractionOptions);
  }
}

