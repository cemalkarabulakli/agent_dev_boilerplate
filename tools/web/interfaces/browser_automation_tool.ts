import type { BrowserResult } from "../types/browser_result";

export interface BrowserArtifactOptions {
  path?: string;
  fullPage?: boolean;
}

export interface BrowserAutomationTool {
  open(url: string): Promise<BrowserResult>;
  click(selector: string): Promise<BrowserResult>;
  type(selector: string, text: string): Promise<BrowserResult>;
  screenshot(options?: BrowserArtifactOptions): Promise<BrowserResult>;
  pdf(options?: BrowserArtifactOptions): Promise<BrowserResult>;
  getContent(): Promise<string>;
  getUrl(): Promise<string>;
  close(): Promise<void>;
}

