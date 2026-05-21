import type { TrendResult } from "../types/trend_result";

export interface TrendOptions {
  region?: string;
  timeframe?: string;
}

export interface TrendProviderTool {
  getTrend(keyword: string, options?: TrendOptions): Promise<TrendResult>;
  compareTrends(keywords: string[], options?: TrendOptions): Promise<TrendResult[]>;
  getRelatedQueries(keyword: string, options?: TrendOptions): Promise<string[]>;
}

