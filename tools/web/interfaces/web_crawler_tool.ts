import type { CrawlResult } from "../types/crawl_result";

export interface WebCrawlerOptions {
  maxPages?: number;
  maxDepth?: number;
  obeyRobotsTxt?: boolean;
}

export interface CrawlJobConfig extends WebCrawlerOptions {
  id: string;
  startUrl: string;
  cron?: string;
}

export interface WebCrawlerTool {
  crawl(startUrl: string, options?: WebCrawlerOptions): Promise<CrawlResult>;
  crawlDomain(domain: string, options?: WebCrawlerOptions): Promise<CrawlResult>;
  scheduleCrawl(jobConfig: CrawlJobConfig): Promise<{ jobId: string; scheduled: boolean }>;
}

