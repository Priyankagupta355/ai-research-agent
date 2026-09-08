import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote


def search_web(query: str, max_results: int = 5) -> str:
    """
    Search the web using DuckDuckGo HTML results.

    Returns:
        A formatted string containing title, URL and snippet
        for each search result.
    """

    if not query or not query.strip():
        return "Error: Search query is empty."

    # --------------------------------------------------------
    # Configuration
    # --------------------------------------------------------

    query = query.strip()

    max_results = max(
        1,
        min(int(max_results), 5)
    )

    url = "https://html.duckduckgo.com/html/"

    params = {
        "q": query
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/140.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    # --------------------------------------------------------
    # Send request
    # --------------------------------------------------------

    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

    except requests.RequestException as e:

        return (
            f"Search request failed: {str(e)}"
        )

    # --------------------------------------------------------
    # Parse HTML
    # --------------------------------------------------------

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    results = []

    # --------------------------------------------------------
    # Extract search results
    # --------------------------------------------------------

    result_blocks = soup.select(
        ".result"
    )

    for result in result_blocks:

        if len(results) >= max_results:
            break

        # ----------------------------------------------------
        # Title + URL
        # ----------------------------------------------------

        link_tag = result.select_one(
            ".result__a"
        )

        if not link_tag:
            continue

        title = link_tag.get_text(
            " ",
            strip=True
        )

        link = link_tag.get(
            "href"
        )

        if not title or not link:
            continue

        # ----------------------------------------------------
        # Decode DuckDuckGo redirect URL
        # ----------------------------------------------------

        if link.startswith("//duckduckgo.com/l/?"):

            try:

                from urllib.parse import urlparse, parse_qs

                parsed = urlparse(
                    "https:" + link
                )

                query_params = parse_qs(
                    parsed.query
                )

                if "uddg" in query_params:

                    link = unquote(
                        query_params["uddg"][0]
                    )

            except Exception:
                pass

        # ----------------------------------------------------
        # Snippet
        # ----------------------------------------------------

        snippet_tag = result.select_one(
            ".result__snippet"
        )

        if snippet_tag:

            snippet = snippet_tag.get_text(
                " ",
                strip=True
            )

        else:

            snippet = "No snippet available."

        # ----------------------------------------------------
        # Store result
        # ----------------------------------------------------

        results.append(

            {
                "title": title,
                "url": link,
                "snippet": snippet
            }
        )

    # --------------------------------------------------------
    # No results
    # --------------------------------------------------------

    if not results:

        return (
            f"No search results found for query: "
            f"{query}"
        )

    # --------------------------------------------------------
    # Format results
    # --------------------------------------------------------

    formatted_results = []

    for index, result in enumerate(
        results,
        start=1
    ):

        formatted_results.append(

            f"""
Result {index}

Title:
{result["title"]}

URL:
{result["url"]}

Snippet:
{result["snippet"]}
""".strip()
        )

    return "\n\n".join(
        formatted_results
    )