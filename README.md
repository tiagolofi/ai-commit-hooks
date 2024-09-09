# ai-commit-hooks
Analisando commits com o ChatGPT

### Padrões de Commit

A base do prompt usada é explorada aqui em [iuricode/padroes-de-commit](https://github.com/iuricode/padroes-de-commits).

> _De acordo com a documentação do Conventional Commits, commits semânticos são uma convenção simples para ser utilizada nas mensagens de commit. Essa convenção define um conjunto de regras para criar um histórico de commit explícito, o que facilita a criação de ferramentas automatizadas._

### Pré-requisitos

- Git/Git Bash
- Chave de API da Open AI

### Configurando

1. Rode o projeto [AI Commits Hooks API](https://github.com/tiagolofi/ai-commit-hooks-api);

2. Gere e aprove seus tokens de consumo em `/q/api-docs`;

2. Adicione o arquivo `prepare-commit-msg` no diretório `.git/hooks/`.

```bash
#!/bin/sh
COMMIT_MSG_FILE=$1

GIT_DIFF=$(git diff --staged)

API_RESPONSE=$(
    curl -X 'POST' \
    'http://localhost:8080/commit/gpt-4o-mini' \
    -H 'Token-Consumo: SEU_TOKEN_GERADO_NA_APLICACAO' \
    -H 'Content-Type: text/plain' \
    -d "$GIT_DIFF"
)

COMMIT=$(echo $API_RESPONSE | grep -o '"respostaGPT4oMini": *"[^"]*"' | awk -F'"' '{print $4}')

echo "$COMMIT" > temp_msg
cat "$COMMIT_MSG_FILE" >> temp_msg
mv temp_msg "$COMMIT_MSG_FILE"
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")
if [[ -z "$COMMIT_MSG" || "$COMMIT_MSG" =~ ^[[:space:]]*$ ]]; then
    exit 1 # erro: mensagem vazia
fi
```

### Como isso funciona

![](ai-commit-dark.png)

**OBS**: no vscode é possível stagear as alterações sem utilizar diretamente `git add`. Este por sua vez, é acionado por trás dos panos.

### Features (em breve)

| Feature | O que é | Feito |
|:--------|:--------|:-----:|
| **Acompanhar a evolução dos modelos** | Trabalhar com outros tipos de contrato disponibilizados pela OpenAI | [ ] |
| **Retirar acoplamento ao Python** | Construir um tratamento de texto do `git diff` (pode se mostrar bastante complexo), sem utilizar utilitários como o `jq`. | [x] |
| **Serviço que gera os commits** | Executa uma chamada via curl com um contrato muito simples (não será application/json). | [x] | 

