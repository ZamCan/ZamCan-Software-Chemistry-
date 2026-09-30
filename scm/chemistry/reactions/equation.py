from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class Species:
    formula: str

    def __post_init__(self) -> None:
        if not isinstance(self.formula, str) or not self.formula.strip():
            raise ValueError("species formula must not be empty")


@dataclass(frozen=True)
class ReactionSide:
    species: tuple[Species, ...]

    def __post_init__(self) -> None:
        if not self.species:
            raise ValueError("reaction side must contain at least one species")


@dataclass(frozen=True)
class ChemicalEquation:
    reactants: ReactionSide
    products: ReactionSide

    @classmethod
    def from_formulas(
        cls,
        reactants: tuple[str, ...],
        products: tuple[str, ...],
    ) -> "ChemicalEquation":
        return cls(
            ReactionSide(tuple(Species(x) for x in reactants)),
            ReactionSide(tuple(Species(x) for x in products)),
        )


@dataclass(frozen=True)
class BalancedEquation:
    equation: ChemicalEquation
    reactant_coefficients: tuple[int, ...]
    product_coefficients: tuple[int, ...]
    balanced: bool

    def formatted(self) -> str:
        left = " + ".join(
            _format_term(c, s.formula)
            for c, s in zip(
                self.reactant_coefficients,
                self.equation.reactants.species,
            )
        )
        right = " + ".join(
            _format_term(c, s.formula)
            for c, s in zip(
                self.product_coefficients,
                self.equation.products.species,
            )
        )
        return f"{left} → {right}"


def _format_term(coefficient: int, formula: str) -> str:
    return formula if coefficient == 1 else f"{coefficient}{formula}"
