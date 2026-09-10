# GUIA DE USO — VULNFORGE

## Manual completo para iniciantes em Pentest e Segurança da Informação

**Projeto:** VulnForge  
**Autor:** NT969  
**Versão do manual:** 1.0  
**Idioma:** Português (Brasil)

---

# 1. Bem-vindo ao VulnForge

O VulnForge é uma ferramenta de reconhecimento e análise de aplicações web desenvolvida em Python.

A ideia deste projeto é ajudar quem está começando em Pentest a entender, na prática, como uma aplicação web pode ser analisada de forma organizada.

O projeto também pode servir como uma base para profissionais de segurança que estejam realizando testes com autorização.

> **IMPORTANTE:** nunca utilize o VulnForge contra sistemas, sites, servidores, APIs ou redes sem autorização.

Um Pentest profissional não começa pelo ataque. Ele começa pela autorização, definição do escopo e planejamento.

---

# 2. Para quem é este manual?

Este manual foi escrito para pessoas que:

- nunca usaram Linux;
- estão começando a usar o terminal;
- querem aprender Pentest;
- querem aprender segurança web;
- querem entender ferramentas de segurança;
- querem aprender Python aplicado à segurança;
- querem estudar para trabalhar com segurança ofensiva;
- querem entender como funciona o VulnForge.

Você não precisa ser especialista para começar.

O importante é avançar por etapas.

---

# 3. O que é Pentest?

Pentest é a abreviação de **Penetration Test**, ou teste de intrusão.

É um processo autorizado usado para encontrar e avaliar falhas de segurança.

Um profissional de Pentest pode procurar problemas como:

- autenticação inadequada;
- autorização incorreta;
- exposição de informações;
- configurações inseguras;
- problemas em cabeçalhos HTTP;
- entradas de usuário mal tratadas;
- endpoints expostos;
- falhas de validação;
- vulnerabilidades em aplicações web.

O objetivo profissional não é simplesmente "invadir".

O objetivo é:

1. descobrir;
2. validar;
3. documentar;
4. explicar o risco;
5. recomendar correção;
6. fornecer evidências dentro do escopo autorizado.

---

# 4. Pentest não é a mesma coisa que ataque criminoso

A principal diferença é a **autorização**.

Em um Pentest legítimo existe uma autorização clara.

Normalmente existe um documento ou contrato definindo:

- quem autorizou o teste;
- quais sistemas podem ser testados;
- quais endereços estão no escopo;
- quais horários são permitidos;
- quais técnicas podem ser utilizadas;
- quais técnicas são proibidas;
- como os resultados devem ser comunicados.

Exemplo:

> Uma empresa autoriza o teste do domínio `exemplo.com`, somente entre 22h e 5h, sem realizar ataques de negação de serviço.

Nesse caso, o profissional precisa respeitar exatamente essas regras.

---

# 5. O que é uma vulnerabilidade?

Uma vulnerabilidade é uma fraqueza que pode permitir um comportamento indesejado ou inseguro.

Exemplo simples:

Imagine uma aplicação que recebe:

```text
nome=Marcio
```

e coloca esse valor diretamente em uma página sem tratamento adequado.

O comportamento da aplicação pode revelar que a entrada do usuário está chegando até a resposta.

Isso não significa automaticamente que existe uma vulnerabilidade explorável.

É necessário analisar o contexto.

Por isso, um bom profissional não transforma qualquer resultado de ferramenta em "vulnerabilidade confirmada".

---

# 6. O que é reconhecimento?

Reconhecimento é a etapa em que o profissional tenta entender o alvo.

Pode envolver:

- domínio;
- páginas;
- URLs;
- formulários;
- parâmetros;
- endpoints;
- tecnologias;
- respostas HTTP;
- cabeçalhos;
- recursos disponíveis.

Existem dois conceitos importantes:

### Reconhecimento passivo

Busca informações sem interagir diretamente com o alvo de maneira significativa.

### Reconhecimento ativo

Interage diretamente com o alvo.

O VulnForge realiza principalmente atividades de reconhecimento e alguns testes ativos não destrutivos.

---

# 7. O que é HTTP?

HTTP significa **HyperText Transfer Protocol**.

É um dos principais protocolos utilizados na comunicação entre navegador e servidor web.

Quando você acessa:

```text
http://127.0.0.1:8000
```

o navegador envia uma requisição.

O servidor responde.

Uma resposta HTTP pode conter:

- código de status;
- cabeçalhos;
- conteúdo;
- cookies;
- redirecionamentos.

---

# 8. Códigos HTTP básicos

Alguns códigos importantes:

### 200 — OK

A requisição foi processada com sucesso.

### 301 / 302 — Redirecionamento

O servidor está indicando outro endereço.

### 400 — Bad Request

A requisição possui algum problema.

### 401 — Unauthorized

É necessária autenticação.

### 403 — Forbidden

O servidor recusou o acesso.

### 404 — Not Found

O recurso não foi encontrado.

### 500 — Internal Server Error

O servidor encontrou um erro interno.

---

# 9. O que é um parâmetro?

Parâmetros são valores enviados para uma aplicação.

Exemplo:

```text
https://exemplo.local/busca?q=teste
```

Nesse exemplo:

```text
q=teste
```

é um parâmetro.

O nome é:

```text
q
```

O valor é:

```text
teste
```

Outro exemplo:

```text
?id=10
```

Aqui o parâmetro é:

```text
id
```

---

# 10. O que é um formulário?

Um formulário HTML permite que o usuário envie informações para uma aplicação.

Exemplo:

```html
<form action="/login" method="POST">
    <input name="username">
    <input name="password" type="password">
    <button type="submit">Entrar</button>
</form>
```

Nesse exemplo temos parâmetros:

```text
username
password
```

O VulnForge consegue descobrir formulários e seus campos.

---

# 11. GET e POST

Existem vários métodos HTTP.

Os dois mais importantes para este projeto são:

## GET

Normalmente utiliza parâmetros na URL.

Exemplo:

```text
/busca?q=teste
```

## POST

Normalmente envia os dados no corpo da requisição.

Exemplo:

```text
username=marcio&password=teste
```

O VulnForge possui análise de parâmetros GET e testes ativos específicos para formulários POST.

---

# 12. O que é o VulnForge?

O VulnForge foi organizado em módulos.

Estrutura principal:

```text
VulnForge/
├── vulnforge.py
├── scanner/
│   ├── __init__.py
│   ├── target.py
│   ├── headers.py
│   ├── crawler.py
│   ├── forms.py
│   ├── parameters.py
│   ├── endpoints.py
│   ├── input_analysis.py
│   └── active.py
├── reports/
├── requirements.txt
├── README.md
├── teste_form.html
├── laboratorio_post.py
└── GUIA_DE_USO.md
```

Cada módulo possui uma função.

---

# 13. Entendendo os módulos

## target.py

Verifica o alvo e coleta informações básicas da resposta HTTP.

## headers.py

Analisa cabeçalhos relacionados à segurança.

## crawler.py

Percorre recursos internos do mesmo domínio dentro do limite configurado.

## forms.py

Procura formulários HTML.

## parameters.py

Identifica parâmetros dos formulários e URLs.

## endpoints.py

Ajuda a identificar endpoints e recursos encontrados.

## input_analysis.py

Classifica parâmetros encontrados.

## active.py

Executa testes ativos não destrutivos.

## vulnforge.py

É o ponto principal de execução.

Ele coordena os módulos.

---

# 14. O que é o terminal?

O terminal é uma interface para executar comandos.

Em vez de clicar em ícones, você pode escrever comandos.

Exemplo:

```bash
pwd
```

O comando mostra em qual diretório você está.

Outro:

```bash
ls
```

mostra arquivos e pastas.

---

# 15. Comandos básicos do Linux

## Ver diretório atual

```bash
pwd
```

## Listar arquivos

```bash
ls
```

## Entrar em uma pasta

```bash
cd nome-da-pasta
```

## Voltar uma pasta

```bash
cd ..
```

## Limpar a tela

```bash
clear
```

## Criar uma pasta

```bash
mkdir nome-da-pasta
```

## Criar arquivo vazio

```bash
touch arquivo.txt
```

## Ler arquivo

```bash
cat arquivo.txt
```

## Ver arquivo com linhas numeradas

```bash
nl -ba arquivo.txt
```

---

# 16. Termux e Kali Linux

O projeto pode ser estudado em um ambiente Linux.

No Android, uma possibilidade é utilizar o Termux.

Também é possível utilizar Kali Linux em uma máquina virtual ou outro ambiente apropriado.

É importante entender a diferença entre:

- sistema operacional;
- terminal;
- shell;
- ambiente virtual;
- aplicação.

O Termux é um ambiente de terminal para Android.

O Kali Linux é uma distribuição Linux voltada para segurança e testes.

Você não precisa do Kali para aprender todos os conceitos do VulnForge.

---

# 17. Preparando o ambiente

Você precisa de:

- Python;
- Git;
- VulnForge;
- acesso a um laboratório autorizado.

No Termux, primeiro atualize os pacotes:

```bash
pkg update
```

Depois:

```bash
pkg upgrade
```

Instale Python:

```bash
pkg install python
```

Instale Git:

```bash
pkg install git
```

Confira:

```bash
python --version
```

e:

```bash
git --version
```

---

# 18. Obtendo o VulnForge

O repositório do projeto é:

```text
https://github.com/NT969/VulnForge
```

Para clonar:

```bash
git clone https://github.com/NT969/VulnForge.git
```

Entre na pasta:

```bash
cd VulnForge
```

Confira os arquivos:

```bash
ls
```

---

# 19. Instalando as dependências

O projeto utiliza dependências listadas em:

```text
requirements.txt
```

Instale com:

```bash
pip install -r requirements.txt
```

As principais bibliotecas utilizadas são:

- requests;
- beautifulsoup4.

---

# 20. Testando o Python

Antes de executar o projeto, teste:

```bash
python --version
```

Depois:

```bash
python -m py_compile vulnforge.py
```

Se não aparecer erro, a sintaxe do arquivo principal está correta.

Você também pode verificar os módulos:

```bash
python -m py_compile scanner/*.py
```

---

# 21. Criando um laboratório local

Uma das melhores formas de aprender é criar um ambiente local.

Assim você pode testar sem atingir sistemas de terceiros.

Entre na pasta do projeto:

```bash
cd ~/VulnForge
```

Inicie um servidor HTTP simples:

```bash
python -m http.server 8000
```

O servidor ficará disponível em:

```text
http://127.0.0.1:8000
```

`127.0.0.1` representa o próprio dispositivo.

---

# 22. O que é localhost?

`localhost` normalmente representa o próprio computador ou dispositivo.

O endereço:

```text
127.0.0.1
```

é um endereço de loopback IPv4.

Ele é muito útil para laboratórios locais.

Exemplo:

```text
http://127.0.0.1:8000
```

significa que o servidor está rodando localmente na porta 8000.

---

# 23. Executando o VulnForge

Com o laboratório funcionando, abra outro terminal.

Entre no projeto:

```bash
cd ~/VulnForge
```

Execute:

```bash
python vulnforge.py
```

O programa solicitará o alvo conforme a implementação atual.

Para um laboratório local, utilize um endereço como:

```text
http://127.0.0.1:8000
```

---

# 24. O fluxo do VulnForge

De maneira simplificada:

```text
ALVO
  |
  v
Verificação HTTP
  |
  v
Cabeçalhos
  |
  v
Crawler
  |
  v
Formulários
  |
  v
Testes ativos
  |
  v
Parâmetros
  |
  v
Endpoints
  |
  v
Relatórios
```

Esse fluxo ajuda a organizar o processo.

---

# 25. Descoberta de recursos

O crawler procura links internos.

Por exemplo:

```text
/
├── index.html
├── login.html
├── contato.html
└── produtos.html
```

O objetivo é montar uma visão inicial da aplicação.

O crawler atual possui limite de páginas e restringe a navegação ao mesmo domínio.

---

# 26. Limitação importante do crawler

Encontrar um arquivo não significa que ele seja uma vulnerabilidade.

Por exemplo:

```text
/.git/
```

ser encontrado durante o reconhecimento é uma informação importante.

Mas é necessário avaliar:

- se realmente está acessível;
- quais arquivos podem ser obtidos;
- qual o impacto;
- se isso está dentro do escopo;
- se existe risco real.

Ferramentas ajudam a encontrar pistas.

O profissional é responsável pela análise.

---

# 27. Descoberta de formulários

O VulnForge procura elementos HTML como:

```html
<form>
```

e identifica campos.

Exemplo:

```html
<form action="/login" method="POST">
    <input name="username">
    <input name="password">
    <input name="token">
</form>
```

O resultado pode indicar:

```text
username
password
token
```

---

# 28. Classificação de parâmetros

O módulo `input_analysis.py` ajuda a organizar parâmetros.

Exemplo:

```text
username  -> AUTENTICAÇÃO
password  -> AUTENTICAÇÃO
token     -> TOKEN
id        -> IDENTIFICADOR
q         -> BUSCA/FILTRO
```

Essa classificação não prova uma vulnerabilidade.

Ela ajuda o pentester a priorizar a investigação.

---

# 29. O que é um teste ativo?

Um teste ativo envia uma requisição modificada ao alvo.

Isso é diferente de simplesmente observar uma página.

No VulnForge, o teste ativo implementado é propositalmente simples e não destrutivo.

Ele utiliza um marcador único.

Exemplo:

```text
VULNFORGE_a1b2c3d4
```

O valor é enviado para um parâmetro.

Depois o VulnForge verifica se esse marcador aparece na resposta.

---

# 30. Reflexão de parâmetro

Imagine que o teste envia:

```text
username=VULNFORGE_123456
```

e o servidor responde:

```html
<p>Usuário recebido: VULNFORGE_123456</p>
```

O marcador foi refletido.

O relatório pode mostrar:

```text
Refletido: True
```

Isso significa:

> O valor enviado apareceu no conteúdo da resposta.

Não significa automaticamente:

> "Existe XSS".

A confirmação de uma vulnerabilidade específica exige testes adicionais e análise contextual.

---

# 31. Refletido True e False

## True

O marcador enviado apareceu na resposta.

## False

O marcador não apareceu na resposta.

Exemplo:

```text
Parâmetro: username
Refletido: True
```

Pode indicar que o valor está sendo devolvido pela aplicação.

Já:

```text
Parâmetro: password
Refletido: False
```

significa que o marcador não foi encontrado na resposta analisada.

Isso pode acontecer porque:

- o campo não é exibido;
- a aplicação ignora o valor;
- o valor é transformado;
- ocorre redirecionamento;
- a resposta não contém o valor;
- existe algum processamento intermediário.

---

# 32. Laboratório POST

O projeto possui:

```text
laboratorio_post.py
```

Ele cria um pequeno servidor HTTP local para estudar requisições POST.

Para iniciar:

```bash
python laboratorio_post.py
```

Ele utiliza:

```text
http://127.0.0.1:8081
```

O laboratório recebe campos como:

```text
username
password
token
```

e foi criado para demonstrar reflexão de entrada de maneira controlada.

---

# 33. Segurança do laboratório POST

O laboratório foi projetado para uso local.

Ele escuta em:

```text
127.0.0.1
```

Isso é diferente de colocar um servidor deliberadamente acessível pela rede.

Para estudos, prefira:

- localhost;
- máquinas virtuais;
- ambientes de treinamento;
- aplicações deliberadamente vulneráveis;
- sistemas onde você tenha autorização.

---

# 34. Testando o formulário local

Se o formulário estiver configurado para apontar ao laboratório POST, o VulnForge pode executar os testes ativos.

Exemplo de resultado:

```text
Testes ativos executados: 3
```

E:

```text
username -> POST -> HTTP 200 -> Refletido True
password -> POST -> HTTP 200 -> Refletido False
token    -> POST -> HTTP 200 -> Refletido False
```

Esse resultado é uma evidência do comportamento observado no laboratório.

---

# 35. Relatório TXT

O VulnForge gera relatório em texto.

Um relatório pode conter:

```text
ALVO
RECURSOS
FORMULÁRIOS
PARÂMETROS
ENDPOINTS
TESTES ATIVOS
VULNERABILIDADES
```

O TXT é útil para:

- terminal;
- logs;
- revisão rápida;
- armazenamento;
- comparação;
- automação futura.

---

# 36. Relatório HTML

O relatório HTML facilita a leitura no navegador.

Ele possui seções organizadas.

Os recursos podem ser expandidos.

Os formulários podem ser analisados.

Os parâmetros podem ser consultados.

Os testes ativos possuem informações como:

- URL;
- parâmetro;
- método;
- status HTTP;
- reflexão;
- marcador.

---

# 37. Onde ficam os relatórios?

Os relatórios são armazenados na pasta:

```text
reports/
```

Exemplo:

```text
reports/scan_20260910_163657.txt
```

e:

```text
reports/scan_20260910_163657.html
```

Os relatórios podem também ser copiados para outro diretório para consulta.

---

# 38. Como abrir um relatório HTML

Uma maneira simples é utilizar um servidor HTTP local.

Por exemplo:

```bash
python -m http.server 8090 --directory ~/storage/downloads
```

Depois abra no navegador:

```text
http://127.0.0.1:8090
```

Escolha o relatório HTML.

Se a porta estiver ocupada, utilize outra porta livre.

Exemplo:

```bash
python -m http.server 8091 --directory ~/storage/downloads
```

---

# 39. O que observar em um relatório

Não leia apenas o número de descobertas.

Observe:

### Alvo

Confirme se o endereço analisado está correto.

### Status HTTP

Veja como o servidor respondeu.

### Recursos

Entenda a superfície encontrada.

### Formulários

Veja quais entradas existem.

### Parâmetros

Identifique pontos de entrada.

### Endpoints

Observe os caminhos encontrados.

### Testes ativos

Analise o comportamento das entradas.

### Vulnerabilidades

Leia descrição, severidade e recomendação.

---

# 40. Severidade

O VulnForge pode classificar achados por níveis como:

```text
INFO
LOW
MEDIUM
HIGH
CRITICAL
```

A classificação deve ser interpretada com cuidado.

Um cabeçalho ausente, por exemplo, pode ter impacto menor que uma falha de autenticação.

A severidade final em um Pentest profissional deve considerar:

- impacto;
- possibilidade de exploração;
- exposição;
- contexto;
- dados envolvidos;
- privilégios;
- facilidade de exploração.

---

# 41. Cabeçalhos de segurança

O módulo de cabeçalhos verifica itens como:

```text
Content-Security-Policy
X-Frame-Options
X-Content-Type-Options
Strict-Transport-Security
Referrer-Policy
Permissions-Policy
```

Esses cabeçalhos podem ajudar a reduzir determinados riscos.

Porém, ausência de um cabeçalho não significa automaticamente comprometimento do sistema.

---

# 42. Content-Security-Policy

O CSP pode ajudar a controlar quais recursos uma página pode carregar ou executar.

É um mecanismo importante para reduzir determinadas classes de ataques, especialmente relacionados à execução de conteúdo não confiável.

O CSP deve ser configurado de acordo com a aplicação.

---

# 43. X-Frame-Options

Esse cabeçalho ajuda a controlar se uma página pode ser carregada dentro de frames.

Uma configuração adequada pode ajudar contra determinados cenários de clickjacking.

---

# 44. X-Content-Type-Options

Uma configuração comum é:

```text
nosniff
```

Ela ajuda o navegador a respeitar o tipo de conteúdo declarado.

---

# 45. Strict-Transport-Security

Também conhecido como HSTS.

É utilizado para instruir navegadores a preferirem HTTPS em determinados cenários.

Ele deve ser configurado corretamente e usado com HTTPS.

---

# 46. Referrer-Policy

Controla informações de referência enviadas pelo navegador em determinadas requisições.

Uma política adequada pode reduzir exposição desnecessária de informações.

---

# 47. Permissions-Policy

Permite controlar determinados recursos e capacidades disponíveis para documentos e contextos incorporados.

A configuração depende da necessidade da aplicação.

---

# 48. O que o VulnForge NÃO faz

O VulnForge atual não deve ser tratado como uma ferramenta completa de exploração.

Ele não substitui:

- Burp Suite;
- testes manuais;
- análise de código;
- conhecimento de HTTP;
- análise de autenticação;
- validação de autorização;
- revisão de arquitetura;
- conhecimento de vulnerabilidades.

Ele é uma base de reconhecimento e análise.

---

# 49. Por que testes manuais são importantes?

Ferramentas automatizadas trabalham com regras.

Uma aplicação real pode ter comportamentos que uma ferramenta não entende.

O pentester precisa pensar:

```text
O que acontece se eu alterar este parâmetro?
```

```text
Este usuário pode acessar este recurso?
```

```text
Existe diferença entre usuário comum e administrador?
```

```text
O servidor está validando a autorização?
```

Essas perguntas exigem raciocínio.

---

# 50. Burp Suite

O Burp Suite é uma das ferramentas mais importantes para testes de aplicações web.

Ele permite estudar:

- requisições;
- respostas;
- parâmetros;
- cookies;
- headers;
- sessões;
- autenticação;
- APIs;
- comportamento da aplicação.

Uma ferramenta como o Burp complementa o VulnForge.

Um fluxo de estudo pode ser:

```text
VulnForge
   ↓
Reconhecimento
   ↓
Burp Suite
   ↓
Análise manual
   ↓
Validação
   ↓
Relatório
```

---

# 51. Aprendendo HTTP antes de atacar

Antes de estudar exploração, aprenda:

- GET;
- POST;
- PUT;
- DELETE;
- PATCH;
- headers;
- cookies;
- sessões;
- status codes;
- query string;
- body;
- JSON;
- URL encoding;
- redirects.

Sem entender HTTP, muitas ferramentas parecem apenas uma sequência de botões.

---

# 52. Python para Pentest

Python é muito útil para segurança.

Você pode usar Python para:

- automatizar tarefas;
- processar respostas;
- criar scanners;
- analisar arquivos;
- criar clientes HTTP;
- manipular JSON;
- trabalhar com sockets;
- gerar relatórios.

No VulnForge, Python é utilizado para integrar essas ideias.

---

# 53. Conceitos de Python importantes

Comece por:

```text
variáveis
tipos
if
for
while
funções
listas
dicionários
sets
exceções
módulos
classes
```

Depois estude:

```text
requests
BeautifulSoup
urllib
JSON
regex
arquivos
logging
argparse
```

---

# 54. Exemplo simples de Python

```python
nome = "VulnForge"

if nome:
    print("Projeto:", nome)
```

Outro:

```python
for numero in range(5):
    print(numero)
```

O objetivo não é decorar.

É entender a lógica.

---

# 55. Exemplo de requisição HTTP em Python

Uma ideia básica:

```python
import requests

resposta = requests.get(
    "http://127.0.0.1:8000",
    timeout=10
)

print(resposta.status_code)
```

Isso mostra como um programa pode conversar com um servidor HTTP.

---

# 56. Tratamento de erros

Aplicações de segurança precisam tratar erros.

Exemplo:

```python
try:
    resposta = requests.get(
        "http://127.0.0.1:8000",
        timeout=10
    )
except requests.RequestException as erro:
    print("Erro:", erro)
```

Isso evita que um erro de rede derrube todo o programa.

---

# 57. Git

Git é utilizado para controlar versões do código.

Comandos básicos:

```bash
git status
```

Ver alterações.

```bash
git add .
```

Adicionar alterações.

```bash
git commit -m "mensagem"
```

Criar commit.

```bash
git push
```

Enviar alterações ao repositório remoto.

---

# 58. Verificando alterações

Antes de fazer commit:

```bash
git status
```

Depois:

```bash
git diff
```

Uma prática importante é revisar o que será enviado.

Não coloque no GitHub:

- senhas;
- tokens;
- chaves privadas;
- credenciais;
- dados pessoais;
- arquivos de clientes;
- relatórios confidenciais.

---

# 59. .gitignore

O projeto possui um `.gitignore`.

Exemplo:

```text
__pycache__/
*.pyc
reports/
```

Isso ajuda a evitar que determinados arquivos sejam enviados ao Git.

Relatórios reais de clientes nunca devem ser publicados em repositório público.

---

# 60. Estrutura profissional de um Pentest

Um Pentest normalmente pode ser dividido em:

```text
1. Autorização
2. Escopo
3. Reconhecimento
4. Enumeração
5. Análise
6. Validação
7. Exploração controlada
8. Pós-exploração autorizada
9. Evidências
10. Relatório
11. Reteste
```

Nem todo projeto utiliza exatamente essa ordem.

O processo depende do escopo.

---

# 61. Escopo

Escopo define o que pode ser testado.

Exemplo:

```text
Permitido:
app.exemplo.com
api.exemplo.com

Não permitido:
portal.exemplo.com
infra.exemplo.com
sistema de terceiros
```

Mesmo que você descubra um endereço fora do escopo, não significa que pode testá-lo.

---

# 62. Rules of Engagement

As Rules of Engagement, ou regras de engajamento, definem como o teste deve ocorrer.

Podem estabelecer:

- horários;
- limites;
- contatos;
- técnicas permitidas;
- técnicas proibidas;
- tratamento de dados;
- limites de impacto;
- procedimentos para incidentes.

Um pentester profissional respeita essas regras.

---

# 63. Testes destrutivos

Evite ações que possam:

- derrubar serviços;
- apagar dados;
- modificar dados reais;
- causar indisponibilidade;
- bloquear usuários;
- gerar custos inesperados.

Se um teste de maior impacto for necessário, ele deve estar explicitamente autorizado e planejado.

O VulnForge prioriza testes não destrutivos nesta etapa.

---

# 64. Falsos positivos

Um falso positivo ocorre quando uma ferramenta indica algo que parece ser um problema, mas a análise mostra que não existe vulnerabilidade real.

Exemplo:

```text
Cabeçalho ausente
```

Isso pode ser uma recomendação de segurança.

Mas não significa necessariamente que um atacante conseguirá comprometer o sistema.

Por isso:

> ferramenta encontra sinais; profissional confirma.

---

# 65. Falsos negativos

Um falso negativo ocorre quando existe um problema, mas a ferramenta não o identifica.

Isso pode acontecer porque:

- o scanner não possui aquela técnica;
- a aplicação é muito complexa;
- a vulnerabilidade depende de lógica;
- a autenticação é necessária;
- o comportamento depende de estado;
- existe uma API específica;
- o parâmetro está oculto.

Por isso Pentest não deve depender de uma única ferramenta.

---

# 66. Como interpretar um achado

Para cada achado, pergunte:

### O que foi encontrado?

Descreva o comportamento.

### Onde?

URL, endpoint, parâmetro ou recurso.

### Como foi identificado?

Descreva a técnica.

### É reproduzível?

Confirme novamente quando apropriado.

### Qual o impacto?

Explique o risco.

### Como corrigir?

Apresente uma recomendação.

---

# 67. Exemplo de evidência

Em um laboratório:

```text
URL:
http://127.0.0.1:8000/teste

Parâmetro:
q

Marcador:
VULNFORGE_123456

Resultado:
Refletido = True
```

Essa evidência demonstra reflexão.

Para afirmar uma vulnerabilidade específica, ainda é necessário analisar o contexto.

---

# 68. Boas práticas durante os testes

Sempre:

- confirme o alvo;
- confirme o escopo;
- faça backup quando autorizado;
- registre suas ações;
- evite alterações desnecessárias;
- utilize identificadores únicos;
- documente evidências;
- mantenha os testes reproduzíveis;
- respeite limites de velocidade;
- comunique incidentes.

---

# 69. O que estudar depois do VulnForge

Uma trilha recomendada:

## Etapa 1 — Linux

Aprenda:

```text
terminal
arquivos
permissões
processos
rede
SSH
grep
find
curl
```

## Etapa 2 — Redes

Aprenda:

```text
IP
TCP
UDP
DNS
HTTP
HTTPS
portas
sockets
NAT
```

## Etapa 3 — Web

Aprenda:

```text
HTML
CSS
JavaScript
HTTP
cookies
sessões
APIs
JSON
```

## Etapa 4 — Python

Aprenda programação e automação.

## Etapa 5 — Segurança Web

Estude o OWASP Top 10 e vulnerabilidades relacionadas a aplicações web.

---

# 70. OWASP Top 10

O OWASP Top 10 é uma referência importante para estudar segurança de aplicações web.

Entre os temas estudados estão categorias relacionadas a:

- controle de acesso;
- falhas criptográficas;
- injeção;
- design inseguro;
- configuração insegura;
- componentes vulneráveis;
- autenticação;
- integridade;
- logging e monitoramento;
- tratamento de exceções.

Use a documentação oficial do OWASP como referência atualizada durante seus estudos.

---

# 71. Laboratórios para aprender

Prefira ambientes criados para treinamento.

Exemplos conhecidos incluem:

- OWASP Juice Shop;
- PortSwigger Web Security Academy;
- DVWA;
- máquinas de laboratório;
- aplicações deliberadamente vulneráveis;
- CTFs autorizados.

Esses ambientes permitem aprender exploração sem atacar terceiros.

---

# 72. Metodologia de estudo

Não tente aprender tudo em uma semana.

Uma rotina eficiente:

```text
30 min — teoria
30 min — prática
30 min — laboratório
30 min — revisão
```

O mais importante é consistência.

---

# 73. Como estudar uma vulnerabilidade

Para cada vulnerabilidade:

```text
1. O que é?
2. Por que acontece?
3. Como identificar?
4. Como reproduzir em laboratório?
5. Qual o impacto?
6. Como corrigir?
7. Como detectar novamente?
```

Essa abordagem cria conhecimento real.

---

# 74. Mentalidade de um pentester

Um bom profissional não pensa:

> "Como eu invado?"

Ele pensa:

> "Qual comportamento inseguro existe aqui e como posso demonstrá-lo de maneira controlada?"

Depois:

> "Qual é o impacto?"

E finalmente:

> "Como isso pode ser corrigido?"

---

# 75. Documentação é parte do Pentest

Se você encontrou algo importante, registre.

Anote:

```text
data
hora
alvo
endpoint
parâmetro
requisição
resposta
resultado
impacto
evidência
correção
```

Uma descoberta que não pode ser reproduzida é muito menos útil.

---

# 76. Problemas comuns

## Python não encontrado

Verifique:

```bash
python --version
```

Se necessário, instale Python.

---

## Git não encontrado

Verifique:

```bash
git --version
```

No Termux:

```bash
pkg install git
```

---

## Dependência faltando

Execute:

```bash
pip install -r requirements.txt
```

---

## Porta ocupada

Se aparecer:

```text
Address already in use
```

significa que a porta já está sendo utilizada.

Escolha outra porta, por exemplo:

```bash
python -m http.server 8090
```

---

# 77. Verificando processos Python

Não mate processos aleatoriamente.

Primeiro investigue.

Você pode verificar processos Python com:

```bash
ps -A | grep python
```

Observe qual processo está rodando.

Se você iniciou um servidor em determinado terminal, normalmente pode encerrá-lo com:

```text
CTRL+C
```

Isso é mais seguro do que matar processos sem saber o que estão fazendo.

---

# 78. Erros de sintaxe Python

Se houver erro:

```text
SyntaxError
```

compile o arquivo:

```bash
python -m py_compile vulnforge.py
```

Para módulos:

```bash
python -m py_compile scanner/*.py
```

Para investigar linhas:

```bash
nl -ba vulnforge.py
```

Isso mostra os números das linhas.

---

# 79. Erros HTTP

Se o VulnForge retornar um código inesperado:

1. teste a URL no navegador;
2. teste com `curl`;
3. confirme se o servidor está funcionando;
4. confira a porta;
5. confira o método HTTP;
6. confira o formulário;
7. confira o endpoint.

Exemplo:

```bash
curl -i http://127.0.0.1:8000
```

---

# 80. Como usar curl para estudar HTTP

Um GET simples:

```bash
curl -i http://127.0.0.1:8000
```

O `-i` mostra os cabeçalhos da resposta.

Isso é excelente para aprender HTTP.

Para POST em um laboratório autorizado:

```bash
curl -i -X POST \
  -d "username=teste" \
  http://127.0.0.1:8081/login
```

Use somente contra o laboratório ou alvo autorizado.

---

# 81. Entendendo portas

Uma porta identifica um serviço dentro de uma máquina.

Exemplo:

```text
127.0.0.1:8000
```

Significa:

```text
IP: 127.0.0.1
Porta: 8000
```

No laboratório:

```text
8000
```

pode ser usado pelo servidor HTML.

Enquanto:

```text
8081
```

pode ser usado pelo laboratório POST.

---

# 82. Por que usar portas diferentes?

Porque dois serviços não podem normalmente ocupar a mesma combinação de endereço e porta ao mesmo tempo.

Por isso:

```text
127.0.0.1:8000
```

e:

```text
127.0.0.1:8081
```

podem representar serviços diferentes.

---

# 83. Como melhorar o VulnForge no futuro

Possíveis evoluções:

- suporte a autenticação autorizada;
- configuração de escopo;
- rate limiting;
- timeout configurável;
- exportação JSON;
- configuração via argumentos;
- logging;
- fingerprints de tecnologias;
- análise de APIs;
- suporte a OpenAPI;
- melhor classificação de achados;
- evidências detalhadas;
- comparação entre scans;
- testes adicionais não destrutivos;
- interface gráfica.

Cada recurso novo deve ser implementado com segurança e controle de escopo.

---

# 84. Arquitetura modular

A separação dos módulos permite evoluir o projeto.

Por exemplo:

```text
target.py
```

cuida do alvo.

```text
crawler.py
```

cuida do crawling.

```text
forms.py
```

cuida dos formulários.

```text
active.py
```

cuida dos testes ativos.

Isso facilita:

- manutenção;
- testes;
- correções;
- expansão;
- aprendizado.

---

# 85. Como contribuir com o projeto

Antes de alterar o código:

```bash
git status
```

Depois faça a alteração.

Teste:

```bash
python -m py_compile vulnforge.py
python -m py_compile scanner/*.py
```

Depois:

```bash
git diff
```

Se estiver tudo correto:

```bash
git add .
git commit -m "descreva a alteração"
git push
```

---

# 86. Checklist antes de executar

Antes de qualquer teste:

```text
[ ] Tenho autorização?
[ ] O alvo está no escopo?
[ ] Sei exatamente qual URL testar?
[ ] O horário está autorizado?
[ ] A técnica é permitida?
[ ] Existe risco de indisponibilidade?
[ ] Tenho um laboratório caso seja necessário?
[ ] Estou registrando os resultados?
```

Se alguma resposta for "não", pare e esclareça antes de continuar.

---

# 87. Checklist do laboratório

```text
[ ] Python instalado
[ ] Git instalado
[ ] VulnForge instalado
[ ] Dependências instaladas
[ ] Servidor local funcionando
[ ] Porta correta
[ ] Formulário correto
[ ] Laboratório POST funcionando
[ ] Relatório sendo gerado
```

---

# 88. Checklist de análise

```text
[ ] Alvo
[ ] Recursos
[ ] Formulários
[ ] Parâmetros
[ ] Endpoints
[ ] Cabeçalhos
[ ] Testes ativos
[ ] Evidências
[ ] Impacto
[ ] Recomendações
```

---

# 89. Glossário

## Endpoint

Um caminho ou recurso acessível por uma aplicação.

Exemplo:

```text
/api/users
```

## Parâmetro

Valor enviado para uma aplicação.

## Payload

Dados utilizados durante um teste.

## Request

Requisição enviada ao servidor.

## Response

Resposta recebida do servidor.

## Crawler

Ferramenta que percorre recursos e links.

## Recon

Abreviação comum para reconnaissance.

## Scope

Escopo autorizado do teste.

## Finding

Achado identificado durante a análise.

## False Positive

Resultado indicado como problema, mas que não representa uma vulnerabilidade real após validação.

## False Negative

Vulnerabilidade existente que não foi identificada pela ferramenta.

---

# 90. O caminho para virar Pentester

Uma possível evolução:

```text
Linux
  ↓
Redes
  ↓
HTTP
  ↓
Web
  ↓
Python
  ↓
OWASP
  ↓
Burp Suite
  ↓
Laboratórios
  ↓
Pentest Web
  ↓
APIs
  ↓
Active Directory
  ↓
Red Team
```

Não é obrigatório seguir exatamente essa ordem.

Mas os fundamentos são importantes.

---

# 91. O que estudar para Red Team

Depois dos fundamentos de Pentest, você pode estudar:

- redes;
- Windows;
- Active Directory;
- Linux;
- PowerShell;
- Python;
- segurança web;
- APIs;
- cloud;
- identidade;
- detecção;
- logs;
- evasão em ambientes de laboratório;
- operações de Red Team.

Sempre pratique em ambientes autorizados.

---

# 92. Certificações

Depois de construir uma boa base, algumas pessoas estudam para certificações.

Exemplos de áreas:

- fundamentos de segurança;
- segurança de redes;
- Pentest;
- web security;
- Red Team;
- Active Directory.

Não comece pelas certificações sem construir fundamentos.

Conhecimento prático e capacidade de explicar o que você fez são muito importantes.

---

# 93. Como montar um portfólio

Um projeto como o VulnForge pode fazer parte de um portfólio.

Mostre:

- objetivo;
- arquitetura;
- código;
- testes;
- laboratório;
- relatórios de exemplo;
- documentação;
- limitações;
- melhorias futuras.

Nunca publique dados de clientes ou informações confidenciais.

---

# 94. Exemplo de projeto de portfólio

Você pode demonstrar:

```text
1. Laboratório local
2. Aplicação de teste
3. Reconhecimento
4. Descoberta de formulário
5. Descoberta de parâmetros
6. Teste ativo não destrutivo
7. Análise manual
8. Relatório
9. Correção
10. Reteste
```

Isso demonstra mais maturidade do que simplesmente mostrar uma ferramenta executando comandos.

---

# 95. A regra de ouro

Guarde esta frase:

> **Não teste porque você consegue. Teste porque você tem autorização.**

E outra:

> **Não confunda resultado de ferramenta com vulnerabilidade confirmada.**

Essas duas ideias são fundamentais para quem quer trabalhar profissionalmente com segurança ofensiva.

---

# 96. Resumo do VulnForge

O VulnForge atualmente ajuda a:

- verificar um alvo HTTP;
- coletar informações básicas;
- analisar cabeçalhos;
- descobrir recursos;
- descobrir formulários;
- identificar parâmetros;
- classificar entradas;
- descobrir endpoints;
- executar testes ativos não destrutivos;
- verificar reflexão de parâmetros;
- gerar relatórios TXT;
- gerar relatórios HTML.

Ele deve ser utilizado como ferramenta de apoio.

---

# 97. Resumo do aprendizado

Se você chegou até aqui, já conhece conceitos fundamentais:

```text
HTTP
URL
GET
POST
Parâmetros
Formulários
Endpoints
Crawler
Headers
Reconhecimento
Teste ativo
Reflexão
Relatório
Escopo
Autorização
Pentest
```

O próximo passo é praticar.

---

# 98. Exercício 1 — Servidor local

Execute:

```bash
python -m http.server 8000
```

Abra:

```text
http://127.0.0.1:8000
```

Observe os recursos.

Depois utilize o VulnForge no laboratório.

---

# 99. Exercício 2 — Formulário

Analise um formulário local.

Identifique:

```text
action
method
username
password
token
```

Depois observe como o VulnForge registra esses campos.

---

# 100. Exercício 3 — Reflexão

Utilize o laboratório POST.

Observe:

```text
username -> refletido
password -> não refletido
token -> não refletido
```

Tente explicar por que os resultados são diferentes.

A resposta está no comportamento do servidor.

---

# 101. Exercício 4 — Relatório

Abra o relatório HTML.

Procure:

```text
Recursos
Formulários
Parâmetros
Endpoints
Testes ativos
Vulnerabilidades
```

Tente explicar cada seção com suas próprias palavras.

---

# 102. Exercício 5 — Pensamento de Pentester

Escolha um parâmetro de laboratório e responda:

```text
Qual é o nome?
Onde ele aparece?
Qual método é utilizado?
Qual é a resposta HTTP?
O valor é refletido?
Qual seria o próximo teste seguro?
```

Esse exercício desenvolve raciocínio.

---

# 103. Próximo nível

Depois de dominar o VulnForge, avance para:

```text
HTTP profundo
↓
Burp Suite
↓
OWASP
↓
Juice Shop
↓
PortSwigger Academy
↓
APIs
↓
Autenticação
↓
Autorização
↓
Pentest profissional
```

Depois:

```text
Windows
↓
Active Directory
↓
PowerShell
↓
Red Team
```

---

# 104. Conclusão

O VulnForge não foi criado para substituir o conhecimento do pentester.

Ele foi criado para ajudar a construir esse conhecimento.

Aprender segurança ofensiva é aprender a:

- observar;
- questionar;
- testar;
- validar;
- documentar;
- corrigir.

Comece pequeno.

Use laboratórios.

Aprenda os fundamentos.

Depois aumente a complexidade.

E sempre respeite autorização e escopo.

---

# 105. Referência rápida de comandos

## Entrar no projeto

```bash
cd ~/VulnForge
```

## Listar arquivos

```bash
ls
```

## Ver status Git

```bash
git status
```

## Instalar dependências

```bash
pip install -r requirements.txt
```

## Validar Python

```bash
python -m py_compile vulnforge.py
```

## Validar módulos

```bash
python -m py_compile scanner/*.py
```

## Servidor HTTP local

```bash
python -m http.server 8000
```

## Laboratório POST

```bash
python laboratorio_post.py
```

## Servidor para visualizar Downloads

```bash
python -m http.server 8090 --directory ~/storage/downloads
```

## Testar HTTP

```bash
curl -i http://127.0.0.1:8000
```

---

# 106. Comandos Git rápidos

```bash
git status
```

```bash
git diff
```

```bash
git add .
```

```bash
git commit -m "mensagem"
```

```bash
git push
```

---

# 107. Último conselho

Não tenha pressa para decorar comandos.

Entenda o que cada comando faz.

Quando aparecer um erro:

1. leia;
2. descubra em qual arquivo ocorreu;
3. veja a linha;
4. entenda a causa;
5. corrija;
6. teste novamente;
7. documente.

É assim que você deixa de apenas copiar comandos e começa a pensar como profissional.

---

# 108. Aviso de segurança

Este manual é educacional.

As técnicas descritas devem ser utilizadas somente:

- em sistemas próprios;
- em laboratórios;
- em CTFs autorizados;
- em ambientes de treinamento;
- ou em sistemas para os quais exista autorização explícita.

O usuário é responsável por garantir que possui permissão para realizar qualquer teste.

---

# 109. Fim

**VulnForge — Reconhecimento, aprendizado e segurança ofensiva responsável.**

Aprenda.

Pratique.

Documente.

Evolua.

Sempre com autorização.
