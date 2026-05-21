# python-api-lab

Repositório de estudos práticos desenvolvido durante o curso **"Claude e Python: desenvolva assistentes com a API da Anthropic"** da Alura.

## Sobre o curso

| | |
|---|---|
| **Instrutora** | [Laís Urano](https://br.linkedin.com/in/laís-urano-9a41451b3) |
| **Carga horária** | 8h |
| **Plataforma** | [Alura](https://www.alura.com.br) |

### Módulos

| # | Módulo | Duração |
|---|--------|---------|
| 1 | Console e API da Anthropic | 19 min |
| 2 | Prompt Engineering e Prompt Template | 30 min |
| 3 | Verificando custos e tokens utilizados | 18 min |
| 4 | Controle de erros | 22 min |
| 5 | Análise de fraudes | 20 min |

---

## Conceitos aprendidos

### Console e API da Anthropic
- Navegação no [Anthropic Console](https://console.anthropic.com) para criar assistentes e testar prompts
- Geração e gestão de chaves de API
- Inicialização do cliente `anthropic.Anthropic()` com autenticação via variável de ambiente
- Estrutura da chamada `client.messages.create()`: `model`, `max_tokens`, `system`, `messages`
- Leitura da resposta em `message.content[0].text`

### Prompt Engineering e Prompt Template
- **System prompt**: instrução de papel e comportamento do assistente
- **Prompt template**: uso de f-strings para injetar variáveis dinâmicas no prompt
- **Formato de saída**: especificação explícita do formato esperado (estrutura, campos, unidades)
- **Few-shot examples**: inclusão de exemplos dentro do prompt para guiar o modelo
- **Temperature**: uso de `temperature=0` para respostas determinísticas e reprodutíveis
- Seleção de modelo por custo: `claude-haiku` para tarefas simples, `claude-sonnet` para análises complexas

### Verificando custos e tokens utilizados
- Acesso ao objeto `response.usage` para monitorar consumo
- `usage.input_tokens`: tokens enviados (prompt + system)
- `usage.output_tokens`: tokens gerados pelo modelo
- Estratégia de escolha de modelo baseada no custo por token

### Controle de erros
- `anthropic.APIConnectionError`: falha de conexão com o servidor
- `anthropic.RateLimitError`: limite de requisições atingido (HTTP 429)
- `anthropic.APIStatusError`: outros erros HTTP (com acesso a `e.status_code` e `e.response`)
- Bloco `try/except` genérico como fallback final

### Análise em lote (batch processing)
- Leitura de arquivos externos com função utilitária (`carrega`)
- Persistência de resultados em arquivos com função utilitária (`salva`)
- Iteração sobre listas para processar múltiplos itens em sequência
- Pipeline encadeado: saída de uma etapa alimenta a próxima

---

## Projetos

### `main.py`
Primeira chamada à API da Anthropic. Solicita ao modelo uma lista de alimentos relacionados a um ingrediente.

**Conceitos**: autenticação, `messages.create()`, leitura de resposta.

---

### `base.py`
Template base reutilizável para qualquer chamada à API, com `system prompt`, `user prompt`, `model`, `max_tokens` e `temperature` já estruturados.

**Conceitos**: estrutura padrão de uma chamada à API.

---

### `categorizador.py`
Categoriza alimentos em categorias definidas pelo usuário via input interativo (`while True`). Utiliza `claude-haiku` por ser uma tarefa simples e de baixo custo.

**Conceitos**: prompt template com variáveis, formato de saída, few-shot example, seleção de modelo por custo, loop interativo.

```
$ python categorizador.py
Digite as categorias válidas, separadas por vírgula: Bebida, Comida Salgada, Comida Doce
Digite o nome do alimento, ou 'sair' para encerrar: Coca-Cola
Produto: Coca-Cola
Categoria: Bebida
```

---

### `identificador_de_perfil.py`
Lê uma lista de 100 clientes com seus históricos de consumo alimentar (CSV) e identifica o perfil de cada um em até 3 palavras. Exibe os tokens consumidos ao final.

**Conceitos**: leitura de arquivo, `temperature=0`, monitoramento de tokens (`input_tokens`, `output_tokens`).

```
$ python identificador_de_perfil.py
...
Tokens de entrada 3200
Tokens de saída 450
```

---

### `analisador_de_sentimentos.py`
Processa avaliações de restaurantes a partir de arquivos `.txt` e gera uma análise com: resumo, sentimento geral (Positivo / Negativo / Neutro), 3 pontos fortes e 3 pontos fracos. O resultado é salvo em arquivo.

**Conceitos**: leitura e escrita de arquivos, processamento em lote, controle de erros (`APIConnectionError`, `RateLimitError`, `APIStatusError`).

```
$ python analisador_de_sentimentos.py
Iniciando análise de sentimentos para o restaurante: Restaurante de Comida Chinesa
Análise de sentimentos concluída com sucesso para o restaurante: Restaurante de Comida Chinesa
...
```

Arquivos gerados em `dados/avaliacoes/analise-<nome>.txt`.

---

### `analisador_de_transacoes.py`
Pipeline financeiro com três etapas encadeadas para detecção e tratamento de fraudes:

```
transacoes.csv
     │
     ▼
[1] analisador_de_transacoes()  →  transacoes.json
     │ (filtra status "Possível Fraude")
     ▼
[2] gerar_relatorio()           →  parecer-<id>-<produto>-<status>.json
     │
     ▼
[3] gerar_recomendacao()        →  recomendacao-<id>-<produto>-<status>.json
```

**Etapa 1 — Identificação de fraudes**: analisa o CSV e classifica cada transação como `"Aprovado"` ou `"Possível Fraude"` com base em valores discrepantes e localização geográfica.

**Etapa 2 — Parecer**: para cada transação suspeita, gera um parecer JSON com justificativa da fraude.

**Etapa 3 — Recomendação**: com base no parecer, gera recomendação técnica (`"Notificar Cliente"`, `"Acionar setor Anti-Fraude"` ou `"Realizar Verificação Manual"`) e classifica o tipo de fraude.

**Conceitos**: pipeline multi-etapa, parsing e limpeza de JSON (`removeprefix("```json")`), escrita de arquivos, controle de erros, função auxiliar `chamar_api()` reutilizável.

---

### `helpers.py`
Funções utilitárias de I/O usadas pelos scripts acima.

```python
carrega(nome_do_arquivo)  # lê e retorna o conteúdo de um arquivo
salva(nome_do_arquivo, conteudo)  # escreve conteúdo em um arquivo
```

---

## Tecnologias

- Python 3.12
- [Anthropic SDK](https://github.com/anthropics/anthropic-sdk-python) — `anthropic`
- `python-dotenv` — gestão de variáveis de ambiente

### Modelos utilizados

| Modelo | Uso |
|--------|-----|
| `claude-sonnet-4-6` | Análises complexas (sentimentos, fraudes, perfil) |
| `claude-haiku-4-5` | Tarefas simples e de baixo custo (categorizador) |

---

## Configuração

### 1. Variável de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
ANTHROPIC_API_KEY=sua_chave_aqui
```

> Ou configure como secret no GitHub Codespaces em **Settings → Codespaces → Secrets**.

### 2. Instalação das dependências

```bash
pip install anthropic python-dotenv
```

### 3. Execução

```bash
python main.py
python categorizador.py
python identificador_de_perfil.py
python analisador_de_sentimentos.py
python analisador_de_transacoes.py
```

---

## Estrutura do repositório

```
python-api-lab/
├── dados/
│   ├── avaliacoes/
│   │   ├── avaliacoes-Restaurante de Comida Chinesa.txt
│   │   ├── avaliacoes-Restaurante de Bolos e Doces.txt
│   │   ├── avaliacoes-Restaurante de Comida Vegana.txt
│   │   ├── analise-Restaurante de Comida Chinesa.txt   # gerado
│   │   ├── analise-Restaurante de Bolos e Doces.txt    # gerado
│   │   └── analise-Restaurante de Comida Vegana.txt    # gerado
│   └── lista_de_consumo/
│       ├── lista_de_consumo_100_clientes.csv
│       └── lista_de_consumo_100_clientes.txt
├── main.py                          # 1ª chamada à API
├── base.py                          # template base reutilizável
├── categorizador.py                 # categorização interativa de alimentos
├── identificador_de_perfil.py       # perfil de consumo + monitoramento de tokens
├── analisador_de_sentimentos.py     # análise de sentimentos em lote
├── analisador_de_transacoes.py      # pipeline de detecção de fraudes
├── helpers.py                       # funções utilitárias de I/O
├── transacoes.csv                   # dados de entrada do pipeline
├── transacoes.json                  # gerado pelo pipeline
├── parecer-*.json                   # gerados pelo pipeline
├── recomendacao-*.json              # gerados pelo pipeline
├── .env                             # não versionado
└── .gitignore
```

---

## Autor

[Everson Rubira](https://github.com/EversonRubira)
