from __future__ import annotations

from typing import Dict

from .base import IsotopeRecord


_ISOTOPES_BY_NAME: Dict[str, IsotopeRecord] = {}
_ISOTOPES_BY_SYMBOL: Dict[str, IsotopeRecord] = {}
_ISOTOPES_BY_IDENTITY: Dict[tuple[int, int], IsotopeRecord] = {}


def register_isotope(isotope: IsotopeRecord) -> None:
    """
    Register one isotope knowledge record.

    Isotope identity is uniquely determined by (Z, A).
    Names and symbols are lookup aliases for that identity.
    """
    if not isinstance(isotope, IsotopeRecord):
        raise TypeError("isotope must be an IsotopeRecord")

    identity = isotope.identity

    if identity in _ISOTOPES_BY_IDENTITY:
        raise ValueError(
            f"isotope identity {identity} is already registered"
        )

    name_key = isotope.name.casefold()
    symbol_key = isotope.symbol.casefold()

    if name_key in _ISOTOPES_BY_NAME:
        raise ValueError(
            f"isotope name {isotope.name!r} is already registered"
        )

    if symbol_key in _ISOTOPES_BY_SYMBOL:
        raise ValueError(
            f"isotope symbol {isotope.symbol!r} is already registered"
        )

    _ISOTOPES_BY_IDENTITY[identity] = isotope
    _ISOTOPES_BY_NAME[name_key] = isotope
    _ISOTOPES_BY_SYMBOL[symbol_key] = isotope


def get_isotope(identifier: str | tuple[int, int]) -> IsotopeRecord:
    """
    Retrieve an isotope by name, symbol, or identity (Z, A).
    """
    if isinstance(identifier, tuple):
        if len(identifier) != 2:
            raise ValueError(
                "isotope identity must be a (Z, A) tuple"
            )

        try:
            return _ISOTOPES_BY_IDENTITY[identifier]
        except KeyError as exc:
            raise KeyError(
                f"Unknown isotope identity: {identifier!r}"
            ) from exc

    if not isinstance(identifier, str):
        raise TypeError(
            "isotope identifier must be a string or (Z, A) tuple"
        )

    key = identifier.strip().casefold()

    if not key:
        raise ValueError(
            "isotope identifier must not be empty"
        )

    if key in _ISOTOPES_BY_NAME:
        return _ISOTOPES_BY_NAME[key]

    if key in _ISOTOPES_BY_SYMBOL:
        return _ISOTOPES_BY_SYMBOL[key]

    raise KeyError(
        f"Unknown isotope: {identifier!r}"
    )


def all_isotopes() -> tuple[IsotopeRecord, ...]:
    """Return all registered isotope records."""
    return tuple(_ISOTOPES_BY_IDENTITY.values())


__all__ = [
    "register_isotope",
    "get_isotope",
    "all_isotopes",
]
