from .base import IsotopeRecord
from .registry import (
    all_isotopes,
    get_isotope,
    register_isotope,
)
from .hydrogen import (
    deuterium,
    protium,
    tritium,
)

__all__ = [
    "IsotopeRecord",
    "all_isotopes",
    "get_isotope",
    "register_isotope",
    "deuterium",
    "protium",
    "tritium",
]
