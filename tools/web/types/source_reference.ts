export interface SourceReference {
  id: string;
  source: string;
  source_type: string;
  query: string;
  title: string;
  url: string;
  author_or_channel: string;
  collected_at: string;
  published_at?: string;
  raw_file: string;
  processed_file?: string;
  confidence: number;
  is_mock: boolean;
  notes?: string;
}
