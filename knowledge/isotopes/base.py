from __future__ import annotations

from dataclasses import dataclass

from scm.matter.isotopes import Isotope


@dataclass(frozen=True)
class IsotopeRecord:
    """
    Scientific knowledge record describing a specific isotope.

    Isotope identity remains defined by the underlying SCM
    Isotope object: (atomic number Z, mass number A).
    """

    isotope: Isotope
    name: str
    symbol: str
    stable: bool | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.isotope, Isotope):
            raise TypeError("isotope must be an Isotope")

        if not self.name.strip():
            raise ValueError("isotope name must not be empty")

        if not self.symbol.strip():
            raise ValueError("isotope symbol must not be empty")

        if self.stable is not None and not isinstance(
            self.stable,
            bool,
        ):
            raise TypeError("stable must be a bool or None")

    @property
    def atomic_number(self) -> int:
        return self.isotope.atomic_number

    @property
    def neutron_number(self) -> int:
        return self.isotope.neutron_number

    @property
    def mass_number(self) -> int:
        return self.isotope.mass_number

    @property
    def identity(self) -> tuple[int, int]:
        return self.isotope.identity

    def same_element(self, other: "IsotopeRecord") -> bool:
        if not isinstance(other, IsotopeRecord):
            raise TypeError("other must be an IsotopeRecord")
        return self.isotope.same_element(other.isotope)

    def same_isotope(self, other: "IsotopeRecord") -> bool:
        if not isinstance(other, IsotopeRecord):
            raise TypeError("other must be an IsotopeRecord")
        return self.isotope.same_isotope(other.isotope)

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.symbol}, "
            f"Z={self.atomic_number}, "
            f"A={self.mass_number})"
        )


__all__ = [
    "IsotopeRecord",
]
