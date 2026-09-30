from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RawElementProperty:
    """
    Source-neutral scientific element property.

    No value is assumed when the authoritative source does not
    provide one.
    """

    atomic_number: int
    property_name: str
    value: Any | None = None
    unit: str | None = None
    status: str = "known"
    source: str | None = None
    reference: str | None = None
    conditions: tuple[str, ...] = ()
    uncertainty: float | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.atomic_number, int):
            raise TypeError("atomic_number must be an integer")

        if not 1 <= self.atomic_number <= 118:
            raise ValueError(
                "atomic_number must be between 1 and 118"
            )

        if not isinstance(self.property_name, str):
            raise TypeError(
                "property_name must be a string"
            )

        if not self.property_name.strip():
            raise ValueError(
                "property_name must not be empty"
            )

        if self.unit is not None and not isinstance(
            self.unit,
            str,
        ):
            raise TypeError(
                "unit must be a string or None"
            )

        if self.uncertainty is not None:
            if not isinstance(
                self.uncertainty,
                (int, float),
            ):
                raise TypeError(
                    "uncertainty must be numeric"
                )

            if self.uncertainty < 0:
                raise ValueError(
                    "uncertainty must not be negative"
                )


@dataclass(frozen=True)
class RawElementRecord:
    """
    Source-neutral collection of authoritative properties for
    one element.
    """

    atomic_number: int
    name: str
    symbol: str
    properties: tuple[RawElementProperty, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.atomic_number, int):
            raise TypeError(
                "atomic_number must be an integer"
            )

        if not 1 <= self.atomic_number <= 118:
            raise ValueError(
                "atomic_number must be between 1 and 118"
            )

        if not isinstance(self.name, str):
            raise TypeError("name must be a string")

        if not self.name.strip():
            raise ValueError("name must not be empty")

        if not isinstance(self.symbol, str):
            raise TypeError("symbol must be a string")

        if not self.symbol.strip():
            raise ValueError("symbol must not be empty")

        for property_record in self.properties:
            if not isinstance(
                property_record,
                RawElementProperty,
            ):
                raise TypeError(
                    "properties must contain "
                    "RawElementProperty instances"
                )

            if (
                property_record.atomic_number
                != self.atomic_number
            ):
                raise ValueError(
                    "property atomic_number must match "
                    "record atomic_number"
                )

    def property(
        self,
        property_name: str,
    ) -> RawElementProperty | None:
        target = property_name.strip().casefold()

        for property_record in self.properties:
            if (
                property_record.property_name
                .casefold()
                == target
            ):
                return property_record

        return None
