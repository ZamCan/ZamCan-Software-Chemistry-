from __future__ import annotations

from .base import Atom


def build_atom(
    atomic_number: int,
    *,
    charge_number: int = 0,
    symbol: str | None = None,
) -> Atom:
    if not isinstance(charge_number, int):
        raise TypeError(
            "charge_number must be an integer"
        )

    electron_count = atomic_number - charge_number

    if electron_count < 0:
        raise ValueError(
            "charge would require a negative electron count"
        )

    return Atom.create(
        atomic_number=atomic_number,
        electron_count=electron_count,
        symbol=symbol,
    )


def neutral_atom(
    atomic_number: int,
    *,
    symbol: str | None = None,
) -> Atom:
    return build_atom(
        atomic_number,
        charge_number=0,
        symbol=symbol,
    )


def ion_atom(
    atomic_number: int,
    charge_number: int,
    *,
    symbol: str | None = None,
) -> Atom:
    if charge_number == 0:
        raise ValueError(
            "ion charge_number must not be zero"
        )

    return build_atom(
        atomic_number,
        charge_number=charge_number,
        symbol=symbol,
    )
