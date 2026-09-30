from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RawIsotopeRecord:
    """
    Source-independent intermediate representation of isotope data.

    This record deliberately preserves raw scientific fields without
    forcing them into the final SCM representation.
    """

    atomic_number: int
    mass_number: int

    name: str | None = None
    symbol: str | None = None

    isotopic_mass: float | None = None
    isotopic_mass_uncertainty: float | None = None

    stable: bool | None = None
    naturally_occurring: bool | None = None

    natural_abundance: float | None = None
    natural_abundance_uncertainty: float | None = None

    half_life: float | None = None
    half_life_unit: str | None = None

    spin: str | None = None
    parity: str | None = None

    mass_excess: float | None = None
    mass_excess_uncertainty: float | None = None

    binding_energy: float | None = None
    binding_energy_uncertainty: float | None = None

    notes: str | None = None
