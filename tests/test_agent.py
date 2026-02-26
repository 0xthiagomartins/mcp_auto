from src.agent import extract_filters


def test_extract_filters_from_free_text() -> None:
    text = "Quero um Toyota flex automática até 90000 a partir de 2018"
    parsed = extract_filters(text)

    assert parsed["brand"] == "toyota"
    assert parsed["fuel_type"] == "flex"
    assert parsed["transmission"] == "automática"
    assert parsed["max_price"] == 90000.0
    assert parsed["min_year"] == 2018
