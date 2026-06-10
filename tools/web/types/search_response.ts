import type { WebSearchResult } from "./web_search_result";

export interface SearchResponse {
  provider: string;
  query: string;
  results: WebSearchResult[];
  answer?: string;
  raw?: unknown;
  isMock: boolean;
  retrievedAt: string;
  warnings?: string[];
}
