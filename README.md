# Desafio Técnico C2S — Catálogo de Veículos com MCP

Projeto em Python que implementa:

1. **Modelagem de dados** de automóveis (11+ atributos).
2. **Script de população** com dados fictícios (120 veículos).
3. **Fluxo Cliente > Servidor > Banco** usando mensagens no formato JSON-RPC compatíveis com o estilo do protocolo MCP.
4. **Aplicação de terminal com agente virtual**, com conversa natural para coletar filtros e buscar veículos.

## Estrutura

- `src/models.py`: entidade `Vehicle` com atributos do automóvel.
- `src/database.py`: configuração SQLite e sessão SQLite (sqlite3).
- `src/repository.py`: camada de consulta por filtros.
- `src/mcp_server.py`: servidor MCP-like (JSON-RPC via stdio).
- `src/mcp_client.py`: cliente que conversa com o servidor.
- `src/agent.py`: agente virtual no terminal.
- `scripts/seed_data.py`: gera e insere dados fakes.
- `tests/`: testes unitários básicos.

## Requisitos

- Python 3.11+

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate
pip install pytest
python scripts/seed_data.py
python main.py
```

## Exemplo de conversa

- Usuário: `quero um toyota automático até 100000`
- Agente: pergunta combustível (se faltando), ano, etc.
- Agente envia filtros ao cliente MCP.
- Cliente manda requisição ao servidor MCP.
- Servidor consulta SQLite via camada de repositório e retorna resultados.

## Testes

```bash
pytest
```
