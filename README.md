# python-api-lab

Repositório de estudos práticos desenvolvido durante o curso **"Claude e Python: desenvolva assistentes com a API da Anthropic"** da Alura.

## Sobre o curso

Curso ministrado por [Laís Urano](https://br.linkedin.com/in/laís-urano-9a41451b3) com foco em integração da API da Anthropic com Python, prompt engineering e tratamento de erros em chamadas de IA.

## Projetos

### `main.py`
Primeiro contato com a API — chamada simples para listar alimentos relacionados a um ingrediente.

### `categorizador.py`
Categorizador de alimentos por tipo: Bebida, Comida Salgada ou Comida Doce.

### `identificador_de_perfil.py`
Identificação de perfil de consumo alimentar a partir de uma lista de pratos por cliente.

### `analisador_de_sentimentos.py`
Análise de sentimentos de avaliações de restaurantes a partir de ficheiros `.txt`, com geração de resumo, sentimento geral, pontos fortes e fracos.

### `analisador_de_transacoes.py`
Pipeline de análise financeira com três etapas encadeadas:
1. Identificação de possíveis fraudes em transações CSV
2. Geração de parecer para transações suspeitas
3. Geração de recomendação técnica por transação

## Tecnologias

- Python 3.12
- [Anthropic SDK](https://github.com/anthropic-ai/anthropic-sdk-python)
- `python-dotenv`

## Configuração

### Variável de ambiente

Crie um ficheiro `.env` na raiz do projeto:

```
ANTHROPIC_API_KEY=sua_chave_aqui
```

Ou configure como secret no GitHub Codespaces em **Settings → Codespaces → Secrets**.

### Instalação

```bash
pip install anthropic python-dotenv
```

### Execução

```bash
python nome_do_script.py
```

## Estrutura

```
python-api-lab/
├── dados/
│   └── avaliacoes/        # ficheiros .txt com avaliações e análises geradas
├── main.py
├── categorizador.py
├── identificador_de_perfil.py
├── analisador_de_sentimentos.py
├── analisador_de_transacoes.py
├── helpers.py
├── transacoes.csv
├── transacoes.json
├── .env                   # não versionado
└── .gitignore
```

## Autor

[Everson Rubira](https://github.com/EversonRubira)
