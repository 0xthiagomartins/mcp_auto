"""Popula o banco com no mínimo 100 veículos fictícios."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from faker import Faker
from sqlmodel import Session, select

from src.domain.models import Vehicle
from src.infrastructure.database import engine, init_db

Faker.seed(42)
fake = Faker("pt_BR")

MARCAS_MODELOS = [
    ("Volkswagen", ["Golf", "Polo", "T-Cross", "Nivus", "Virtus", "Taos", "Jetta"]),
    ("Fiat", ["Uno", "Argo", "Cronos", "Mobi", "Pulse", "Strada", "Toro"]),
    ("Chevrolet", ["Onix", "Tracker", "Cruze", "Spin", "S10", "Montana"]),
    ("Ford", ["Ka", "EcoSport", "Ranger", "Maverick"]),
    ("Toyota", ["Corolla", "Hilux", "Yaris", "Corolla Cross", "RAV4"]),
    ("Honda", ["Civic", "HR-V", "City", "WR-V"]),
    ("Hyundai", ["HB20", "Creta", "Tucson", "ix35"]),
    ("Renault", ["Kwid", "Sandero", "Duster", "Oroch", "Captur"]),
    ("Jeep", ["Compass", "Renegade"]),
]

COMBUSTIVEIS = ["flex", "gasolina", "etanol", "diesel"]
TRANSMISSOES = ["manual", "automatico", "automatizado"]
CARROCERIAS = ["sedan", "hatch", "suv", "pickup"]
CORES = [
    "branco", "preto", "prata", "cinza", "vermelho", "azul", "bege", "dourado"
]


def _gerar_veiculo() -> Vehicle:
    marca, modelos = fake.random_element(MARCAS_MODELOS)
    modelo = fake.random_element(modelos)
    ano = fake.random_int(min=2015, max=2025)
    motor = fake.random_element(["1.0", "1.3", "1.4", "1.5", "1.6", "2.0", "2.0 turbo"])
    combustivel = fake.random_element(COMBUSTIVEIS)
    cor = fake.random_element(CORES)
    km = fake.random_int(min=0, max=150_000)
    portas = fake.random_element([2, 4])
    transmissao = fake.random_element(TRANSMISSOES)
    # Faixa de preço plausível por ano
    base = 40_000 + (ano - 2015) * 3_000 + fake.random_int(0, 80_000)
    preco = round(base + fake.random_int(-5_000, 15_000), 2)
    carroceria = fake.random_element(CARROCERIAS)
    return Vehicle(
        marca=marca,
        modelo=modelo,
        ano=ano,
        motorizacao=motor,
        tipo_combustivel=combustivel,
        cor=cor,
        quilometragem=km,
        numero_portas=portas,
        transmissao=transmissao,
        preco=preco,
        carroceria=carroceria,
    )


def run(quantidade: int = 100):
    init_db()
    with Session(engine) as session:
        result = session.exec(select(Vehicle))
        existentes = len(result.all())
        if existentes >= quantidade:
            print(f"Banco já possui {existentes} veículos. Nada a inserir.")
            return
        faltam = quantidade - existentes
        for _ in range(faltam):
            session.add(_gerar_veiculo())
        session.commit()
        total = existentes + faltam
        print(f"Inseridos {faltam} veículos. Total: {total}.")


if __name__ == "__main__":
    run(100)
