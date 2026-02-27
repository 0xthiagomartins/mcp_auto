"""Agente conversacional com tool de busca via MCP (LangChain + LiteLLM)."""
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage

from langchain.agents import create_agent as langchain_create_agent
from langchain_litellm import ChatLiteLLM

from src.application.mcp_client import search_vehicles


@tool
def buscar_veiculos(
    marca: str | None = None,
    modelo: str | None = None,
    ano_min: int | None = None,
    ano_max: int | None = None,
    tipo_combustivel: str | None = None,
    cor: str | None = None,
    preco_min: float | None = None,
    preco_max: float | None = None,
    km_max: int | None = None,
    transmissao: str | None = None,
    limite: int = 20,
) -> list[dict]:
    """Busca veículos no catálogo por filtros: marca, modelo, ano (min/max), tipo_combustivel (flex, gasolina, etanol, diesel), cor, preco_min, preco_max, km_max, transmissao (manual, automatico). Use apenas os filtros que o usuário informou. Retorna lista com marca, modelo, ano, cor, quilometragem e preço."""
    return search_vehicles(
        marca=marca,
        modelo=modelo,
        ano_min=ano_min,
        ano_max=ano_max,
        tipo_combustivel=tipo_combustivel,
        cor=cor,
        preco_min=preco_min,
        preco_max=preco_max,
        km_max=km_max,
        transmissao=transmissao,
        limite=limite,
    )


SYSTEM = """Você é um assistente de busca de veículos. Converse de forma natural com o usuário.
Faça perguntas para entender o que ele quer: marca, modelo, ano, combustível, faixa de preço, cor, quilometragem máxima, etc.
Quando tiver informações suficientes (ou o usuário pedir para buscar), use a ferramenta buscar_veiculos com os filtros coletados.
Ao receber os resultados, apresente-os de forma amigável: marca, modelo, ano, cor, quilometragem e preço para cada veículo."""


def create_agent(model: str = "gpt-4o-mini"):
    llm = ChatLiteLLM(model=model, temperature=0)
    graph = langchain_create_agent(
        model=llm,
        tools=[buscar_veiculos],
        system_prompt=SYSTEM,
    )
    return graph


def invoke_agent(agent, user_input: str, chat_history: list) -> str:
    """Invoca o agente e retorna o texto da última mensagem do assistente."""
    messages = []
    for m in chat_history:
        if m.get("role") == "user" or (hasattr(m, "type") and "human" in str(m.type).lower()):
            content = m.get("content", getattr(m, "content", ""))
            messages.append(HumanMessage(content=content))
        elif m.get("role") == "assistant" or (hasattr(m, "type") and "ai" in str(m.type).lower()):
            content = m.get("content", getattr(m, "content", ""))
            messages.append(AIMessage(content=content))
    messages.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": messages})
    out_messages = result.get("messages", [])
    for msg in reversed(out_messages):
        if isinstance(msg, AIMessage) and msg.content:
            return msg.content if isinstance(msg.content, str) else str(msg.content)
    return ""


def format_vehicles_response(vehicles: list[dict]) -> str:
    if not vehicles:
        return "Nenhum veículo encontrado com os filtros informados."
    lines = []
    for i, v in enumerate(vehicles, 1):
        lines.append(
            f"{i}. **{v.get('marca', '')} {v.get('modelo', '')}** — {v.get('ano', '')} | "
            f"Cor: {v.get('cor', '')} | {v.get('quilometragem', 0):,} km | R$ {v.get('preco', 0):,.2f}"
        )
    return "\n".join(lines)
