export interface CrawlResult {
  startUrl: string;
  pages: Array<{ url: string; title: string; text: string; status: number }>;
  crawledAt: string;
  provider: string;
  isMock: boolean;
  metadata?: Record<string, unknown>;
}

