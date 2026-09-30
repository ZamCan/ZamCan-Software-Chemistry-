from __future__ import annotations

from dataclasses import dataclass

from scm.core import Quantity
from scm.matter.species import ChemicalSpecies
from scm.matter.states import ChemicalState

from .stoichiometry import ReactionStoichiometry


@dataclass(frozen=True)
class SpeciesExtentChange:
    """Stoichiometric amount change for one chemical species."""

    species: ChemicalSpecies
    coefficient: int
    change: Quantity

    def __post_init__(self) -> None:
        if not isinstance(self.species, ChemicalSpecies):
            raise TypeError("species must be a ChemicalSpecies")

        if not isinstance(self.coefficient, int):
            raise TypeError("coefficient must be an integer")

        if self.coefficient <= 0:
            raise ValueError("coefficient must be greater than zero")

        if not isinstance(self.change, Quantity):
            raise TypeError("change must be a Quantity")

        if self.change.dimension != Quantity(1.0, "mol").dimension:
            raise ValueError(
                "change must have amount-of-substance dimension"
            )


@dataclass(frozen=True)
class ReactionExtentLimit:
    """Maximum stoichiometrically feasible reaction extent."""

    extent: Quantity
    limiting_species: ChemicalSpecies

    def __post_init__(self) -> None:
        if not isinstance(self.extent, Quantity):
            raise TypeError("extent must be a Quantity")

        if self.extent.dimension != Quantity(1.0, "mol").dimension:
            raise ValueError(
                "extent must have amount-of-substance dimension"
            )

        if self.extent.value < 0:
            raise ValueError("extent cannot be negative")

        if not isinstance(self.limiting_species, ChemicalSpecies):
            raise TypeError(
                "limiting_species must be a ChemicalSpecies"
            )


class ReactionExtentCalculator:
    """Calculate stoichiometric reaction extent from an initial state.

    This calculator performs material-availability accounting only.

    It does not determine:
    - whether a reaction occurs,
    - reaction rate,
    - equilibrium,
    - thermodynamic feasibility,
    - kinetic feasibility,
    - competing reactions,
    - incomplete conversion,
    - material losses,
    - phase transfer,
    - escaped or dissolved products.
    """

    name = "reaction_extent"

    def maximum_extent(
        self,
        reaction: ReactionStoichiometry,
        state: ChemicalState,
    ) -> ReactionExtentLimit:
        if not isinstance(reaction, ReactionStoichiometry):
            raise TypeError(
                "reaction must be a ReactionStoichiometry"
            )

        if not isinstance(state, ChemicalState):
            raise TypeError(
                "state must be a ChemicalState"
            )

        candidates: list[tuple[ChemicalSpecies, float]] = []

        for term in reaction.reactants:
            amount = self._moles_of(state, term.species)

            if term.coefficient <= 0:
                raise ValueError(
                    "reactant coefficient must be greater than zero"
                )

            candidates.append(
                (
                    term.species,
                    amount / term.coefficient,
                )
            )

        if not candidates:
            raise ValueError(
                "reaction must contain at least one reactant"
            )

        limiting_species, extent_value = min(
            candidates,
            key=lambda item: item[1],
        )

        return ReactionExtentLimit(
            extent=Quantity(extent_value, "mol"),
            limiting_species=limiting_species,
        )

    def changes_at_extent(
        self,
        reaction: ReactionStoichiometry,
        extent: Quantity,
    ) -> tuple[SpeciesExtentChange, ...]:
        if not isinstance(reaction, ReactionStoichiometry):
            raise TypeError(
                "reaction must be a ReactionStoichiometry"
            )

        if not isinstance(extent, Quantity):
            raise TypeError(
                "extent must be a Quantity"
            )

        if extent.dimension != Quantity(1.0, "mol").dimension:
            raise ValueError(
                "extent must have amount-of-substance dimension"
            )

        extent_moles = extent.to("mol").value

        if extent_moles < 0:
            raise ValueError("extent cannot be negative")

        changes: list[SpeciesExtentChange] = []

        for term in reaction.reactants:
            changes.append(
                SpeciesExtentChange(
                    species=term.species,
                    coefficient=term.coefficient,
                    change=Quantity(
                        -term.coefficient * extent_moles,
                        "mol",
                    ),
                )
            )

        for term in reaction.products:
            changes.append(
                SpeciesExtentChange(
                    species=term.species,
                    coefficient=term.coefficient,
                    change=Quantity(
                        term.coefficient * extent_moles,
                        "mol",
                    ),
                )
            )

        return tuple(changes)

    @staticmethod
    def _moles_of(
        state: ChemicalState,
        species: ChemicalSpecies,
    ) -> float:
        total = 0.0

        for component in state.components:
            if component.species == species:
                total += component.moles

        return total


reaction_extent_calculator = ReactionExtentCalculator()
