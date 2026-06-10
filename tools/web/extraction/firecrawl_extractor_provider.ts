import { MockExtractorProvider } from "./mock_extractor_provider";
import type { WebExtractionOptions } from "../interfaces/web_extractor_tool";
import type { ExtractionResult } from "../types/extraction_result";

const FIRECRAWL_BASE_URL = "https://api.firecrawl.dev/v1";

export class FirecrawlExtractorProvider extends MockExtractorProvider {
  constructor(private readonly apiKey?: string) {
    super();
  }

  override async extract(url: string, options: WebExtractionOptions = {}): Promise<ExtractionResult> {
    if (!this.apiKey) {
      return super.extract(url, options);
    }

    const body: Record<string, unknown> = {
      url,
      formats: ["markdown"],
      onlyMainContent: options.onlyMainContent !== false,
    };

    if (options.includeHtml) {
      (body.formats as string[]).push("html");
    }

    const response = await fetch(`${FIRECRAWL_BASE_URL}/scrape`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${this.apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Firecrawl scrape failed (${response.status}): ${error}`);
    }

    const data = (await response.json()) as {
      success: boolean;
      data?: {
        markdown?: string;
        metadata?: { title?: string; [key: string]: unknown };
      };
    };

    if (!data.success || !data.data) {
      throw new Error(`Firecrawl returned unsuccessful response for ${url}`);
    }

    const markdown = data.data.markdown ?? "";
    const title = (data.data.metadata?.title as string) ?? url;

    return {
      url,
      title,
      markdown,
      text: markdown.replace(/[#*`>\-_\[\]()]/g, "").trim(),
      extractedAt: new Date().toISOString(),
      provider: "firecrawl",
      isMock: false,
      metadata: { ...(data.data.metadata ?? {}), options },
    };
  }

  override async extractMany(urls: string[], options?: WebExtractionOptions): Promise<ExtractionResult[]> {
    return Promise.all(urls.map((url) => this.extract(url, options)));
  }

  override async extractMarkdown(url: string, options?: WebExtractionOptions): Promise<string> {
    return (await this.extract(url, options)).markdown;
  }

  override async extractPricingPage(url: string, options?: WebExtractionOptions): Promise<ExtractionResult> {
    return this.extract(url, { ...options, onlyMainContent: true });
  }

  override async extractLandingPage(url: string, options?: WebExtractionOptions): Promise<ExtractionResult> {
    return this.extract(url, { ...options, onlyMainContent: true });
  }
}
