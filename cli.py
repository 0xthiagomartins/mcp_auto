#!/usr/bin/env python3
"""CLI: chat no terminal com o agente de busca de veículos (MCP)."""
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.application.agent import create_agent, invoke_agent
from src.application.mcp_client import init_mcp_client


def main():
    print("Agente de busca de veículos (MCP)")
    print("Digite sua mensagem e Enter. 'sair' ou Ctrl+D para encerrar.\n")
    init_mcp_client()
    agent = create_agent()
    history = []
    while True:
        try:
            line = input("Você: ").strip()
        except EOFError:
            break
        if not line:
            continue
        if line.lower() in ("sair", "exit", "quit"):
            break
        history.append({"role": "user", "content": line})
        reply = invoke_agent(agent, line, history[:-1])
        print(f"\nAssistente: {reply}\n")
        history.append({"role": "assistant", "content": reply})
    print("Até mais.")


if __name__ == "__main__":
    main()
