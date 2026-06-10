import type { SemanticSearchTool } from "../interfaces/semantic_search_tool";
import type { SearchOptions } from "../types/search_options";
import type { SearchResponse } from "../types/search_response";
import type { WebSearchResult } from "../types/web_search_result";

const MOCK_SEMANTIC_RESULTS: WebSearchResult[] = [
  {
    title: "High-Ticket Consulting Offer Framework — Expert Authority",
    url: "https://mock.example.com/high-ticket-consulting-framework",
    snippet: "A structured approach to building high-ticket consulting offers using the P.D.A. framework.",
    source: "mock_semantic",
    score: 0.97,
    isMock: true,
    metadata: { semantic_score: 0.97, provider: "mock_semantic" },
  },
  {
    title: "RAG Source Discovery for Expert Business Research",
    url: "https://mock.example.com/rag-source-discovery-expert-business",
    snippet: "How to use semantic search to discover authoritative sources for RAG pipelines.",
    source: "mock_semantic",
    score: 0.91,
    isMock: true,
    metadata: { semantic_score: 0.91, provider: "mock_semantic" },
  },
  {
    title: "AI Automation Agency — Positioning and Offer Design",
    url: "https://mock.example.com/ai-automation-agency-positioning",
    snippet: "Positioning strategies and offer design for AI automation agencies targeting high-ticket clients.",
    source: "mock_semantic",
    score: 0.88,
    isMock: true,
    metadata: { semantic_score: 0.88, provider: "mock_semantic" },
  },
];

export class MockSemanticSearchProvider implements SemanticSearchTool {
  async search(query: string, options: SearchOptions = {}): Promise<SearchResponse> {
    const maxResults = options.maxResults ?? 10;
    return {
      provider: "mock_semantic",
      query,
      results: MOCK_SEMANTIC_RESULTS.slice(0, maxResults),
      isMock: true,
      retrievedAt: new Date().toISOString(),
      warnings: ["Mock semantic search — set EXA_API_KEY and WEB_TOOLS_MODE=live for real results"],
    };
  }

  async findSourcesForRag(query: string, options?: SearchOptions): Promise<SearchResponse> {
    return this.search(query, options);
  }

  async findSimilar(urlOrText: string, options?: SearchOptions): Promise<SearchResponse> {
    return this.search(`similar to: ${urlOrText}`, options);
  }
}
