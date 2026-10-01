from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scm.matter.species import ChemicalSpecies


@dataclass(frozen=True)
class ChemicalIdentityKey:
    """Deterministic identity boundary for a chemical species."""

    composition: tuple[tuple[str, int], ...]
    charge_number: int
    radical: bool
    isotopes: tuple[tuple[str, int, int], ...] = ()

    @classmethod
    def from_species(cls, species: "ChemicalSpecies") -> "ChemicalIdentityKey":
        counts = tuple(sorted(species.element_counts.items()))
        isotopes: list[tuple[str, int, int]] = []

        z = getattr(species, "atomic_number", None)
        a = getattr(species, "mass_number", None)
        symbol = getattr(species, "symbol", None)

        if z is not None and a is not None:
            if not isinstance(a, int) or a < z:
                raise ValueError("invalid isotope mass number on species")
            isotopes.append((str(symbol), int(z), int(a)))

        return cls(
            composition=counts,
            charge_number=species.charge_number,
            radical=species.radical,
            isotopes=tuple(isotopes),
        )


def identity_key(species: "ChemicalSpecies") -> ChemicalIdentityKey:
    return ChemicalIdentityKey.from_species(species)
