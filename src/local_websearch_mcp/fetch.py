from __future__ import annotations

from typing import Dict
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/123.0.0.0 Safari/537.36"
)


def _is_http_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def fetch_page(url: str, max_chars: int = 12000, timeout_s: int = 20) -> Dict[str, str]:
    if not _is_http_url(url):
        raise ValueError("url must be a valid http(s) URL")
    if max_chars < 1000 or max_chars > 200000:
        raise ValueError("max_chars must be in [1000, 200000]")

    response = requests.get(url, timeout=timeout_s, headers={"User-Agent": USER_AGENT})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    title = soup.title.get_text(" ", strip=True) if soup.title else ""

    candidates = []
    for selector in ["main", "article", "section", "body"]:
        for node in soup.select(selector):
            text = node.get_text(" ", strip=True)
            if text:
                candidates.append(text)

    text = max(candidates, key=len) if candidates else soup.get_text(" ", strip=True)
    text = " ".join(text.split())

    return {
        "url": url,
        "title": title,
        "content": text[:max_chars],
        "truncated": len(text) > max_chars,
    }
