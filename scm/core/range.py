from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass(frozen=True)
class ValueRange(Generic[T]):
    """
    Inclusive scientific value interval.

    Represents a bounded range from minimum to maximum.
    """

    minimum: T
    maximum: T

    def __post_init__(self) -> None:
        if self.minimum > self.maximum:
            raise ValueError(
                "minimum cannot be greater than maximum"
            )

    def contains(self, value: T) -> bool:
        return self.minimum <= value <= self.maximum

    def __str__(self) -> str:
        return f"[{self.minimum}, {self.maximum}]"


__all__ = [
    "ValueRange",
]
