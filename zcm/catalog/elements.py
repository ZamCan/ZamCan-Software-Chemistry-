from __future__ import annotations

from knowledge.elements.registry import (
    all_elements,
    get_element,
)
from knowledge.elements.base import ElementRecord
from scm.chemistry.engine import ChemistryModule


class ElementCatalog(ChemistryModule):
    """
    ZCM-facing element catalog.

    Consumes the authoritative SCM knowledge layer without
    maintaining a duplicate element database.
    """

    name = "elements"

    def capabilities(self) -> frozenset[str]:
        return frozenset({
            "periodic_table",
            "element_lookup",
            "element_search",
            "element_properties",
        })

    def get(self, identifier: str) -> ElementRecord:
        if not isinstance(identifier, str):
            raise TypeError("element identifier must be a string")

        return get_element(identifier)

    def all(self) -> tuple[ElementRecord, ...]:
        return all_elements()

    def search(self, query: str) -> tuple[ElementRecord, ...]:
        if not isinstance(query, str):
            raise TypeError("query must be a string")

        target = query.strip().casefold()

        if not target:
            raise ValueError("query must not be empty")

        results = []

        for element in self.all():
            if (
                target in element.name.casefold()
                or target in element.symbol.casefold()
                or target == str(element.atomic_number)
            ):
                results.append(element)

        return tuple(results)


element_catalog = ElementCatalog()
