from __future__ import annotations

from dataclasses import dataclass
import sqlite3

from .models import Vehicle


@dataclass
class VehicleFilters:
    brand: str | None = None
    model: str | None = None
    year: int | None = None
    fuel_type: str | None = None
    transmission: str | None = None
    max_price: float | None = None
    min_year: int | None = None


def _row_to_vehicle(row: sqlite3.Row) -> Vehicle:
    return Vehicle(
        id=row["id"],
        brand=row["brand"],
        model=row["model"],
        year=row["year"],
        engine=row["engine"],
        fuel_type=row["fuel_type"],
        color=row["color"],
        mileage_km=row["mileage_km"],
        doors=row["doors"],
        transmission=row["transmission"],
        body_type=row["body_type"],
        price_brl=row["price_brl"],
    )


def search_vehicles(conn: sqlite3.Connection, filters: VehicleFilters, limit: int = 10) -> list[Vehicle]:
    clauses: list[str] = []
    values: list[object] = []

    if filters.brand:
        clauses.append("LOWER(brand) LIKE ?")
        values.append(f"%{filters.brand.lower()}%")
    if filters.model:
        clauses.append("LOWER(model) LIKE ?")
        values.append(f"%{filters.model.lower()}%")
    if filters.year:
        clauses.append("year = ?")
        values.append(filters.year)
    if filters.min_year:
        clauses.append("year >= ?")
        values.append(filters.min_year)
    if filters.fuel_type:
        clauses.append("LOWER(fuel_type) LIKE ?")
        values.append(f"%{filters.fuel_type.lower()}%")
    if filters.transmission:
        clauses.append("LOWER(transmission) LIKE ?")
        values.append(f"%{filters.transmission.lower()}%")
    if filters.max_price is not None:
        clauses.append("price_brl <= ?")
        values.append(filters.max_price)

    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    query = f"SELECT * FROM vehicles {where} ORDER BY price_brl ASC LIMIT ?"
    values.append(limit)

    rows = conn.execute(query, values).fetchall()
    return [_row_to_vehicle(row) for row in rows]
