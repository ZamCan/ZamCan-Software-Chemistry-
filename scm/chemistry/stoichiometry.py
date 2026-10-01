from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping

@dataclass(frozen=True)
class StoichiometricResult:
    extent: Fraction
    limiting_reactants: tuple[str, ...]
    consumed: Mapping[str, Fraction]
    produced: Mapping[str, Fraction]
    excess_remaining: Mapping[str, Fraction]

def solve_stoichiometry(reactants: Mapping[str, Fraction|int|float],
                        products: Mapping[str, Fraction|int|float],
                        coefficients: Mapping[str, int]) -> StoichiometricResult:
    if not reactants: raise ValueError("reactants are required")
    extent = None
    limits = []
    for species, amount in reactants.items():
        coefficient = coefficients.get(species)
        if not coefficient or coefficient <= 0: raise ValueError(f"Missing positive coefficient for {species}")
        ratio = Fraction(amount) / coefficient
        if extent is None or ratio < extent: extent, limits = ratio, [species]
        elif ratio == extent: limits.append(species)
    consumed = {s: extent*coefficients[s] for s in reactants}
    produced = {s: extent*coefficients[s] for s in products}
    excess = {s: Fraction(a)-consumed[s] for s,a in reactants.items()}
    return StoichiometricResult(extent, tuple(limits), consumed, produced, excess)
