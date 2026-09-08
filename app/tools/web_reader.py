import requests
from bs4 import BeautifulSoup


def read_webpage(
    url: str | None = None,
    cursor: int | None = None,
    loc: int | None = None
) -> str:
    """
    Read the text content of a webpage.
    """

    if not url:
        return (
            "Error: read_webpage requires a complete URL. "
            "Use the URL returned by search_web."
        )

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # Unnecessary HTML elements remove karo
    for element in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header"
    ]):
        element.decompose()

    text = soup.get_text(
        separator=" ",
        strip=True
    )

    # Bahut large webpage ko limit karenge
    return text[:5000]