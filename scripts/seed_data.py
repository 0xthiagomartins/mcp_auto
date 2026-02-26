from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.database import get_connection, init_db

CATALOG = {
    "Fiat": ["Argo", "Cronos", "Toro", "Pulse"],
    "Ford": ["Ka", "EcoSport", "Ranger", "Focus"],
    "Chevrolet": ["Onix", "Cruze", "S10", "Tracker"],
    "Toyota": ["Corolla", "Yaris", "Hilux", "SW4"],
    "Honda": ["Civic", "City", "HR-V", "Fit"],
    "Hyundai": ["HB20", "Creta", "Tucson", "ix35"],
    "Volkswagen": ["Gol", "Polo", "T-Cross", "Nivus"],
    "Nissan": ["Versa", "Kicks", "Sentra", "Frontier"],
}

FUEL_TYPES = ["gasolina", "etanol", "flex", "diesel", "híbrido", "elétrico"]
TRANSMISSIONS = ["manual", "automática", "cvt"]
BODY_TYPES = ["hatch", "sedan", "suv", "pickup"]
COLORS = ["preto", "branco", "prata", "cinza", "azul", "vermelho"]


def build_vehicle_tuple() -> tuple[object, ...]:
    brand = random.choice(list(CATALOG.keys()))
    model = random.choice(CATALOG[brand])
    year = random.randint(2008, 2024)
    mileage = random.randint(0, 220_000)
    price = max(25_000, 180_000 - (2025 - year) * random.randint(2_500, 7_000) - mileage * 0.05)

    return (
        brand,
        model,
        year,
        f"{random.choice([1.0, 1.3, 1.6, 2.0, 3.0])}L",
        random.choice(FUEL_TYPES),
        random.choice(COLORS),
        mileage,
        random.choice([2, 4]),
        random.choice(TRANSMISSIONS),
        random.choice(BODY_TYPES),
        round(price, 2),
    )


def main() -> None:
    init_db()
    with get_connection() as conn:
        existing = conn.execute("SELECT COUNT(*) AS c FROM vehicles").fetchone()["c"]
        target = 120
        to_create = max(0, target - existing)

        if to_create:
            conn.executemany(
                """
                INSERT INTO vehicles (
                    brand, model, year, engine, fuel_type, color,
                    mileage_km, doors, transmission, body_type, price_brl
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [build_vehicle_tuple() for _ in range(to_create)],
            )
            conn.commit()

        current = conn.execute("SELECT COUNT(*) AS c FROM vehicles").fetchone()["c"]

    print(f"Banco populado. Registros atuais: {current}")


if __name__ == "__main__":
    main()
