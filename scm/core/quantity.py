from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .units import Dimension, convert, get_unit


@dataclass(frozen=True)
class Quantity:
    value: float
    unit: str
    _dimension: Optional[Dimension] = None

    @property
    def dimension(self) -> Dimension:
        if self._dimension is not None:
            return self._dimension
        return get_unit(self.unit).dimension

    @property
    def is_absolute_temperature(self) -> bool:
        """Whether this quantity represents an absolute temperature."""
        return self.dimension == get_unit("K").dimension

    def to(self, target_unit: str) -> "Quantity":
        converted_value = convert(self.value, self.unit, target_unit)
        return Quantity(converted_value, target_unit)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Quantity):
            return NotImplemented

        if self.dimension != other.dimension:
            return False

        try:
            converted = other.to(self.unit)
        except ValueError:
            return False

        return self.value == converted.value

    def __neg__(self) -> "Quantity":
        return Quantity(
            -self.value,
            self.unit,
            _dimension=self.dimension,
        )

    def __add__(self, other):
        from .temperature_difference import TemperatureDifference

        if isinstance(other, TemperatureDifference):
            if self.dimension != other.dimension:
                raise ValueError(
                    "Cannot add a temperature difference to a "
                    "non-temperature quantity"
                )

            # Convert the difference to the absolute temperature's
            # canonical scale, then add its magnitude without applying
            # an affine offset.
            from .units import get_unit

            temperature_unit = get_unit(self.unit)
            difference = other.value / temperature_unit.scale

            return Quantity(
                self.value + difference,
                self.unit,
                _dimension=self.dimension,
            )

        if not isinstance(other, Quantity):
            return NotImplemented

        if self.dimension != other.dimension:
            raise ValueError(
                f"Incompatible dimensions: "
                f"{self.dimension} != {other.dimension}"
            )

        if self.is_absolute_temperature:
            raise ValueError(
                "Cannot add two absolute temperatures; "
                "add a TemperatureDifference instead"
            )

        other_converted = other.to(self.unit)

        return Quantity(
            self.value + other_converted.value,
            self.unit,
        )

    def __radd__(self, other):
        from .temperature_difference import TemperatureDifference

        if isinstance(other, TemperatureDifference):
            return other + self

        return NotImplemented

    def __sub__(self, other):
        from .temperature_difference import TemperatureDifference

        if isinstance(other, TemperatureDifference):
            if self.dimension != other.dimension:
                raise ValueError(
                    "Cannot subtract a temperature difference from "
                    "a non-temperature quantity"
                )

            from .units import get_unit

            temperature_unit = get_unit(self.unit)
            difference = other.value / temperature_unit.scale

            return Quantity(
                self.value - difference,
                self.unit,
                _dimension=self.dimension,
            )

        if not isinstance(other, Quantity):
            return NotImplemented

        if self.dimension != other.dimension:
            raise ValueError(
                f"Incompatible dimensions: "
                f"{self.dimension} != {other.dimension}"
            )

        if self.is_absolute_temperature:
            from .temperature_difference import TemperatureDifference

            # Absolute temperature subtraction produces a difference.
            self_kelvin = self.to("K").value
            other_kelvin = other.to("K").value

            return TemperatureDifference(
                Quantity(
                    self_kelvin - other_kelvin,
                    "K",
                )
            )

        other_converted = other.to(self.unit)

        return Quantity(
            self.value - other_converted.value,
            self.unit,
        )

    def __rsub__(self, other):
        from .temperature_difference import TemperatureDifference

        if isinstance(other, TemperatureDifference):
            return NotImplemented

        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            if self.is_absolute_temperature:
                raise ValueError(
                    "Cannot multiply an absolute temperature by a scalar"
                )

            return Quantity(
                self.value * other,
                self.unit,
                _dimension=self.dimension,
            )

        if isinstance(other, Quantity):
            if self.is_absolute_temperature or other.is_absolute_temperature:
                raise ValueError(
                    "Cannot multiply absolute temperature quantities"
                )

            dimension = self.dimension * other.dimension

            scale = (
                get_unit(self.unit).scale
                * get_unit(other.unit).scale
            )

            base_value = self.value * other.value * scale

            return Quantity(
                base_value,
                _dimension_to_unit(dimension),
                _dimension=dimension,
            )

        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError(
                    "Cannot divide Quantity by zero"
                )

            if self.is_absolute_temperature:
                raise ValueError(
                    "Cannot divide an absolute temperature by a scalar"
                )

            return Quantity(
                self.value / other,
                self.unit,
                _dimension=self.dimension,
            )

        if isinstance(other, Quantity):
            if other.value == 0:
                raise ZeroDivisionError(
                    "Cannot divide by zero Quantity"
                )

            if self.is_absolute_temperature or other.is_absolute_temperature:
                raise ValueError(
                    "Cannot divide quantities involving absolute temperature"
                )

            dimension = self.dimension / other.dimension

            scale = (
                get_unit(self.unit).scale
                / get_unit(other.unit).scale
            )

            base_value = self.value / other.value * scale

            return Quantity(
                base_value,
                _dimension_to_unit(dimension),
                _dimension=dimension,
            )

        return NotImplemented

def _dimension_to_unit(dimension: Dimension) -> str:
    known = {
        Dimension(): "1",
        Dimension(mass=1): "kg",
        Dimension(length=1): "m",
        Dimension(time=1): "s",
        Dimension(temperature=1): "K",
        Dimension(amount=1): "mol",
        Dimension(mass=1, amount=-1): "kg/mol",
        Dimension(current=1): "A",
        Dimension(angle=1): "rad",

        # Derived SI dimensions
        Dimension(time=1, current=1): "C",
        Dimension(length=2): "m²",
        Dimension(length=3): "m³",
        Dimension(mass=1, length=-3): "kg/m³",
        Dimension(amount=1, length=-3): "mol/m³",
        Dimension(mass=1, length=2, time=-2): "J",
        Dimension(mass=1, length=2, time=-1): "J·s",
        Dimension(mass=1, length=-1, time=-2): "Pa",
    }

    try:
        return known[dimension]
    except KeyError as exc:
        raise ValueError(
            f"No canonical unit registered for dimension: {dimension}"
        ) from exc
