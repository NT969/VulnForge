import argparse
import shutil
from datetime import datetime
from html import escape
from pathlib import Path

from scanner.target import check_target
from scanner.headers import check_security_headers
from scanner.crawler import crawl
from scanner.forms import discover_forms
from scanner.parameters import discover_parameters
from scanner.endpoints import discover_endpoints
from scanner.input_analysis import analyze_parameters
from scanner.active import test_parameter_reflection, test_form_parameter_reflection


def normalize_url(url):
    url = url.strip()

    if not url:
        return ""

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    return url


def classify_resource(url):
    resource_url = url.lower()

    if "/.git/" in resource_url or resource_url.endswith("/.git"):
        return "CRÍTICO"

    if (
        "/.env" in resource_url
        or resource_url.endswith(
            (".bak", ".backup", ".old", ".zip", ".tar", ".gz", ".sql")
        )
    ):
        return "ALTO"

    if (
        "/__pycache__/" in resource_url
        or resource_url.endswith((".pyc", ".pyo"))
    ):
        return "MÉDIO"

    return "NORMAL"


def copy_to_downloads(path):
    downloads = Path.home() / "storage" / "downloads"

    if not downloads.exists():
        return None

    try:
        destination = downloads / path.name
        shutil.copy2(path, destination)
        return destination
    except OSError:
        return None


def build_html(
    url,
    scan_date,
    findings,
    pages,
    forms,
    parameters,
    endpoints,
    active_tests,
):
    counts = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
        "INFO": 0,
    }

    severity_labels = {
        "CRITICAL": "CRÍTICO",
        "HIGH": "ALTO",
        "MEDIUM": "MÉDIO",
        "LOW": "BAIXO",
        "INFO": "INFORMAÇÃO",
    }

    for item in findings:
        severity = item.get("severity", "INFO")

        if severity in counts:
            counts[severity] += 1

    resource_rows = ""

    for resource in pages:
        resource_url = resource["url"]
        classification = classify_resource(resource_url)

        resource_rows += (
            '<details class="resource-card">'
            f"<summary>{escape(resource_url)}"
            f'<span class="badge">{classification}</span>'
            "</summary>"
            '<div class="resource-details">'
            f"<p><b>Status HTTP:</b> {resource['status_code']}</p>"
            f"<p><b>Tipo de conteúdo:</b> "
            f"{escape(resource['content_type'])}</p>"
            f"<p><b>Tamanho:</b> {resource['size']} bytes</p>"
            f"<p><b>Classificação:</b> {classification}</p>"
            f'<p><a href="{escape(resource_url)}" '
            'target="_blank">Abrir recurso</a></p>'
            "</div>"
            "</details>"
        )

    if not resource_rows:
        resource_rows = (
            '<div class="empty-resource">'
            "Nenhum recurso descoberto."
            "</div>"
        )

    form_rows = ""

    for number, form in enumerate(forms, 1):
        fields_html = ""

        for field in form.get("fields", []):
            field_name = escape(str(field.get("name", "")))
            field_type = escape(str(field.get("type", "")))

            fields_html += (
                '<div class="field-item">'
                f"<b>{field_name}</b>"
                f" <span>({field_type})</span>"
                "</div>"
            )

        if not fields_html:
            fields_html = (
                '<div class="field-item">'
                "Nenhum campo identificado."
                "</div>"
            )

        form_rows += (
            '<details class="form-card">'
            f"<summary>Formulário {number} — "
            f"{escape(str(form.get('method', 'GET')))}</summary>"
            '<div class="form-details">'
            f"<p><b>Página:</b> "
            f"{escape(str(form.get('page_url', '')))}</p>"
            f"<p><b>Método:</b> "
            f"{escape(str(form.get('method', 'GET')))}</p>"
            f"<p><b>Destino:</b> "
            f"{escape(str(form.get('action', '')))}</p>"
            "<p><b>Campos:</b></p>"
            f"{fields_html}"
            "</div>"
            "</details>"
        )

    if not form_rows:
        form_rows = (
            '<div class="empty-resource">'
            "Nenhum formulário descoberto."
            "</div>"
        )

    parameter_rows = ""

    for number, parameter in enumerate(parameters, 1):
        source = escape(str(parameter.get("source", "")))
        page_url = escape(str(parameter.get("page_url", "")))
        name = escape(str(parameter.get("name", "")))
        parameter_type = escape(str(parameter.get("type", "")))
        category = escape(str(parameter.get("category", "GERAL")))
        method = escape(str(parameter.get("method", "")))
        action = escape(str(parameter.get("action", "")))

        parameter_rows += (
            '<details class="parameter-card">'
            f"<summary>Parâmetro {number} — {name}</summary>"
            '<div class="parameter-details">'
            f"<p><b>Origem:</b> {source}</p>"
            f"<p><b>Página:</b> {page_url}</p>"
            f"<p><b>Nome:</b> {name}</p>"
            f"<p><b>Tipo:</b> {parameter_type}</p>"
            f"<p><b>Categoria:</b> {category}</p>"
            f"<p><b>Método:</b> {method}</p>"
            f"<p><b>Destino:</b> {action}</p>"
            "</div>"
            "</details>"
        )

    if not parameter_rows:
        parameter_rows = (
            '<div class="empty-resource">'
            "Nenhum parâmetro descoberto."
            "</div>"
        )

    endpoint_rows = ""

    for number, endpoint in enumerate(endpoints, 1):
        endpoint_url = escape(str(endpoint.get("url", "")))
        method = escape(str(endpoint.get("method", "GET")))
        source = escape(str(endpoint.get("source", "")))

        endpoint_rows += (
            '<details class="endpoint-card">'
            f"<summary>Endpoint {number} — {method}</summary>"
            '<div class="endpoint-details">'
            f"<p><b>URL:</b> {endpoint_url}</p>"
            f"<p><b>Método:</b> {method}</p>"
            f"<p><b>Origem:</b> {source}</p>"
            "</div>"
            "</details>"
        )

    if not endpoint_rows:
        endpoint_rows = (
            '<div class="empty-resource">'
            "Nenhum endpoint descoberto."
            "</div>"
        )

    finding_rows = ""

    for item in findings:
        severity = item.get("severity", "INFO")
        label = severity_labels.get(severity, severity)

        finding_rows += (
            "<tr>"
            f"<td>{escape(str(item.get('type', '')))}</td>"
            f"<td>{escape(label)}</td>"
            f"<td>{escape(str(item.get('parameter', '')))}</td>"
            f"<td>{escape(str(item.get('description', '')))}</td>"
            f"<td>{escape(str(item.get('recommendation', '')))}</td>"
            "</tr>"
        )

    if not finding_rows:
        finding_rows = (
            '<tr><td colspan="5">'
            "Nenhuma vulnerabilidade encontrada."
            "</td></tr>"
        )

    active_tests_html = ""

    if active_tests:
        for number, test in enumerate(active_tests, 1):
            active_tests_html += (
                '<div class="resource-card">'
                f'<div class="resource-details">'
                f'<p><b>Teste:</b> {escape(str(test.get("type", "Reflexão de parâmetro")))}</p>'
                f'<p><b>URL:</b> {escape(str(test.get("url", "N/A")))}</p>'
                f'<p><b>Parâmetro:</b> {escape(str(test.get("parameter", "N/A")))}</p>'
                f'<p><b>Método:</b> {escape(str(test.get("method", "N/A")))}</p>'
                f'<p><b>Status HTTP:</b> {escape(str(test.get("status_code", "N/A")))}</p>'
                f'<p><b>Refletido:</b> {escape(str(test.get("reflected", "N/A")))}</p>'
                f'<p><b>Marcador:</b> {escape(str(test.get("marker", "N/A")))}</p>'
                '</div>'
                '</div>'
            )
    else:
        active_tests_html = (
            '<div class="resource-card">'
            '<div class="resource-details">'
            '<p>Nenhum teste ativo executado.</p>'
            '</div>'
            '</div>'
        )

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Relatório VulnForge</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background: #f4f4f4;
    margin: 0;
    padding: 20px;
}}

main {{
    max-width: 1200px;
    margin: auto;
    background: white;
    padding: 25px;
    border-radius: 10px;
}}

h1 {{
    margin-top: 0;
}}

h2 {{
    margin-top: 30px;
}}

.summary {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 10px;
    margin-bottom: 30px;
}}

.card {{
    border: 1px solid #ccc;
    padding: 12px;
    border-radius: 8px;
}}

.small {{
    color: #555;
}}

.resources,
.forms,
.parameters,
.endpoints {{
    margin-bottom: 30px;
}}

.resource-card,
.form-card,
.parameter-card,
.endpoint-card {{
    border: 1px solid #ccc;
    border-radius: 8px;
    margin-bottom: 10px;
    overflow: hidden;
    background: #fff;
}}

.resource-card summary,
.form-card summary,
.parameter-card summary,
.endpoint-card summary {{
    cursor: pointer;
    padding: 12px;
    font-weight: bold;
    line-height: 1.5;
    overflow-wrap: anywhere;
    word-break: break-word;
}}

.resource-details,
.form-details,
.parameter-details,
.endpoint-details {{
    padding: 12px 14px;
    border-top: 1px solid #ccc;
    overflow-wrap: anywhere;
    word-break: break-word;
}}

.resource-details p,
.form-details p,
.parameter-details p,
.endpoint-details p {{
    margin: 8px 0;
}}

.resource-details a {{
    display: inline-block;
    margin-top: 5px;
    padding: 8px 10px;
    border: 1px solid #999;
    border-radius: 6px;
    text-decoration: none;
}}

.badge {{
    display: block;
    width: fit-content;
    margin-top: 8px;
    padding: 4px 8px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 12px;
    font-weight: bold;
}}

.field-item {{
    border: 1px solid #ddd;
    border-radius: 6px;
    padding: 8px;
    margin: 6px 0;
}}

.field-item span {{
    color: #555;
}}

.empty-resource {{
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 12px;
}}

.table-container {{
    overflow-x: auto;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 30px;
    min-width: 700px;
}}

th,
td {{
    border: 1px solid #ccc;
    padding: 8px;
    text-align: left;
    vertical-align: top;
}}

th {{
    background: #eee;
}}

a {{
    word-break

: break-word;
}}

@media (max-width: 700px) {{

    body {{
        padding: 10px;
    }}

    main {{
        padding: 15px;
        border-radius: 8px;
    }}

    h1 {{
        font-size: 24px;
    }}

    h2 {{
        font-size: 21px;
    }}

    .resource-card summary,
    .form-card summary,
    .parameter-card summary,
    .endpoint-card summary {{
        font-size: 14px;
        padding: 12px;
    }}

    .resource-details,
    .form-details,
    .parameter-details,
    .endpoint-details {{
        font-size: 14px;
    }}

    .badge {{
        display: block;
        margin-top: 8px;
    }}

}}

</style>
</head>

<body>

<main>

<h1>Relatório de Segurança VulnForge</h1>

<p>
<b>Alvo:</b> {escape(url)}
</p>

<p>
<b>Data da varredura:</b> {escape(scan_date)}
</p>

<h2>Resumo</h2>

<div class="summary">

<div class="card">
<b>Crítico</b><br>
{counts["CRITICAL"]}
</div>

<div class="card">
<b>Alto</b><br>
{counts["HIGH"]}
</div>

<div class="card">
<b>Médio</b><br>
{counts["MEDIUM"]}
</div>

<div class="card">
<b>Baixo</b><br>
{counts["LOW"]}
</div>

<div class="card">
<b>Informação</b><br>
{counts["INFO"]}
</div>

<div class="card">
<b>Total</b><br>
{len(findings)}
</div>

</div>

<h2>Recursos descobertos</h2>

<div class="resources">
{resource_rows}
</div>

<h2>Formulários descobertos</h2>

<div class="forms">
{form_rows}
</div>

<h2>Parâmetros descobertos</h2>

<div class="parameters">
{parameter_rows}
</div>

<h2>Endpoints descobertos</h2>

<div class="endpoints">
{endpoint_rows}
</div>

<h2>Testes ativos</h2>

<div class="resources">
{active_tests_html}
</div>

<h2>Vulnerabilidades</h2>

<div class="table-container">

<table>

<tr>
<th>Tipo</th>
<th>Severidade</th>
<th>Parâmetro</th>
<th>Descrição</th>
<th>Recomendação</th>
</tr>

{finding_rows}

</table>

</div>

<p class="small">
Gerado pelo VulnForge.
</p>

<p class="small">
Somente para testes de segurança autorizados.
</p>

</main>

</body>
</html>"""


def build_text(
    url,
    scan_date,
    findings,
    pages,
    forms,
    parameters,
    endpoints,
    active_tests,
):
    lines = []

    lines.append("VULNFORGE")
    lines.append("Scanner Automatizado de Segurança Web")
    lines.append("Versão 1.0.0")
    lines.append("=" * 60)

    lines.append(f"Alvo: {url}")
    lines.append(f"Data da varredura: {scan_date}")

    lines.append("")
    lines.append("TESTES ATIVOS")
    lines.append("=" * 60)

    if active_tests:
        for number, test in enumerate(active_tests, 1):
            lines.append("")
            lines.append(f"[{number}] Teste: {"Reflexão de parâmetro"}")
            lines.append(f"URL: {test.get("url", "N/A")}")
            lines.append(f"Parâmetro: {test.get("parameter", "N/A")}")
            lines.append(f"Método: {test.get("method", "N/A")}")
            lines.append(f"Status HTTP: {test.get("status_code", "N/A")}")
            lines.append(f"Refletido: {test.get("reflected", "N/A")}")
            lines.append(f"Marcador: {test.get("marker", "N/A")}")
    else:
        lines.append("")
        lines.append("Nenhum teste ativo executado.")

    lines.append("")
    lines.append("VULNERABILIDADES")
    lines.append("=" * 60)

    for number, item in enumerate(findings, 1):
        lines.append("")
        lines.append(f"[{number}] {item.get('type', '')}")
        lines.append(
            f"Severidade: {item.get('severity', '')}"
        )
        lines.append(
            f"Parâmetro: {item.get('parameter', '')}"
        )
        lines.append(
            f"Descrição: {item.get('description', '')}"
        )
        lines.append(
            f"Recomendação: {item.get('recommendation', '')}"
        )

    lines.append("")
    lines.append("RECURSOS DESCOBERTOS")
    lines.append("=" * 60)

    for number, resource in enumerate(pages, 1):
        lines.append("")
        lines.append(f"[{number}] {resource['url']}")
        lines.append(
            f"Status HTTP: {resource['status_code']}"
        )
        lines.append(
            f"Tipo de conteúdo: {resource['content_type']}"
        )
        lines.append(
            f"Tamanho: {resource['size']} bytes"
        )
        lines.append(
            f"Classificação: {classify_resource(resource['url'])}"
        )

    lines.append("")
    lines.append("FORMULÁRIOS DESCOBERTOS")
    lines.append("=" * 60)

    if forms:
        for number, form in enumerate(forms, 1):
            lines.append("")
            lines.append(f"[{number}] FORMULÁRIO")
            lines.append(
                f"Página: {form.get('page_url', '')}"
            )
            lines
            lines.append(
                f"Método: {form.get('method', 'GET')}"
            )
            lines.append(
                f"Destino: {form.get('action', '')}"
            )
            lines.append("Campos:")

            for field in form.get("fields", []):
                lines.append(
                    f"  - {field.get('name', '')} "
                    f"({field.get('type', '')})"
                )
    else:
        lines.append("")
        lines.append("Nenhum formulário descoberto.")

    lines.append("")
    lines.append("PARÂMETROS DESCOBERTOS")
    lines.append("=" * 60)

    if parameters:
        for number, parameter in enumerate(parameters, 1):
            lines.append("")
            lines.append(f"[{number}] PARÂMETRO")
            lines.append(
                f"Origem: {parameter.get('source', '')}"
            )
            lines.append(
                f"Página: {parameter.get('page_url', '')}"
            )
            lines.append(
                f"Nome: {parameter.get('name', '')}"
            )
            lines.append(
                f"Tipo: {parameter.get('type', '')}"
            )
            lines.append(
                f"Categoria: {parameter.get('category', 'GERAL')}"
            )
            lines.append(
                f"Método: {parameter.get('method', '')}"
            )
            lines.append(
                f"Destino: {parameter.get('action', '')}"
            )
    else:
        lines.append("")
        lines.append("Nenhum parâmetro descoberto.")

    lines.append("")
    lines.append("ENDPOINTS DESCOBERTOS")
    lines.append("=" * 60)

    if endpoints:
        for number, endpoint in enumerate(endpoints, 1):
            lines.append("")
            lines.append(f"[{number}] ENDPOINT")
            lines.append(
                f"URL: {endpoint.get('url', '')}"
            )
            lines.append(
                f"Método: {endpoint.get('method', 'GET')}"
            )
            lines.append(
                f"Origem: {endpoint.get('source', '')}"
            )
    else:
        lines.append("")
        lines.append("Nenhum endpoint descoberto.")

    lines.append("")
    lines.append("=" * 60)
    lines.append("Gerado pelo VulnForge.")
    lines.append("Somente para testes de segurança autorizados.")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="VulnForge - Scanner Automatizado de Segurança Web"
    )

    parser.add_argument(
        "--url",
        help="URL do alvo autorizado"
    )

    args = parser.parse_args()

    url = args.url.strip() if args.url else ""

    if not url:
        url = input("Digite a URL do alvo: ").strip()

    url = normalize_url(url)

    if not url:
        print("[-] URL não informada.")
        return

    print("=" * 60)
    print("VULNFORGE")
    print("Scanner Automatizado de Segurança Web")
    print("Versão 1.0.0")
    print("=" * 60)

    print(f"[*] Alvo: {url}")
    print("[*] Verificando alvo...")

    target = check_target(url)

    if not target["success"]:
        print("[-] Não foi possível acessar o alvo.")
        print(f"[-] Erro: {target['error']}")
        return

    print(f"[+] HTTP {target['status_code']}")

    print("[*] Analisando cabeçalhos de segurança...")

    findings = check_security_headers(target["headers"])

    print(
        f"[+] Vulnerabilidades encontradas: {len(findings)}"
    )

    print("[*] Mapeando recursos...")

    try:
        pages = crawl(url, max_pages=20)
    except Exception as error:
        print(f"[-] Erro no crawler: {error}")
        pages = []

    print(f"[+] Recursos descobertos: {len(pages)}")

    print("[*] Descobrindo formulários...")

    forms = []

    for page in pages:
        page_url = page["url"]
        content_type = page.get("content_type", "").lower()

        if "text/html" not in content_type:
            continue

       
        try:
            discovered = discover_forms(page_url)
            forms.extend(discovered)
        except Exception as error:
            print(
                f"[-] Erro ao analisar formulário em "
                f"{page_url}: {error}"
            )

    print(f"[+] Formulários descobertos: {len(forms)}")

    print("[*] Executando testes ativos não destrutivos...")

    active_tests = []

    for form in forms:
        method = form.get("method", "GET").upper()

        if method != "POST":
            continue

        for field in form.get("fields", []):
            parameter_name = field.get("name", "").strip()

            if not parameter_name:
                continue

            try:
                result = test_form_parameter_reflection(
                    form,
                    parameter_name
                )
                active_tests.append(result)
            except Exception as error:
                active_tests.append({
                    "tested": False,
                    "parameter": parameter_name,
                    "method": method,
                    "error": str(error)
                })

    print(f"[+] Testes ativos executados: {len(active_tests)}")


    print("[*] Inventariando parâmetros...")

    try:
        parameters = discover_parameters(
            pages,
            forms
        )
    except Exception as error:
        print(
            f"[-] Erro ao inventariar parâmetros: {error}"
        )
        parameters = []

    parameters = analyze_parameters(parameters)
    print(f"[+] Parâmetros descobertos: {len(parameters)}")

    print("[*] Inventariando endpoints...")

    try:
        endpoints = discover_endpoints(
            pages,
            forms
        )
    except Exception as error:
        print(
            f"[-] Erro ao inventariar endpoints: {error}"
        )
        endpoints = []

    print(f"[+] Endpoints descobertos: {len(endpoints)}")

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    scan_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    txt_path = reports_dir / f"scan_{timestamp}.txt"
    html_path = reports_dir / f"scan_{timestamp}.html"

    text_report = build_text(
        url,
        scan_date,
        findings,
        pages,
        forms,
        parameters,
        endpoints,
    active_tests
    )

    html_report = build_html(
        url,
        scan_date,
        findings,
        pages,
        forms,
        parameters,
        endpoints,
    active_tests
    )

    txt_path.write_text(
        text_report,
        encoding="utf-8"
    )

    html_path.write_text(
        html_report,
        encoding="utf-8"
    )

    print(f"[+] Relatório TXT: {txt_path}")
    print(f"[+] Relatório HTML: {html_path}")

    txt_download = copy_to_downloads(txt_path)
    html_download = copy_to_downloads(html_path)

    if txt_download:
        print(
            f"[+] TXT copiado para Downloads: {txt_download}"
        )

    if html_download:
        print(
            f"[+] HTML copiado para Downloads: {html_download}"
        )

    print("[+] Varredura concluída.")


if __name__ == "__main__":
    main()
