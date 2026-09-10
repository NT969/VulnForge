from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs


class LabHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        tamanho = int(self.headers.get("Content-Length", 0))
        corpo = self.rfile.read(tamanho).decode("utf-8")

        dados = parse_qs(corpo)
        username = dados.get("username", [""])[0]

        resposta = f"""
<html>
<body>
<h1>Laboratório POST</h1>
<p>Usuário recebido: {username}</p>
</body>
</html>
"""

        corpo_resposta = resposta.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo_resposta)))
        self.end_headers()

        self.wfile.write(corpo_resposta)

    def log_message(self, format, *args):
        pass


server = HTTPServer(("127.0.0.1", 8081), LabHandler)

print("Laboratório POST iniciado em http://127.0.0.1:8081")
print("Use somente para testes locais autorizados.")

server.serve_forever()
