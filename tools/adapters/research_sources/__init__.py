"""Research source adapters."""

from tools.adapters.research_sources.bg_mamma_adapter import BGMammaAdapter
from tools.adapters.research_sources.clickbank_adapter import ClickBankAdapter
from tools.adapters.research_sources.facebook_ad_library_adapter import FacebookAdLibraryAdapter
from tools.adapters.research_sources.github_trends_adapter import GitHubTrendsAdapter
from tools.adapters.research_sources.google_trends_adapter import GoogleTrendsAdapter
from tools.adapters.research_sources.quora_adapter import QuoraAdapter
from tools.adapters.research_sources.reddit_adapter import RedditAdapter
from tools.adapters.research_sources.web_search_adapter import WebSearchAdapter
from tools.adapters.research_sources.youtube_adapter import YouTubeAdapter
from tools.adapters.research_sources.competitor_source_provider import CompetitorSourceProvider

ADAPTERS = {
    "bg_mamma_adapter": BGMammaAdapter,
    "bg_mamma_source_provider": BGMammaAdapter,
    "clickbank_adapter": ClickBankAdapter,
    "clickbank_source_provider": ClickBankAdapter,
    "competitor_source_provider": CompetitorSourceProvider,
    "facebook_ad_library_adapter": FacebookAdLibraryAdapter,
    "facebook_ad_library_source_provider": FacebookAdLibraryAdapter,
    "github_trends_adapter": GitHubTrendsAdapter,
    "github_trends_source_provider": GitHubTrendsAdapter,
    "google_trends_adapter": GoogleTrendsAdapter,
    "google_trends_source_provider": GoogleTrendsAdapter,
    "quora_adapter": QuoraAdapter,
    "quora_source_provider": QuoraAdapter,
    "reddit_adapter": RedditAdapter,
    "reddit_source_provider": RedditAdapter,
    "web_search_adapter": WebSearchAdapter,
    "web_search_source_provider": WebSearchAdapter,
    "youtube_adapter": YouTubeAdapter,
    "youtube_source_provider": YouTubeAdapter,
}
