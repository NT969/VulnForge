import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def discover_forms(url):
    """
    Descobre formulários HTML em um alvo autorizado.

    Retorna:
    - URL da página
    - método HTTP
    - action
    - campos encontrados
    """

    session = requests.Session()

    session.headers.update({
        "User-Agent": "VulnForge/1.0"
    })

    results = []

    try:
        response = session.get(
            url,
            timeout=10,
            allow_redirects=True
        )

        if "text/html" not in response.headers.get(
            "Content-Type",
            ""
        ):
            return results

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for form in soup.find_all("form"):

            method = form.get(
                "method",
                "GET"
            ).upper()

            action = form.get(
                "action",
                ""
            )

            action_url = urljoin(
                response.url,
                action
            )

            fields = []

            for field in form.find_all(
                ["input", "textarea", "select"]
            ):

                name = field.get("name")

                if not name:
                    continue

                field_type = field.get(
                    "type",
                    field.name
                )

                fields.append({
                    "name": name,
                    "type": field_type,
                })

            results.append({
                "page_url": response.url,
                "method": method,
                "action": action_url,
                "fields": fields,
            })

    except requests.RequestException:
        return results

    return results
