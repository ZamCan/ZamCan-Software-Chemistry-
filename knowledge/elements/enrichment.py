from __future__ import annotations

from dataclasses import replace
from typing import Callable

from .base import ElementRecord


ElementEnricher = Callable[
    [ElementRecord],
    ElementRecord,
]


_ENRICHERS: dict[int, ElementEnricher] = {}


def register_enricher(
    atomic_number: int,
    enricher: ElementEnricher,
) -> None:
    """
    Register a scientific enrichment provider for an element.
    """

    if atomic_number < 1:
        raise ValueError(
            "atomic number must be at least 1"
        )

    if not callable(enricher):
        raise TypeError(
            "enricher must be callable"
        )

    if atomic_number in _ENRICHERS:
        raise ValueError(
            f"an enricher is already registered for "
            f"atomic number {atomic_number}"
        )

    _ENRICHERS[atomic_number] = enricher


def get_enricher(
    atomic_number: int,
) -> ElementEnricher | None:
    """
    Return the registered enricher for an element,
    or None when no enricher exists.
    """

    return _ENRICHERS.get(atomic_number)


def enrich_element(
    element: ElementRecord,
    enricher: ElementEnricher,
) -> ElementRecord:
    """
    Apply a scientific knowledge enricher to an ElementRecord.
    """

    if not isinstance(element, ElementRecord):
        raise TypeError(
            "element must be an ElementRecord"
        )

    if not callable(enricher):
        raise TypeError(
            "enricher must be callable"
        )

    enriched = enricher(element)

    if not isinstance(enriched, ElementRecord):
        raise TypeError(
            "enricher must return an ElementRecord"
        )

    return enriched


def enrich_registered(
    element: ElementRecord,
) -> ElementRecord:
    """
    Apply the registered enricher for the element, if one exists.
    """

    enricher = get_enricher(
        element.atomic_number
    )

    if enricher is None:
        return element

    return enrich_element(
        element,
        enricher,
    )


def add_properties(
    element: ElementRecord,
    *properties,
) -> ElementRecord:
    """
    Return a new ElementRecord with additional
    scientific properties attached.
    """

    return replace(
        element,
        properties=element.properties + tuple(properties),
    )


__all__ = [
    "ElementEnricher",
    "register_enricher",
    "get_enricher",
    "enrich_element",
    "enrich_registered",
    "add_properties",
]
