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

ADAPTERS = {
    "bg_mamma_adapter": BGMammaAdapter,
    "clickbank_adapter": ClickBankAdapter,
    "facebook_ad_library_adapter": FacebookAdLibraryAdapter,
    "github_trends_adapter": GitHubTrendsAdapter,
    "google_trends_adapter": GoogleTrendsAdapter,
    "quora_adapter": QuoraAdapter,
    "reddit_adapter": RedditAdapter,
    "web_search_adapter": WebSearchAdapter,
    "youtube_adapter": YouTubeAdapter,
}
