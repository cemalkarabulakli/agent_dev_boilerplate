import { BaseMockSourceProvider } from "./custom_source_provider";

export class BgMammaSourceProvider extends BaseMockSourceProvider {
  constructor() {
    super("bg_mamma", "forum", "bg", "local_language_pain");
  }
}

