import { BaseMockSourceProvider } from "./custom_source_provider";

export class CompetitorsSourceProvider extends BaseMockSourceProvider {
  constructor() {
    super("competitors", "competitor_monitoring", "en", "competitor_signal");
  }
}

