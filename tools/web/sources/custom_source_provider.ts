import type { SourceCollectionOptions, SourceCollectorTool } from "../interfaces/source_collector_tool";
import type { ProcessedSignal, SourceSignal } from "../types/source_signal";

export class BaseMockSourceProvider implements SourceCollectorTool {
  constructor(
    protected readonly source = "custom",
    protected readonly sourceType = "custom",
    protected readonly language = "en",
    protected readonly insightType = "market_signal",
  ) {}

  async collect(query: string, options: SourceCollectionOptions = {}): Promise<SourceSignal[]> {
    const limit = Math.min(options.limit ?? 2, 5);
    return Array.from({ length: limit }).map((_, index) => {
      const id = `${this.source}_${index + 1}`;
      return {
        id,
        source: this.source,
        source_type: this.sourceType,
        query,
        title: `Mock ${this.source} signal ${index + 1}`,
        url: `mock://${this.source}/${id}`,
        text: `Mock ${this.source} evidence for ${query}. Configure the source provider for live collection.`,
        language: this.language,
        author_or_channel: "mock",
        collected_at: new Date().toISOString(),
        reference_id: `mock_ref_${id}`,
        metadata: { mode: options.mode ?? "mock" },
        is_mock: true,
      };
    });
  }

  async process(rawSignals: SourceSignal[]): Promise<ProcessedSignal[]> {
    return rawSignals.map((signal) => ({
      id: `processed_${signal.id}`,
      source: signal.source,
      raw_signal_ids: [signal.id],
      reference_ids: [signal.reference_id],
      insight_type: this.insightType,
      summary: `Candidate ${this.insightType} from ${signal.source}: ${signal.text}`,
      evidence: [signal.text],
      source_urls: [signal.url],
      confidence: signal.is_mock ? 0.55 : 0.7,
      scores: { source_confidence: signal.is_mock ? 0.55 : 0.7 },
      status: "candidate",
      recommendation: "Needs human review before strategy changes.",
      created_at: new Date().toISOString(),
      is_mock: signal.is_mock,
    }));
  }

  async generateReport(processedSignals: ProcessedSignal[]): Promise<string> {
    const lines = [`# ${this.source} Source Report`, "", "## Candidate Signals"];
    for (const signal of processedSignals) {
      lines.push(`- ${signal.summary} References: ${signal.reference_ids.join(", ")}`);
    }
    lines.push("", "## References");
    for (const signal of processedSignals) {
      lines.push(`- ${signal.reference_ids.join(", ")}`);
    }
    return `${lines.join("\n")}\n`;
  }
}

export class CustomSourceProvider extends BaseMockSourceProvider {}
