# AlphaAI MCP server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Official MCP Registry](https://img.shields.io/badge/MCP%20Registry-io.github.makeev%2Falphai--mcp-blue)](https://registry.modelcontextprotocol.io/v0/servers/io.github.makeev%2Falphai-mcp/versions/latest)
[![Smithery](https://img.shields.io/badge/Smithery-Listed-000000)](https://smithery.ai/servers/mihail-makeev/alphai-news)
[![mcp.so](https://img.shields.io/badge/mcp.so-Listed-1c1c1c)](https://mcp.so/server/alphai-news/makeev)
[![Glama](https://glama.ai/mcp/servers/makeev/alphai-mcp/badges/score.svg)](https://glama.ai/mcp/servers/makeev/alphai-mcp)
[![Mentioned in Awesome MCP Servers](https://awesome.re/mentioned-badge.svg)](https://github.com/punkpeye/awesome-mcp-servers)

**Real-time, AI-enriched financial news for AI agents and trading bots** — over the
[Model Context Protocol](https://modelcontextprotocol.io). Hosted at **`mcp.alphai.io`**,
no install, OAuth (no API key to paste), free tier 100 calls/day.

Every story is enriched with **per-ticker analysis**, a **category** (14 buckets), and a
**1–10 relevance score**, so an agent can filter to what actually matters before spending
a reasoning token.

> This repo is the public home + `server.json` manifest of the **hosted** AlphaAI MCP
> server (the listing on [Smithery](https://smithery.ai/servers/mihail-makeev/alphai-news),
> [Glama](https://glama.ai/mcp/servers/makeev/alphai-mcp),
> [mcp.so](https://mcp.so/server/alphai-news/makeev), the
> [MCP Registry](https://registry.modelcontextprotocol.io) and
> [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)). The product is
> [AlphaAI](https://alphai.io) — a financial-news platform built for AI agents. There is
> **nothing to self-host**: to use it, just connect to `https://mcp.alphai.io/mcp`.

## Connect

The server speaks **Streamable HTTP** at `https://mcp.alphai.io/mcp`. Add it to any
OAuth-capable MCP client. Claude Code:

```bash
claude mcp add --transport http alphai https://mcp.alphai.io/mcp
```

The first tool call opens a browser for **OAuth 2.1** (DCR + PKCE) — a login, no key to
copy-paste. ChatGPT, Claude Desktop / claude.ai, Cursor, VS Code, Windsurf and Gemini
connect the same way. Or use the one-click listing on
[Smithery](https://smithery.ai/servers/mihail-makeev/alphai-news).

### Other clients

| Client | Config |
|---|---|
| **Claude Desktop / claude.ai** | Settings → Connectors → Add custom connector → `https://mcp.alphai.io/mcp` |
| **Cursor** | `~/.cursor/mcp.json` → `{ "mcpServers": { "alphai": { "type": "http", "url": "https://mcp.alphai.io/mcp" } } }` |
| **VS Code Copilot** | `.vscode/mcp.json` → `{ "servers": { "alphai": { "type": "http", "url": "https://mcp.alphai.io/mcp" } } }` |
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
| `alphai_tickers` | Discover supported tickers — US stocks, ETFs, crypto & foreign listings |
| `alphai_alerts_list` / `_subscribe` / `_unsubscribe` | Manage your own ticker alert subscriptions *(Basic/Pro)* |

All tools are **read-only** except the `alphai_alerts_*` writes, which only ever touch the
caller's own subscriptions. Full schemas, params and defaults are advertised by the server
(annotations included) and documented at [alphai.io/mcp](https://alphai.io/mcp).

## Tiers

| | Free | Basic | Pro |
|---|---|---|---|
| Price | $0 (no card) | $2.99/mo | $9.99/mo |
| Rate limit — burst | 20 / min | 60 / min | 300 / min |
| Rate limit — daily | 100 / day | 10,000 / day | 100,000 / day |
| Alert tools | — | ✓ | ✓ |
| Page size | 10 | 10 | up to 50 (bulk) |

## Authentication

**OAuth 2.1** with [Dynamic Client Registration (RFC 7591)](https://datatracker.ietf.org/doc/html/rfc7591)
and [PKCE](https://datatracker.ietf.org/doc/html/rfc7636) per the
[MCP authorization spec](https://modelcontextprotocol.io/specification/authorization).
Compatible clients discover the OAuth metadata automatically — no manual API key setup.
Tool *discovery* (`tools/list`) is open; calling a tool requires the OAuth login.

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

MIT licensed. Built by [AlphaAI](https://alphai.io).
