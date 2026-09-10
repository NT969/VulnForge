from urllib.parse import parse_qsl, urlparse


def discover_parameters(pages, forms):
    """
    Cria um inventário de pontos de entrada encontrados
    durante o reconhecimento passivo.

    Não envia requisições adicionais ao alvo.
    """

    parameters = []
    seen = set()

    def add_parameter(
        source,
        page_url,
        name,
        parameter_type,
        method="GET",
        action=""
    ):
        key = (
            source,
            page_url,
            name,
            parameter_type,
            method,
            action,
        )

        if key in seen:
            return

        seen.add(key)

        parameters.append({
            "source": source,
            "page_url": page_url,
            "name": name,
            "type": parameter_type,
            "method": method,
            "action": action,
        })

    # Parâmetros encontrados nas URLs
    for page in pages:
        page_url = page.get("url", "")

        if not page_url:
            continue

        parsed = urlparse(page_url)

        for name, value in parse_qsl(
            parsed.query,
            keep_blank_values=True
        ):
            add_parameter(
                source="URL",
                page_url=page_url,
                name=name,
                parameter_type="query",
                method="GET",
                action=page_url,
            )

    # Parâmetros encontrados nos formulários
    for form in forms:
        page_url = form.get("page_url", "")
        method = form.get("method", "GET").upper()
        action = form.get("action", "")

        for field in form.get("fields", []):
            name = field.get("name", "")
            field_type = field.get("type", "")

            if not name:
                continue

            add_parameter(
                source="FORMULÁRIO",
                page_url=page_url,
                name=name,
                parameter_type=field_type,
                method=method,
                action=action,
            )

    return parameters
