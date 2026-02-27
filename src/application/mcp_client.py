"""Cliente MCP: envia filtros ao servidor e devolve resultados (fluxo Client > Server > DB)."""
import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MCP_SERVER_SCRIPT = PROJECT_ROOT / "src" / "infrastructure" / "mcp_server.py"


def _build_args(
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
) -> dict:
    args = {"limite": limite}
    if marca is not None and str(marca).strip():
        args["marca"] = str(marca).strip()
    if modelo is not None and str(modelo).strip():
        args["modelo"] = str(modelo).strip()
    if ano_min is not None:
        args["ano_min"] = int(ano_min)
    if ano_max is not None:
        args["ano_max"] = int(ano_max)
    if tipo_combustivel is not None and str(tipo_combustivel).strip():
        args["tipo_combustivel"] = str(tipo_combustivel).strip()
    if cor is not None and str(cor).strip():
        args["cor"] = str(cor).strip()
    if preco_min is not None:
        args["preco_min"] = float(preco_min)
    if preco_max is not None:
        args["preco_max"] = float(preco_max)
    if km_max is not None:
        args["km_max"] = int(km_max)
    if transmissao is not None and str(transmissao).strip():
        args["transmissao"] = str(transmissao).strip()
    return args


def _parse_result(result) -> list[dict]:
    if getattr(result, "isError", False) or (hasattr(result, "is_error") and result.is_error):
        return []
    if getattr(result, "structuredContent", None):
        sc = result.structuredContent
        if isinstance(sc, list):
            return sc
        if isinstance(sc, dict):
            return [sc]
    for content in getattr(result, "content", []) or []:
        if isinstance(content, types.TextContent):
            try:
                data = json.loads(content.text)
                return data if isinstance(data, list) else [data]
            except (json.JSONDecodeError, TypeError):
                return []
    return []


async def search_vehicles_async(
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
    """Chama a tool search_vehicles no servidor MCP e retorna a lista de veículos."""
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(MCP_SERVER_SCRIPT)],
        env=None,
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            arguments = _build_args(
                marca=marca, modelo=modelo, ano_min=ano_min, ano_max=ano_max,
                tipo_combustivel=tipo_combustivel, cor=cor,
                preco_min=preco_min, preco_max=preco_max, km_max=km_max,
                transmissao=transmissao, limite=limite,
            )
            result = await session.call_tool("search_vehicles", arguments=arguments)
            return _parse_result(result)


def search_vehicles(
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
    """Versão síncrona para uso em Streamlit/notebook."""
    return asyncio.run(
        search_vehicles_async(
            marca=marca, modelo=modelo, ano_min=ano_min, ano_max=ano_max,
            tipo_combustivel=tipo_combustivel, cor=cor,
            preco_min=preco_min, preco_max=preco_max, km_max=km_max,
            transmissao=transmissao, limite=limite,
        )
    )
