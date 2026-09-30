from __future__ import annotations

from knowledge.elements.loaders.source import ElementDataSource


class ElementSourceCatalog:
    """
    Registry of element scientific-data sources.
    """

    def __init__(self) -> None:
        self._sources: dict[str, ElementDataSource] = {}

    def register(self, source: ElementDataSource) -> None:
        if not isinstance(source, ElementDataSource):
            raise TypeError(
                "source must be an ElementDataSource"
            )

        if source.name in self._sources:
            raise ValueError(
                f"source already registered: {source.name}"
            )

        self._sources[source.name] = source

    def get(self, name: str) -> ElementDataSource:
        try:
            return self._sources[name]
        except KeyError as exc:
            raise KeyError(
                f"unknown element data source: {name}"
            ) from exc

    def all(self) -> tuple[ElementDataSource, ...]:
        return tuple(self._sources.values())


element_sources = ElementSourceCatalog()


__all__ = [
    "ElementSourceCatalog",
    "element_sources",
]
