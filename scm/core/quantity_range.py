from __future__ import annotations

from dataclasses import dataclass

from .quantity import Quantity


@dataclass(frozen=True)
class QuantityRange:
    """
    Inclusive scientific interval whose bounds are Quantities.

    Both bounds must have compatible dimensions and are normalized
    to the minimum bound's unit.
    """

    minimum: Quantity
    maximum: Quantity

    def __post_init__(self) -> None:
        if self.minimum.dimension != self.maximum.dimension:
            raise ValueError(
                "quantity range bounds must have compatible dimensions"
            )

        normalized_maximum = self.maximum.to(self.minimum.unit)

        if self.minimum.value > normalized_maximum.value:
            raise ValueError(
                "minimum cannot be greater than maximum"
            )

    @property
    def dimension(self):
        return self.minimum.dimension

    def contains(self, value: Quantity) -> bool:
        if value.dimension != self.dimension:
            raise ValueError(
                "value must have the same dimension as the range"
            )

        normalized_value = value.to(self.minimum.unit)

        return (
            self.minimum.value
            <= normalized_value.value
            <= self.maximum.to(self.minimum.unit).value
        )

    def __str__(self) -> str:
        return (
            f"[{self.minimum}, "
            f"{self.maximum.to(self.minimum.unit)}]"
        )


__all__ = [
    "QuantityRange",
]
