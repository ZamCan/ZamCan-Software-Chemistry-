from __future__ import annotations

from dataclasses import dataclass

from scm.core import Evidence, Quantity, QuantityRange, Uncertainty
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
    evidence: tuple[Evidence, ...] = ()
    atomic_weight_uncertainty: Uncertainty | None = None


@dataclass(frozen=True)
class MolarMassCalculation:
    """
    Detailed result of a composition-derived molar-mass calculation.
    """

    species: ChemicalSpecies
    molar_mass: MassQuantity
    terms: tuple[MolarMassTerm, ...]
