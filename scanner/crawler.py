import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def crawl(url, max_pages=20):
    """
    Descobre recursos internos de um alvo autorizado.
    Limita a navegação ao mesmo domínio.
    """

    session = requests.Session()
    session.headers.update({
        "User-Agent": "VulnForge/1.0"
    })

    base_domain = urlparse(url).netloc
    visited = set()
    queue = [url]
    results = []

    while queue and len(visited) < max_pages:
        current_url = queue.pop(0)

        if current_url in visited:
            continue

        try:
            response = session.get(
                current_url,
                timeout=10,
                allow_redirects=True
            )

            visited.add(current_url)

            content_type = response.headers.get(
                "Content-Type",
                "unknown"
            )

            results.append({
                "url": current_url,
                "status_code": response.status_code,
                "content_type": content_type,
                "size": len(response.content),
            })

            if "text/html" not in content_type:
                continue

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            for link in soup.find_all("a", href=True):
                next_url = urljoin(
                    response.url,
                    link["href"]
                )

                parsed = urlparse(next_url)

                if parsed.scheme not in ("http", "https"):
                    continue

                if parsed.netloc != base_domain:
                    continue

                clean_url = next_url.split("#")[0]

                if (
                    clean_url not in visited
                    and clean_url not in queue
                ):
                    queue.append(clean_url)

        except requests.RequestException:
            continue

    return results
