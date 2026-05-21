import { BaseMockSourceProvider } from "./custom_source_provider";

export class RedditSourceProvider extends BaseMockSourceProvider {
  constructor() {
    super("reddit", "community", "en", "raw_pain_language");
  }
}

