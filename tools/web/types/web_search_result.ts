export interface WebSearchResult {
  title: string;
  url: string;
  snippet: string;
  source: string;
  score: number;
  publishedAt?: string;
  isMock: boolean;
  metadata?: Record<string, unknown>;
}

