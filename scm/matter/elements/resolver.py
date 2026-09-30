from __future__ import annotations

from scm.matter.elements import Element


def resolve_element(identifier: str | int) -> Element:
    """
    Resolve an element identifier to the structural Element identity.

    Accepted identifiers:
        - atomic number, e.g. 11
        - element symbol, e.g. "Na"
        - element name, e.g. "Sodium"

    Structural identity is always represented by Element(Z).
    Names, symbols, and scientific properties remain owned by
    knowledge.elements.
    """

    if isinstance(identifier, bool):
        raise TypeError("element identifier must be a string or integer")

    if isinstance(identifier, int):
        if not 1 <= identifier <= 118:
            raise ValueError(
                "atomic number must be between 1 and 118"
            )
        return Element(identifier)

    if not isinstance(identifier, str):
        raise TypeError("element identifier must be a string or integer")

    value = identifier.strip()

    if not value:
        raise ValueError("element identifier must not be empty")

    # Lazy import prevents the knowledge ↔ matter circular dependency.
    from knowledge.elements import get_element

    record = get_element(value)

    return Element(record.atomic_number)


__all__ = ["resolve_element"]
