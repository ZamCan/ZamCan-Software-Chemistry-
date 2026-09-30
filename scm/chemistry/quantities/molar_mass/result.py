from __future__ import annotations

from dataclasses import dataclass

from scm.core import Quantity, QuantityRange
from scm.matter.species import ChemicalSpecies


MassQuantity = Quantity | QuantityRange


@dataclass(frozen=True)
class MolarMassTerm:
    """
    One elemental contribution to a molar-mass calculation.
    """

    element: str
    count: int
    atomic_mass: Quantity | QuantityRange
    contribution: Quantity | QuantityRange


@dataclass(frozen=True)
class MolarMassCalculation:
    """
    Detailed result of a composition-derived molar-mass calculation.
    """

    species: ChemicalSpecies
    molar_mass: MassQuantity
    terms: tuple[MolarMassTerm, ...]
