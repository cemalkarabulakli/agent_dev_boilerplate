export interface CrawlOptions {
  maxPages?: number;
  maxDepth?: number;
  followExternalLinks?: boolean;
  includePatterns?: string[];
  excludePatterns?: string[];
  timeoutMs?: number;
  respectRobotsTxt?: boolean;
}

export interface CrawlResult {
  startUrl: string;
  pages: Array<{ url: string; title: string; text: string; status: number }>;
  crawledAt: string;
  provider: string;
  isMock: boolean;
  retrievedAt: string;
  warnings?: string[];
  metadata?: Record<string, unknown>;
}
