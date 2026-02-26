from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "vehicles.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS vehicles (
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
            )
            """
        )
        conn.commit()
