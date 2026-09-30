from __future__ import annotations

from typing import Dict

from .base import ElementRecord
from .builder import build_element_record
from .data.periodic_table import all_periodic_elements
from .enrichment import enrich_registered
from .properties import enrich_element_with_atomic_properties

# Import provider registrations.
# The imported module registers available scientific enrichers.
from . import providers  # noqa: F401


_ELEMENTS: Dict[str, ElementRecord] = {}

for data in all_periodic_elements():
    element = build_element_record(data)

    # Apply existing element-level enrichers.
    element = enrich_registered(element)

    # Apply registered atomic-property knowledge.
    element = enrich_element_with_atomic_properties(element)

    _ELEMENTS[element.name.casefold()] = element
    _ELEMENTS[element.symbol.casefold()] = element
    _ELEMENTS[str(element.atomic_number)] = element


def get_element(identifier: str | int) -> ElementRecord:
    """
    Find an element by name, symbol, or atomic number.

    Accepted identifiers:
        - element name, e.g. "Hydrogen"
        - element symbol, e.g. "H"
        - atomic number, e.g. 1
    """

    if isinstance(identifier, bool):
        raise TypeError(
            "element identifier must be a string or integer"
        )

    if isinstance(identifier, int):
        if not 1 <= identifier <= 118:
            raise ValueError(
                "atomic number must be between 1 and 118"
            )
        key = str(identifier)

    elif isinstance(identifier, str):
        key = identifier.strip().casefold()

        if not key:
            raise ValueError(
                "element identifier must not be empty"
            )

    else:
        raise TypeError(
            "element identifier must be a string or integer"
        )

    try:
        return _ELEMENTS[key]
    except KeyError as exc:
        raise KeyError(
            f"Unknown element: {identifier!r}"
        ) from exc


def all_elements() -> tuple[ElementRecord, ...]:
    """Return all unique element records."""

    return tuple(
        dict.fromkeys(_ELEMENTS.values())
    )


__all__ = [
    "get_element",
    "all_elements",
]
