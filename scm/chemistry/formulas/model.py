from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FormulaComponent:
    element: str
    count: int = 1

    def __post_init__(self) -> None:
        if not isinstance(self.element, str) or not self.element.strip():
            raise ValueError("element must not be empty")

        if not isinstance(self.count, int):
            raise TypeError("count must be an integer")

        if self.count < 1:
            raise ValueError("count must be at least 1")


@dataclass(frozen=True)
class ChemicalFormula:
    original: str
    components: tuple[FormulaComponent, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.original, str) or not self.original.strip():
            raise ValueError("formula must not be empty")

        if not self.components:
            raise ValueError("formula must contain components")

    @property
    def element_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}

        for component in self.components:
            counts[component.element] = (
                counts.get(component.element, 0)
                + component.count
            )

        return counts

    def __str__(self) -> str:
        return self.original
