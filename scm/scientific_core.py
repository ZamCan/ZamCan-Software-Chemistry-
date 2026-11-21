"""Evidence-aware, dependency-free chemistry computation primitives.

Balances ordinary molecular equations by exact rational linear algebra.
This is not a reaction feasibility or mechanism predictor.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from functools import reduce
from math import gcd, lcm, sqrt, isfinite
import re

_TOKEN = re.compile(r"([A-Z][a-z]?|\\(|\\)|[0-9]+)")
class ChemistryInputError(ValueError):
    """Invalid chemical input or insufficient scientific information."""

def composition(formula: str) -> dict[str, int]:
    """Parse neutral molecular formulae, including nested parentheses."""
    if not formula or not isinstance(formula, str):
        raise ChemistryInputError("A nonempty formula is required")
    tokens = _TOKEN.findall(formula)
    if "".join(tokens) != formula:
        raise ChemistryInputError("Unsupported formula syntax")
    stack = [{}]
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == "(":
            stack.append({})
            i += 1
        elif token == ")":
            if len(stack) == 1:
                raise ChemistryInputError("Unmatched closing parenthesis")
            group = stack.pop()
            i += 1
            count = int(tokens[i]) if i < len(tokens) and tokens[i].isdigit() else 1
            if count < 1 or not group:
                raise ChemistryInputError("Invalid group multiplier")
            if i < len(tokens) and tokens[i].isdigit():
                i += 1
            for symbol, amount in group.items():
                stack[-1][symbol] = stack[-1].get(symbol, 0) + amount * count
        elif re.fullmatch(r"[A-Z][a-z]?", token):
            symbol = token
            i += 1
            count = int(tokens[i]) if i < len(tokens) and tokens[i].isdigit() else 1
            if count < 1:
                raise ChemistryInputError("Invalid atom count")
            if i < len(tokens) and tokens[i].isdigit():
                i += 1
            stack[-1][symbol] = stack[-1].get(symbol, 0) + count
        else:
            raise ChemistryInputError("Unexpected token")
    if len(stack) != 1 or not stack[0]:
        raise ChemistryInputError("Unbalanced or empty formula")
    return stack[0]

def balance(reactants: list[str], products: list[str]) -> dict:
    """Return primitive positive integer coefficients or reject ambiguous systems.

    All provided species are required to participate. Charge, isotopes,
    reaction feasibility and phase behavior are outside this solver's scope.
    """
    if not reactants or not products or len(reactants) + len(products) < 2:
        raise ChemistryInputError("Both sides must contain species")
    species = reactants + products
    parsed = [composition(s) for s in species]
    elements = sorted(set().union(*(p.keys() for p in parsed)))
    matrix = [[Fraction(p.get(el, 0) * (1 if j < len(reactants) else -1))
               for j, p in enumerate(parsed)] for el in elements]
    rows, cols = len(matrix), len(species)
    pivots = []
    r = 0
    for c in range(cols):
        pivot = next((k for k in range(r, rows) if matrix[k][c]), None)
        if pivot is None:
            continue
        matrix[r], matrix[pivot] = matrix[pivot], matrix[r]
        scale = matrix[r][c]
        matrix[r] = [v / scale for v in matrix[r]]
        for k in range(rows):
            if k != r:
                factor = matrix[k][c]
                matrix[k] = [a - factor * b for a, b in zip(matrix[k], matrix[r])]
        pivots.append(c)
        r += 1
        if r == rows:
            break
    free = [c for c in range(cols) if c not in pivots]
    if len(free) != 1:
        raise ChemistryInputError("No unique stoichiometric ratio for supplied species")
    vector = [Fraction(0) for _ in range(cols)]
    vector[free[0]] = Fraction(1)
    for row, pivot in enumerate(pivots):
        vector[pivot] = -matrix[row][free[0]]
    if any(v <= 0 for v in vector):
        raise ChemistryInputError("No all-positive balance for supplied species")
    denominator = lcm(*(v.denominator for v in vector))
    integers = [int(v * denominator) for v in vector]
    divisor = reduce(gcd, integers)
    integers = [v // divisor for v in integers]
    return {"reactants": dict(zip(reactants, integers[:len(reactants)])),
            "products": dict(zip(products, integers[len(reactants):])),
            "method": "exact rational nullspace; mass conservation",
            "validation_status": "calculated_not_experimentally_verified"}

@dataclass(frozen=True)
class Measurement:
    value: float
    standard_uncertainty: float
    unit: str

    def __post_init__(self):
        if not isfinite(self.value) or not isfinite(self.standard_uncertainty):
            raise ChemistryInputError("Measurements must be finite")
        if self.standard_uncertainty < 0:
            raise ChemistryInputError("Uncertainty must be nonnegative")

def titration_concentration(analyte_volume: Measurement,
                            titrant_volume: Measurement,
                            titrant_concentration: Measurement,
                            analyte_coefficient: int = 1,
                            titrant_coefficient: int = 1) -> dict:
    """Calculate analyte molarity from one known stoichiometric reaction.

    Assumes independent standard uncertainties, complete reaction and an
    appropriate endpoint. Volume units must match; concentration is mol/L.
    """
    a, t, c = analyte_volume, titrant_volume, titrant_concentration
    if a.unit != t.unit or c.unit != "mol/L":
        raise ChemistryInputError("Volumes must share a unit; concentration must be mol/L")
    if any(x.value <= 0 for x in (a, t, c)):
        raise ChemistryInputError("Volumes and concentration must be positive")
    if analyte_coefficient < 1 or titrant_coefficient < 1:
        raise ChemistryInputError("Stoichiometric coefficients must be positive")
    value = c.value * t.value / a.value * analyte_coefficient / titrant_coefficient
    relative_variance = sum((x.standard_uncertainty / x.value) ** 2 for x in (a, t, c))
    return {"value": value, "standard_uncertainty": value * sqrt(relative_variance),
            "unit": "mol/L", "validation_status": "calculated_not_experimentally_verified",
            "assumptions": ["complete stoichiometric reaction", "appropriate endpoint",
                            "independent standard uncertainties", "provided values are valid"]}
