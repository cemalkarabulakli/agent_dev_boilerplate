export interface ExtractionOptions {
  onlyMainContent?: boolean;
  includeHtml?: boolean;
  includeLinks?: boolean;
  timeoutMs?: number;
  waitForSelector?: string;
  retries?: number;
}
