from __future__ import annotations

import argparse
import json

from mcp.server.fastmcp import FastMCP

from .fetch import fetch_page
from .search import search_web

mcp = FastMCP("local-websearch")


@mcp.tool()
def web_search(query: str, max_results: int = 5) -> dict:
    """Search the web directly using DuckDuckGo HTML results.

    Args:
        query: Search query text.
        max_results: Number of results to return (1-20).
    """
    results = search_web(query=query, max_results=max_results)
    return {"query": query, "results": results, "count": len(results)}


@mcp.tool()
def web_fetch(url: str, max_chars: int = 12000) -> dict:
    """Fetch and extract readable text content from a URL.

    Args:
        url: HTTP or HTTPS URL.
        max_chars: Maximum number of characters returned.
    """
    return fetch_page(url=url, max_chars=max_chars)


def _run_self_test() -> None:
    payload = {
        "server": "local-websearch",
        "status": "ok",
        "tools": ["web_search", "web_fetch"],
    }
    print(json.dumps(payload, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local web search MCP server.")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Print a small health payload and exit without starting the MCP transport.",
    )
    args = parser.parse_args()

    if args.self_test:
        _run_self_test()
        return

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
