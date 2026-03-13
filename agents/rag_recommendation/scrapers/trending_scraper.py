"""
Trending Content Scraper

Scrapes trending AI agents & agentic AI content from 6 live sources:
- arXiv (cs.AI, cs.MA, cs.CL)
- HackerNews (Algolia API)
- Reddit (public JSON API)
- GitHub Trending
- AI Lab Blogs (RSS feeds)
- HuggingFace Daily Papers
"""

import asyncio
import logging
import hashlib
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import feedparser
import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class TrendingItem:
    """Normalized trending content item from any source."""
    title: str
    url: str
    source: str                     # e.g. "arxiv", "hackernews", "reddit"
    summary: str = ""
    tags: List[str] = field(default_factory=list)
    score: float = 0.0              # engagement / trending score
    published_at: str = ""          # ISO timestamp
    authors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    item_id: str = ""               # deterministic hash

    def __post_init__(self):
        if not self.item_id:
            self.item_id = hashlib.md5(
                f"{self.source}:{self.url}".encode()
            ).hexdigest()[:12]

    def to_dict(self) -> dict:
        return asdict(self)

    @property
    def text_for_embedding(self) -> str:
        """Combined text used for vector embedding."""
        parts = [self.title]
        if self.summary:
            parts.append(self.summary[:500])
        if self.tags:
            parts.append(" ".join(self.tags))
        return " | ".join(parts)


# ---------------------------------------------------------------------------
# Keyword filters
# ---------------------------------------------------------------------------

AGENT_KEYWORDS = [
    "ai agent", "agentic ai", "agentic", "multi-agent", "multiagent",
    "autonomous agent", "llm agent", "agent framework", "tool use",
    "function calling", "mcp", "a]gent protocol",
    "rag", "retrieval augmented", "chain of thought",
    "reasoning", "planning agent", "agent memory",
    "autogen", "crewai", "langchain", "langgraph",
    "openai agents", "anthropic claude", "google adk",
    "agent orchestration", "agent workflow",
    "computer use", "browser agent", "code agent",
]

def _matches_agent_topic(text: str) -> bool:
    """Check if text is related to AI agents / agentic AI."""
    lower = text.lower()
    return any(kw in lower for kw in AGENT_KEYWORDS)


# ---------------------------------------------------------------------------
# Scraper class
# ---------------------------------------------------------------------------

class TrendingScraper:
    """
    Scrapes trending AI-agent content from multiple sources.

    Usage:
        scraper = TrendingScraper()
        items = await scraper.scrape_all()
    """

    CACHE_TTL = 1800  # 30 min

    def __init__(self, timeout: float = 20.0):
        self._timeout = timeout
        self._cache: Dict[str, Any] = {}

    # -- public API ---------------------------------------------------------

    async def scrape_all(self, filter_agents: bool = True) -> List[TrendingItem]:
        """Scrape all sources in parallel and return unified list."""
        results = await asyncio.gather(
            self.scrape_arxiv(),
            self.scrape_hackernews(),
            self.scrape_reddit(),
            self.scrape_github_trending(),
            self.scrape_ai_blogs(),
            self.scrape_huggingface(),
            return_exceptions=True,
        )

        items: List[TrendingItem] = []
        source_names = [
            "arxiv", "hackernews", "reddit",
            "github", "ai_blogs", "huggingface",
        ]
        for name, result in zip(source_names, results):
            if isinstance(result, Exception):
                logger.warning(f"Scraper {name} failed: {result}")
                continue
            items.extend(result)

        if filter_agents:
            items = [i for i in items if _matches_agent_topic(i.text_for_embedding)]

        logger.info(f"Scraped {len(items)} total items (filtered={filter_agents})")
        return items

    # -- arXiv --------------------------------------------------------------

    async def scrape_arxiv(self, max_results: int = 40) -> List[TrendingItem]:
        """Scrape recent arXiv papers via the Atom API."""
        cached = self._from_cache("arxiv")
        if cached is not None:
            return cached

        query = (
            "cat:cs.AI+OR+cat:cs.MA+OR+cat:cs.CL"
            "+AND+"
            "(all:agent+OR+all:agentic+OR+all:multi-agent+OR+all:autonomous+agent)"
        )
        url = (
            f"http://export.arxiv.org/api/query?"
            f"search_query={query}&start=0&max_results={max_results}"
            f"&sortBy=submittedDate&sortOrder=descending"
        )

        items: List[TrendingItem] = []
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(url)
                resp.raise_for_status()

            feed = feedparser.parse(resp.text)
            for entry in feed.entries:
                authors = [a.get("name", "") for a in entry.get("authors", [])]
                categories = [t["term"] for t in entry.get("tags", [])]
                items.append(TrendingItem(
                    title=entry.get("title", "").replace("\n", " ").strip(),
                    url=entry.get("link", ""),
                    source="arxiv",
                    summary=entry.get("summary", "").replace("\n", " ").strip()[:600],
                    tags=categories[:5],
                    score=0.7,  # base score for academic papers
                    published_at=entry.get("published", ""),
                    authors=authors,
                    metadata={"arxiv_id": entry.get("id", "").split("/abs/")[-1]},
                ))
        except Exception as e:
            logger.error(f"arXiv scrape error: {e}")

        self._to_cache("arxiv", items)
        return items

    # -- HackerNews ---------------------------------------------------------

    async def scrape_hackernews(self, num_stories: int = 30) -> List[TrendingItem]:
        """Scrape HackerNews via Algolia search API (free, no key)."""
        cached = self._from_cache("hackernews")
        if cached is not None:
            return cached

        query = "AI agent OR agentic AI OR multi-agent OR LLM agent"
        url = (
            f"https://hn.algolia.com/api/v1/search_by_date?"
            f"query={query}&tags=story&hitsPerPage={num_stories}"
        )

        items: List[TrendingItem] = []
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(url)
                resp.raise_for_status()
                data = resp.json()

            for hit in data.get("hits", []):
                points = hit.get("points") or 0
                comments = hit.get("num_comments") or 0
                story_url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}"
                items.append(TrendingItem(
                    title=hit.get("title", ""),
                    url=story_url,
                    source="hackernews",
                    summary=f"{points} points, {comments} comments on HN",
                    tags=["hackernews"],
                    score=min(1.0, points / 300),  # normalize: 300 pts = 1.0
                    published_at=hit.get("created_at", ""),
                    authors=[hit.get("author", "")],
                    metadata={"hn_id": hit.get("objectID", ""), "points": points, "comments": comments},
                ))
        except Exception as e:
            logger.error(f"HackerNews scrape error: {e}")

        self._to_cache("hackernews", items)
        return items

    # -- Reddit -------------------------------------------------------------

    async def scrape_reddit(self, limit: int = 25) -> List[TrendingItem]:
        """Scrape Reddit hot posts from AI-related subreddits."""
        cached = self._from_cache("reddit")
        if cached is not None:
            return cached

        subreddits = ["MachineLearning", "artificial", "LangChain", "LocalLLaMA"]
        items: List[TrendingItem] = []

        headers = {"User-Agent": "TrendingAI-Agent-Scraper/1.0"}

        for sub in subreddits:
            url = f"https://www.reddit.com/r/{sub}/hot.json?limit={limit}"
            try:
                async with httpx.AsyncClient(timeout=self._timeout, headers=headers) as client:
                    resp = await client.get(url)
                    if resp.status_code != 200:
                        continue
                    data = resp.json()

                for post in data.get("data", {}).get("children", []):
                    d = post.get("data", {})
                    ups = d.get("ups", 0)
                    items.append(TrendingItem(
                        title=d.get("title", ""),
                        url=f"https://reddit.com{d.get('permalink', '')}",
                        source="reddit",
                        summary=d.get("selftext", "")[:400],
                        tags=[f"r/{sub}"],
                        score=min(1.0, ups / 500),
                        published_at=datetime.fromtimestamp(d.get("created_utc", 0)).isoformat(),
                        authors=[d.get("author", "")],
                        metadata={"subreddit": sub, "ups": ups, "num_comments": d.get("num_comments", 0)},
                    ))
            except Exception as e:
                logger.warning(f"Reddit r/{sub} scrape error: {e}")

        self._to_cache("reddit", items)
        return items

    # -- GitHub Trending ----------------------------------------------------

    async def scrape_github_trending(self) -> List[TrendingItem]:
        """Scrape GitHub trending repos (HTML scrape — no API key needed)."""
        cached = self._from_cache("github")
        if cached is not None:
            return cached

        url = "https://github.com/trending?since=weekly&spoken_language_code=en"
        items: List[TrendingItem] = []

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(url)
                resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")
            for article in soup.select("article.Box-row")[:30]:
                h2 = article.select_one("h2 a")
                if not h2:
                    continue
                repo_path = h2.get("href", "").strip("/")
                name = repo_path.split("/")[-1] if "/" in repo_path else repo_path

                desc_p = article.select_one("p")
                description = desc_p.get_text(strip=True) if desc_p else ""

                # Stars this period
                stars_span = article.select_one("span.d-inline-block.float-sm-right")
                stars_text = stars_span.get_text(strip=True) if stars_span else "0"
                stars_num = int(re.sub(r"[^\d]", "", stars_text) or "0")

                lang_span = article.select_one("span[itemprop='programmingLanguage']")
                lang = lang_span.get_text(strip=True) if lang_span else ""

                items.append(TrendingItem(
                    title=f"{repo_path}",
                    url=f"https://github.com/{repo_path}",
                    source="github",
                    summary=description,
                    tags=["github", lang] if lang else ["github"],
                    score=min(1.0, stars_num / 1000),
                    published_at=datetime.now().isoformat(),
                    authors=[repo_path.split("/")[0]] if "/" in repo_path else [],
                    metadata={"stars_period": stars_num, "language": lang},
                ))
        except Exception as e:
            logger.error(f"GitHub trending scrape error: {e}")

        self._to_cache("github", items)
        return items

    # -- AI Lab Blogs (RSS) -------------------------------------------------

    async def scrape_ai_blogs(self) -> List[TrendingItem]:
        """Scrape AI lab blogs via RSS feeds."""
        cached = self._from_cache("ai_blogs")
        if cached is not None:
            return cached

        feeds = {
            "OpenAI": "https://openai.com/blog/rss.xml",
            "Google AI": "https://blog.google/technology/ai/rss/",
            "Meta AI": "https://ai.meta.com/blog/rss/",
            "Hugging Face": "https://huggingface.co/blog/feed.xml",
            "LangChain": "https://blog.langchain.dev/rss/",
        }

        items: List[TrendingItem] = []

        async def _fetch_feed(name: str, feed_url: str):
            try:
                async with httpx.AsyncClient(timeout=self._timeout, follow_redirects=True) as client:
                    resp = await client.get(feed_url)
                    if resp.status_code != 200:
                        return []
                feed = feedparser.parse(resp.text)
                result = []
                for entry in feed.entries[:10]:
                    # Clean HTML from summary
                    raw_summary = entry.get("summary", "")
                    clean_summary = BeautifulSoup(raw_summary, "html.parser").get_text()[:400]
                    result.append(TrendingItem(
                        title=entry.get("title", ""),
                        url=entry.get("link", ""),
                        source="ai_blogs",
                        summary=clean_summary,
                        tags=[name.lower().replace(" ", "_"), "blog"],
                        score=0.75,  # blogs from major labs are high-value
                        published_at=entry.get("published", ""),
                        authors=[name],
                        metadata={"blog_source": name},
                    ))
                return result
            except Exception as e:
                logger.warning(f"Blog feed {name} error: {e}")
                return []

        results = await asyncio.gather(*[
            _fetch_feed(name, url) for name, url in feeds.items()
        ])
        for batch in results:
            items.extend(batch)

        self._to_cache("ai_blogs", items)
        return items

    # -- HuggingFace Daily Papers -------------------------------------------

    async def scrape_huggingface(self) -> List[TrendingItem]:
        """Scrape HuggingFace daily papers page."""
        cached = self._from_cache("huggingface")
        if cached is not None:
            return cached

        url = "https://huggingface.co/papers"
        items: List[TrendingItem] = []

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(url)
                resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")

            # HF papers page uses article tags or specific classes
            for article in soup.select("article, div.paper-card, a[href*='/papers/']")[:30]:
                # Try to extract title and link
                link_el = article if article.name == "a" else article.select_one("a[href*='/papers/']")
                if not link_el:
                    continue

                href = link_el.get("href", "")
                if not href.startswith("/papers/"):
                    continue

                title_el = link_el.select_one("h3") or link_el
                title_text = title_el.get_text(strip=True)
                if not title_text or len(title_text) < 10:
                    continue

                # Extract upvotes if present
                vote_el = article.select_one("[class*='vote'], [class*='like']")
                votes = 0
                if vote_el:
                    vote_text = re.sub(r"[^\d]", "", vote_el.get_text())
                    votes = int(vote_text) if vote_text else 0

                items.append(TrendingItem(
                    title=title_text,
                    url=f"https://huggingface.co{href}",
                    source="huggingface",
                    summary="",
                    tags=["huggingface", "papers"],
                    score=min(1.0, votes / 100) if votes else 0.6,
                    published_at=datetime.now().isoformat(),
                    metadata={"hf_votes": votes},
                ))
        except Exception as e:
            logger.error(f"HuggingFace scrape error: {e}")

        self._to_cache("huggingface", items)
        return items

    # -- cache helpers ------------------------------------------------------

    def _from_cache(self, key: str) -> Optional[List[TrendingItem]]:
        if key in self._cache:
            entry = self._cache[key]
            age = (datetime.now() - entry["ts"]).total_seconds()
            if age < self.CACHE_TTL:
                return entry["data"]
            del self._cache[key]
        return None

    def _to_cache(self, key: str, data: List[TrendingItem]):
        self._cache[key] = {"data": data, "ts": datetime.now()}
