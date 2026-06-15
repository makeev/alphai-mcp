# AlphaAI MCP server

[![alphai-mcp MCP server](https://glama.ai/mcp/servers/makeev/alphai-mcp/badges/score.svg)](https://glama.ai/mcp/servers/makeev/alphai-mcp)

**Real-time, AI-enriched financial news for AI agents and trading bots** — over the
[Model Context Protocol](https://modelcontextprotocol.io). Hosted at
**`mcp.alphai.io`**, no install, OAuth (no API key to paste), free tier 100 calls/hour.

Every story is enriched with **per-ticker analysis**, a **category** (14 buckets), and a
**1–10 relevance score**, so an agent can filter to what actually matters before spending
a reasoning token.

> This repo is the public home of the **hosted** AlphaAI MCP server (the listing you'll
> find on [Smithery](https://smithery.ai/servers/mihail-makeev/alphai-news),
> [Glama](https://glama.ai/mcp/servers/makeev/alphai-mcp), and the MCP Registry). The product is [AlphaAI](https://alphai.io) — a financial-news
> platform built for AI agents.

## Connect

The server speaks **Streamable HTTP** at `https://mcp.alphai.io/mcp`. Add it to any
OAuth-capable MCP client. Claude Code:

```bash
claude mcp add --transport http alphai https://mcp.alphai.io/mcp
```

The first tool call opens a browser for **OAuth 2.1** — a login, no key to copy-paste.
ChatGPT, Claude Desktop / claude.ai, Cursor, VS Code, Windsurf and Gemini connect the
same way. Or use the one-click listing on
[Smithery](https://smithery.ai/servers/mihail-makeev/alphai-news).

### Other clients

| Client | Config |
|---|---|
| **Claude Desktop / claude.ai** | Settings → Connectors → Add custom connector → `https://mcp.alphai.io/mcp` |
| **Cursor** | `~/.cursor/mcp.json` → `{ "mcpServers": { "alphai": { "url": "https://mcp.alphai.io/mcp" } } }` |
| **Generic** | Streamable HTTP, URL `https://mcp.alphai.io/mcp`, OAuth 2.1 |

## Tools (11)

| Tool | What it does |
|---|---|
| `alphai_news_search` | Full-text + filtered news search (query, tickers, category, dates, relevance) |
| `alphai_ticker_news` | Latest news for one ticker (optionally incl. insider) |
| `alphai_trending` | Biggest stories of the last 48h by relevance |
| `alphai_actionable_now` | Breaking, decision-grade news (actionability + novelty gate) |
| `alphai_insider_news` | SEC Form 4 insider trades + 13F ownership moves as news |
| `alphai_pair_analysis` | Two-ticker read-across (news naming both companies) |
| `alphai_article` | Fetch a single article by `uid` |
| `alphai_tickers` | Discover supported stock / ETF tickers |
| `alphai_alerts_list` / `_subscribe` / `_unsubscribe` | Manage your own ticker alert subscriptions *(Basic/Pro)* |

All tools are **read-only** except the `alphai_alerts_*` writes, which only ever touch the
caller's own subscriptions. Full schemas, params and defaults are advertised by the server
(annotations included) and documented at [alphai.io/mcp](https://alphai.io/mcp).

## Tiers

| | Free | Basic | Pro |
|---|---|---|---|
| Price | $0 (no card) | $2.99/mo | $9.99/mo |
| Rate limit | 100 / hour | 1,000 / hour | 10,000 / hour |
| Alert tools | — | ✓ | ✓ |
| Page size | 10 | 10 | up to 50 (bulk) |

## Ready-made Claude Code skills

Drop-in skills that drive these tools (stock brief, market pulse, insider radar,
peer read-across, manage alerts): **[makeev/alphai-claude-skills](https://github.com/makeev/alphai-claude-skills)**.

## Links

- **Playground & docs** — https://alphai.io/mcp
- **REST API & SDKs** (Python + TypeScript) — https://alphai.io/developers
- **Smithery listing** — https://smithery.ai/servers/mihail-makeev/alphai-news
- **Glama listing** — https://glama.ai/mcp/servers/makeev/alphai-mcp
- **Changelog** — https://alphai.io/changelog

## Notes

- This is a **hosted** server — to *use* it, connect to `https://mcp.alphai.io/mcp`; there
  is nothing to self-host. The product source lives in the AlphaAI backend; this repo is the
  catalog home + `server.json` manifest.
- `glama_server.py` + `Dockerfile` are an **introspection build**: a tiny stdio server that
  declares the same 11 tools (identical names, schemas, descriptions, annotations) so MCP
  directories can read the tool catalog without OAuth. Its handlers don't run the queries —
  they point back at the hosted endpoint, where the real data and auth live.
- News, not advice. The tools summarize reporting; they don't give buy/sell calls.
- `raw_text` (full article bodies) is never served — copyright. Responses carry titles,
  AI summaries, per-ticker analysis, categories and relevance scores.

MIT licensed. Built by [AlphaAI](https://alphai.io).
