# local-websearch-mcp

Small Python MCP server that provides two tools:

- `web_search`: search the public web through DuckDuckGo HTML results
- `web_fetch`: fetch a page and extract readable text

No API key is required.

## Requirements

- Linux server or workstation
- Python 3.10+
- Outbound internet access for:
  - `pip install`
  - web searches and page fetches at runtime

## Quick install

```bash
git clone <this-repo-url> local-websearch-mcp
cd local-websearch-mcp
chmod +x install.sh
./install.sh
```

That creates `.venv/`, installs the package, and runs a built-in health check.

## Manual install

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install .
local-websearch-mcp --self-test
```

## Run

```bash
.venv/bin/local-websearch-mcp
```

Or:

```bash
python -m local_websearch_mcp.server
```

## MCP client config

Use the installed executable directly:

```json
{
  "mcpServers": {
    "local-websearch": {
      "command": "/absolute/path/to/local-websearch-mcp/.venv/bin/local-websearch-mcp"
    }
  }
}
```

## Health check

```bash
.venv/bin/local-websearch-mcp --self-test
```

Expected output:

```json
{
  "server": "local-websearch",
  "status": "ok",
  "tools": ["web_search", "web_fetch"]
}
```

## Tools

- `web_search(query: str, max_results: int = 5)`
- `web_fetch(url: str, max_chars: int = 12000)`

## Local demo

```bash
python examples/simple_client.py
```

## Repo contents

- `src/local_websearch_mcp/`: MCP server and helpers
- `examples/`: local demo client
- `install.sh`: one-command local install

## Notes

- DuckDuckGo HTML markup can change, so selectors may need maintenance.
- This server uses direct HTTP requests. Respect site terms and robots policies.
