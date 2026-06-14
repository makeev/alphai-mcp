"""Introspection build of the AlphaAI MCP server (stdio).

The canonical AlphaAI MCP server is **hosted** at https://mcp.alphai.io/mcp
(Streamable HTTP, OAuth 2.1). This module is a small, dependency-light stdio
build that declares the *same 11 tools* — identical names, parameter schemas,
descriptions and behavior annotations as the live server — so MCP directories
(e.g. Glama) can start it and read the tool catalog via ``tools/list`` without
going through OAuth.

The tool **handlers here do not execute** — they return a short notice pointing
at the hosted endpoint, because the real data lives behind the hosted server.
To actually call these tools, connect to https://mcp.alphai.io/mcp over OAuth
(``claude mcp add --transport http alphai https://mcp.alphai.io/mcp``).
"""

from datetime import datetime
from enum import Enum
from typing import Annotated, Literal

from fastmcp import FastMCP
from pydantic import Field


class NewsCategory(str, Enum):
    earnings = "earnings"
    mergers_acquisitions = "mergers_acquisitions"
    regulation = "regulation"
    macro_economy = "macro_economy"
    sector_analysis = "sector_analysis"
    market_movers = "market_movers"
    technology = "technology"
    commodities = "commodities"
    crypto = "crypto"
    ipo = "ipo"
    geopolitics = "geopolitics"
    insider = "insider"
    corporate_actions = "corporate_actions"
    other = "other"


_HOSTED = (
    "AlphaAI runs as a hosted MCP server at https://mcp.alphai.io/mcp. This "
    "local build exists only so MCP directories can introspect the tool catalog; "
    "connect to the hosted endpoint over OAuth to actually run this tool "
    "(claude mcp add --transport http alphai https://mcp.alphai.io/mcp). "
    "Docs: https://alphai.io/mcp"
)

mcp = FastMCP(name="alphai")


@mcp.tool(
    name="alphai_news_search",
    description=(
        "Search AlphaAI's enriched financial news feed. Filter by free-text "
        "query (tokens are AND-matched across title and summary), ticker "
        "symbols, category, date range, and minimum relevance score (1-10). "
        "Results are paginated with an opaque cursor. Set collapse_stories=true "
        "to get one row per story instead of every syndicated reprint, with a "
        "sources_count corroboration signal."
    ),
    annotations={
        "title": "Search financial news",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def alphai_news_search(
    q: Annotated[str | None, Field(description="Free-text query; tokens AND-matched in title/summary.")] = None,
    tickers: Annotated[list[str] | None, Field(description="Restrict to news mentioning these tickers.")] = None,
    category: Annotated[NewsCategory | None, Field(description="Restrict to one news category.")] = None,
    from_date: Annotated[datetime | None, Field(description="News on/after this ISO time (UTC if naive).")] = None,
    to_date: Annotated[datetime | None, Field(description="News on/before this ISO time (UTC if naive).")] = None,
    min_relevance: Annotated[int, Field(ge=1, le=10, description="Minimum AI relevance score, 1-10.")] = 6,
    page_size: Annotated[int, Field(ge=1, le=50, description="Items/page. 10 Basic / 50 Pro (tools.bulk).")] = 10,
    cursor: Annotated[str | None, Field(description="Opaque cursor from a prior next_cursor.")] = None,
    collapse_stories: Annotated[
        bool,
        Field(
            description=(
                "Collapse syndicated reprints to one representative per story and "
                "populate story_id/sources_count/sources (default false)."
            )
        ),
    ] = False,
) -> str:
    return _HOSTED


@mcp.tool(
    name="alphai_ticker_news",
    description=(
        "Latest news for a single ticker (e.g. 'AAPL'). Cursor-paginated; "
        "returns the same shape as alphai_news_search. Insider news (SEC Form 4 "
        "trades + 13F ownership moves) for the ticker is included by default — "
        "pass include_insider=false for a pure non-insider feed. Set "
        "collapse_stories=true to get one row per story instead of every "
        "syndicated reprint. Sets unknown_ticker=true when the symbol isn't a "
        "recognized active ticker."
    ),
    annotations={
        "title": "Ticker news feed",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def alphai_ticker_news(
    ticker: Annotated[str, Field(description="Ticker symbol, e.g. 'AAPL'.")],
    include_insider: Annotated[bool, Field(description="Include insider/13F ownership news; default true.")] = True,
    page_size: Annotated[int, Field(ge=1, le=50, description="Items/page. 10 Basic / 50 Pro (tools.bulk).")] = 10,
    cursor: Annotated[str | None, Field(description="Opaque cursor from a prior next_cursor.")] = None,
    collapse_stories: Annotated[
        bool,
        Field(
            description=(
                "Collapse syndicated reprints to one representative per story and "
                "populate story_id/sources_count/sources (default false)."
            )
        ),
    ] = False,
) -> str:
    return _HOSTED


@mcp.tool(
    name="alphai_trending",
    description=(
        "Top news from the last 48h ranked by AI-assigned relevance. Use this "
        "when the user asks 'what's moving' / 'what's the big story'. Lower "
        "min_relevance to surface weaker movers. Syndicated reprints of one "
        "story are collapsed to a single representative by default "
        "(dedupe=false to keep all)."
    ),
    annotations={
        "title": "Trending news (48h)",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def alphai_trending(
    limit: Annotated[int, Field(ge=1, le=50, description="Stories. 10 Basic / 50 Pro (tools.bulk).")] = 10,
    min_relevance: Annotated[int, Field(ge=1, le=10, description="Min AI relevance 1-10; default 8.")] = 8,
    dedupe: Annotated[bool, Field(description="Collapse syndicated reprints by story (default true).")] = True,
) -> str:
    return _HOSTED


@mcp.tool(
    name="alphai_actionable_now",
    description=(
        "Breaking, decision-grade news from the last few hours. The primary "
        "filter is the enricher's actionability score, and the gate is strict: "
        "by default only actionability='high' (a concrete trading decision to "
        "act on TODAY — fresh guidance cut, halted trading, breaking M&A, "
        "surprise print) qualifies. Big-but-not-urgent stories scored 'medium' "
        "(shape a position over days/weeks) never appear at the default floor "
        "no matter how high their novelty — pass min_actionability='medium' to "
        "include them, or use alphai_trending / alphai_ticker_news for the "
        "broader tape. An empty list outside US market hours (nights, "
        "weekends) is expected — it means no high-actionability prints in the "
        "window, not an error; widen hours or min_actionability before "
        "concluding nothing happened. min_novelty is a secondary threshold "
        "that drops post-event recaps of already-public stories. Ordered "
        "novelty-first; syndicated reprints collapsed by story (dedupe=false "
        "to keep all)."
    ),
    annotations={
        "title": "Actionable-now feed",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def alphai_actionable_now(
    limit: Annotated[int, Field(ge=1, le=50, description="Stories. 10 Basic / 50 Pro (tools.bulk).")] = 10,
    hours: Annotated[int, Field(ge=1, le=48, description="Look-back window in hours; default 6.")] = 6,
    min_novelty: Annotated[int, Field(ge=1, le=10, description="Min information_novelty 1-10; default 7.")] = 7,
    min_actionability: Annotated[
        Literal["high", "medium"],
        Field(
            description=(
                "Actionability floor. 'high' (default) = only act-today items; "
                "'medium' also includes stories that shape a position over days/weeks."
            )
        ),
    ] = "high",
    dedupe: Annotated[bool, Field(description="Collapse syndicated reprints by story (default true).")] = True,
) -> str:
    return _HOSTED


@mcp.tool(
    name="alphai_insider_news",
    description=(
        "Ownership-change news: SEC Form 4 insider trades (company officers, "
        "directors and 10% owners buying or selling their own stock) plus 13F "
        "institutional ownership moves (funds and foundations increasing or "
        "trimming stakes). Optionally filter by ticker and date range. "
        "Cursor-paginated; same shape as alphai_news_search. Roughly equivalent "
        "to alphai_news_search(category='insider'), exposed as a dedicated tool. "
        "Sets unknown_ticker=true when a ticker filter isn't a recognized active "
        "symbol."
    ),
    annotations={
        "title": "Insider & ownership news",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def alphai_insider_news(
    ticker: Annotated[str | None, Field(description="Restrict to one ticker, e.g. 'AAPL'.")] = None,
    from_date: Annotated[datetime | None, Field(description="On/after this ISO time (UTC if naive).")] = None,
    to_date: Annotated[datetime | None, Field(description="On/before this ISO time (UTC if naive).")] = None,
    min_relevance: Annotated[int, Field(ge=1, le=10, description="Minimum AI relevance score, 1-10.")] = 6,
    page_size: Annotated[int, Field(ge=1, le=50, description="Items/page. 10 Basic / 50 Pro (tools.bulk).")] = 10,
    cursor: Annotated[str | None, Field(description="Opaque cursor from a prior next_cursor.")] = None,
) -> str:
    return _HOSTED


@mcp.tool(
    name="alphai_pair_analysis",
    description=(
        "Compare two tickers (e.g. NVDA and AMD). Returns news naming BOTH "
        "companies — where the cross-ticker read-across lives (a peer's print "
        "resetting the other's setup, a shared supplier/customer) — plus each "
        "ticker's own recent news for context. Any symbol that isn't a "
        "recognized active ticker is listed in unknown_tickers and contributes "
        "no rows."
    ),
    annotations={
        "title": "Two-ticker read-across",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def alphai_pair_analysis(
    ticker_a: Annotated[str, Field(description="First ticker, e.g. 'NVDA'.")],
    ticker_b: Annotated[str, Field(description="Second ticker, e.g. 'AMD'.")],
    min_relevance: Annotated[int, Field(ge=1, le=10, description="Minimum AI relevance score, 1-10.")] = 6,
    limit: Annotated[int, Field(ge=1, le=10, description="Max rows per list (both / each ticker).")] = 5,
) -> str:
    return _HOSTED


@mcp.tool(
    name="alphai_article",
    description=(
        "Fetch a single article (with full enrichment: ticker analysis, "
        "context, key entities) by its uid. The full article body is "
        "intentionally not served (copyright) — this is the canonical "
        "single-article lookup, not a fuller view. Raises not_found for an "
        "unknown uid."
    ),
    annotations={
        "title": "Fetch article by uid",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def alphai_article(
    uid: Annotated[str, Field(description="The article uid from any feed response.")],
) -> str:
    return _HOSTED


@mcp.tool(
    name="alphai_tickers",
    description=(
        "List supported stock and ETF tickers. Optionally filter by query "
        "(prefix on ticker, substring on name) or by sector."
    ),
    annotations={
        "title": "List supported tickers",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def alphai_tickers(
    q: Annotated[str | None, Field(description="Prefix match on ticker, substring on name.")] = None,
    sector: Annotated[str | None, Field(description="Filter by sector (case-insensitive).")] = None,
    limit: Annotated[int, Field(ge=1, le=500, description="Max rows to return.")] = 100,
    offset: Annotated[int, Field(ge=0, description="Pagination offset.")] = 0,
) -> str:
    return _HOSTED


@mcp.tool(
    name="alphai_alerts_list",
    description=(
        "List the caller's active ticker news-alert subscriptions, "
        "including per-subscription filters (category whitelist, minimum "
        "relevance score, delivery mode)."
    ),
    annotations={
        "title": "List my alert subscriptions",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def alphai_alerts_list() -> str:
    return _HOSTED


@mcp.tool(
    name="alphai_alerts_subscribe",
    description=(
        "Subscribe the caller to ticker news alerts. Optional category_filter "
        "(e.g. ['earnings','insider']) restricts which categories trigger; "
        "min_relevance_score raises the threshold. This is a partial update: "
        "omitting either field on an existing subscription preserves its "
        "current value, and a brand-new subscription defaults min_relevance_score "
        "to 6. Raises tier_not_paid / unknown_ticker / limit_reached."
    ),
    annotations={
        "title": "Subscribe to ticker alerts",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def alphai_alerts_subscribe(
    ticker: Annotated[str, Field(description="Ticker to subscribe to (active symbol).")],
    category_filter: Annotated[
        list[NewsCategory] | None,
        Field(description="Categories that trigger alerts."),
    ] = None,
    min_relevance_score: Annotated[
        int | None, Field(ge=0, le=10, description="Min relevance to alert on.")
    ] = None,
) -> str:
    return _HOSTED


@mcp.tool(
    name="alphai_alerts_unsubscribe",
    description=(
        "Soft-disable the caller's news-alert subscription for the given "
        "ticker. Idempotent — returns {removed: false} if the alert was "
        "already inactive. Raises unknown_ticker for an unrecognized symbol."
    ),
    annotations={
        "title": "Unsubscribe from ticker alerts",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def alphai_alerts_unsubscribe(
    ticker: Annotated[str, Field(description="Ticker to unsubscribe from.")],
) -> str:
    return _HOSTED


if __name__ == "__main__":
    mcp.run()
