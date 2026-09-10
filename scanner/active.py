import secrets
import requests
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse


def generate_marker():
    return "VULNFORGE_" + secrets.token_hex(8)


def test_parameter_reflection(url, parameter, timeout=10):
    """
    Teste ativo não destrutivo para parâmetros GET.

    Substitui o valor do parâmetro por um marcador
    e verifica se o marcador aparece na resposta.

    Use somente em alvos autorizados.
    """

    parsed = urlparse(url)

    query = parse_qsl(
        parsed.query,
        keep_blank_values=True
    )

    if not query:
        return {
            "tested": False,
            "reason": "URL sem parâmetros GET"
        }

    parameter_name = parameter.strip()

    if not parameter_name:
        return {
            "tested": False,
            "reason": "Parâmetro vazio"
        }

    found = False
    new_query = []
    marker = generate_marker()

    for name, value in query:
        if name == parameter_name:
            new_query.append((name, marker))
            found = True
        else:
            new_query.append((name, value))

    if not found:
        return {
            "tested": False,
            "reason": "Parâmetro não encontrado na URL"
        }

    modified_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            urlencode(new_query),
            parsed.fragment,
        )
    )

    try:
        response = requests.get(
            modified_url,
            timeout=timeout,
            allow_redirects=True,
            headers={
                "User-Agent": "VulnForge/1.0"
            },
        )

        reflected = marker in response.text

        return {
            "tested": True,
            "parameter": parameter_name,
            "method": "GET",
            "marker": marker,
            "url": modified_url,
            "status_code": response.status_code,
            "reflected": reflected,
        }

    except requests.RequestException as error:
        return {
            "tested": False,
            "parameter": parameter_name,
            "method": "GET",
            "error": str(error),
        }


def test_form_parameter_reflection(
    form,
    parameter,
    timeout=10
):
    """
    Teste ativo não destrutivo para parâmetros de formulário POST.

    Envia um marcador apenas no parâmetro selecionado
    e verifica se o marcador aparece na resposta.

    Use somente em alvos autorizados.
    """

    action = form.get("action", "").strip()
    method = form.get("method", "GET").upper()

    if not action:
        return {
            "tested": False,
            "reason": "Formulário sem destino"
        }

    if method != "POST":
        return {
            "tested": False,
            "reason": "Formulário não utiliza POST"
        }

    parameter_name = parameter.strip()

    if not parameter_name:
        return {
            "tested": False,
            "reason": "Parâmetro vazio"
        }

    fields = form.get("fields", [])

    field_names = {
        field.get("name", "")
        for field in fields
        if field.get("name")
    }

    if parameter_name not in field_names:
        return {
            "tested": False,
            "parameter": parameter_name,
            "reason": "Parâmetro não encontrado no formulário"
        }

    marker = generate_marker()

    data = {}

    for field in fields:
        name = field.get("name", "")

        if not name:
            continue

        if name == parameter_name:
            data[name] = marker
        else:
            field_type = field.get("type", "text")

            if field_type == "hidden":
                data[name] = field.get("value", "")
            else:
                data[name] = "VULNFORGE_TEST"

    try:
        response = requests.post(
            action,
            data=data,
            timeout=timeout,
            allow_redirects=True,
            headers={
                "User-Agent": "VulnForge/1.0"
            },
        )

        reflected = marker in response.text

        return {
            "tested": True,
            "parameter": parameter_name,
            "method": "POST",
            "marker": marker,
            "url": action,
            "status_code": response.status_code,
            "reflected": reflected,
        }

    except requests.RequestException as error:
        return {
            "tested": False,
            "parameter": parameter_name,
            "method": "POST",
            "error": str(error),
        }
