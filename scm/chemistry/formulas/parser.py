from __future__ import annotations

import re

from .model import ChemicalFormula, FormulaComponent


_ELEMENT = re.compile(r"([A-Z][a-z]?)(\d*)")


def parse_formula(formula: str) -> ChemicalFormula:
    if not isinstance(formula, str):
        raise TypeError("formula must be a string")

    formula = formula.strip()

    if not formula:
        raise ValueError("formula must not be empty")

    components: list[FormulaComponent] = []
    position = 0

    for match in _ELEMENT.finditer(formula):
        if match.start() != position:
            raise ValueError(
                f"unsupported formula syntax near: {formula[position:]}"
            )

        symbol, count_text = match.groups()
        count = int(count_text) if count_text else 1

        components.append(
            FormulaComponent(
                element=symbol,
                count=count,
            )
        )

        position = match.end()

    if position != len(formula):
        raise ValueError(
            f"unsupported formula syntax near: {formula[position:]}"
        )

    return ChemicalFormula(
        original=formula,
        components=tuple(components),
    )
