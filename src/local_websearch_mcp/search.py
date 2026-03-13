from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import List
from urllib.parse import parse_qs, quote_plus, unquote, urlparse

import requests
from bs4 import BeautifulSoup


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/123.0.0.0 Safari/537.36"
)


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str


def _clean_result_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.path.startswith("/l/"):
        qs = parse_qs(parsed.query)
        target = qs.get("uddg", [""])[0]
        if target:
            return unquote(target)
    return url


def search_web(query: str, max_results: int = 5, timeout_s: int = 15) -> List[dict]:
    if not query.strip():
        raise ValueError("query cannot be empty")
    if max_results < 1 or max_results > 20:
        raise ValueError("max_results must be in [1, 20]")

    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    response = requests.get(url, timeout=timeout_s, headers={"User-Agent": USER_AGENT})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    items: List[SearchResult] = []

    for node in soup.select(".result"):
        link = node.select_one(".result__a")
        snippet_el = node.select_one(".result__snippet")
        if not link:
            continue

        href = link.get("href", "").strip()
        if not href:
            continue

        items.append(
            SearchResult(
                title=link.get_text(strip=True),
                url=_clean_result_url(href),
                snippet=snippet_el.get_text(" ", strip=True) if snippet_el else "",
            )
        )
        if len(items) >= max_results:
            break

    return [asdict(item) for item in items]
