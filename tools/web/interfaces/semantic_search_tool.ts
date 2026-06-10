import type { SearchOptions } from "../types/search_options";
import type { SearchResponse } from "../types/search_response";

export interface SemanticSearchTool {
  search(query: string, options?: SearchOptions): Promise<SearchResponse>;
  findSourcesForRag?(query: string, options?: SearchOptions): Promise<SearchResponse>;
  findSimilar?(urlOrText: string, options?: SearchOptions): Promise<SearchResponse>;
}
