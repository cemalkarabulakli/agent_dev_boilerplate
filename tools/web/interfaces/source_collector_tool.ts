import type { ProcessedSignal, SourceSignal } from "../types/source_signal";

export interface SourceCollectionOptions {
  limit?: number;
  mode?: "mock" | "api" | "scrape" | "manual";
  includeReferences?: boolean;
}

export interface SourceCollectorTool {
  collect(query: string, options?: SourceCollectionOptions): Promise<SourceSignal[]>;
  process(rawSignals: SourceSignal[], options?: SourceCollectionOptions): Promise<ProcessedSignal[]>;
  generateReport(processedSignals: ProcessedSignal[], options?: SourceCollectionOptions): Promise<string>;
}

