import { BaseMockSourceProvider } from "./custom_source_provider";

export class GoogleTrendsSourceProvider extends BaseMockSourceProvider {
  constructor() {
    super("google_trends", "trend", "en", "demand_trend");
  }
}

