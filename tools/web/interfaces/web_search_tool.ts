import type { WebSearchResult } from "../types/web_search_result";

export interface WebSearchOptions {
  maxResults?: number;
  includeNews?: boolean;
  country?: string;
  language?: string;
}

export interface WebSearchTool {
  search(query: string, options?: WebSearchOptions): Promise<WebSearchResult[]>;
  searchNews(query: string, options?: WebSearchOptions): Promise<WebSearchResult[]>;
  findCompetitors(companyOrNicheOrUrl: string, options?: WebSearchOptions): Promise<WebSearchResult[]>;
  findLatest(query: string, options?: WebSearchOptions): Promise<WebSearchResult[]>;
}

