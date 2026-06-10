import type { SearchOptions } from "../types/search_options";
import type { SearchResponse } from "../types/search_response";

/** @deprecated Use SearchOptions from types/search_options */
export type WebSearchOptions = SearchOptions;

export interface WebSearchTool {
  search(query: string, options?: SearchOptions): Promise<SearchResponse>;
  findLatest(query: string, options?: SearchOptions): Promise<SearchResponse>;
  findCompetitors(query: string, options?: SearchOptions): Promise<SearchResponse>;
  /** @deprecated Prefer findLatest() for latest content */
  searchNews(query: string, options?: SearchOptions): Promise<SearchResponse>;
}
