from urllib.parse import urlparse


def discover_endpoints(pages, forms):
    """
    Cria um inventário de endpoints observados durante
    o reconhecimento autorizado.

    Não envia requisições adicionais.
    """

    endpoints = []
    seen = set()

    def add_endpoint(
        url,
        method="GET",
        source="CRAWLER"
    ):
        if not url:
            return

        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            return

        key = (
            method.upper(),
            url,
            source,
        )

        if key in seen:
            return

        seen.add(key)

        endpoints.append({
            "url": url,
            "method": method.upper(),
            "source": source,
        })

    for page in pages:
        add_endpoint(
            page.get("url", ""),
            method="GET",
            source="CRAWLER",
        )

    for form in forms:
        add_endpoint(
            form.get("action", ""),
            method=form.get("method", "GET"),
            source="FORMULÁRIO",
        )

    return endpoints
