import { BaseMockSourceProvider } from "./custom_source_provider";

export class QuoraSourceProvider extends BaseMockSourceProvider {
  constructor() {
    super("quora", "question_answer", "en", "customer_questions");
  }
}

