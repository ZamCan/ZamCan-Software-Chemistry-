from __future__ import annotations

from dataclasses import dataclass

from scm.chemistry.amount import AmountOfSubstance
from scm.matter.species import ChemicalSpecies


@dataclass(frozen=True)
class StateComponent:
    """
    A chemical species together with its amount in a chemical state.

    Chemical identity belongs to ChemicalSpecies.
    Amount belongs to AmountOfSubstance.
    This class connects the two without duplicating either model.
    """

    species: ChemicalSpecies
    amount: AmountOfSubstance

    def __post_init__(self) -> None:
        if not isinstance(self.species, ChemicalSpecies):
            raise TypeError(
                "species must be a ChemicalSpecies"
            )

        if not isinstance(self.amount, AmountOfSubstance):
            raise TypeError(
                "amount must be an AmountOfSubstance"
            )

        if not self.amount.entity.strip():
            raise ValueError(
                "amount entity must not be empty"
            )

    @property
    def quantity(self):
        """Return the underlying amount-of-substance Quantity."""
        return self.amount.quantity

    @property
    def entity(self) -> str:
        """Return the semantic entity description of the amount."""
        return self.amount.entity

    @property
    def moles(self) -> float:
        """Return the amount in mol."""
        return self.amount.value
