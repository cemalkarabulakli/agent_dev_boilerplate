import type { BrowserArtifactOptions, BrowserAutomationTool } from "../interfaces/browser_automation_tool";
import type { BrowserResult } from "../types/browser_result";

export class MockBrowserProvider implements BrowserAutomationTool {
  private currentUrl = "mock://browser/not-opened";

  async open(url: string): Promise<BrowserResult> {
    this.currentUrl = url;
    return this.result("open");
  }

  async click(selector: string): Promise<BrowserResult> {
    return this.result("click", { selector });
  }

  async type(selector: string, text: string): Promise<BrowserResult> {
    return this.result("type", { selector, textLength: text.length });
  }

  async screenshot(options: BrowserArtifactOptions = {}): Promise<BrowserResult> {
    return this.result("screenshot", options);
  }

  async pdf(options: BrowserArtifactOptions = {}): Promise<BrowserResult> {
    return this.result("pdf", options);
  }

  async getContent(): Promise<string> {
    return "Mock browser content. Configure Playwright for live browser automation.";
  }

  async getUrl(): Promise<string> {
    return this.currentUrl;
  }

  async close(): Promise<void> {
    this.currentUrl = "mock://browser/closed";
  }

  private result(action: string, metadata: Record<string, unknown> = {}): BrowserResult {
    return { url: this.currentUrl, action, ok: true, provider: "mock_browser", isMock: true, metadata };
  }
}

