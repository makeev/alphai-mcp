# AI agent installation guide

AlphaAI is a hosted remote MCP server. There is nothing to download, build, or run
locally. Do not clone this repository to install the server; the repository only
documents it.

## Connection details

- Endpoint: `https://mcp.alphai.io/mcp`
- Transport: Streamable HTTP
- Auth: OAuth 2.1 with Dynamic Client Registration and PKCE. The MCP client opens a
  browser window for login on first connect. There is no API key, token, or
  environment variable to configure.

## Configuration

For JSON-config clients (Cline, Cursor and similar), add the server to the MCP
settings file:

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

Some clients name the streamable HTTP type differently (for example `streamableHttp`).
If `http` is rejected, use the client's streamable HTTP variant with the same URL.

Claude Code:

```bash
claude mcp add --transport http alphai https://mcp.alphai.io/mcp
```

VS Code Copilot (`.vscode/mcp.json`) uses `servers` instead of `mcpServers` with the
same entry shape.

## Verify the installation

After the OAuth login completes, call `alphai_trending` with default arguments. A JSON
list of scored news stories confirms the connection works end to end.

## Limits and notes

- Free tier: 20 requests per minute, 100 requests per day, no card required.
- All tools are read-only except `alphai_alerts_*`, which manage only the caller's own
  alert subscriptions and require a Basic or Pro plan.
- Developer docs: https://alphai.io/developers
