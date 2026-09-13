import requests
from bs4 import BeautifulSoup


def read_webpage(
    url: str | None = None,
    cursor: int | None = None,
    loc: int | None = None
) -> str:
    """
    Read and extract useful text content from a webpage.

    Returns a clear error message instead of crashing when
    a webpage cannot be accessed.
    """

    if not url:
        return (
            "SOURCE_UNAVAILABLE: read_webpage requires a complete URL. "
            "Use a URL returned by search_web."
        )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=15,
            allow_redirects=True
        )

        # Handle common HTTP errors without crashing the agent
        if response.status_code == 404:
            return (
                f"SOURCE_UNAVAILABLE: The webpage returned 404 Not Found: {url}. "
                "Do not use this source. Try another search result."
            )

        if response.status_code == 403:
            return (
                f"SOURCE_UNAVAILABLE: Access to this webpage was forbidden: {url}. "
                "Do not use this source. Try another search result."
            )

        if response.status_code >= 400:
            return (
                f"SOURCE_UNAVAILABLE: The webpage returned HTTP "
                f"{response.status_code}: {url}. "
                "Try another source."
            )

        response.raise_for_status()

    except requests.exceptions.Timeout:
        return (
            f"SOURCE_UNAVAILABLE: The webpage timed out while loading: {url}. "
            "Try another source."
        )

    except requests.exceptions.ConnectionError:
        return (
            f"SOURCE_UNAVAILABLE: Could not connect to the webpage: {url}. "
            "Try another source."
        )

    except requests.exceptions.RequestException as error:
        return (
            f"SOURCE_UNAVAILABLE: Could not read webpage: {url}. "
            f"Error: {error}. Try another source."
        )

    try:
        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove unnecessary HTML elements
        for element in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "noscript",
            "svg"
        ]):
            element.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        # Clean excessive whitespace
        text = " ".join(text.split())

        if not text:
            return (
                f"SOURCE_UNAVAILABLE: No readable text was found on: {url}. "
                "Try another source."
            )

        # Limit webpage content
        return text[:5000]

    except Exception as error:
        return (
            f"SOURCE_UNAVAILABLE: Failed to extract webpage content from {url}. "
            f"Error: {error}. Try another source."
        )