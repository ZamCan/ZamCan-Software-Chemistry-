from __future__ import annotations

from dataclasses import dataclass

from scm.matter.nuclei import Nucleus


@dataclass(frozen=True)
class Isotope:
    """
    Structural identity of an isotope.

    Isotope identity is determined by:
        Z = atomic number
        A = mass number

    Electronic state is intentionally outside this model.
    """

    nucleus: Nucleus

    def __post_init__(self) -> None:
        if not isinstance(self.nucleus, Nucleus):
            raise TypeError("nucleus must be a Nucleus")

    @classmethod
    def from_za(
        cls,
        atomic_number: int,
        mass_number: int,
    ) -> "Isotope":
        """
        Construct an isotope from atomic number Z and mass number A.
        """
        return cls(
            nucleus=Nucleus.from_mass_number(
                atomic_number,
                mass_number,
            )
        )

    @classmethod
    def from_zn(
        cls,
        atomic_number: int,
        neutron_number: int,
    ) -> "Isotope":
        """
        Construct an isotope from atomic number Z and neutron number N.
        """
        return cls(
            nucleus=Nucleus(
                proton_count=atomic_number,
                neutron_count=neutron_number,
            )
        )

    @property
    def atomic_number(self) -> int:
        """Z: number of protons."""
        return self.nucleus.atomic_number

    @property
    def neutron_number(self) -> int:
        """N: number of neutrons."""
        return self.nucleus.neutron_number

    @property
    def mass_number(self) -> int:
        """A: total number of nucleons."""
        return self.nucleus.mass_number

    @property
    def identity(self) -> tuple[int, int]:
        """
        Machine-safe isotope identity:
            (Z, A)
        """
        return self.nucleus.identity

    @property
    def proton_count(self) -> int:
        return self.atomic_number

    @property
    def nucleon_count(self) -> int:
        return self.mass_number

    def same_element(self, other: "Isotope") -> bool:
        """
        Return True when two isotopes have the same elemental identity.
        """
        if not isinstance(other, Isotope):
            raise TypeError("other must be an Isotope")

        return self.atomic_number == other.atomic_number

    def same_isotope(self, other: "Isotope") -> bool:
        """
        Return True when two objects represent the same isotope.
        """
        if not isinstance(other, Isotope):
            raise TypeError("other must be an Isotope")

        return self.identity == other.identity

    def __str__(self) -> str:
        return (
            f"Isotope(Z={self.atomic_number}, "
            f"N={self.neutron_number}, "
            f"A={self.mass_number})"
        )
