from local_websearch_mcp.fetch import fetch_page
from local_websearch_mcp.search import search_web


def main() -> None:
    results = search_web("Utnapishtim", max_results=3)
    print("Search results:")
    for item in results:
        print(item["title"], item["url"])

    if results:
        page = fetch_page(results[0]["url"], max_chars=1200)
        print("\nFetched page:")
        print(page["title"])
        print(page["content"])


if __name__ == "__main__":
    main()
