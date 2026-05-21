import { BaseMockSourceProvider } from "./custom_source_provider";

export class ClickBankSourceProvider extends BaseMockSourceProvider {
  constructor() {
    super("clickbank", "marketplace", "en", "offer_pattern");
  }
}

