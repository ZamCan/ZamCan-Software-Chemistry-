from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ValueRelation(str, Enum):
    EXACT = "exact"
    APPROXIMATE = "approximate"
    LOWER_LIMIT = "lower_limit"
    UPPER_LIMIT = "upper_limit"


@dataclass(frozen=True)
class ScientificValue:
    """
    A numerical scientific value with uncertainty semantics.

    The numerical value itself does not imply that the value is exact.
    Relation describes how the reported value should be interpreted.
    """

    value: float
    unit: str
    uncertainty: float | None = None
    relation: ValueRelation = ValueRelation.EXACT

    def __post_init__(self) -> None:
        if not isinstance(self.value, (int, float)):
            raise TypeError("value must be numeric")

        if not self.unit.strip():
            raise ValueError("unit must not be empty")

        if self.uncertainty is not None and self.uncertainty < 0:
            raise ValueError(
                "uncertainty cannot be negative"
            )

        if not isinstance(self.relation, ValueRelation):
            raise TypeError(
                "relation must be a ValueRelation"
            )
