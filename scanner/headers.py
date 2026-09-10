SECURITY_HEADERS = {
    "Content-Security-Policy": {
        "severity": "MEDIUM",
        "description": "Ajuda a reduzir ataques de XSS e injeção de conteúdo.",
        "recommendation": "Configure uma Content-Security-Policy adequada."
    },
    "X-Frame-Options": {
        "severity": "MEDIUM",
        "description": "Ajuda a reduzir ataques de clickjacking.",
        "recommendation": "Configure X-Frame-Options ou utilize frame-ancestors na CSP."
    },
    "X-Content-Type-Options": {
        "severity": "LOW",
        "description": "Ajuda a impedir MIME sniffing.",
        "recommendation": "Configure X-Content-Type-Options: nosniff."
    },
    "Strict-Transport-Security": {
        "severity": "LOW",
        "description": "Instrui o navegador a utilizar HTTPS.",
        "recommendation": "Configure HSTS quando o sistema estiver sendo servido por HTTPS."
    },
    "Referrer-Policy": {
        "severity": "LOW",
        "description": "Controla as informações de referência enviadas pelo navegador.",
        "recommendation": "Configure uma política de Referrer-Policy apropriada."
    },
    "Permissions-Policy": {
        "severity": "INFO",
        "description": "Controla o acesso a determinados recursos do navegador.",
        "recommendation": "Configure Permissions-Policy conforme as necessidades da aplicação."
    }
}


def check_security_headers(headers):
    findings = []

    for header, details in SECURITY_HEADERS.items():
        if header not in headers:
            findings.append({
                "type": "Missing Security Header",
                "severity": details["severity"],
                "parameter": header,
                "description": details["description"],
                "recommendation": details["recommendation"]
            })

    return findings
