import { BaseMockSourceProvider } from "./custom_source_provider";

export class YouTubeSourceProvider extends BaseMockSourceProvider {
  constructor() {
    super("youtube", "video", "en", "content_angle");
  }
}

