import sqlite3

from src.repository import VehicleFilters, search_vehicles


def test_search_vehicles_filters_by_brand_and_price() -> None:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        CREATE TABLE vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            engine TEXT NOT NULL,
            fuel_type TEXT NOT NULL,
            color TEXT NOT NULL,
            mileage_km INTEGER NOT NULL,
            doors INTEGER NOT NULL,
            transmission TEXT NOT NULL,
            body_type TEXT NOT NULL,
            price_brl REAL NOT NULL
        );
        INSERT INTO vehicles (brand, model, year, engine, fuel_type, color, mileage_km, doors, transmission, body_type, price_brl)
        VALUES
            ('Toyota', 'Corolla', 2020, '2.0L', 'flex', 'preto', 45000, 4, 'automática', 'sedan', 98000),
            ('Ford', 'Ka', 2018, '1.0L', 'flex', 'branco', 80000, 4, 'manual', 'hatch', 42000);
        """
    )

    rows = search_vehicles(conn, VehicleFilters(brand="Toy", max_price=100000))

    assert len(rows) == 1
    assert rows[0].model == "Corolla"
