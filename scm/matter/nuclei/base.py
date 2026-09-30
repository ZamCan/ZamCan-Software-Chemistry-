from __future__ import annotations

from dataclasses import dataclass

from scm.matter.particles import Particle


@dataclass(frozen=True)
class Nucleus:
    """
    Structural model of an atomic nucleus.

    A nucleus is represented by its proton and neutron counts.

    Proton count Z determines the elemental identity.
    Neutron count N determines the isotope together with Z.
    Electrons are intentionally not part of this model.
    """

    proton_count: int
    neutron_count: int

    def __post_init__(self) -> None:
        if isinstance(self.proton_count, bool):
            raise TypeError("proton_count must be an integer")

        if not isinstance(self.proton_count, int):
            raise TypeError("proton_count must be an integer")

        if not 1 <= self.proton_count <= 118:
            raise ValueError(
                "proton_count must be between 1 and 118"
            )

        if isinstance(self.neutron_count, bool):
            raise TypeError("neutron_count must be an integer")

        if not isinstance(self.neutron_count, int):
            raise TypeError("neutron_count must be an integer")

        if self.neutron_count < 0:
            raise ValueError(
                "neutron_count cannot be negative"
            )

    @classmethod
    def from_mass_number(
        cls,
        atomic_number: int,
        mass_number: int,
    ) -> "Nucleus":
        """
        Construct a nucleus from Z and A.

        N is derived as:
            N = A - Z
        """

        if isinstance(atomic_number, bool):
            raise TypeError("atomic_number must be an integer")

        if not isinstance(atomic_number, int):
            raise TypeError("atomic_number must be an integer")

        if not isinstance(mass_number, int) or isinstance(
            mass_number, bool
        ):
            raise TypeError("mass_number must be an integer")

        if mass_number < atomic_number:
            raise ValueError(
                "mass_number cannot be less than atomic_number"
            )

        return cls(
            proton_count=atomic_number,
            neutron_count=mass_number - atomic_number,
        )

    @property
    def atomic_number(self) -> int:
        """Z: number of protons in the nucleus."""
        return self.proton_count

    @property
    def neutron_number(self) -> int:
        """N: number of neutrons in the nucleus."""
        return self.neutron_count

    @property
    def mass_number(self) -> int:
        """A: total number of nucleons, A = Z + N."""
        return self.proton_count + self.neutron_count

    @property
    def nucleon_count(self) -> int:
        return self.mass_number

    @property
    def identity(self) -> tuple[int, int]:
        """
        Nuclear identity represented as (Z, A).
        """
        return (
            self.atomic_number,
            self.mass_number,
        )

    def contains(self, particle: Particle) -> bool:
        """Return whether the supplied particle is classified as a nucleon."""
        return particle.is_nucleon

    def __str__(self) -> str:
        return (
            f"Nucleus(Z={self.atomic_number}, "
            f"N={self.neutron_number}, "
            f"A={self.mass_number})"
        )
