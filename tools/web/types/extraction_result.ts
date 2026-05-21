export interface ExtractionResult {
  url: string;
  title: string;
  markdown: string;
  text: string;
  extractedAt: string;
  provider: string;
  isMock: boolean;
  metadata?: Record<string, unknown>;
}

