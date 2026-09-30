from __future__ import annotations

from dataclasses import dataclass, field

from scm.matter.atoms import Atom
from scm.matter.composition import Composition
from scm.matter.species import ChemicalSpecies
from knowledge.elements.registry import get_element


@dataclass(frozen=True)
class Ion(ChemicalSpecies):
    """
    Monatomic ion.

    Atomic number identifies the element.

    Charge number determines electron count:

        electrons = Z - charge

    Composition is automatically derived from the element identity.
    """

    atomic_number: int = 1
    charge_number: int = 1
    symbol: str | None = None
    composition: Composition = field(init=False)

    def __post_init__(self) -> None:
        if not isinstance(self.atomic_number, int):
            raise TypeError(
                "atomic_number must be an integer"
            )

        if not 1 <= self.atomic_number <= 118:
            raise ValueError(
                "atomic_number must be between 1 and 118"
            )

        if not isinstance(self.charge_number, int):
            raise TypeError(
                "charge_number must be an integer"
            )

        if self.charge_number == 0:
            raise ValueError(
                "an ion must have a non-zero charge"
            )

        if self.electron_count < 0:
            raise ValueError(
                "ion cannot have a negative electron count"
            )

        if self.symbol is not None:
            if not isinstance(self.symbol, str):
                raise TypeError(
                    "symbol must be a string"
                )

            if not self.symbol.strip():
                raise ValueError(
                    "symbol must not be empty"
                )

        element_record = get_element(self.atomic_number)
        canonical_symbol = element_record.symbol

        if self.symbol is None:
            symbol = canonical_symbol
        else:
            symbol = self.symbol.strip()

            supplied_record = get_element(symbol)

            if supplied_record.atomic_number != self.atomic_number:
                raise ValueError(
                    "symbol does not match atomic_number"
                )

            symbol = supplied_record.symbol

        object.__setattr__(self, "symbol", symbol)

        composition = Composition.from_mapping(
            {
                canonical_symbol: 1
            }
        )

        object.__setattr__(
            self,
            "composition",
            composition,
        )

        super().__post_init__()

    @classmethod
    def create(
        cls,
        atomic_number: int,
        charge_number: int,
        *,
        symbol: str | None = None,
    ) -> "Ion":
        return cls(
            atomic_number=atomic_number,
            charge_number=charge_number,
            symbol=symbol,
        )

    @property
    def proton_count(self) -> int:
        return self.atomic_number

    @property
    def electron_count(self) -> int:
        return (
            self.atomic_number
            - self.charge_number
        )

    @property
    def electron_delta(self) -> int:
        return -self.charge_number

    @property
    def is_cation(self) -> bool:
        return self.charge_number > 0

    @property
    def is_anion(self) -> bool:
        return self.charge_number < 0

    @property
    def classification(self) -> str:
        return (
            "cation"
            if self.is_cation
            else "anion"
        )

    @property
    def atom_state(self) -> Atom:
        return Atom.create(
            atomic_number=self.atomic_number,
            electron_count=self.electron_count,
            symbol=self.symbol,
        )

    @property
    def configuration(self):
        return self.atom_state.configuration

    @property
    def valence_electron_count(self) -> int:
        return self.configuration.valence_electron_count

    def __str__(self) -> str:
        return (
            f"{self.symbol or f'Z={self.atomic_number}'}"
            f"{self.charge_symbol}"
        )
