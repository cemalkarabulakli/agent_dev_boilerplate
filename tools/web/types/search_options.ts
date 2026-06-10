export type SearchProviderName = "searxng" | "tavily" | "mock";

export type SemanticSearchProviderName = "exa" | "mock";

export interface SearchOptions {
  provider?: SearchProviderName | SemanticSearchProviderName;
  maxResults?: number;
  language?: string;
  region?: string;
  freshness?: "day" | "week" | "month" | "year" | "any";
  includeRawContent?: boolean;
  includeAnswer?: boolean;
  domains?: string[];
  excludeDomains?: string[];
  site?: string;
  timeoutMs?: number;
  retries?: number;
  /** @deprecated Use SearchOptions.region instead */
  country?: string;
}
