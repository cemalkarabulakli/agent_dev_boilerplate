export interface BrowserResult {
  url: string;
  action: string;
  ok: boolean;
  content?: string;
  artifactPath?: string;
  provider: string;
  isMock: boolean;
  metadata?: Record<string, unknown>;
}

