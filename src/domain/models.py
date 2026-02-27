from sqlmodel import Field, SQLModel


class Vehicle(SQLModel, table=True):
    """Esquema de automóvel com atributos relevantes para busca."""

    __tablename__ = "vehicles"

    id: int | None = Field(default=None, primary_key=True)
    marca: str = Field(index=True)
    modelo: str = Field(index=True)
    ano: int = Field(index=True)
    motorizacao: str  # ex: 1.0, 2.0 turbo
    tipo_combustivel: str = Field(index=True)  # flex, gasolina, etanol, diesel, eletrico
    cor: str = Field(index=True)
    quilometragem: int = Field(index=True)
    numero_portas: int
    transmissao: str = Field(index=True)  # manual, automatico, automatizado
    preco: float = Field(index=True)
    carroceria: str  # sedan, hatch, suv, pickup
