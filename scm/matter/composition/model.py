from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from scm.matter.elements import Element, resolve_element


@dataclass(frozen=True, order=True)
class CompositionComponent:
    """
    One elemental component of a chemical composition.

    The stored element identifier is always normalized to the
    canonical chemical symbol.

    Example:
        H2O -> H x 2, O x 1
    """

    element: str
    count: int

    def __post_init__(self) -> None:
        if not isinstance(self.element, str):
            raise TypeError("element must be a string")

        element = self.element.strip()

        if not element:
            raise ValueError("element must not be empty")

        if not isinstance(self.count, int):
            raise TypeError("count must be an integer")

        if self.count <= 0:
            raise ValueError("count must be greater than zero")

        # Resolve through the identity/knowledge bridge.
        # This guarantees that the stored identifier is a real
        # chemical element rather than an arbitrary string.
        structural_element = resolve_element(element)

        # The matter-layer Element owns only Z. The knowledge layer
        # provides the canonical symbol.
        from knowledge.elements import get_element

        record = get_element(structural_element.atomic_number)
        canonical_symbol = record.symbol

        object.__setattr__(self, "element", canonical_symbol)


@dataclass(frozen=True)
class Composition:
    """
    First-class elemental composition.

    Composition contains elemental identity/counts only.
    Molecular structure, bonding, phase, charge and other state
    belong to higher chemical-species layers.
    """

    components: tuple[CompositionComponent, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.components, tuple):
            raise TypeError("components must be a tuple")

        if not all(
            isinstance(component, CompositionComponent)
            for component in self.components
        ):
            raise TypeError(
                "all components must be CompositionComponent instances"
            )

        if len(self.components) == 0:
            raise ValueError(
                "composition must contain at least one element"
            )

        symbols = [component.element for component in self.components]

        if len(symbols) != len(set(symbols)):
            raise ValueError(
                "composition cannot contain duplicate element entries"
            )

    @classmethod
    def from_mapping(
        cls,
        components: dict[str, int],
    ) -> "Composition":
        if not isinstance(components, dict):
            raise TypeError("components must be a dictionary")

        return cls(
            tuple(
                CompositionComponent(
                    element=symbol,
                    count=count,
                )
                for symbol, count in components.items()
            )
        )

    @classmethod
    def from_components(
        cls,
        components: Iterable[CompositionComponent],
    ) -> "Composition":
        return cls(tuple(components))

    @property
    def element_counts(self) -> dict[str, int]:
        return {
            component.element: component.count
            for component in self.components
        }

    @property
    def element_symbols(self) -> tuple[str, ...]:
        return tuple(
            component.element
            for component in self.components
        )

    @property
    def elements(self) -> tuple[Element, ...]:
        """
        Return structural Element identities for all components.

        Element identity is represented by atomic number Z.
        """
        return tuple(
            resolve_element(component.element)
            for component in self.components
        )

    def element(self, symbol: str) -> Element:
        """
        Resolve a component symbol to its structural Element identity.

        Raises:
            KeyError: if the element is not part of this composition.
        """
        if not isinstance(symbol, str):
            raise TypeError("symbol must be a string")

        normalized = symbol.strip()

        if not normalized:
            raise ValueError("symbol must not be empty")

        for component in self.components:
            record = _element_record(component.element)

            if record.symbol.casefold() == normalized.casefold():
                return record.element

        raise KeyError(
            f"element {symbol!r} is not part of this composition"
        )

    @property
    def total_atoms(self) -> int:
        return sum(
            component.count
            for component in self.components
        )

    def count(self, element: str) -> int:
        """
        Return the count for an element symbol.

        Symbol matching is case-insensitive.
        """
        if not isinstance(element, str):
            raise TypeError("element must be a string")

        target = element.strip().casefold()

        if not target:
            raise ValueError("element must not be empty")

        for component in self.components:
            if component.element.casefold() == target:
                return component.count

        return 0

    def contains(self, element: str) -> bool:
        return self.count(element) > 0

    def __str__(self) -> str:
        parts: list[str] = []

        for component in self.components:
            count = (
                ""
                if component.count == 1
                else str(component.count)
            )
            parts.append(
                f"{component.element}{count}"
            )

        return "".join(parts)


def _element_record(symbol: str):
    """
    Resolve a canonical element symbol to its knowledge record.

    Kept private so Composition's public structural API remains based
    on scm.matter.elements.Element.
    """
    from knowledge.elements import get_element

    return get_element(symbol)
