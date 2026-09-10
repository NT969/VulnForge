import requests


def check_target(url):
    """
    Verifica se o alvo está acessível e coleta
    algumas informações básicas da resposta HTTP.
    """

    try:
        response = requests.get(
            url,
            timeout=10,
            allow_redirects=True,
            headers={
                "User-Agent": "VulnForge/1.0"
            }
        )

        return {
            "success": True,
            "status_code": response.status_code,
            "final_url": response.url,
            "server": response.headers.get(
                "Server",
                "Not disclosed"
            ),
            "content_type": response.headers.get(
                "Content-Type",
                "Not disclosed"
            ),
            "headers": dict(response.headers),
        }

    except requests.RequestException as error:
        return {
            "success": False,
            "error": str(error)
        }

