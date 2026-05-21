import type { SourceReference } from "./source_reference";

export interface SourceSignal {
  id: string;
  source: string;
  source_type: string;
  query: string;
  title: string;
  url: string;
  text: string;
  language: string;
  author_or_channel: string;
  collected_at: string;
  published_at?: string;
  reference_id: string;
  metadata: Record<string, unknown>;
  is_mock: boolean;
}

export interface ProcessedSignal {
  id: string;
  source: string;
  raw_signal_ids: string[];
  reference_ids: string[];
  insight_type: string;
  summary: string;
  evidence: string[];
  source_urls: string[];
  confidence: number;
  scores: Record<string, number>;
  status: "raw" | "candidate" | "validated" | "rejected" | "needs_human_review";
  recommendation: string;
  created_at: string;
  is_mock: boolean;
}

export interface SourceCollectionResult {
  rawSignals: SourceSignal[];
  processedSignals: ProcessedSignal[];
  references: SourceReference[];
  reportMarkdown: string;
}
