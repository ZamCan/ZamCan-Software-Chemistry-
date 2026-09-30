from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from scm.core.scientific_values import ScientificValue


@dataclass(frozen=True)
class IsotopeData:
    """
    Normalized scientific representation of a nuclide.

    Identity:
        Z = atomic number
        A = mass number

    Nuclear-state-specific information is intentionally handled
    separately by the SCM nuclear-state model.
    """

    atomic_number: int
    mass_number: int

    name: Optional[str] = None
    symbol: Optional[str] = None

    isotopic_mass: Optional[ScientificValue] = None

    stable: Optional[bool] = None
    naturally_occurring: Optional[bool] = None

    natural_abundance: Optional[ScientificValue] = None

    half_life: Optional[ScientificValue] = None

    spin: Optional[str] = None
    parity: Optional[str] = None

    mass_excess: Optional[ScientificValue] = None
    binding_energy: Optional[ScientificValue] = None

    notes: Optional[str] = None

    def __post_init__(self) -> None:
        if not isinstance(self.atomic_number, int):
            raise TypeError("atomic_number must be an integer")

        if not 1 <= self.atomic_number <= 118:
            raise ValueError(
                "atomic_number must be between 1 and 118"
            )

        if not isinstance(self.mass_number, int):
            raise TypeError("mass_number must be an integer")

        if self.mass_number < self.atomic_number:
            raise ValueError(
                "mass_number cannot be less than atomic_number"
            )

        if self.stable is not None and not isinstance(
            self.stable,
            bool,
        ):
            raise TypeError(
                "stable must be a bool or None"
            )

        if (
            self.naturally_occurring is not None
            and not isinstance(
                self.naturally_occurring,
                bool,
            )
        ):
            raise TypeError(
                "naturally_occurring must be a bool or None"
            )

        for field_name in (
            "isotopic_mass",
            "natural_abundance",
            "half_life",
            "mass_excess",
            "binding_energy",
        ):
            value = getattr(self, field_name)

            if value is not None and not isinstance(
                value,
                ScientificValue,
            ):
                raise TypeError(
                    f"{field_name} must be a ScientificValue or None"
                )

        if self.natural_abundance is not None:
            if self.natural_abundance.unit != "1":
                raise ValueError(
                    "natural_abundance must be dimensionless"
                )

        if self.stable is True and self.half_life is not None:
            raise ValueError(
                "stable isotopes must not have a finite half-life"
            )

    @property
    def neutron_number(self) -> int:
        return self.mass_number - self.atomic_number

    @property
    def identity(self) -> tuple[int, int]:
        return (
            self.atomic_number,
            self.mass_number,
        )
