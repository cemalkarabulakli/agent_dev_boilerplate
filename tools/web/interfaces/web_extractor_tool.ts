import type { ExtractionResult } from "../types/extraction_result";

export interface WebExtractionOptions {
  includeHtml?: boolean;
  onlyMainContent?: boolean;
  waitForSelector?: string;
}

export interface WebExtractorTool {
  extract(url: string, options?: WebExtractionOptions): Promise<ExtractionResult>;
  extractMany(urls: string[], options?: WebExtractionOptions): Promise<ExtractionResult[]>;
  extractMarkdown(url: string, options?: WebExtractionOptions): Promise<string>;
  extractPricingPage(url: string, options?: WebExtractionOptions): Promise<ExtractionResult>;
  extractLandingPage(url: string, options?: WebExtractionOptions): Promise<ExtractionResult>;
}

