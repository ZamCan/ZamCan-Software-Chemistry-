from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from .conditions import Conditions
from .evidence import Evidence, normalize_evidence
from .enums import ScientificStatus
from .property_kind import PropertyKind
from .quantity import Quantity
from .quantity_range import QuantityRange
from .uncertainty import Uncertainty


PropertyValue = Union[Quantity, QuantityRange]


@dataclass(frozen=True)
class ScientificProperty:
    """
    Scientific property with machine-readable kind, value,
    conditions, evidence, uncertainty, and scientific status.

    Evidence is stored internally as an immutable tuple so a
    scientific property can be supported by multiple independent
    sources.
    """

    name: str
    quantity: PropertyValue
    status: ScientificStatus
    kind: PropertyKind = PropertyKind.OTHER
    conditions: Conditions | None = None
    uncertainty: Uncertainty | None = None
    evidence: Evidence | tuple[Evidence, ...] | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError(
                "property name must not be empty"
            )

        if not isinstance(
            self.quantity,
            (Quantity, QuantityRange),
        ):
            raise TypeError(
                "quantity must be a Quantity or QuantityRange"
            )

        if not isinstance(
            self.status,
            ScientificStatus,
        ):
            raise TypeError(
                "status must be a ScientificStatus"
            )

        if not isinstance(
            self.kind,
            PropertyKind,
        ):
            raise TypeError(
                "kind must be a PropertyKind"
            )

        normalized = normalize_evidence(
            self.evidence
        )

        object.__setattr__(
            self,
            "evidence",
            normalized,
        )

    @property
    def is_range(self) -> bool:
        """Return True when the property contains a value range."""

        return isinstance(
            self.quantity,
            QuantityRange,
        )

    @property
    def dimension(self):
        """Return the physical dimension of the property value."""

        return self.quantity.dimension

    @property
    def primary_evidence(self) -> Evidence | None:
        """
        Return the first evidence record, if one exists.

        This provides convenient access for callers that only need
        one representative or primary evidence record.
        """

        if not self.evidence:
            return None

        return self.evidence[0]

    def __str__(self) -> str:
        return f"{self.name}: {self.quantity}"


__all__ = [
    "PropertyValue",
    "ScientificProperty",
]
