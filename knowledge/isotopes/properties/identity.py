from __future__ import annotations

from dataclasses import dataclass

from scm.core import PropertyKind


@dataclass(frozen=True)
class IsotopePropertyIdentity:
    """
    Stable identity for a scientific isotope property.

    An isotope is identified by:
        Z = atomic number
        A = mass number

    Conditions and evidence are intentionally excluded from
    identity because multiple scientific records may describe
    the same property under different conditions or sources.
    """

    atomic_number: int
    mass_number: int
    kind: PropertyKind

    def __post_init__(self) -> None:
        if not isinstance(self.atomic_number, int):
            raise TypeError("atomic number must be an integer")

        if not 1 <= self.atomic_number <= 118:
            raise ValueError(
                "atomic number must be between 1 and 118"
            )

        if not isinstance(self.mass_number, int):
            raise TypeError("mass number must be an integer")

        if self.mass_number < self.atomic_number:
            raise ValueError(
                "mass number cannot be less than atomic number"
            )

        if not isinstance(self.kind, PropertyKind):
            raise TypeError("kind must be a PropertyKind")


__all__ = [
    "IsotopePropertyIdentity",
]
