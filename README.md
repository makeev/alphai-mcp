# AlphAI MCP server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Official MCP Registry](https://img.shields.io/badge/MCP%20Registry-io.github.makeev%2Falphai--mcp-blue)](https://registry.modelcontextprotocol.io/v0/servers/io.github.makeev%2Falphai-mcp/versions/latest)
[![Smithery](https://img.shields.io/badge/Smithery-Listed-000000)](https://smithery.ai/servers/mihail-makeev/alphai-news)
[![mcp.so](https://img.shields.io/badge/mcp.so-Listed-1c1c1c)](https://mcp.so/server/alphai-news/makeev)
[![Glama](https://glama.ai/mcp/connectors/io.github.makeev/alphai-mcp/badges/score.svg)](https://glama.ai/mcp/connectors/io.github.makeev/alphai-mcp)
[![Mentioned in Awesome MCP Servers](https://awesome.re/mentioned-badge.svg)](https://github.com/punkpeye/awesome-mcp-servers)

**A [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server for financial
news, stock market sentiment and SEC Form 4 insider trading data** — built for AI agents
and trading bots. Hosted at **`mcp.alphai.io`**, no install, OAuth (no API key to paste),
free tier 20 req/min and 100 req/day.

Every story is enriched with **per-ticker analysis**, a **category** (14 buckets), and a
**1–10 relevance score**, so an agent can filter to what actually matters before spending
a reasoning token.

> This repo is the public home + `server.json` manifest of the **hosted** AlphAI MCP
> server (the listing on [Smithery](https://smithery.ai/servers/mihail-makeev/alphai-news),
> [Glama](https://glama.ai/mcp/connectors/io.github.makeev/alphai-mcp),
> [mcp.so](https://mcp.so/server/alphai-news/makeev), the
> [MCP Registry](https://registry.modelcontextprotocol.io) and
> [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)). The product is
> [AlphAI](https://alphai.io) — a financial-news platform built for AI agents. There is
> **nothing to self-host**: to use it, just connect to `https://mcp.alphai.io/mcp`.

## Connect

The server speaks **Streamable HTTP** at `https://mcp.alphai.io/mcp`. Add it to any
OAuth-capable MCP client. Claude Code:

```bash
claude mcp add --transport http alphai https://mcp.alphai.io/mcp
```

Connecting opens a browser for **OAuth 2.1** (DCR + PKCE) — a login, no key to
copy-paste. ChatGPT, Claude Desktop / claude.ai, Cursor, VS Code, Windsurf and Gemini
connect the same way. Or use the one-click listing on
[Smithery](https://smithery.ai/servers/mihail-makeev/alphai-news).

JSON config clients (Cline, Cursor and similar):

```json
{
  "mcpServers": {
    "alphai": {
      "type": "http",
      "url": "https://mcp.alphai.io/mcp"
    }
  }
}
```

### Other clients

| Client | Config |
|---|---|
| **Claude Desktop / claude.ai** | Settings → Connectors → Add custom connector → `https://mcp.alphai.io/mcp` |
| **Cursor** | `~/.cursor/mcp.json` → `{ "mcpServers": { "alphai": { "type": "http", "url": "https://mcp.alphai.io/mcp" } } }` |
| **VS Code Copilot** | `.vscode/mcp.json` → `{ "servers": { "alphai": { "type": "http", "url": "https://mcp.alphai.io/mcp" } } }` |
| **Generic** | Streamable HTTP, URL `https://mcp.alphai.io/mcp`, OAuth 2.1 |

## Tools (18)

MCP Server URL: https://mcp.alphai.io/mcp

- `alphai_news_search` - Full-text + filtered news search (query, tickers, category, dates, relevance)
- `alphai_ticker_news` - Latest news for one ticker (optionally incl. insider)
- `alphai_trending` - Biggest stories of the last 48h by relevance
- `alphai_actionable_now` - Breaking, decision-grade news (actionability + novelty gate)
- `alphai_insider_news` - SEC Form 4 insider-trade news
- `alphai_pair_analysis` - Two-ticker read-across (news naming both companies)
- `alphai_article` - Fetch a single article by `uid` (adds a structured `earnings` read on SEC filings)
- `alphai_earnings` - AlphAI's filing-verified earnings reads per ticker, plus the next report date
- `alphai_calendar` - Scheduled macro releases (CPI, FOMC, jobless claims) with times and the coverage that followed
- `alphai_macro` - Macro-economy feed (prints, central banks, rates, FX, commodities)
- `alphai_tickers` - Discover supported tickers (US stocks, ETFs, crypto & foreign listings, incl. each one's `next_report_date`)
- `alphai_watchlist_brief` - Recent news and filing events for your saved watchlist, on every plan
- `alphai_radar` - News activity and tone across the market or your saved watchlist, with linked evidence, 4h/24h windows and snapshot-pinned pagination
- `search` / `fetch` - Citation-ready article discovery and retrieval for compatible research clients
- `alphai_alerts_list` / `alphai_alerts_subscribe` / `alphai_alerts_unsubscribe` - Manage your own ticker alert subscriptions *(Basic/Pro)*

All tools are **read-only** except the `alphai_alerts_*` writes, which only ever touch the
caller's own subscriptions. Full schemas, params and defaults are advertised by the server
(annotations included) and documented at [alphai.io/mcp](https://alphai.io/mcp).

## Tiers

| | Free | Basic | Pro |
|---|---|---|---|
| Price | $0 (no card) | $2.99/mo | $9.99/mo |
| Rate limit — burst | 20 / min | 60 / min | 150 / min |
| Rate limit — daily | 100 / day | 10,000 / day | 100,000 / day |
| Alert tools | — | ✓ | ✓ |
| News page size | up to 20 | up to 20 | up to 50 (bulk) |
| News archive | 30 days | 90 days | 180 days |
| Radar market + saved watchlist | ✓ | ✓ | ✓ |
| Radar added delay | 60 min | 15 min | None |

Radar refreshes each minute. Delays apply to the complete snapshot, including
supporting headlines; collection and enrichment add processing time. Its
descriptive beta scores are not predictions or confirmed alerts. Radar accepts
up to 100 rows per call on every plan, with no separate ticker allowance; saved
watchlists retain their existing limits (Free 10 companies, paid unlimited).

## Authentication

**OAuth 2.1** with [Dynamic Client Registration (RFC 7591)](https://datatracker.ietf.org/doc/html/rfc7591)
and [PKCE](https://datatracker.ietf.org/doc/html/rfc7636) per the
[MCP authorization spec](https://modelcontextprotocol.io/specification/authorization).
Compatible clients discover the OAuth metadata automatically — no manual API key setup.
Both tool discovery (`tools/list`) and calls require authentication. Headless
clients can use the same API key as the REST API in an `Authorization: Bearer
ak_live_…` header; never put a key in the URL. OAuth and API keys have tool parity.

## Ready-made Claude Code skills

Drop-in skills that drive these tools (stock brief, market pulse, insider radar,
peer read-across, manage alerts): **[makeev/alphai-claude-skills](https://github.com/makeev/alphai-claude-skills)**.

## Links

- **Playground & docs** — https://alphai.io/mcp
- **REST API & SDKs** (Python + TypeScript) — https://alphai.io/developers
- **Smithery listing** — https://smithery.ai/servers/mihail-makeev/alphai-news
- **Glama connector** — https://glama.ai/mcp/connectors/io.github.makeev/alphai-mcp
- **MCP Registry** — `io.github.makeev/alphai-mcp`
- **Changelog** — https://alphai.io/changelog

## Notes

- This is a **hosted** server — to *use* it, connect to `https://mcp.alphai.io/mcp`; there
  is nothing to self-host. This repo is the catalog home + `server.json` manifest.
- News, not advice. The tools summarize reporting; they don't give buy/sell calls.
- `raw_text` (full article bodies) is never served — copyright. Responses carry titles,
  AI summaries, per-ticker analysis, categories and relevance scores.

MIT licensed. Built by [AlphAI](https://alphai.io).
