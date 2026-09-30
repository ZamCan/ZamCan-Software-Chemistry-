from __future__ import annotations

from dataclasses import dataclass

from scm.core import Quantity
from scm.matter.particles import Particle
from knowledge.constants.physical import N_A


@dataclass(frozen=True)
class MolarMass:
    """
    Molar mass of a specified type of entity.

    quantity:
        Mass per amount of substance.

    entity:
        The specified entity represented by the molar mass.

    Examples:
        electron
        proton
        neutron
        atom
        molecule
        formula unit
    """

    quantity: Quantity
    entity: str

    def __post_init__(self) -> None:
        expected_dimension = Quantity(
            1.0,
            "kg",
        ).dimension / Quantity(
            1.0,
            "mol",
        ).dimension

        if self.quantity.dimension != expected_dimension:
            raise ValueError(
                "MolarMass requires a mass/amount quantity "
                "with dimension kg/mol"
            )

        if not self.entity.strip():
            raise ValueError("entity must not be empty")

    @property
    def value(self) -> float:
        """Return the numerical molar mass in kg/mol."""
        return self.quantity.to("kg/mol").value

    def to(self, target_unit: str) -> Quantity:
        """Return the molar mass converted to another compatible unit."""
        return self.quantity.to(target_unit)

    @classmethod
    def from_particle(cls, particle: Particle) -> "MolarMass":
        """
        Calculate molar mass from the particle rest mass.

        M = m_entity × N_A
        """
        mass = particle.rest_mass
        molar_mass = mass * N_A

        return cls(
            Quantity(
                molar_mass.value,
                "kg/mol",
            ),
            particle.name,
        )

    def __str__(self) -> str:
        return f"{self.value} kg/mol {self.entity}"
