from __future__ import annotations

from dataclasses import dataclass, field

from scm.core import ScientificProperty
from scm.core.property_kind import PropertyKind
from scm.matter.elements import Element

from .categories import ElementCategory


@dataclass(frozen=True)
class ElementRecord:
    """
    Scientific knowledge record associated with an element identity.

    The structural identity remains owned by
    scm.matter.elements.Element.

    This record adds periodic-table classification and
    scientific properties without duplicating identity semantics.
    """

    element: Element
    name: str
    symbol: str
    period: int
    group: int | None
    block: str
    category: ElementCategory = ElementCategory.UNKNOWN
    properties: tuple[ScientificProperty, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("element name must not be empty")

        if not self.symbol.strip():
            raise ValueError("element symbol must not be empty")

        if self.period < 1:
            raise ValueError("period must be at least 1")

        if self.group is not None and not 1 <= self.group <= 18:
            raise ValueError("group must be between 1 and 18")

        if not self.block.strip():
            raise ValueError("element block must not be empty")

        if not isinstance(self.category, ElementCategory):
            raise TypeError(
                "category must be an ElementCategory"
            )

        if not isinstance(self.properties, tuple):
            raise TypeError(
                "properties must be a tuple of ScientificProperty"
            )

        for prop in self.properties:
            if not isinstance(prop, ScientificProperty):
                raise TypeError(
                    "every element property must be a ScientificProperty"
                )

    @property
    def atomic_number(self) -> int:
        """Return atomic number Z from structural element identity."""
        return self.element.atomic_number

    @property
    def identity(self) -> int:
        """Machine-safe element identity: atomic number Z."""
        return self.element.identity

    def get_property(self, name: str) -> ScientificProperty | None:
        """
        Return the first property with the requested name.

        Property names are treated case-insensitively.
        """
        target = name.strip().casefold()

        if not target:
            raise ValueError("property name must not be empty")

        for prop in self.properties:
            if prop.name.casefold() == target:
                return prop

        return None

    def get_property_by_kind(
        self,
        kind: PropertyKind,
    ) -> ScientificProperty | None:
        """
        Return the first property matching a PropertyKind.
        """

        if not isinstance(kind, PropertyKind):
            raise TypeError(
                "kind must be a PropertyKind"
            )

        for prop in self.properties:
            if prop.kind is kind:
                return prop

        return None

    def __str__(self) -> str:
        return f"{self.name} ({self.symbol}, Z={self.atomic_number})"
