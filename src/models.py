from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Vehicle:
    id: int
    brand: str
    model: str
    year: int
    engine: str
    fuel_type: str
    color: str
    mileage_km: int
    doors: int
    transmission: str
    body_type: str
    price_brl: float

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "brand": self.brand,
            "model": self.model,
            "year": self.year,
            "engine": self.engine,
            "fuel_type": self.fuel_type,
            "color": self.color,
            "mileage_km": self.mileage_km,
            "doors": self.doors,
            "transmission": self.transmission,
            "body_type": self.body_type,
            "price_brl": round(self.price_brl, 2),
        }
