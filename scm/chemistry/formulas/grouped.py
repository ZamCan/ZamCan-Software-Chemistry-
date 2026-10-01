from __future__ import annotations

import re

from .model import ChemicalFormula, FormulaComponent

_TOKEN = re.compile(r"[A-Z][a-z]?|\d+|[()]|[.]")

def parse_grouped_formula(formula: str) -> ChemicalFormula:
    text = formula.strip()
    if not text:
        raise ValueError("formula must not be empty")
    tokens = _TOKEN.findall(text)
    if "".join(tokens) != text:
        raise ValueError("unsupported formula syntax")
    counts, pos = _sequence(tokens, 0)
    if pos != len(tokens):
        raise ValueError("unexpected formula token")
    return ChemicalFormula(
        original=text,
        components=tuple(FormulaComponent(k, v) for k, v in counts.items()),
    )

def _sequence(tokens: list[str], pos: int, closing: str | None = None):
    out: dict[str, int] = {}
    while pos < len(tokens):
        t = tokens[pos]
        if closing and t == closing:
            return out, pos + 1
        if t == ")":
            raise ValueError("unexpected closing parenthesis")
        if t == "(":
            nested, pos = _sequence(tokens, pos + 1, ")")
            mult, pos = _number(tokens, pos)
            for k, v in nested.items():
                out[k] = out.get(k, 0) + v * mult
            continue
        if t == ".":
            raise ValueError("hydrate notation requires a future hydrate model")
        if t.isdigit():
            raise ValueError("unexpected multiplier")
        pos += 1
        mult, pos = _number(tokens, pos)
        out[t] = out.get(t, 0) + mult
    if closing:
        raise ValueError("unterminated group")
    return out, pos

def _number(tokens: list[str], pos: int):
    if pos < len(tokens) and tokens[pos].isdigit():
        n = int(tokens[pos])
        if n < 1:
            raise ValueError("multiplier must be positive")
        return n, pos + 1
    return 1, pos
