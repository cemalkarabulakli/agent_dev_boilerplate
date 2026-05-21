import { BaseMockSourceProvider } from "./custom_source_provider";

export class WebSearchSourceProvider extends BaseMockSourceProvider {
  constructor() {
    super("web_search", "search", "en", "source_discovery");
  }
}

