from __future__ import annotations

from dataclasses import replace

from knowledge.elements.base import ElementRecord

from .conversion import convert_atomic_properties


def enrich_element_with_atomic_properties(
    element: ElementRecord,
) -> ElementRecord:
    """
    Attach all registered atomic properties to an ElementRecord.

    The original ElementRecord is not mutated. A new record is returned.
    """

    if not isinstance(
        element,
        ElementRecord,
    ):
        raise TypeError(
            "element must be an ElementRecord"
        )

    atomic_properties = convert_atomic_properties(
        element.atomic_number
    )

    if not atomic_properties:
        return element

    return replace(
        element,
        properties=(
            *element.properties,
            *atomic_properties,
        ),
    )


__all__ = [
    "enrich_element_with_atomic_properties",
]
