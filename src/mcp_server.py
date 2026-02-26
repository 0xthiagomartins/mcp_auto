from __future__ import annotations

import json
import sys
from typing import Any

from .database import get_connection, init_db
from .repository import VehicleFilters, search_vehicles


def handle_request(payload: dict[str, Any]) -> dict[str, Any]:
    req_id = payload.get("id")
    method = payload.get("method")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "vehicle-mcp-server", "version": "1.0.0"},
            },
        }

    if method == "vehicles.search":
        params = payload.get("params", {})
        filters = VehicleFilters(
            brand=params.get("brand"),
            model=params.get("model"),
            year=params.get("year"),
            fuel_type=params.get("fuel_type"),
            transmission=params.get("transmission"),
            max_price=params.get("max_price"),
            min_year=params.get("min_year"),
        )
        limit = int(params.get("limit", 10))
        with get_connection() as conn:
            results = search_vehicles(conn, filters, limit=limit)

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"vehicles": [vehicle.to_dict() for vehicle in results]},
        }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def run() -> None:
    init_db()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
            response = handle_request(payload)
        except json.JSONDecodeError:
            response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"},
            }
        sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    run()
