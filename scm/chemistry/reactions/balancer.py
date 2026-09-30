from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import re

from .equation import BalancedEquation, ChemicalEquation


_ELEMENT = re.compile(r"([A-Z][a-z]?)(\d*)")


def parse_formula(formula: str) -> dict[str, int]:
    formula = formula.strip()
    if not formula:
        raise ValueError("empty chemical formula")

    counts: dict[str, int] = defaultdict(int)
    position = 0

    for match in _ELEMENT.finditer(formula):
        if match.start() != position:
            raise ValueError(f"unsupported formula syntax: {formula}")

        element, number = match.groups()
        counts[element] += int(number or "1")
        position = match.end()

    if position != len(formula):
        raise ValueError(f"unsupported formula syntax: {formula}")

    return dict(counts)


def balance_equation(equation: ChemicalEquation) -> BalancedEquation:
    species = (
        equation.reactants.species +
        equation.products.species
    )

    atoms = sorted({
        element
        for species_item in species
        for element in parse_formula(species_item.formula)
    })

    matrix: list[list[Fraction]] = []

    for element in atoms:
        row = []
        for index, species_item in enumerate(species):
            count = parse_formula(species_item.formula).get(element, 0)
            sign = 1 if index < len(equation.reactants.species) else -1
            row.append(Fraction(sign * count))
        matrix.append(row)

    vector = _null_vector(matrix)

    reactant_count = len(equation.reactants.species)
    reactants = tuple(int(vector[i]) for i in range(reactant_count))
    products = tuple(int(vector[i]) for i in range(reactant_count, len(vector)))

    return BalancedEquation(
        equation=equation,
        reactant_coefficients=reactants,
        product_coefficients=products,
        balanced=True,
    )


def _null_vector(matrix: list[list[Fraction]]) -> list[int]:
    if not matrix:
        raise ValueError("equation contains no atoms")

    rows = len(matrix)
    cols = len(matrix[0])

    a = [row[:] for row in matrix]
    pivot_columns: list[int] = []
    pivot_row = 0

    for column in range(cols):
        pivot = next(
            (
                r for r in range(pivot_row, rows)
                if a[r][column] != 0
            ),
            None,
        )

        if pivot is None:
            continue

        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]

        divisor = a[pivot_row][column]
        a[pivot_row] = [
            value / divisor for value in a[pivot_row]
        ]

        for r in range(rows):
            if r == pivot_row:
                continue

            factor = a[r][column]

            if factor != 0:
                a[r] = [
                    a[r][c] - factor * a[pivot_row][c]
                    for c in range(cols)
                ]

        pivot_columns.append(column)
        pivot_row += 1

        if pivot_row == rows:
            break

    free_columns = [
        c for c in range(cols)
        if c not in pivot_columns
    ]

    if not free_columns:
        raise ValueError("equation has no non-trivial balancing solution")

    free = free_columns[-1]
    solution = [Fraction(0) for _ in range(cols)]
    solution[free] = Fraction(1)

    for row, column in reversed(
        list(enumerate(pivot_columns))
    ):
        total = sum(
            a[row][c] * solution[c]
            for c in free_columns
        )
        solution[column] = -total

    denominators = [value.denominator for value in solution]

    lcm = 1
    for denominator in denominators:
        lcm = _lcm(lcm, denominator)

    integers = [
        int(value * lcm)
        for value in solution
    ]

    gcd = 0
    for value in integers:
        gcd = _gcd(gcd, abs(value))

    integers = [value // gcd for value in integers]

    if all(value <= 0 for value in integers):
        integers = [-value for value in integers]

    if any(value <= 0 for value in integers):
        raise ValueError("unable to obtain positive stoichiometric coefficients")

    return integers


def _gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def _lcm(a: int, b: int) -> int:
    return abs(a * b) // _gcd(a, b)
