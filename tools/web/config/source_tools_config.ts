declare const process: { env?: Record<string, string | undefined> };

export interface SourceToolsConfig {
  mode: "mock" | "api" | "scrape" | "manual";
  providers: Record<string, string>;
}

export function loadSourceToolsConfig(env: Record<string, string | undefined> = process.env ?? {}): SourceToolsConfig {
  const mode = (env.RESEARCH_MODE as SourceToolsConfig["mode"]) || "mock";
  return {
    mode,
    providers: {
      quora: "quora_source_provider",
      bgMamma: "bg_mamma_source_provider",
      facebookAdLibrary: "facebook_ad_library_source_provider",
      reddit: "reddit_source_provider",
      googleTrends: "google_trends_source_provider",
      githubTrends: "github_trends_source_provider",
      clickbank: "clickbank_source_provider",
      youtube: "youtube_source_provider",
      webSearch: "web_search_source_provider",
      competitors: "competitors_source_provider",
    },
  };
}

