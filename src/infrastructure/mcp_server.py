"""Servidor MCP: interpreta filtros, consulta o banco e devolve resultados (Client > Server > DB)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sqlmodel import Session, select

from src.domain.models import Vehicle
from src.infrastructure.database import engine, init_db
from fastmcp import FastMCP

mcp = FastMCP("Veículos MCP")


def _row_to_display(v: Vehicle) -> dict:
    return {
        "marca": v.marca,
        "modelo": v.modelo,
        "ano": v.ano,
        "cor": v.cor,
        "quilometragem": v.quilometragem,
        "preco": v.preco,
    }


@mcp.tool
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
    """Busca veículos no banco aplicando os filtros informados. Retorna lista com marca, modelo, ano, cor, quilometragem e preço."""
    init_db()
    with Session(engine) as session:
        stmt = select(Vehicle)
        if marca is not None and marca.strip():
            stmt = stmt.where(Vehicle.marca.ilike(f"%{marca.strip()}%"))
        if modelo is not None and modelo.strip():
            stmt = stmt.where(Vehicle.modelo.ilike(f"%{modelo.strip()}%"))
        if ano_min is not None:
            stmt = stmt.where(Vehicle.ano >= ano_min)
        if ano_max is not None:
            stmt = stmt.where(Vehicle.ano <= ano_max)
        if tipo_combustivel is not None and tipo_combustivel.strip():
            stmt = stmt.where(Vehicle.tipo_combustivel.ilike(f"%{tipo_combustivel.strip()}%"))
        if cor is not None and cor.strip():
            stmt = stmt.where(Vehicle.cor.ilike(f"%{cor.strip()}%"))
        if preco_min is not None:
            stmt = stmt.where(Vehicle.preco >= preco_min)
        if preco_max is not None:
            stmt = stmt.where(Vehicle.preco <= preco_max)
        if km_max is not None:
            stmt = stmt.where(Vehicle.quilometragem <= km_max)
        if transmissao is not None and transmissao.strip():
            stmt = stmt.where(Vehicle.transmissao.ilike(f"%{transmissao.strip()}%"))
        stmt = stmt.limit(limite)
        result = session.exec(stmt)
        return [_row_to_display(v) for v in result.all()]


if __name__ == "__main__":
    mcp.run()
