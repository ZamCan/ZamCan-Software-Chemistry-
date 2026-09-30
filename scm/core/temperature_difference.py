from __future__ import annotations

from dataclasses import dataclass

from .quantity import Quantity


@dataclass(frozen=True)
class TemperatureDifference:
    """
    A temperature interval (ΔT), not an absolute temperature.

    Temperature differences are represented internally in kelvin-scale
    magnitude. Unlike absolute temperatures, they have no affine offset.
    """

    quantity: Quantity

    def __post_init__(self) -> None:
        if not isinstance(self.quantity, Quantity):
            raise TypeError("quantity must be a Quantity")

        if self.quantity.dimension != Quantity(1.0, "K").dimension:
            raise ValueError(
                "TemperatureDifference requires a temperature quantity"
            )

        # A temperature difference must not carry an absolute-temperature
        # affine interpretation. Internally, K is the canonical difference
        # representation.
        normalized = self.quantity.to("K")

        object.__setattr__(self, "quantity", normalized)

    @property
    def dimension(self):
        """The temperature dimension shared with absolute temperature."""
        return self.quantity.dimension

    @property
    def value(self) -> float:
        """Temperature-difference magnitude in kelvin."""
        return self.quantity.value

    @property
    def unit(self) -> str:
        return "K"

    def to(self, target_unit: str) -> Quantity:
        """
        Convert the temperature difference to a temperature-scale unit.

        The conversion is scale-only: no absolute-temperature offset is
        applied to a difference.
        """
        if Quantity(1.0, target_unit).dimension != self.quantity.dimension:
            raise ValueError(
                f"TemperatureDifference requires a temperature unit: "
                f"{target_unit}"
            )

        from .units import get_unit

        definition = get_unit(target_unit)

        # Temperature differences use only the scale component.
        converted = self.value / definition.scale

        return Quantity(converted, target_unit)

    def __add__(
        self,
        other,
    ):
        if isinstance(other, TemperatureDifference):
            return TemperatureDifference(
                Quantity(self.value + other.value, "K")
            )

        if isinstance(other, Quantity):
            if other.dimension != self.dimension:
                return NotImplemented

            # An absolute temperature plus a difference produces an
            # absolute temperature, preserving the absolute unit.
            return other + self

        return NotImplemented

    def __sub__(
        self,
        other: "TemperatureDifference",
    ) -> "TemperatureDifference":
        if not isinstance(other, TemperatureDifference):
            return NotImplemented

        return TemperatureDifference(
            Quantity(self.value - other.value, "K")
        )

    def __neg__(self) -> "TemperatureDifference":
        return TemperatureDifference(
            Quantity(-self.value, "K")
        )

    def __mul__(self, other: int | float) -> "TemperatureDifference":
        if not isinstance(other, (int, float)):
            return NotImplemented

        return TemperatureDifference(
            Quantity(self.value * other, "K")
        )

    def __rmul__(self, other: int | float) -> "TemperatureDifference":
        return self.__mul__(other)

    def __truediv__(self, other: int | float) -> "TemperatureDifference":
        if not isinstance(other, (int, float)):
            return NotImplemented

        if other == 0:
            raise ZeroDivisionError(
                "Cannot divide TemperatureDifference by zero"
            )

        return TemperatureDifference(
            Quantity(self.value / other, "K")
        )

    def __str__(self) -> str:
        return f"Δ{self.value:g} K"
