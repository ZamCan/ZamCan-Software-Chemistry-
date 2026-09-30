from __future__ import annotations

from dataclasses import dataclass

from scm.core import Quantity
from knowledge.constants.physical import N_A


@dataclass(frozen=True)
class EntityCount:
    """
    Number of specified entities.

    Examples of entities:
        atoms
        molecules
        ions
        electrons
        protons
        neutrons
        formula units

    Entity count is mathematically dimensionless, but the semantic
    identity of the entity is retained separately.
    """

    value: float
    entity: str

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("entity count cannot be negative")

        if not self.entity.strip():
            raise ValueError("entity must not be empty")

    def to_amount(self) -> "AmountOfSubstance":
        """Convert entity count to amount of substance."""
        amount = self.value / N_A.value

        return AmountOfSubstance(
            Quantity(amount, "mol"),
            self.entity,
        )


@dataclass(frozen=True)
class AmountOfSubstance:
    """
    Amount of a specified type of entity.

    The numerical amount is represented by a Quantity in mol.
    """

    quantity: Quantity
    entity: str

    def __post_init__(self) -> None:
        if self.quantity.dimension.amount != 1:
            raise ValueError(
                "AmountOfSubstance requires a quantity "
                "with amount-of-substance dimension"
            )

        if not self.entity.strip():
            raise ValueError("entity must not be empty")

    @property
    def value(self) -> float:
        """Return the numerical amount in mol."""
        return self.quantity.to("mol").value

    def to_entity_count(self) -> EntityCount:
        """Convert amount of substance to number of entities."""
        count = self.value * N_A.value

        return EntityCount(
            count,
            self.entity,
        )

    def __str__(self) -> str:
        return f"{self.value} mol {self.entity}"
