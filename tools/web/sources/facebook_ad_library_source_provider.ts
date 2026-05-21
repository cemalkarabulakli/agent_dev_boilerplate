import { BaseMockSourceProvider } from "./custom_source_provider";

export class FacebookAdLibrarySourceProvider extends BaseMockSourceProvider {
  constructor() {
    super("facebook_ad_library", "ad_library", "en", "ad_angle");
  }
}

