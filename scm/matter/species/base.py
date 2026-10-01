from __future__ import annotations

from dataclasses import dataclass

from scm.matter.composition import Composition


@dataclass(frozen=True)
class ChemicalSpecies:
    """
    Base chemical entity shared by atoms, ions, molecules, radicals
    and other chemically meaningful species.

    This class describes chemical identity at the species level without
    pretending that every species has the same structural model.
    """

    composition: Composition
    charge_number: int = 0
    radical: bool = False
    name: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.composition, Composition):
            raise TypeError(
                "composition must be a Composition"
            )

        if not isinstance(self.charge_number, int):
            raise TypeError(
                "charge_number must be an integer"
            )

        if not isinstance(self.radical, bool):
            raise TypeError(
                "radical must be a boolean"
            )

        if self.name is not None:
            if not isinstance(self.name, str):
                raise TypeError("name must be a string")

            if not self.name.strip():
                raise ValueError(
                    "name must not be empty"
                )

    @property
    def element_counts(self) -> dict[str, int]:
        return self.composition.element_counts

    @property
    def element_symbols(self) -> tuple[str, ...]:
        return self.composition.element_symbols

    @property
    def atom_count(self) -> int:
        return self.composition.total_atoms

    @property
    def is_neutral(self) -> bool:
        return self.charge_number == 0

    @property
    def is_cation(self) -> bool:
        return self.charge_number > 0

    @property
    def is_anion(self) -> bool:
        return self.charge_number < 0

    @property
    def is_ion(self) -> bool:
        return self.charge_number != 0

    @property
    def is_radical(self) -> bool:
        return self.radical

    @property
    def charge_symbol(self) -> str:
        if self.charge_number == 0:
            return ""

        sign = "+" if self.charge_number > 0 else "-"
        magnitude = abs(self.charge_number)

        return (
            sign
            if magnitude == 1
            else f"{magnitude}{sign}"
        )

    @property
    def formula(self) -> str:
        return str(self.composition)

    @property
    def identity_key(self):
        """Return the deterministic SCM identity key.

        Names are annotations, not identity. Isotope-aware Atom/Ion instances
        contribute their explicit mass number when available.
        """
        from scm.chemistry.identity_key import identity_key
        return identity_key(self)

    def contains_element(self, element: str) -> bool:
        return self.composition.contains(element)

    def __str__(self) -> str:
        return f"{self.formula}{self.charge_symbol}"
