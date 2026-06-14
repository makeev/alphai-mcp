# Introspection build of the AlphaAI MCP server.
#
# The canonical server is HOSTED at https://mcp.alphai.io/mcp (Streamable HTTP,
# OAuth 2.1). This image runs a small stdio build that declares the same 11
# tools so MCP directories (e.g. Glama) can read the tool catalog via tools/list
# without OAuth. The tool handlers point back at the hosted endpoint — see
# glama_server.py and README.md.
FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir "fastmcp>=3,<4"

COPY glama_server.py .

# Speaks MCP over stdio.
CMD ["python", "glama_server.py"]
