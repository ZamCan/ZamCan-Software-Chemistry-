from __future__ import annotations

import pytest

from zcm.catalog import ElementCatalog, element_catalog


def test_catalog_contains_all_118_elements():
    elements = element_catalog.all()

    assert len(elements) == 118
    assert len({element.atomic_number for element in elements}) == 118


def test_catalog_lookup_by_symbol():
    hydrogen = element_catalog.get("H")

    assert hydrogen.name == "Hydrogen"
    assert hydrogen.symbol == "H"
    assert hydrogen.atomic_number == 1


def test_catalog_lookup_by_name():
    oxygen = element_catalog.get("oxygen")

    assert oxygen.name == "Oxygen"
    assert oxygen.symbol == "O"
    assert oxygen.atomic_number == 8


def test_catalog_lookup_by_atomic_number():
    carbon = element_catalog.get("6")

    assert carbon.name == "Carbon"
    assert carbon.symbol == "C"
    assert carbon.atomic_number == 6


def test_catalog_lookup_is_case_insensitive():
    assert element_catalog.get("h") == element_catalog.get("H")
    assert element_catalog.get("CARBON") == element_catalog.get("carbon")


def test_catalog_search_by_name():
    results = element_catalog.search("carbon")

    assert len(results) == 1
    assert results[0].symbol == "C"


def test_catalog_search_by_symbol_substring():
    results = element_catalog.search("Fe")

    symbols = {element.symbol for element in results}

    assert "Fe" in symbols


def test_catalog_search_by_atomic_number():
    results = element_catalog.search("26")

    assert any(element.atomic_number == 26 for element in results)


def test_catalog_rejects_unknown_element():
    with pytest.raises(KeyError):
        element_catalog.get("not-an-element")


def test_catalog_rejects_invalid_lookup():
    with pytest.raises(TypeError):
        element_catalog.get(6)  # type: ignore[arg-type]


def test_catalog_rejects_empty_search():
    with pytest.raises(ValueError):
        element_catalog.search("")


def test_catalog_is_explicitly_reusable():
    catalog = ElementCatalog()

    assert catalog.get("H") == element_catalog.get("H")
