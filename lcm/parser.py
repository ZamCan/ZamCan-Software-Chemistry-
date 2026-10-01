from __future__ import annotations

import re

from .intent import ChemicalIntent, IntentKind


_ELEMENT_RE = re.compile(
    r"^(?:what is|tell me about|describe|lookup|look up|find|"
    r"ni nini|ni element gani|tafuta)\s+(.+?)\??$",
    re.IGNORECASE,
)

_BALANCE_RE = re.compile(
    r"^(?:balance|balance equation|balanc(e|ing)|"
    r"linganisha|linganisha mlinganyo)\s*[:\-]?\s*(.+)$",
    re.IGNORECASE,
)

_REACTION_RE = re.compile(
    r"^(?:will|can|does|assess|predict|is|"
    r"je|inawezekana|inaweza)\s*(?:react|reaction|reaction happen|"
    r"reaction occur|kuitikia|mmenyuko)?\s*[:\-]?\s*(.+)$",
    re.IGNORECASE,
)

_FORMULA_SPLIT_RE = re.compile(r"\s*(?:->|→|=>|=)\s*")


def parse(text: str) -> ChemicalIntent:
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    raw = text.strip()
    if not raw:
        raise ValueError("text must not be empty")

    match = _ELEMENT_RE.match(raw)
    if match:
        return ChemicalIntent(
            kind=IntentKind.ELEMENT_LOOKUP,
            raw_text=raw,
            target=match.group(1).strip(),
        )

    match = _BALANCE_RE.match(raw)
    if match:
        equation = match.group(2).strip()
        reactants, products = _parse_equation(equation)
        return ChemicalIntent(
            kind=IntentKind.BALANCE_EQUATION,
            raw_text=raw,
            reactants=reactants,
            products=products,
        )

    match = _REACTION_RE.match(raw)
    if match:
        equation = match.group(1).strip()
        reactants, products = _parse_equation(equation)
        return ChemicalIntent(
            kind=IntentKind.REACTION_ASSESSMENT,
            raw_text=raw,
            reactants=reactants,
            products=products,
        )

    return ChemicalIntent(
        kind=IntentKind.UNKNOWN,
        raw_text=raw,
        confidence=0.0,
        reasons=("No deterministic chemical intent pattern matched.",),
    )


def _parse_equation(text: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    parts = _FORMULA_SPLIT_RE.split(text, maxsplit=1)
    if len(parts) != 2:
        raise ValueError(
            "chemical equation must contain an arrow or '=' separating "
            "reactants and products"
        )

    reactants = _parse_side(parts[0])
    products = _parse_side(parts[1])
    return reactants, products


def _parse_side(text: str) -> tuple[str, ...]:
    items = tuple(item.strip() for item in text.split("+") if item.strip())
    if not items:
        raise ValueError("chemical equation side must contain a species")
    return items


__all__ = ["parse"]
