import { QuoraSourceProvider } from "../sources/quora_source_provider";
import { BgMammaSourceProvider } from "../sources/bg_mamma_source_provider";
import { FacebookAdLibrarySourceProvider } from "../sources/facebook_ad_library_source_provider";
import { RedditSourceProvider } from "../sources/reddit_source_provider";
import { GoogleTrendsSourceProvider } from "../sources/google_trends_source_provider";
import { GitHubTrendsSourceProvider } from "../sources/github_trends_source_provider";
import { ClickBankSourceProvider } from "../sources/clickbank_source_provider";
import { YouTubeSourceProvider } from "../sources/youtube_source_provider";
import { WebSearchSourceProvider } from "../sources/web_search_source_provider";
import { CompetitorsSourceProvider } from "../sources/competitors_source_provider";
import { CustomSourceProvider } from "../sources/custom_source_provider";

export function createSourceTools(overrides: Record<string, string> = {}) {
  const tools = {
    quora: new QuoraSourceProvider(),
    bgMamma: new BgMammaSourceProvider(),
    facebookAdLibrary: new FacebookAdLibrarySourceProvider(),
    reddit: new RedditSourceProvider(),
    googleTrends: new GoogleTrendsSourceProvider(),
    githubTrends: new GitHubTrendsSourceProvider(),
    clickbank: new ClickBankSourceProvider(),
    youtube: new YouTubeSourceProvider(),
    webSearch: new WebSearchSourceProvider(),
    competitors: new CompetitorsSourceProvider(),
    custom: new CustomSourceProvider(),
  };
  return { ...tools, config: overrides };
}

