import { BaseMockSourceProvider } from "./custom_source_provider";

export class GitHubTrendsSourceProvider extends BaseMockSourceProvider {
  constructor() {
    super("github_trends", "tool_trend", "en", "tool_opportunity");
  }
}

