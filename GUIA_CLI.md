# Guia de uso – CLI e aplicação

## Pré-requisitos

- Python 3.11+ (recomendado 3.14)
- Variável de ambiente para o LLM (ex.: `OPENAI_API_KEY` se for usar OpenAI via LiteLLM)

## 1. Primeira vez: ambiente e banco

Na raiz do projeto:

```bash
# Cria .venv, instala dependências e popula o banco (100+ veículos)
./run.sh
```

Isso abre o **Streamlit** no navegador. Para só preparar o ambiente e **não** abrir o Streamlit, use:

```bash
# Só ambiente + seed (não inicia o app)
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/python scripts/seed_vehicles.py
```

## 2. Rodar a aplicação (Streamlit)

```bash
./run.sh
```

Ou, com o venv já criado:

```bash
.venv/bin/python scripts/seed_vehicles.py   # só se quiser garantir banco de novo
.venv/bin/streamlit run app_streamlit.py
```

Acesse no navegador: **http://localhost:8501**

## 3. Rodar o CLI (chat no terminal)

O CLI é um chat em texto no terminal com o mesmo agente (perguntas, filtros, busca via MCP).

**Opção A** – usando o mesmo script que sobe o Streamlit (cria/atualiza venv e banco, depois abre o CLI):

```bash
./run.sh cli
```

**Opção B** – com o venv já criado:

```bash
.venv/bin/python cli.py
```

Ou ativando o venv antes:

```bash
source .venv/bin/activate
python cli.py
```

**No CLI:**

- Digite sua mensagem e pressione Enter (ex.: “Quero um carro flex até 80 mil”).
- O agente pode perguntar marca, ano, combustível etc.; responda em linguagem natural.
- Quando houver dados suficientes, ele chama a busca MCP e mostra os veículos (marca, modelo, ano, cor, quilometragem, preço).
- Para sair: digite `sair` (ou `exit`/`quit`) ou Ctrl+D.

## 4. Comandos úteis

| Objetivo              | Comando |
|-----------------------|--------|
| Subir app Streamlit   | `./run.sh` |
| Chat no terminal      | `./run.sh cli` ou `.venv/bin/python cli.py` |
| Popular/atualizar DB  | `.venv/bin/python scripts/seed_vehicles.py` |
| Rodar servidor MCP*   | `.venv/bin/python src/infrastructure/mcp_server.py` |

\* O servidor MCP não precisa ser iniciado à mão para o app nem para o CLI; o cliente sobe o processo quando precisa.

## 5. Demo no Jupyter

Abra `notebooks/demo.ipynb` e execute as células na ordem: seed, criação do agente, exemplos de conversa e chamada direta ao MCP.
