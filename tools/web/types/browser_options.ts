export interface BrowserOptions {
  url?: string;
  selector?: string;
  outputPath?: string;
  waitMs?: number;
  fullPage?: boolean;
  format?: "pdf" | "png" | "jpeg";
  viewportWidth?: number;
  viewportHeight?: number;
}

export interface BrowserResult {
  url: string;
  action: string;
  ok: boolean;
  content?: string;
  artifactPath?: string;
  provider: string;
  isMock: boolean;
  retrievedAt: string;
  warnings?: string[];
  metadata?: Record<string, unknown>;
}
