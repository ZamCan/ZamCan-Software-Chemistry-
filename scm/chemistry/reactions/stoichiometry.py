from __future__ import annotations

from dataclasses import dataclass

from scm.matter.species import ChemicalSpecies


@dataclass(frozen=True, order=True)
class StoichiometricTerm:
    """A chemical species and its stoichiometric coefficient."""

    species: ChemicalSpecies
    coefficient: int

    def __post_init__(self) -> None:
        if not isinstance(self.species, ChemicalSpecies):
            raise TypeError("species must be a ChemicalSpecies")

        if not isinstance(self.coefficient, int):
            raise TypeError("coefficient must be an integer")

        if self.coefficient <= 0:
            raise ValueError("coefficient must be greater than zero")


@dataclass(frozen=True)
class ReactionStoichiometry:
    """Stoichiometric representation of a chemical reaction.

    This object describes reaction ratios only.

    It does not represent:
    - actual amounts of material,
    - reaction extent,
    - reaction rate,
    - thermodynamic feasibility,
    - kinetic feasibility,
    - equilibrium,
    - reaction conditions.

    Those belong to later reaction-state and reasoning layers.
    """

    reactants: tuple[StoichiometricTerm, ...]
    products: tuple[StoichiometricTerm, ...]

    def __post_init__(self) -> None:
        if not self.reactants:
            raise ValueError("reaction must contain at least one reactant")

        if not self.products:
            raise ValueError("reaction must contain at least one product")

        if not all(
            isinstance(term, StoichiometricTerm)
            for term in self.reactants
        ):
            raise TypeError(
                "all reactants must be StoichiometricTerm instances"
            )

        if not all(
            isinstance(term, StoichiometricTerm)
            for term in self.products
        ):
            raise TypeError(
                "all products must be StoichiometricTerm instances"
            )

        reactant_species = [term.species for term in self.reactants]
        product_species = [term.species for term in self.products]

        if len(reactant_species) != len(set(reactant_species)):
            raise ValueError(
                "reactants cannot contain duplicate species"
            )

        if len(product_species) != len(set(product_species)):
            raise ValueError(
                "products cannot contain duplicate species"
            )

    @classmethod
    def from_terms(
        cls,
        reactants: tuple[StoichiometricTerm, ...],
        products: tuple[StoichiometricTerm, ...],
    ) -> "ReactionStoichiometry":
        return cls(
            reactants=tuple(reactants),
            products=tuple(products),
        )

    @property
    def reactant_species(self) -> tuple[ChemicalSpecies, ...]:
        return tuple(term.species for term in self.reactants)

    @property
    def product_species(self) -> tuple[ChemicalSpecies, ...]:
        return tuple(term.species for term in self.products)

    @property
    def reactant_coefficients(self) -> tuple[int, ...]:
        return tuple(term.coefficient for term in self.reactants)

    @property
    def product_coefficients(self) -> tuple[int, ...]:
        return tuple(term.coefficient for term in self.products)

    def coefficient_for(
        self,
        species: ChemicalSpecies,
    ) -> int:
        if not isinstance(species, ChemicalSpecies):
            raise TypeError("species must be a ChemicalSpecies")

        for term in self.reactants:
            if term.species == species:
                return term.coefficient

        for term in self.products:
            if term.species == species:
                return term.coefficient

        raise KeyError("species is not part of this reaction")
