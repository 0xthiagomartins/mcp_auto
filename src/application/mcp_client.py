"""Cliente MCP: envia filtros ao servidor e devolve resultados (fluxo Client > Server > DB).
Mantém um único processo do servidor e uma sessão reutilizada por todas as chamadas."""
import asyncio
import json
import queue
import sys
import threading
from pathlib import Path

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MCP_SERVER_SCRIPT = PROJECT_ROOT / "src" / "infrastructure" / "mcp_server.py"

_request_queue: queue.Queue = queue.Queue()
_connection_ready = threading.Event()
_loop: asyncio.AbstractEventLoop | None = None
_loop_thread: threading.Thread | None = None
_lock = threading.Lock()


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


async def _connection_loop_async() -> None:
    global _connection_ready
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(MCP_SERVER_SCRIPT)],
        env=None,
    )
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                _connection_ready.set()
                while True:
                    item = await asyncio.get_event_loop().run_in_executor(None, _request_queue.get)
                    if item is None:
                        break
                    arguments, future = item
                    try:
                        result = await session.call_tool("search_vehicles", arguments=arguments)
                        future.set_result(_parse_result(result))
                    except Exception as e:
                        future.set_exception(e)
    finally:
        _connection_ready.clear()


def _run_connection_loop() -> None:
    global _loop
    _loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_loop)
    try:
        _loop.run_until_complete(_connection_loop_async())
    finally:
        _loop.close()


def _ensure_connection(timeout: float = 15.0) -> None:
    global _loop_thread
    with _lock:
        if _loop_thread is not None and _loop_thread.is_alive():
            if _connection_ready.is_set():
                return
        _connection_ready.clear()
        _loop_thread = threading.Thread(target=_run_connection_loop, daemon=True)
        _loop_thread.start()
    if not _connection_ready.wait(timeout=timeout):
        raise RuntimeError("MCP: timeout aguardando servidor inicializar.")


def init_mcp_client(timeout: float = 15.0) -> None:
    """Inicializa o servidor MCP em background ao subir o app (idempotente)."""
    _ensure_connection(timeout=timeout)


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
    """Versão síncrona: usa um único servidor MCP em background e reutiliza a sessão."""
    import concurrent.futures
    _ensure_connection()
    arguments = _build_args(
        marca=marca, modelo=modelo, ano_min=ano_min, ano_max=ano_max,
        tipo_combustivel=tipo_combustivel, cor=cor,
        preco_min=preco_min, preco_max=preco_max, km_max=km_max,
        transmissao=transmissao, limite=limite,
    )
    future: concurrent.futures.Future = concurrent.futures.Future()
    _request_queue.put((arguments, future))
    return future.result(timeout=30)
