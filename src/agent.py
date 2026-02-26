from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from .mcp_client import MCPVehicleClient

KNOWN_BRANDS = [
    "fiat",
    "ford",
    "chevrolet",
    "toyota",
    "honda",
    "hyundai",
    "volkswagen",
    "nissan",
    "renault",
    "jeep",
    "bmw",
    "audi",
]

KNOWN_FUELS = ["gasolina", "etanol", "flex", "diesel", "híbrido", "elétrico"]
KNOWN_TRANSMISSIONS = ["manual", "automática", "cvt"]


@dataclass
class ConversationState:
    filters: dict[str, Any] = field(default_factory=dict)


def extract_filters(message: str) -> dict[str, Any]:
    text = message.lower()
    found: dict[str, Any] = {}

    for brand in KNOWN_BRANDS:
        if brand in text:
            found["brand"] = brand
            break

    for fuel in KNOWN_FUELS:
        if fuel in text:
            found["fuel_type"] = fuel
            break

    for transmission in KNOWN_TRANSMISSIONS:
        if transmission in text:
            found["transmission"] = transmission
            break

    year_match = re.search(r"\b(19\d{2}|20\d{2})\b", text)
    if year_match:
        found["year"] = int(year_match.group(1))

    min_year_match = re.search(r"(a partir de|depois de)\s*(19\d{2}|20\d{2})", text)
    if min_year_match:
        found["min_year"] = int(min_year_match.group(2))

    max_price_match = re.search(r"(?:até|max(?:imo)?)\s*(?:r\$)?\s*(\d{2,6})", text)
    if max_price_match:
        found["max_price"] = float(max_price_match.group(1))

    model_match = re.search(r"modelo\s+([\w-]+)", text)
    if model_match:
        found["model"] = model_match.group(1)

    return found


def next_question(state: ConversationState) -> str | None:
    if "brand" not in state.filters:
        return "Tem alguma marca de preferência? (ex.: Toyota, Ford, Honda)"
    if "fuel_type" not in state.filters:
        return "Você procura qual tipo de combustível? (flex, diesel, elétrico...)"
    if "max_price" not in state.filters:
        return "Qual o teto de preço aproximado? Você pode dizer algo como 'até 90000'."
    return None


def format_results(vehicles: list[dict[str, Any]]) -> str:
    if not vehicles:
        return "Não encontrei veículos com esses critérios. Quer ajustar algum filtro?"

    lines = ["Encontrei estes veículos para você:"]
    for vehicle in vehicles:
        lines.append(
            "- {brand} {model} | {year} | {color} | {mileage_km} km | R$ {price_brl}".format(**vehicle)
        )
    return "\n".join(lines)


def run_cli_agent() -> None:
    print("Olá! Sou seu agente virtual de veículos. Me diga o que você procura :)\n")
    state = ConversationState()
    client = MCPVehicleClient()

    try:
        while True:
            question = next_question(state)
            if question:
                user_message = input(f"{question}\n> ").strip()
            else:
                user_message = input("Se quiser, acrescente mais detalhes ou pressione ENTER para buscar:\n> ").strip()

            if user_message.lower() in {"sair", "exit", "quit"}:
                print("Até a próxima!")
                return

            state.filters.update(extract_filters(user_message))

            if next_question(state) is None:
                vehicles = client.search_vehicles({**state.filters, "limit": 8})
                print("\n" + format_results(vehicles) + "\n")

                keep = input("Quer fazer outra busca? (sim/não)\n> ").strip().lower()
                if keep not in {"sim", "s", "yes", "y"}:
                    print("Obrigado! Encerrando agente.")
                    return
                state = ConversationState()
                print()
    finally:
        client.close()
