def classify_parameter(name):
    """
    Classifica um parâmetro pelo nome.
    Não envia requisições e não executa payloads.
    """

    if not name:
        return "DESCONHECIDO"

    value = name.strip().lower()

    authentication = {
        "user",
        "username",
        "usuario",
        "login",
        "email",
        "e-mail",
        "password",
        "senha",
        "pass",
    }

    tokens = {
        "token",
        "csrf",
        "xsrf",
        "auth",
        "authorization",
        "session",
        "sessionid",
    }

    identifiers = {
        "id",
        "user_id",
        "userid",
        "account_id",
        "product_id",
        "item_id",
        "order_id",
    }

    urls = {
        "url",
        "uri",
        "redirect",
        "redirect_url",
        "return_url",
        "next",
        "callback",
    }

    search = {
        "q",
        "query",
        "search",
        "keyword",
        "term",
        "filter",
    }

    file_related = {
        "file",
        "filename",
        "path",
        "filepath",
        "upload",
        "document",
    }

    if value in authentication:
        return "AUTENTICAÇÃO"

    if value in tokens:
        return "TOKEN"

    if value in identifiers:
        return "IDENTIFICADOR"

    if value in urls:
        return "URL/REDIRECIONAMENTO"

    if value in search:
        return "BUSCA/FILTRO"

    if value in file_related:
        return "ARQUIVO/CAMINHO"

    return "GERAL"


def analyze_parameters(parameters):
    """
    Adiciona uma categoria aos parâmetros já descobertos.
    """

    analyzed = []

    for parameter in parameters:
        item = dict(parameter)

        item["category"] = classify_parameter(
            item.get("name", "")
        )

        analyzed.append(item)

    return analyzed
