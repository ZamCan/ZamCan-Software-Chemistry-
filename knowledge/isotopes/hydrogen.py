from __future__ import annotations

from scm.matter.isotopes import Isotope
from scm.matter.nuclei import Nucleus

from .base import IsotopeRecord
from .registry import register_isotope


protium = IsotopeRecord(
    isotope=Isotope(Nucleus(1, 0)),
    name="Protium",
    symbol="¹H",
    stable=True,
)

deuterium = IsotopeRecord(
    isotope=Isotope(Nucleus(1, 1)),
    name="Deuterium",
    symbol="²H",
    stable=True,
)

tritium = IsotopeRecord(
    isotope=Isotope(Nucleus(1, 2)),
    name="Tritium",
    symbol="³H",
    stable=False,
)


register_isotope(protium)
register_isotope(deuterium)
register_isotope(tritium)


__all__ = [
    "protium",
    "deuterium",
    "tritium",
]
