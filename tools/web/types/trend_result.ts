export interface TrendResult {
  keyword: string;
  region?: string;
  timeframe?: string;
  interestTrend: "rising" | "flat" | "declining" | "unknown";
  relatedQueries: string[];
  confidence: number;
  provider: string;
  isMock: boolean;
  metadata?: Record<string, unknown>;
}

